from lxml import html
import requests

def open_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    page = requests.get(url, headers = headers)
    return page

def parse_crypto(page):
    results = []
    tree = html.fromstring(page.content)
    numbers = tree.xpath('//div[@class = "row"]')[0]
    price = numbers.xpath('//div[@class="birzha_info_head_rates"]/text()')[0]
    up = numbers.xpath('//div[@class="birzha_info_head_rates up" or @class="birzha_info_head_rates down"]/text()')[0]
    dates = tree.xpath('//div[@class = "birzha_info"]')[0]
    day = dates.xpath('//div[@class = "birzha_info_rates up" or @class = "birzha_info_rates down"]/text()')
    results.append({
        'price': price.split()[0],
        'up': up.split()[0],
        'day': day[0].split()[0],
        'week': day[1].split()[0],
        'month': day[2].split()[0],
        'sixmonth': day[3].split()[0]
    })
    return results
def parse_top_crypto(page):
    results = []
    names = []
    hrefs = []
    tree = html.fromstring(page.content)
    table = tree.xpath('//table[@class = "items"]//tbody[@class = "table-body"]//tr[@class = "odd" or @class = "even"]')
    name = table[0].xpath('//div[@class = "names"]//a//text()')
    for i in range(12):
        names.append(name[i].strip())
    links = table[0].xpath('//div[@class = "names"]//a')[0:12]
    for link in links:
        href = link.get('href').split("/")[2]
        hrefs.append(href)
    results.append(names)
    results.append(hrefs)

    return results
page = open_page('https://myfin.by/crypto-rates/')
print(parse_top_crypto(page))