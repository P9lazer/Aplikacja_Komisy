from tkinter import *
import tkintermapview

komisy: list = []

class Komisy:
    def __init__(self, name, adress, phone, website, map_widget):
        self.name = name
        self.adress = adress
        self.phone = phone
        self.website = website
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=f'{self.name}',
            command = self.show_details
        )
        self.car = []

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url = f'https://pl.wikipedia.org/wiki/{self.location}'
        response = requests.get(adres_url)
        if response.status_code == 200:
            response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
            return [
                float(response_html.select('.latittude')[1].text.replace(',', '.')),
                float(response_html.select('.longitude')[1].text.replace(',', '.')),
            ]

    root = Tk()
    root.geometry('1200x800')
    root.title('System zarządzania komisami samochodowymi')

    ramka_lista_komistow = Frame(root)
    ramka_formularz_komis = Frame(root)
    ramka_formularz_samochod = Frame(root)
    ramka_mapa = Frame(root)
    ramka_lista_samochodow = Frame(root)

    ramka_lista_komistow.grid(row=0, column=0, padx=10, pady=5)


    root.mainloop()