from bs4 import BeautifulSoup as bs
import requests

def get_all_links(str_page):
    '''
    This function takes all links from a page
    '''

    soup = bs(str_page, features="html.parser")

    link_tags = soup.find_all("a")

    links = set(tag.get("href") for tag in link_tags 
        if tag.get("href"))

    return links

def look_for_sites(site, prof=0):

        response = requests.get(site)
        texto =  response.text

        links = [ link for link in get_all_links(texto)
            if link[:20] == "https://g1.globo.com"]
        
        if prof <= 3:
            for link in links[:3]:
                n_prof = prof + 1
                look_for_sites(link, prof=n_prof)

        print(f"{site}\t{texto[:15]}")

def main(site):
        look_for_sites(site)

if __name__ == "__main__":

    site = "http://www.g1.com.br"

    main(site)