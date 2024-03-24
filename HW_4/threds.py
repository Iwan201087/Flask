import threading
import time
import requests
import sys

def get_file(url, start_time):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")
    else:
        print(f"Failed to download {url}: HTTP status code {response.status_code}")

def main(urls):
    threads = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=get_file, args=[url, start_time])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
        main(urls)
    else:
        urls = [
            'https://images.pexels.com/photos/19597529/pexels-photo-19597529.jpeg',
            'https://images.pexels.com/photos/19808874/pexels-photo-19808874.jpeg',
            'https://images.pexels.com/photos/12801958/pexels-photo-12801958.jpeg'
        ]
        main(urls)