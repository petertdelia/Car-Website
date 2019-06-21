# make_db creates a list of cars and inserts them into a sql database

import requests, time
from bs4 import BeautifulSoup

def make_soup(url,headers):
    r = requests.get(url, headers=headers)
    r.status_code
    soup_html = BeautifulSoup(r.text)
    time.sleep(2)
    r.close() # is this necessary or does it even work?
    return soup_html

def find_number_of_pages(soup_html):
    num_pages_container = soup_html.findAll("ul", {"id":"paginationStationContainer"})
    num_pages_text = num_pages_container[0].text.split()
    num_pages = int(num_pages_text[2])
    return num_pages

def make_car_list(num_pages):
    car_list = []
    for i in range(1,num_pages + 1): 
        url = 'https://www.carsforsale.com/Search?Make=Ford&Model=Edge&Conditions=used&PageNumber=' + str(i) + '&OrderBy=Relevance&OrderDirection=Desc'
        headers = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0','serverid':'extweb203|XPqvG|XPquy','Cookie':'__cfduid=d9506a80c78c5c2890782574b34f03cc81559932617'}
        soup_html = make_soup(url,headers)
        name_containers = soup_html.findAll("a", {"class":"vehicle-name"})

        temp_car_list = [[] for i in range(len(name_containers))]
        print('length of name_containers is' + str(len(name_containers)))
        print('length of temp_car_list is' + str(len(temp_car_list)))
        i=0
        for index in name_containers:  
            name = name_containers[i].h4.text  
            temp_car_list[i] = name.split()
            i+=1

        mileages = soup_html.findAll("div",{"class":"specs-miles"})
        print('length of mileages is' + str(len(mileages)))
        for i in range(len(mileages)): 
            mileages[i] = mileages[i].text.split()
            mileage = mileages[i]
            mileages[i] = mileage[0]
            try:
                temp_car_list[i].append(mileages[i])
            except IndexError:
                print('index out of range--oops!')
            
        car_list.extend(temp_car_list)
    return car_list

url = 'https://www.carsforsale.com/Search?Make=Ford&Model=Edge&Conditions=used&PageNumber=1&OrderBy=Relevance&OrderDirection=Desc'
headers = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0','serverid':'extweb203|XPqvG|XPquy'}

soup_html = make_soup(url,headers)
num_pages = find_number_of_pages(soup_html)
car_list = make_car_list(soup_html)

def make_url()
