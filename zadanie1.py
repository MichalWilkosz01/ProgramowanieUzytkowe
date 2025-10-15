import requests
from bs4 import BeautifulSoup 
import pandas as pd
import re

def polskie_nazwisko(nazwisko):
    # Wyrażenie regularne do wykrywania polskich znaków
    polskie_znaki = re.compile(r'[ąćęłńóśźż]')
    return len(polskie_znaki.findall(nazwisko))

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
    if a_tag:
        # Wyciągamy pełne imię i nazwisko
        full_name = a_tag.get_text(strip=True)
        
        # Rozdzielamy pełne imię i nazwisko
        first_name, last_name = full_name.split(' ', 1)  # Dzielimy po pierwszej spacji
        
        # Dodajemy do listy jako krotki
        senatorowie.append({'first_name': first_name, 'last_name': last_name})

df = pd.DataFrame(senatorowie)

# Wyświetlamy wynik
print(df)
count_ends_with_a = df['first_name'].str.endswith('a').sum()
count_senators = len(df) - count_ends_with_a
# Wyświetlamy wynik
df['polish_chars_count_in_lastname'] = df['last_name'].apply(polskie_nazwisko)
count_polish_lastnames = df['polish_chars_count_in_lastname'].sum()

print(f"Liczba senatorów z polskimi znakami w nazwisku: {count_polish_lastnames}")
print(f"Liczba senatorek: {count_ends_with_a}")
print(f"Liczba senatorów: {count_senators}")
