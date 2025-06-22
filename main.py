from tkinter import *
from tkinter import messagebox
import tkintermapview

dealerships: list = []

class Dealership:
    def __init__(self, name, address, phone, website, map_widget=None):
        self.name = name
        self.address = address  # Używamy address zamiast location
        self.phone = phone
        self.website = website
        self.coordinates = self.get_coordinates()
        self.marker = None
        if map_widget:
            self.marker = map_widget.set_marker(
                self.coordinates[0],
                self.coordinates[1],
                text=f'{self.name}',
                command=self.show_details
            )
        self.cars = []

    def get_coordinates(self) -> list:
        # Zmieniamy self.location na self.address
        try:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="komis_samochodowy")
            location = geolocator.geocode(self.address)
            if location:
                return [location.latitude, location.longitude]
            return [52.2297, 21.0122]  # Domyślne współrzędne Warszawy
        except:
            return [52.2297, 21.0122]  # Fallback na Warszawę

    def add_car(self, brand, model, year, price, mileage):
        self.cars.append({
            'brand': brand,
            'model': model,
            'year': year,
            'price': price,
            'mileage': mileage
        })

    def show_details(self):
        i = listbox_lista_komisow.index(ACTIVE)
        show_dealership_details()


def add_dealership() -> None:
    name = entry_nazwa.get()
    address = entry_adres.get()
    phone = entry_telefon.get()
    website = entry_website.get()

    dealership = Dealership(
        name=name,
        address=address,
        phone=phone,
        website=website,
        map_widget=map_widget
    )
    dealerships.append(dealership)

    entry_nazwa.delete(0, END)
    entry_adres.delete(0, END)
    entry_telefon.delete(0, END)
    entry_website.delete(0, END)

    entry_nazwa.focus()
    show_dealerships()


def show_dealerships() -> None:
    listbox_lista_komisow.delete(0, END)
    for idx, dealership in enumerate(dealerships):
        listbox_lista_komisow.insert(idx, f'{idx + 1}. {dealership.name}')


def remove_dealership():
    i = listbox_lista_komisow.index(ACTIVE)
    dealerships[i].marker.delete()
    dealerships.pop(i)
    show_dealerships()


def edit_dealership():
    i = listbox_lista_komisow.index(ACTIVE)
    dealership = dealerships[i]

    entry_nazwa.insert(0, dealership.name)
    entry_adres.insert(0, dealership.address)
    entry_telefon.insert(0, dealership.phone)
    entry_website.insert(0, dealership.website)

    button_dodaj_komis.config(text='Zapisz', command=lambda: update_dealership(i))


def update_dealership(i):
    name = entry_nazwa.get()
    address = entry_adres.get()
    phone = entry_telefon.get()
    website = entry_website.get()

    dealerships[i].name = name
    dealerships[i].address = address
    dealerships[i].phone = phone
    dealerships[i].website = website

    dealerships[i].coordinates = dealerships[i].get_coordinates()
    dealerships[i].marker.delete()
    dealerships[i].marker = map_widget.set_marker(
        dealerships[i].coordinates[0],
        dealerships[i].coordinates[1],
        text=f'{dealerships[i].name}',
        command=dealerships[i].show_details
    )

    show_dealerships()
    button_dodaj_komis.config(text='Dodaj komis', command=add_dealership)

    entry_nazwa.delete(0, END)
    entry_adres.delete(0, END)
    entry_telefon.delete(0, END)
    entry_website.delete(0, END)
    entry_nazwa.focus()


def show_dealership_details() -> None:
    i = listbox_lista_komisow.index(ACTIVE)
    dealership = dealerships[i]

    label_szczegoly_nazwa_wartosc.config(text=dealership.name)
    label_szczegoly_adres_wartosc.config(text=dealership.address)
    label_szczegoly_telefon_wartosc.config(text=dealership.phone)
    label_szczegoly_website_wartosc.config(text=dealership.website)

    # Wyświetlanie listy samochodów
    listbox_samochody.delete(0, END)
    for car in dealership.cars:
        listbox_samochody.insert(END, f"{car['brand']} {car['model']} ({car['year']}) - {car['price']} PLN")

    map_widget.set_zoom(15)
    map_widget.set_position(dealership.coordinates[0], dealership.coordinates[1])


def add_car_to_dealership():
    try:
        # Sprawdź czy wybrano komis
        if not listbox_lista_komisow.curselection():
            messagebox.showerror("Błąd", "Wybierz komis z listy przed dodaniem samochodu")
            return

        i = listbox_lista_komisow.curselection()[0]
        brand = entry_marka.get()
        model = entry_model.get()
        year = entry_rok.get()
        price = entry_cena.get()
        mileage = entry_przebieg.get()

        # Walidacja danych
        if not all([brand, model, year, price, mileage]):
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione")
            return

        dealerships[i].add_car(
            brand=brand,
            model=model,
            year=int(year),
            price=float(price),
            mileage=int(mileage)
        )

        # Wyczyść pola i odśwież widok
        entry_marka.delete(0, END)
        entry_model.delete(0, END)
        entry_rok.delete(0, END)
        entry_cena.delete(0, END)
        entry_przebieg.delete(0, END)

        show_dealership_details()

    except ValueError:
        messagebox.showerror("Błąd", "Rok, cena i przebieg muszą być liczbami")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {str(e)}")


# Główne okno aplikacji
root = Tk()
root.geometry("1200x800")
root.title("System zarządzania komisami samochodowymi")

# Ramki interfejsu
ramka_lista_komisow = Frame(root)
ramka_formularz_komis = Frame(root)
ramka_formularz_samochod = Frame(root)
ramka_szczegoly = Frame(root)
ramka_mapa = Frame(root)
ramka_lista_samochodow = Frame(root)

ramka_lista_komisow.grid(row=0, column=0, padx=10, pady=5)
ramka_formularz_komis.grid(row=0, column=1, padx=10, pady=5)
ramka_formularz_samochod.grid(row=0, column=2, padx=10, pady=5)
ramka_szczegoly.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
ramka_lista_samochodow.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
ramka_mapa.grid(row=2, column=2, padx=10, pady=5)

root.mainloop()