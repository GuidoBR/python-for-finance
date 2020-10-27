import asyncio
import aiohttp
import time
from os.path import join
from urllib.request import urlretrieve



BASE_URL = 'http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A'
DEST_FOLDER = './dados-historico-b3/'

import os
from multiprocessing import Pool, cpu_count
import urllib.request

urlbasepath='http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A'
ext='.zip'
# não dá pra usar os cores pois os downlads dependem da sua banda
multiplier=2
# troca pelo path que você preferir ex: c:/
destinationPath = DEST_FOLDER
print("destino dos arquivos: %s " % destinationPath)
urls=[urlbasepath+str(i)+ext for i in range(1986,2019)]

def download_zips(url):
  file_name = url.split("/")[-1]
  print("\n iniciando download {} ".format(file_name))
  urllib.request.urlretrieve(url, destinationPath+file_name)
  print("\n Download {} finalizado".format(file_name))

if __name__ == "__main__":
  pool = Pool(cpu_count()*multiplier)
  results = pool.map(download_zips, urls)
  pool.close()
  pool.join()
