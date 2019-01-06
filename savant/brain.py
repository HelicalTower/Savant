#!/usr/bin/python3

#########################################################################################
#Title: brain.py
#Author: Douglas T.
#Creation Date: 02/01/2019
#Description: This is the brains of the Savant app. This takes in two strings, which
#             contain the sites to be searched and the string to search for.  It then
#             uses Requests to connect to the desired site with the search parameter,
#             and BeautifulSoup to parse the returned html.  The necessary information
#             is then written to the file 'search_results.xlsx' before returning.
#
#Changelog:
#Name:          Date:       Change:
# Douglas T.    02/01/2019  Initial version 
#########################################################################################


import sys
import csv
import requests
from bs4 import BeautifulSoup

def request_work(input_string, site): 

    search_string = str(input_string).replace(' ', '+')
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

    if site == 'amazon':
        url = "https://www.amazon.com/s/ref=nb_sb_noss_1/146-9936988-0016847?url=search-alias%3Daps&field-keywords=" + search_string
    elif site == 'newegg':
        url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + search_string
    else:
        return('Given site cannot be scraped.')

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    return(soup)

def amazon_search(soup):
    names, links, price, review_score = [], [], [], []

    #combo_results = soup.find('div', {'id' : 'a-page'}).find('div', {'id' : 'search-main-wrapper'})
    li_0_results = soup.find_all('li', {'class' : 's-result-item celwidget '})
    li_1_results = soup.find_all('li', {'class': 's-result-item celwidget AdHolder'})
    combo_results = li_0_results + li_1_results
    print(str(len(combo_results)))
    for x in combo_results:
        #names
        names.append((x.find_next('a', 'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal').get('title')).replace(',', ' '))
        #links
        links.append((x.find_next('a', 'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal').get('href')))
        #prices
        price.append(x.find('span', 'a-price').find('span', 'a-offscreen').get_text())

    return(0)
"""
.find('div', 'search-main-wrapper').find('div', 'main').find('div', 'searchTemplate').find('div', 'rightContainerATF').find('div', 'rightResultsATF').find('div', 'resultsCol').find('div', 'centerMinus').find('div', 'atfResults').find('ul', 's-results-list-atf').find_all('li')
    print(str(len(combo_results)))


    combo_results = soup.find_all('a', 'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal')
    for x in combo_results:
        #print(x.get('title'))
        names.append((x.get('title')).replace(',', ''))
        #print(x.get('href'))
        if (x.get('href')).find('/gp/', 0, 4) == -1:
            links.append((x.get('href')).lstrip(' '))
        else:
            links.append('https://www.amazon.com'+(x.get('href')).lstrip(' '))
    
    price_results = soup.find_all('span', 'a-offscreen')
    for x in price_results:
        if x.string != '[Sponsored]':
            #print(x.string)
            price.append(x.string)

    reviews = soup.find_all('span','a-icon-alt')
    print(str(len(reviews)))
    for x in reviews:
        if 'out of' in str(x.contents):
            review_score.append(str(x.contents))
        else:
            review_score.append(' ')
"""
    #return(names, links, price, review_score)

def newegg(soup):
    names, links, price, review_score = [], [], [], []

    combo_results = soup.find_all('div', 'item-container ')
    for x in combo_results:
        #Get title
        names.append((x.find('a', 'item-img').find('img').get('title')).replace(',', ''))
        #Get links
        links.append(x.find('a', 'item-title').get('href'))
        #Get price

        #price.append("$" +x.find('li', 'price-current').find('strong').get_text() + x.find('li', 'price-current').find('sup').get_text())
       
        cost_dollars = x.find('li', 'price-current').find('strong')
        cost_cents = x.find('li', 'price-current').find('sup')

        if cost_dollars is not None and cost_cents is not None:
            price.append(('$' + cost_dollars.get_text() + cost_cents.get_text()).replace(',', ''))
        else:
            price.append("Out of stock")
        #Get review score
        #score = (x.find('a', 'item-rating').get('title'))[-1:]
        score = x.find('a', 'item-rating')
        if score is not None:
            review_score.append((score.get('title'))[-1:] + " out of 5")
        else:
            print(" ")
            review_score.append(' ')

    return(names, links, price, review_score)

def file_write(sites_search, input_string, names, links, price, review_score):
    '''
    with open('search_results.xlsx', 'w') as f:
        f.write(sites_search + ": " + (input_string.replace(',', '+')) + "\n")
        f.write("Name:, Price:, Review Score:, Links:\n")
        for x in range(0, len(names)):
            f.write(names[x] + ", " + price[x] + ", " + review_score[x] + ", " + links[x] + "\n")
    '''
    with open('search_results.csv', 'w', newline ='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([sites_search + ': ' + (input_string.replace(',', ' +'))])
        csv_writer.writerow(['Name:', 'Price:', 'Review Score:', 'Links'])
        for x in range(0, len(names)):
            csv_writer.writerow([names[x], price[x], review_score[x], links[x]])

    return(0)

def file_read():
    full_file = ''

    with open('search_results.csv', 'r', newline='') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            for x in row:
                full_file = full_file + x + '   |   '
            full_file = full_file + '\n'

    return(full_file)

#Used to help with setting up new sites
def soup_write(soup):
    with open('soup.html', 'w') as f:
        f.write(soup)

    return(0)

def start(sites, search):

    sites_search = sites
    input_string = search

    names, links, price, review_score = [], [], [], []

    if "Amazon" in str(sites_search):
        page_soup = request_work(input_string, 'amazon')
        #names, links, price, review_score = amazon_search(page_soup)
        amazon_search(page_soup)
    if "Newegg" in str(sites_search):
        page_soup = request_work(input_string, 'newegg')
        names, links, price, review_score = newegg(page_soup)
   
    #print("names: " + str(len(names)))
    #print("links: " + str(len(links)))
    #print("price: " + str(len(price)))
    #print("review_score: " + str(len(review_score)))    

    file_write(sites_search, input_string, names, links, price, review_score)

