from bs4 import BeautifulSoup
import csv
import json
import os 

source_file = './農業試驗所.html'
output_dir = '../'
output_filename = 'pests_and_diseases'

def write_to_csv(output_list):
    with open(output_dir+output_filename+'.csv', 'w', encoding='utf16', newline='') as csvfile:

        fieldnames = ['圖片', '病蟲害名稱', '危害作物/防治對象', '危害徵狀']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_list)

def write_to_json(output_list):
    with open(output_dir+output_filename+'.json', 'w', encoding='utf16') as file:
        json.dump(output_list, file, ensure_ascii=False)

def check_output_dir():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def main():
    f = open(source_file)
    html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find(id='tablebody')
    soup = soup.find_all('tr')

    output_list = []

    for tr in soup:
        tds = tr.find_all('td', class_='body-item')
        output_list.append(
            {
                '圖片': tds[0].find('img').get('src'),
                '病蟲害名稱': tds[1].find('a').text,
                '危害作物/防治對象': tds[2].find('a').text,
                '危害徵狀': tds[3].find('a').text
            }
        )

    check_output_dir()

    write_to_csv(output_list)

    write_to_json(output_list)

if __name__ == '__main__':
    main()

# import pandas as pd
# df = pd.read_excel('Downloads/病蟲害20231213.xlsx', usecols='B,D,E')
# df.to_csv('out.csv', encoding='utf-16', index=False)