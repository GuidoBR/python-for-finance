import requests

BASE_URL = "http://fundamentus.com.br/"

"""
>>> get_stock_url('ITSA3')
'http://fundamentus.com.br/detalhes.php?papel=ITSA3'
"""
def get_stock_url(stock):
    return "{}detalhes.php?papel={}".format(BASE_URL, stock)


"""
>>> get_base_url()
"http://fundamentus.com.br/"
"""
def get_base_url():
    return "http://fundamentus.com.br/"


def get_stocks():
    with open("fundamentus.txt", "r") as fundamentus_file:
        stocks = fundamentus_file.read().split()
    return stocks

def download_stock_html(stock_url):
    req = requests.get(stock_url)
    return req.content

