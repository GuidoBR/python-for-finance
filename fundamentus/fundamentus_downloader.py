import requests
import sys
import fundamentus

def download_all(stocks, session_id):
    s = requests.Session()
    for stock in stocks:
        referer_url = "{}balancos.php?papel={}&tipo=1".format(
                fundamentus.get_base_url(),stock)
        s.get(referer_url)
        s.headers.update({'Referer': referer_url})
        s.headers.update({'HOST': fundamentus.get_base_url()})
        s.headers.update({'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"})
        s.headers.update({'Cookie': "__utmt=1; PHPSESSID={}; __utma=138951332.685737504.1494551880.1494996032.1495510253.5; __utmb=138951332.4.10.1495510253; __utmc=138951332; __utmz=138951332.1494551880.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)".format(session_id)})

        download_link = "{}planilhas.php?SID={}".format(
                fundamentus.get_base_url(), session_id)
        stock_file = s.get(download_link)

        with open("./balancos/{}.zip".format(stock), 'wb') as f:
            print("Downloading {} ...".format(stock))
            for chunk in stock_file.iter_content(chunk_size=128):
                f.write(chunk)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage example: python fundamentus_downloader.py e81tphr617q54")
    else:
        session_id = sys.argv[1]
        stocks = fundamentus.get_stocks()
        download_all(stocks, session_id)
