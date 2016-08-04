import urllib.request
from bs4 import BeautifulSoup

base_url = 'http://www.domofond.ru/prodazha-kvartiry-magnitogorsk-c2293'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def pagination(html):
    soup = BeautifulSoup(html)
    number = soup.find_all('ul', {'class': 'pagination'})[-1].text
    number = re.sub("\D", "", number)
    return number
    


def parse(html):
    
    soup = BeautifulSoup(html)
    table = soup.find('div', {'id': 'listingResults'})
    rows = table.find_all('div', {'class': 'pull-left df_listingTileContent '})
    
    flats = []
    
    for row in rows:
        #Находим цену квартиры в теге <p> и преобразовываем в текст
        price = row.find('p').text
        #Преобразовываем весь найденный текст в число /отбрасывая все буквы, оставляя лишь числа/
        price = re.sub("\D", "", price)
        
        #Находим цену квадрата квартиры в теге <span>
        square_price = row.find('span').text
        square_price = re.sub("\D", "", square_price)
        
        square = row.find('li').text
        square = re.sub("\D", "", square)
        
        floor = (row.find('li')).find_next('li').text
        floor = re.findall('(\d+)', floor)
        
        address = row.find('span', {'itemprop': 'address'}).text



        #добавляем квартиры в словарь
        flats.append({
                'price': price,
                'square_price': square_price,
                'square': square,
                'floor': floor[0],
                'floor_all': floor[-1],
                'address': address
        })
    
    return flats


def main():
    page_count = int(pagination(get_html(base_url)))
    
    parse(get_html('http://www.domofond.ru/prodazha-kvartiry-magnitogorsk-c2293'))
    
    flats = []
    

    
    
    for page in range(1, 11):
        #print('Parsim %d%%' %(page / page_count * 10))
        flats.extend(parse(get_html(base_url + '?Page=%d' % page)))
    
    for flat in flats:
        print(flat)

                   
if __name__ == '__main__':
    main()
