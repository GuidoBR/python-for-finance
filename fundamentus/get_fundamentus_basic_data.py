"""
Script para pegar P/L, Valor de Mercado, Patrimônio Líquido e Lucro Líquido
de empresas da B3
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://fundamentus.com.br/"

"""
>>> get_stock_url('ITSA3')
'http://fundamentus.com.br/detalhes.php?papel=ITSA3'
"""
def get_stock_url(stock):
    return "{}detalhes.php?papel={}".format(BASE_URL, stock)


def get_stocks():
    with open("fundamentus.txt", "r") as fundamentus_file:
        stocks = fundamentus_file.read().split()
    return stocks

def get_pl(table):
    return table.select('.w2.data')[0].select('.txt')[0].string

def get_patrimonio_liquido(table):
    return table.select('.data span.txt')[5].string

def get_lucro_liquido(table):
    return table.select('.data .txt')[4].string

def get_valor_mercado(table):
    return table.select('.data .txt')[0].string

def get_stock_page(stock_url):
    req = requests.get(stock_url)
    return req.content

def get_fundamentalist_data(stocks):
    stocks_info = []
    for stock in stocks:
        print("Getting data for Stock {}".format(stock))
        stock_url = get_stock_url(stock)
        page = get_stock_page(stock_url)
        html = BeautifulSoup(page, 'html.parser')

        # Tabelas
        # 0 - Cotação
        # 1 - Valor de mercado
        # 2 - Indicadores fundamentalistas
        # 3 - Balanço patrimonial
        # 4 - Demonstrativo de resultados
        tables = html.select("table.w728")

        stocks_info.append({
            'codigo': stock,
            'pl': get_pl(tables[2]),
            'patrimonio_liquido': get_patrimonio_liquido(tables[3]),
            'lucro_liquido': get_lucro_liquido(tables[4]),
            'valor_mercado': get_valor_mercado(tables[1]),
        })

    return stocks_info

def save_data_to_json(data):
    filename = 'fundamentalist_data.json'
    with open(filename, 'w') as f:
        f.write(str(data))


if __name__ == "__main__":
    stocks = get_stocks()
    stocks_info = get_fundamentalist_data(stocks[:])
    save_data_to_json(stocks_info)

