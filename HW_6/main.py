from typing import List

import sqlalchemy
from werkzeug.security import generate_password_hash
from models import User, Product, Order
from tables import users, products, orders, metadata
from fastapi import FastAPI, HTTPException, status
import databases
import uvicorn

DATABASE_URL = "sqlite:///mydatabasehw6.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
app = FastAPI()


@app.get('/')
async def read_root():
    return {'Домашняя работа Fast API': 'Семинар №6'}

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/")
async def create_user(new_user: User):
    hashed_password = generate_password_hash(new_user.password)
    query = users.insert().values(name=new_user.name, surname=new_user.surname, email=new_user.email,
                                  password=hashed_password)
    last_record_id = await database.execute(query)
    check_query = users.select().where(users.c.id == last_record_id)
    created_user = await database.fetch_one(check_query)
    return created_user


@app.post("/orders/")
async def create_order(new_order: Order):
    query = orders.insert().values(user_id=new_order.user_id, product_id=new_order.product_id, date=new_order.date,
                                   status=new_order.status)
    last_record_id = await database.execute(query)
    check_query = orders.select().where(orders.c.id == last_record_id)
    created_order = await database.fetch_one(check_query)
    return created_order


@app.post("/products/")
async def create_product(new_product: Product):
    query = products.insert().values(name=new_product.name, description=new_product.description,
                                     price=new_product.price)
    last_record_id = await database.execute(query)
    check_query = products.select().where(products.c.id == last_record_id)
    created_product = await database.fetch_one(check_query)
    return created_product


@app.put("/users/{user_id)")
async def update_user(user_id: int, new_user: User):
    user_query = users.select().where(users.c.id == user_id)
    existing_user = await database.fetch_one(user_query)
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не найден")

    hashed_password = generate_password_hash(new_user.password)
    query = users.update().where(users.c.id == user_id).values(name=new_user.name, surname=new_user.surname,
                                                               email=new_user.email, password=hashed_password)
    await database.execute(query)
    updated_query = users.select().where(users.c.id == user_id)
    updated_user = await database.fetch_one(updated_query)
    return updated_user


@app.put("/orders/{order_id}")
async def update_order(order_id: int, new_order: Order):
    order_query = orders.select().where(orders.c.id == order_id)
    existing_order = await database.fetch_one(order_query)
    if existing_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой заказ не найден")

    query = orders.update().where(orders.c.id == order_id).values(user_id=new_order.user_id,
                                                                  product_id=new_order.product_id, date=new_order.date,
                                                                  status=new_order.status)
    await database.execute(query)
    updated_query = orders.select().where(orders.c.id == order_id)
    updated_order = await database.fetch_one(updated_query)
    return updated_order


@app.put("/products/{product_id}")
async def update_product(product_id: int, new_product: Product):
    order_query = products.select().where(products.c.id == product_id)
    existing_product = await database.fetch_one(order_query)
    if existing_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой продукт не найден")
    query = products.update().where(products.c.id == product_id).values(name=new_product.name,
                                                                        description=new_product.description,
                                                                        price=new_product.price)
    await database.execute(query)
    updated_query = products.select().where(products.c.id == product_id)
    updated_product = await database.fetch_one(updated_query)
    return updated_product


@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/orders/", response_model=List[Order])
async def read_orders(skip: int = 0, limit: int = 10):
    query = orders.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/products/", response_model=List[Product])
async def read_products(skip: int = 0, limit: int = 10):
    query = products.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не найден")
    return result


@app.get("/orders/{order_id}")
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой заказ не найден")
    return result


@app.get("/products/{products_id}")
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой продукт не найден")
    return result


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не найден")
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": f"Пользователь {user_id} удален"}


@app.delete("/orders/{order_id}")
async def delete_user(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой заказ не найден")
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": f"Заказ {order_id} удален"}


@app.delete("/products/{product_id}")
async def delete_user(product_id: int):
    query = products.select().where(products.c.id == product_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой продукт не найден")
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": f"Продукт {product_id} удален"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)