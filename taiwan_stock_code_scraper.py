import requests
from bs4 import BeautifulSoup
import csv
import json
import re

def get_taiwan_stocks():
    stocks = []

    def process_url(url, market):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='h4')
        if table:
            rows = table.find_all('tr')
            for row in rows[2:]:  # 跳過前兩行（標題和欄位名）
                cols = row.find_all('td')
                if len(cols) >= 4:
                    code_name = cols[0].text.strip().split('\u3000')
                    if len(code_name) == 2:
                        code, name = code_name
                        # 股票代碼是否為四位數字
                        if re.match(r'^\d{4}$', code):
                            stocks.append({
                                "StockCode": code,
                                "StockName": name,
                                "YahooFinanceSymbol": f"{code}.{market}"
                            })
        else:
            print(f"無法在 {url} 找到表格")

    # 爬取上市股票列表
    url_listed = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    process_url(url_listed, 'TW')

    # 爬取上櫃股票列表
    url_otc = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
    process_url(url_otc, 'TWO')

    return stocks

try:
    taiwan_stocks = get_taiwan_stocks()
    print(f"總共找到 {len(taiwan_stocks)} 支股票")


    # 儲存為CSV
    with open('taiwan_stocks.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["StockCode", "StockName", "YahooFinanceSymbol"])
        writer.writeheader()
        writer.writerows(taiwan_stocks)
    print("數據已保存到 taiwan_stocks.csv")

    # 儲存為JSON
    with open('taiwan_stocks.json', 'w', encoding='utf-8') as f:
        json.dump(taiwan_stocks, f, ensure_ascii=False, indent=2)
    print("數據已保存到 taiwan_stocks.json")

except Exception as e:
    print(f"發生錯誤: {e}")
    import traceback
    traceback.print_exc()