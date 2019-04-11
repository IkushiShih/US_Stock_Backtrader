#!/usr/bin/env python
# coding: utf-8

# In[1]:


def scrape():
    import time
    import requests
    from bs4 import BeautifulSoup

    req = requests.get("https://finviz.com/screener.ashx?v=111&f=sh_curvol_o1000,sh_price_u30,sh_relvol_o1.5")
    soup = BeautifulSoup(req.content, 'html.parser')
    pages = int(soup.find_all("a", {"class": "screener-pages"})[-1].text)

    passing_stock = []
    for i in range(pages):
        page_idx = i*20 + 1
        req = requests.get("https://finviz.com/screener.ashx?v=111&f=sh_curvol_o1000,sh_price_u30,sh_relvol_o1.5&r={}".format(str(page_idx)))
        soup = BeautifulSoup(req.content, 'html.parser')
        tickers = soup.find_all('a',{'class':'screener-link-primary'})
        for t in tickers:
            passing_stock.append(t.text)
    return passing_stock

if __name__ == '__main__':
    scrape()


# In[ ]:




