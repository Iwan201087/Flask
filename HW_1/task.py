# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна
# (шапка, меню, подвал), и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
# Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.
from flask import Flask
from flask import render_template

app = Flask(__name__)
context = {
    'data': {'Одежда': ['Куртки', 'Джинсы'], "Обувь": ['Туфли', 'Сапоги']},
}


@app.route('/')
def index():
    context_index = {
        'title': 'Интернет Магазин "Fashion is our profession:)',
        'content_main': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Adipisci et saepe, unde consectetur nemo repellendus!',
    }
    return render_template('index.html', **context_index)


@app.route('/Catalog')
def catalog():
    context['title'] = 'Каталог'
    return render_template('catalog.html', **context)


@app.route('/Catalog/<category>')
def cat(category):
    if category in context['data'].keys():
        context['title'] = category
        return render_template('category.html', **context)
    else:
        context['title'] = 'Ошибка'
        return render_template('error.html', **context)


@app.route('/Catalog/<category>/<product>')
def prod(category, product):
    if category in context['data'].keys() and product in context['data'][category]:
        context['title'] = product
        context['category'] = category
        context['product'] = "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nostrum eveniet officia similique, temporibus ad deleniti tempore iusto nobis repudiandae vel?"
        return render_template('product.html', **context)
    return cat(category)


@app.route('/Contact')
def contact():
    context_contact = {
        'title': 'Контакты',
        'data': {'email': 'fiop@gmail.com', 'tel': '+375297452477'},
    }
    return render_template('contact.html', **context_contact)


if __name__ == '__main__':
    app.run(debug=True)