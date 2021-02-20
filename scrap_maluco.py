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

    return links

async def look_for_sites(session, site, prof=0):

    async with session.get(site) as response:

        texto = await response.text()

        links = [ link for link in get_all_links(texto)
            if link[:20] == "https://g1.globo.com"]
        
        if prof <= 3:
            i = 1
            for link in links:
                if i > 3:
                    break
                if link not in links_acessados:
                    links_acessados.append(link)
                    n_prof = prof + 1
                    await look_for_sites(session, link, prof=n_prof)
                    i = i + 1

        print(f"{site}\t{texto[:15]}")
        links_acessados.append(site)
async def main(site):
    links_acessados.append(site) 
    async with aiohttp.ClientSession() as session:
        await look_for_sites(session, site)

if __name__ == "__main__":

    site = "http://www.g1.com.br"

    asyncio.run(main(site))