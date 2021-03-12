import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
pd.options.display.max_colwidth = 150

links_acessados = []

def get_all_links(str_page):
    '''
    This function takes all links from a page
    '''

    soup = bs(str_page, features="html.parser")

    link_tags = soup.find_all("a")

    links = set(tag.get("href") for tag in link_tags 
        if tag.get("href"))

    return links

def filter_links():
    '''
    This function takes all links from a page
    '''

    links = pd.read_csv("links.csv").squeeze()

    mask_real_links = links.str.contains(pat = 'component')
    print(links[mask_real_links][1])

    return links[mask_real_links]

async def get_titles(session):
    '''
    This function takes all links from a page
    '''

    links = pd.read_csv("links.csv").squeeze()

    mask_real_links = links.str.contains(pat = 'component/k2/item/')
    filtered_links = links[mask_real_links]
    #print(links[mask_real_links][:5])
    clean_filtered_links = []
    df = pd.DataFrame(columns=['link', 'title', 'wr','info'])
    with open("links_filtered.csv", 'w') as filehandle:
        for item in filtered_links:
            if item.find("https://www.latinnews.com/https://www.latinnews.com/") and ("full=true" in item)==False:
                new_item = item.replace("https://www.latinnews.com/https://www.latinnews.com/","https://www.latinnews.com/")
                filehandle.write(f'{new_item}\n')
                clean_filtered_links.append(new_item)
            elif item.find("https://www.latinnews.com/https://www.latinnews.com/https://www.latinnews.com/") and ("full=true" in item)==False:
                new_item = item.replace("https://www.latinnews.com/https://www.latinnews.com/https://www.latinnews.com/","https://www.latinnews.com/")
                filehandle.write(f'{new_item}\n')
                clean_filtered_links.append(new_item)
            else:
                if ("full=true" in item)==False:
                    filehandle.write(f'{item}\n')
                    clean_filtered_links.append(item)
    print("\n========================\n")
    [print(i,link) for i,link in enumerate(clean_filtered_links)]
    print("\n========================\n")

    sem = asyncio.Semaphore(2)
    data = []
    for count, link in enumerate(clean_filtered_links):#[:3]:    
        async with session.get(link) as response:
            print(count, link)
            #await get_info(session,link)
            #print(link)
            text = await response.text()
            soup = bs(text,"html.parser")
            title = soup.select('title')[0].text.strip()
            wr = soup.select('h1')[0].text.strip()
            info = soup.select('div.itemFullText')[0].text.strip()

            #print(f"{link}\n{title}\n{wr}\n{info}")
            values = [link, title, wr, info]
            zipped = zip(list(df), values)
            data.append(dict(zipped))

    df = df.append(data, True)
    df.to_csv('summary-v1.csv')
            

def get_title():
    url="https://www.latinnews.com//component/k2/item/87386.html?archive=33&Itemid=6&cat_id=824689:haiti-crisis-intensifies-as-opposition-makes-good-its-threat"
    url="https://www.latinnews.com//component/k2/item/87560.html?full=true&archive=33&cat_id=824807:argentina-s-fernandez-seeks-mexican-support-for-axis-of-good"
    get_url = requests.get(url)
    get_text = get_url.text
    soup = bs(get_text, "html.parser")
    title = soup.select('h1')[0].text.strip()
    info = soup.select('div.itemFullText')[0].text.strip()
    print(title,info)

def get_info(url):
        
    get_url = requests.get(url)
    get_text = get_url.text
    soup = bs(text,"html.parser")
    title = soup.selec('h1')[0].text.strip()
    with open("info.csv","w") as filehandle:
        filehandle.write(f'{title}\n')

#async def get_info(session, site):
#    try:
#        async with session.get(url) as response:
#            text = await response.text()
#            soup = bs(text,"html.parser")
#            title = soup.select('h1')[0].text.strip()
#            info = soup.select('div.itemFullText')[0].text.strip()
#            with open("info.csv", 'w') as filehandle:
#                filehandle.write(f'{title}\n')
#
async def look_for_sites(session, site, prof=0):

    async with session.get(site) as response:

        texto = await response.text()
        #print(get_all_links(texto))
        links = [link for link in get_all_links(texto)]

        root_page = "https://www.latinnews.com/"
        [links_acessados.append(f"{root_page}{link}") for link in get_all_links(texto) ]
            #if link[:11] == "'/component"]
        #print(links)
        if prof <= 2:
            i = 1
            for link in links:
                if i > 2:
                    break
                if link not in links_acessados:
                    links_acessados.append(f"{root_page}{link}")
                    n_prof = prof + 1
                    await look_for_sites(session, f"{root_page}{link}", prof=n_prof)
                    i = i + 1

        #print(f"{site}\t{texto[:30]}")
        links_acessados.append(site)
        with open("links.csv", 'w') as filehandle:
            for item in links_acessados:
                filehandle.write(f'{item}\n')

        #print(links)
#async def main(site):
#    links_acessados.append(site) 
#    async with aiohttp.ClientSession() as session:
#        await look_for_sites(session, site)
 #      await get_titles(session)

async def main():
    async with aiohttp.ClientSession() as session:
        await get_titles(session)

if __name__ == "__main__":
    site = "https://www.latinnews.com/component/k2/itemlist/category/33.html?archive=true&archive_id=33&period=2021"
    #asyncio.run(main(site))
    #filter_links()
    #get_title()
    #url="https://www.latinnews.com//component/k2/item/87386.html?archive=33&Itemid=6&cat_id=824689:haiti-crisis-intensifies-as-opposition-makes-good-its-threat"
    #print_page(url)
    #get_title()
    asyncio.run(main())
    #print("oi")