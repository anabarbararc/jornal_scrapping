import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from tqdm import tqdm 
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
    Reads the csv file and creates a filtered/clean list 
    '''
    links = pd.read_csv("links.csv").squeeze()

    mask = links.str.contains(pat='component/k2/item/')
    filtered_links = links[mask]

    clean_filtered_links = []

    rootpage = "https://www.latinnews.com/"

    with open("links_filtered.csv", 'w') as filehandle:
        for item in filtered_links:
            if (("full=true" in item)==False):
                if item.find(f"{rootpage}{rootpage}"):
                    new_item = item.replace(f"{rootpage}{rootpage}",f"{rootpage}")
                    filehandle.write(f'{new_item}\n')
                    clean_filtered_links.append(new_item)
                elif item.find(f"{rootpage}{rootpage}{rootpage}"):
                    new_item = item.replace(f"{rootpage}{rootpage}{rootpage}",f"{rootpage}")
                    filehandle.write(f'{new_item}\n')
                    clean_filtered_links.append(new_item)
                else:
                    filehandle.write(f'{item}\n')
                    clean_filtered_links.append(item)

    return clean_filtered_links

async def get_titles(session, list_links):
#    '''
#    This function takes the information from a page
#    '''
    df = pd.DataFrame(columns=['link', 'title', 'wr','info'])
    data = []
    pbar = tqdm(set(list_links))
    for link in pbar:
        pbar.set_description(f"Processing link: {link[0:10]}...{link[-10:-1]} ")
        #print(,flush='True')
        #pbar.set_description("Processing %s" % char)    
        async with session.get(link) as response:
            #await get_info(session,link)
            #print(link)
            text = await response.text()
            soup = bs(text,"html.parser")
            title = soup.select('title')[0].text.strip()
            # sometimes there is a link without the piece of info we want
            if not soup.select('h1')[0].text.strip():
                wr = '0'
            else:
                wr = soup.select('h1')[0].text.strip()
            info = soup.select('div.itemFullText')[0].text.strip()

            #print(f"{link}\n{title}\n{wr}\n{info}")
            values = [link, title, wr, info]
            zipped = zip(list(df), values)
            data.append(dict(zipped))

    df = df.append(data, True)
    #df = df.
    df.to_pickle('summary-v1.pkl')
            
async def look_for_sites(session, site, prof=0):

    async with session.get(site) as response:

        texto = await response.text()
        #print(get_all_links(texto))
        links = [link for link in get_all_links(texto)]

        rootpage = "https://www.latinnews.com/"
        [links_acessados.append(f"{rootpage}{link}") for link in get_all_links(texto) ]

        if prof <= 2:
            i = 1
            for link in links:
                if i > 2:
                    break
                if link not in links_acessados:
                    links_acessados.append(f"{rootpage}{link}")
                    n_prof = prof + 1
                    await look_for_sites(session, f"{rootpage}{link}", prof=n_prof)
                    i = i + 1

        links_acessados.append(site)
        with open("links.csv", 'w') as filehandle:
            for item in links_acessados:
                filehandle.write(f'{item}\n')

async def main():
    links_acessados.append(site) 
    async with aiohttp.ClientSession() as session:
        await look_for_sites(session, site)
    async with aiohttp.ClientSession() as session:
        await get_titles(session,filter_links())

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