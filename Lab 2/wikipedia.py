import requests
from bs4 import BeautifulSoup

base_url = "https://pl.wikipedia.org"
url = 'https://pl.wikipedia.org/wiki/Kategoria:Twierdzenia_matematyczne'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')
hasla = []

pages_div = soup.find("div", id="mw-pages")
if pages_div:
    for group_div in pages_div.find_all("div", class_="mw-category-group"):
        for a_tag in group_div.find_all("a"):
            tekst = a_tag.get_text(strip=True) 
            href = a_tag.get('href')             
            hasla.append((tekst, href))    

print(hasla)
print(f"Liczba haseł: {len(hasla)}")

response = requests.get(base_url + hasla[0][1], headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
for math_tag in soup.find_all("math"):
    math_tag.decompose()

# usuń skrypty i style
for script_or_style in soup(["script", "style"]):
    script_or_style.decompose()

# pobierz tekst
text = soup.get_text()

# usuń nadmiarowe spacje i puste linie
lines = (line.strip() for line in text.splitlines())
cleaned_text = '\n'.join(line for line in lines if line)

print(cleaned_text)



