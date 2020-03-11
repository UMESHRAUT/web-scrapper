import requests
from requests.compat import quote_plus
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
# Create your views here.
BASE_CRAIGSLIST_URL="https://rockford.craigslist.org/search/sss?query={}"
BASE_IMAGE_URL="https://images.craigslist.org/{}_300x300.jpg"
def home(request):
    return render(request,'base.html')


def new_search(request):
    search=request.POST.get('search')
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    models.Search.objects.create(search=search)
    response=requests.get(final_url)
    data=response.text
    soup = BeautifulSoup(data,features='html.parser')

    final_postings=[]

    post_listings = soup.find_all('li',{'class':'result-row'})
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url=post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price ='N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0]
            post_image_url=BASE_IMAGE_URL.format(post_image_id[2:])
            print(post_image_url)
        else:
            post_image_url='https://vignette.wikia.nocookie.net/jumanji/images/c/cf/No-image-icon-15.png/revision/latest?cb=20180911184127'
        final_postings.append((post_title,post_url,post_price,post_image_url))
    #
    # # print(data)
    stuff_for_frontend={
        'search':search,
        'final_postings':final_postings,
        }
    return render(request,'my_app/new_search.html',stuff_for_frontend)
