"""
projekt_3: třetí projekt do Engeto Akademie
author: Jakub Prokeš
email: prokesjakub.ctf@gmail.com
discord: jpctf
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
import time

# arghelp

def help_links():
    
    base_url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    
    soup = get_soup_from_url(base_url)

    if soup:
        rel_links = []
        
        rows = soup.find_all("tr")
        
        for row in rows:
            
            municipality_name_cell = row.find("td", {"headers": lambda x: x and "sb2" in x})
            
            ps32_link = row.find("a", {"href": True, "href": lambda x: x and "ps32" in x})
            
            if municipality_name_cell and ps32_link:
                municipality_name = municipality_name_cell.text.strip()
                municipality_link = f"https://www.volby.cz/pls/ps2017nss/{ps32_link['href']}"
                
                rel_links.append(f'"{municipality_link}" "vysledky_{municipality_name}.csv"')
        
        if rel_links:
            for rel_link in rel_links:
                print(rel_link)
        else:
            print("Nelze najít vhodné argumenty.")
    else:
        print("Chyba při získávání HTML obsahu pro nápovědu. Zkontrolujte připojení.")
        main()

# data

def get_soup_from_url(url: str) -> BeautifulSoup:
    
    try:
        
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    
    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování stránky {url}: {e}")
        return None

def get_municipality_name(soup: BeautifulSoup) -> list:

    return [municipality.get_text(strip=True) for municipality in soup.find_all("td", class_="overflow_name")]

def get_urls(soup: BeautifulSoup) -> list:
    
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    return [f"{base_url}{url.a['href']}" for url in soup.find_all("td", class_='cislo') if url.a]

def get_municipality_code(soup: BeautifulSoup) -> list:

    return [code.get_text(strip=True) for code in soup.find_all("td", class_="cislo")]

def get_political_parties(urls: list) -> list:
    
    parties = []
    for url in urls:
        html = get_soup_from_url(url)
        for party in html.find_all("td", class_="overflow_name"):
            party_name = party.text.strip()
            if party_name not in parties:
                parties.append(party_name)
    return parties

def get_voter_data(urls: list) -> tuple:
    
    registered_voters, envelopes, valid_votes = [], [], []
    
    def extract_data(html: BeautifulSoup, header_id: str) -> list:
       
        return [cell.text.strip() for cell in html.find_all("td", headers=header_id)]

    for url in urls:
        html = get_soup_from_url(url)
        registered_voters.extend(extract_data(html, 'sa2'))
        envelopes.extend(extract_data(html, 'sa3'))
        valid_votes.extend(extract_data(html, 'sa6'))

    return registered_voters, envelopes, valid_votes

def get_vote_results(urls: list) -> list:

    return [
        [votes.text.strip() for votes in get_soup_from_url(url).find_all("td", class_="cislo",
                                                                         headers=["t1sa2 t1sb3", "t2sa2 t2sb3"])]
        for url in urls
    ]

# csv

def create_rows(municipality_code: list, municipality_name: list, url: list) -> list:
    

    print("Data zpracována","Vytvářím soubor CSV",sep="\n")

    registered_voters, envelopes, valid_votes = get_voter_data(url)
    results = get_vote_results(url)

    min_len = min(len(municipality_code), len(municipality_name), len(registered_voters), len(envelopes),
                  len(valid_votes), len(results))

    rows = []
    for i in range(min_len):
        row = [municipality_code[i], municipality_name[i], registered_voters[i], envelopes[i], valid_votes[i]]
        rows.append(row + results[i])

    return rows

def save_to_csv(file_name: str, header: list, rows: list):

    try:
        with open(file_name, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Data uložena do souboru: {file_name}")
    except IOError as e:
        print(f"Chyba při ukládání souboru {file_name}: {e}")
        sys.exit(1)

# UI+

def blink_text(text, intervals, blink_count):
    for _ in range(blink_count):
        print(text, end="\r")  
        time.sleep(intervals)  
        print(" " * len(text), end="\r")
        time.sleep(intervals)

# main

def main():

    c = ("=" * 50)
    print(c,"VOLBY 2017 > CSV SCRAPER",c,sep="\n")
    
    if len(sys.argv) == 1:
        print("Chcete zobrazit vhodné argumenty pro dostupné celky?")
        user_input = input(f"Zapište arghelp pro nápovědu. Pokračovat -> enter.\n:")
        if user_input == "arghelp":
            help_links() 
        else:
            print("Pokračuji bez nápovědy..")
        
    if len(sys.argv) != 3:
        print(c,"Vložte dva argumenty pro spuštění scrapingu.","Zapište příkaz do terminálu ve formátu:",
        "\033[33mpython \033[37mmain.py \033[34m\"url\" \"file_name.csv\"","\033[37m",sep="\n")
        sys.exit(1)
    

    url = sys.argv[1]
    final_file = sys.argv[2]
    
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Chyba: URL musí začínat http:// nebo https://.")
        sys.exit(1)

    if not final_file.endswith(".csv"):
        print("Chyba: Druhý argument musí být soubor s příponou .csv.")
        sys.exit(1)

    blink_text(" :::: Hledám data :::: ", 0.5, 5)

    soup = get_soup_from_url(url)

    if soup:
        municipality_name = get_municipality_name(soup)
        urls = get_urls(soup)
        municipality_code = get_municipality_code(soup)

        parties = get_political_parties(urls)
        rows = create_rows(municipality_code, municipality_name, urls)

        header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + parties
        save_to_csv(final_file, header, rows)
    else:
        print("Chyba při získávání HTML obsahu. Zkontrolujte připojení.")
        sys.exit(1)

if __name__ == "__main__":
    main()
