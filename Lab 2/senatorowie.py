import requests
from bs4 import BeautifulSoup 
import pandas as pd
import re

def polskie_nazwisko(nazwisko):
    polskie_znaki = re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")
    return len(polskie_znaki.findall(nazwisko))

def dwuczlonowe_imie(imie: str):
    podzial = imie.split(' ')
    return len(podzial) > 1

def dwuczlonowe_nazwisko(nazwisko: str):
    return nazwisko.__contains__('-')

url = 'https://www.senat.gov.pl/sklad/senatorowie/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
}

response = requests.get(url, headers=headers)

response.encoding = 'utf-8'
html = response.text
print(response.status_code)
soup = BeautifulSoup(html, 'html.parser')
senatorowie = []

for kontener in soup.find_all("div", class_="senator-kontener"):
    a_tag = kontener.find("a")
    wygasl = kontener.find("p", class_="annotation") #Wygasniety mandat
    if a_tag and not wygasl:
        full_name = a_tag.get_text(strip=True)
        parts = full_name.split()
        first_name = ' '.join(parts[:-1]) 
        last_name = parts[-1]  
        senatorowie.append({'Imie': first_name, 'Nazwisko': last_name})

df = pd.DataFrame(senatorowie)

print(df)
count_ends_with_a = df['Imie'].str.endswith('a').sum()
count_senators = len(df) - count_ends_with_a

df['polish_chars_count_in_lastname'] = df['Nazwisko'].apply(polskie_nazwisko)
count_polish_lastnames = df['polish_chars_count_in_lastname'].sum()
count_dwuczlonowe_imie = df['Imie'].apply(dwuczlonowe_imie).sum()
count_dwuczlonowe_nazwisko = df['Nazwisko'].apply(dwuczlonowe_nazwisko).sum()

print(f"Liczba senatorów z dwuczłonowymi imionami: {count_dwuczlonowe_imie}")
print(f"Liczba senatorów z dwuczłonowymi nazwiskami: {count_dwuczlonowe_nazwisko}")
print(f"Liczba senatorów z polskimi znakami w nazwisku: {count_polish_lastnames}")
print(f"Liczba senatorek: {count_ends_with_a}")
print(f"Liczba senatorów: {count_senators}")
with open("senatorowie.txt", "w") as file:
    file.write(f"{df.drop(columns=["polish_chars_count_in_lastname"]).to_string()}\n")
    file.write(f"Liczba senatorów z dwuczłonowymi imionami: {count_dwuczlonowe_imie}\n")
    file.write(f"Liczba senatorów z dwuczłonowymi nazwiskami: {count_dwuczlonowe_nazwisko}\n")
    file.write(f"Liczba senatorów z polskimi znakami w nazwisku: {count_polish_lastnames}\n")
    file.write(f"Liczba senatorek: {count_ends_with_a}\n")
    file.write(f"Liczba senatorów: {count_senators}\n")   

