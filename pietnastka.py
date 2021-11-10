
import numpy as np
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox


class Pietnastka():



    def __init__(self):
        self.__plansza = self.__przygotuj_nowa_plansze()
        self.__przygotuj_GUI()


    def graj(self):

        self.__okno.mainloop()


    def __przygotuj_nowa_plansze(self):
        a = np.arange(16)
        np.random.shuffle(a)
        p = a.reshape(4, 4)

        return p


    def __przygotuj_GUI(self):

        self.__okno = self.__przygotuj_okno()

        self.__pixelVirtual = tk.PhotoImage(width=1, height=1)

        self.__narysuj_przyciski_menu()
        # self.__kafelki = self.__przygotuj_kafelki()
        # self.__odswiez_kafelki()
        self.__odswiez_GUI()

    def __odswiez_GUI(self):
        self.__kafelki = self.__przygotuj_kafelki()
        self.__odswiez_kafelki()


    def __nowa_gra(self):
        self.__plansza = self.__przygotuj_nowa_plansze()
        self.__wyczysc_kafelki()
        self.__odswiez_GUI()


    def __przygotuj_okno(self, czy_debug = False):
        okno = tk.Tk()

        okno.title("Piętnastka")
        okno.minsize(400, 500)
        okno.maxsize(400, 500)

        return okno

    def __narysuj_przyciski_menu(self, czy_debug = False):

        helv20 = tkFont.Font(family="Helvetica", size=20, weight="bold")

        b = tk.Button(master=self.__okno,
                      width=190,
                      height=30,
                      text="Nowa Gra",
                      fg="red",
                      image=self.__pixelVirtual,
                      compound="c",
                      font=helv20,
                      command=self.__nowa_gra
                      )

        b.place(x=100, y=420)


    def __przygotuj_kafelki(self, czy_debug = False):

        kafelki = []

        helv36 = tkFont.Font(family="Helvetica", size=36, weight="bold")

        for i in range(4):
            linia_kafelkow = []
            for j in range(4):

                napis = "" #plansza[i][j]

                b = tk.Button(master=self.__okno,
                              width=92,
                              height=92,
                              text = napis,
                              image = self.__pixelVirtual,
                              compound = "c",
                              font=helv36,
                              command = (lambda a=i, b=j:self.__przesun_kafelek(a,b))
                              )

                linia_kafelkow.append(b)

            kafelki.append(linia_kafelkow)

        return kafelki

    def __wyczysc_kafelki(self):
        for i in range(4):
            for j in range(4):
                self.__kafelki[i][j].grid_forget()


    def __odswiez_kafelki(self, czy_debug = False):

        '''
        Funkcja ustala etykiety na przyciskach wg przekazanej planszy
        :param przyciski: tablica przycisków
        :param czy_debug: czy wyświetlać komunikaty pomagające w debugowaniu kodu - True/False
        :return:
        '''

        if czy_debug:
            print("funkcja __odswiez_kafelki")
            print(self.__plansza)

        # przepisujemy teksty z planszy na przyciski
        for i in range(4):
            for j in range(4):
                self.__kafelki[i][j]["text"] = self.__plansza[i][j]

        for i in range(4):
            for j in range(4):
                self.__kafelki[i][j].grid_forget()
                if self.__plansza[i][j] != 0:
                    self.__kafelki[i][j].grid(column = j, row = i)


    def __przesun_kafelek(self, w, k, czy_debug = False):

        if czy_debug:
            print("funkcja przesun {} {} {}".format(w, k, self.__plansza[w][k]))

        #szukamy 0 na planszy
        pozycja_zera = np.nonzero(self.__plansza == 0)
        wiersz_zera = int(pozycja_zera[0])
        kolumna_zera = int(pozycja_zera[1])

        if czy_debug:
            print(self.__plansza[wiersz_zera][kolumna_zera])
            print("wiersz_zera = {}, kolumna_zera = {}, wartość = {}".format(wiersz_zera, kolumna_zera, self.__plansza[wiersz_zera][kolumna_zera]))

            print("Różnice: ")
            print(abs(w-wiersz_zera), abs(k-kolumna_zera))

        if (abs(w-wiersz_zera) + abs(k-kolumna_zera)) == 1:

            if czy_debug:
                print("wiersz_zera = {}, kolumna_zera = {}, wartość = {}".format(wiersz_zera, kolumna_zera, self.__plansza[wiersz_zera][kolumna_zera]))
                print("a = {}, b = {}, wartosc_ab = {}".format(w, k, self.__plansza[w][k]))

            self.__plansza[wiersz_zera][kolumna_zera], self.__plansza[w][k] = self.__plansza[w][k], self.__plansza[wiersz_zera][kolumna_zera]

            self.__odswiez_kafelki()

        self.__sprawdz_ulozenie()



    def __sprawdz_ulozenie(self, czy_debug = False):
        prawidlowo = [[ 1,  2,  3,  4],
                      [ 5,  6,  7,  8],
                      [ 9, 10, 11, 12],
                      [13, 14, 15,  0]]

        if np.array_equal(self.__plansza, prawidlowo):
            messagebox.showinfo("Gratulacje!", "Brawo, ułożyłeś układankę!")
