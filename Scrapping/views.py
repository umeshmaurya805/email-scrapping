from django.shortcuts import render
from selenium import  webdriver 
from bs4 import BeautifulSoup
import re
import csv  
import pandas as pd
regex = '^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$'
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
webD = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

from django.http import HttpResponse


def check(email):  
    if(re.search(regex,email)):  
        return 1
    else :
        return 0
          
def download_csv(request,url):
    webD.get(url)
    page_source=webD.page_source
    soup=BeautifulSoup(page_source,"lxml")
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="Emails.csv"'  
    writer = csv.writer(response)  
    for sou in soup.stripped_strings:
        if(check(sou)):
            writer.writerow([sou]) 
    return response


def scrap(request):
    if(request.method=="POST"):
        url=request.POST.get('url')
        return download_csv(request,url)
        
    return render(request,'index.html',{'page':"Home"})
