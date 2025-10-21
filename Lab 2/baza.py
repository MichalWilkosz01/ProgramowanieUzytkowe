import pyodbc
import jsonpickle
from typing import List

class TwierdzenieMatematyczne:
    def __init__(self, id: int, haslo: str, tresc: str):
        self.id = id
        self.haslo = haslo
        self.tresc = tresc

    def __str__(self):
        return f"Id: {self.id}, Hasło: {self.haslo}, Treść: {self.tresc}"
    
class Tabela_TwierdzeniaMatematyczne:
    def __init__(self):
        self.connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=Wikipedia;'
        'Trusted_Connection=yes;'
        )
        self.cursor = None
        self.conn = None
    
    def __enter__(self):
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def pobierz_hasla(self) -> List[TwierdzenieMatematyczne]:
        self.cursor.execute("SELECT * FROM dbo.TwierdzeniaMatematyczne")
        rows = self.cursor.fetchall()
        return [TwierdzenieMatematyczne(row.Id, row.Haslo, row.Tresc) for row in rows]
    
    def dodaj_haslo(self, twierdzenie: TwierdzenieMatematyczne) -> None:
        self.cursor.execute("INSERT INTO dbo.TwierdzeniaMatematyczne (Haslo, Tresc) VALUES (?, ?)", 
                            twierdzenie.haslo, twierdzenie.haslo)
        self.conn.commit()

    def policz_hasla(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM dbo.TwierdzeniaMatematyczne")
        return self.cursor.fetchone()[0]
    
    def usun_wszystko(self) -> None:
        self.cursor.execute("DELETE FROM dbo.TwierdzeniaMatematyczne")
        self.conn.commit()
        
    

if __name__ == "__main__":
    with Tabela_TwierdzeniaMatematyczne() as tabela:
        nowe_twierdzenie = TwierdzenieMatematyczne(0, "Haslo z pythona", "Tresc z Pythona")
        tabela.dodaj_haslo(nowe_twierdzenie)
        hasla = tabela.pobierz_hasla()
        for h in hasla:
            print(h)
        liczba_hasel = tabela.policz_hasla()
        print(liczba_hasel)

        json_data = jsonpickle.encode(hasla, unpicklable=False) #Usuniecie py/obj z serializacji
        with open("hasla.json", "w", encoding="utf-8") as file:
            file.write(jsonpickle.encode(json_data))
            
        tabela.usun_wszystko()

