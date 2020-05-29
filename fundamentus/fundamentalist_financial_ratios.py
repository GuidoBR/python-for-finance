"""
Get Fundamentalist Financial Ratios from Fundamentus website
B3 - BVM&F Bovespa - Brasil, Bolsa, Balcão
"""
from bs4 import BeautifulSoup
import fundamentus
import csv

def extract_data_from(table, position):
    return table.select('.data .txt')[position].string.strip()

def get_fundamentalist_data(stocks):
    stocks_info = []
    for stock in stocks:
        print("Getting data for Stock {}".format(stock))
        stock_url = fundamentus.get_stock_url(stock)
        page = fundamentus.download_stock_html(stock_url)
        html = BeautifulSoup(page, 'html.parser')

        # Tabelas
        # 0 - Cotação
        tables = html.select("table.w728")

        stocks_info.append({
            'codigo': stock,
            # 1 - Valor de mercado
            'valor_mercado': extract_data_from(tables[1], 0),
            'valor_firma': extract_data_from(tables[1], 2),
            'numero_acoes': extract_data_from(tables[1], 3),
            # 2 - Indicadores fundamentalistas
            'p/l': extract_data_from(tables[2], 0),
            'lpa': extract_data_from(tables[2], 1),
            'p/vp': extract_data_from(tables[2], 2),
            'vpa': extract_data_from(tables[2], 3),
            'p/ebit': extract_data_from(tables[2], 4),
            'p/ativos': extract_data_from(tables[2], 5),
            'p/cap.giro': extract_data_from(tables[2], 6),
            'p/ativ.circ.liq': extract_data_from(tables[2], 7),
            # 3 - Balanço patrimonial
            'ativo': extract_data_from(tables[3], 0),
            'disponibilidades': extract_data_from(tables[3], 1),
            'ativo_circulante': extract_data_from(tables[3], 2),
            'div_bruta': extract_data_from(tables[3], 3),
            'div_liquida': extract_data_from(tables[3], 4),
            'patrimonio_liquido': extract_data_from(tables[3], 5),
            # 4 - Demonstrativo de resultados
            'lucro_liquido': extract_data_from(tables[4], 4),
        })

    return stocks_info

def get_headers(stocks):
    return list(stocks_info[0].keys())

def save_data_to_json(data):
    filename = 'fundamentalist_data.json'
    with open(filename, 'w') as f:
        f.write(str(data))

def save_data_to_csv(data):
    filename = 'fundamentalist_data.csv'
    with open(filename, 'w') as f:
        header = get_headers(data)
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)

        for stock in data:
            writer.writerow(stock.values())


if __name__ == "__main__":
    stocks = fundamentus.get_stocks()
    stocks_info = get_fundamentalist_data(stocks)
    save_data_to_csv(stocks_info)

