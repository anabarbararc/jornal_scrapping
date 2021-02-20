import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

links_acessados = []

HOST = "https://liberal.com.br"
lenHOST = len(HOST)

def get_all_links(str_page):
    '''
    This function takes all links from a page
    '''

    soup = bs(str_page, features="html.parser")

    link_tags = soup.find_all("a")

    links = set(tag.get("href") for tag in link_tags 
        if tag.get("href"))

    return links

async def look_for_sites(session, site, sem, prof=0):

    #Block semaphore
    #await sem.acquire()
    async with sem:
        async with session.get(site) as response:

            texto = await response.text()

            links = [ link for link in get_all_links(texto)
                if link[:lenHOST] == HOST]
            
            if prof <= 3:
                i = 1
                for link in links:
                    if i > 3:
                        break
                    if link not in links_acessados:
                        links_acessados.append(link)
                        n_prof = prof + 1
                        await look_for_sites(session, link, sem, prof=n_prof)
                        i = i + 1

            print(f"{site}\t{texto[:15]}")
            links_acessados.append(site)
   # sem.release()

async def main(site):
    links_acessados.append(site) 
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        await look_for_sites(session, site, sem)

if __name__ == "__main__":

    site = HOST

    asyncio.run(main(site))