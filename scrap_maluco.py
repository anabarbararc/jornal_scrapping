import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

links_acessados = []

def get_all_links(str_page):
    '''
    This function takes all links from a page
    '''

    soup = bs(str_page, features="html.parser")

    link_tags = soup.find_all("a")

    links = set(tag.get("href") for tag in link_tags 
        if tag.get("href"))
    #weeklyreport = set(tag.get("h1") for tag in link_tags 
    #    if tag.get("h1"))

    return links


async def look_for_sites(session, site, prof=0):

    async with session.get(site) as response:

        texto = await response.text()
        #print(get_all_links(texto))
        links = [link for link in get_all_links(texto)]
        [links_acessados.append(f"https://www.latinnews.com/{link}") for link in get_all_links(texto)]
            #if link[:11] == "'/component"]
        #print(links)
        if prof <= 2:
            i = 1
            for link in links:
                if i > 2:
                    break
                if link not in links_acessados:
                    links_acessados.append(f"https://www.latinnews.com/{link}")
                    n_prof = prof + 1
                    await look_for_sites(session, f"https://www.latinnews.com/{link}", prof=n_prof)
                    i = i + 1

        #print(f"{site}\t{texto[:30]}")
        links_acessados.append(site)
        with open("links.csv", 'w') as filehandle:
            for item in links_acessados:
                filehandle.write(f'{item}\n')

        print(links_acessados)

async def main(site):
    links_acessados.append(site) 
    async with aiohttp.ClientSession() as session:
        await look_for_sites(session, site)

if __name__ == "__main__":

    site = "https://www.latinnews.com/component/k2/itemlist/category/33.html?archive=true&archive_id=33&period=2021"

    asyncio.run(main(site))