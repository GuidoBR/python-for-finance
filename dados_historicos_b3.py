import asyncio
import aiohttp
import time
from os.path import join
from urllib.request import urlretrieve



BASE_URL = 'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A'
DEST_FOLDER = './dados-historico-b3/'

@asyncio.coroutine
def get_year(year):
    return f"{BASE_URL}{year}.zip"

@asyncio.coroutine
def download_one(year):
    data_url = yield from get_year(year)
    print(f'Downloading {data_url}')
    urlretrieve(data_url, join(DEST_FOLDER, data_url[-8:]))
    return data_url

def download_many(year_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(year) for year in year_list]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()

    return len(res)

def main(download_many):
    t0 = time.time()
    print('Starting...')
    count = download_many(range(1986, 2021))
    elapsed = time.time() - t0
    msg = '\n{} data downloaded in {:.2f}s'
    print(msg.format(count, elapsed))

if __name__ == '__main__':
    main(download_many)
