import matplotlib.pyplot as plt
import numpy as np
import math


class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # odleglosc od srodka ukladu wspolzednych
        self.odleglosc = math.sqrt(x**2 + y**2)

    def __add__(self, other):
        return Punkt(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y


class Linia:

    def __init__(self, punkt1, punkt2):
        self.x1 = punkt1.x
        self.x2 = punkt2.x
        self.y1 = punkt1.y
        self.y2 = punkt2.y
        self.punkt1 = punkt1
        self.punkt2 = punkt2
        self.dlugosc = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

        # warunki dla prostych pionowych i poziomych
        if punkt1.y == punkt2.y:
            self.a = 0
        elif punkt1.x == punkt2.x:
            self.a = None
        else:
            self.a = (self.y2 - self.y1) / (self.x2 - self.x1)

        # przecięcie z OY
        if self.a is None:
            self.b = None
        else:
            self.b = (self.y1 - (self.x1 * self.a))

    def __len__(self):
        return self.dlugosc

    def rown_print(self):
        if self.punkt1.x == self.punkt2.x and self.punkt1.y == self.punkt2.y:
            print("Punkty są identyczne")
        elif self.punkt1.x == self.punkt2.x:
            print("Wykres pionowy")
        elif self.b == 0 and self.a == 0:
            print("Wykres OX")
        elif self.b == 0:
            print("Równanie prostej ma postać: y = " + str(self.b) + "x")
        elif self.a == 0:
            print("Wykres poziomy")
        elif self.punkt1 == self.punkt2:
            print("Nie da się stworzyć prostej z dwóch identycznych punktów")
        else:
            print("Równanie prostej ma postać: y = " + str(self.a) + "x + (" + str(self.b) + ")")

    def row_prostej(self):
        if self.punkt1.x == self.punkt2.x and self.punkt1.y == self.punkt2.y:
            return

        elif self.y1 == self.y2:
            # Pozioma prosta
            plt.scatter([self.x1, self.x2], [self.y1, self.y2], c='hotpink', label='Punkty', marker='x', s=100)
            plt.axhline(self.y1, c='hotpink', label='Prosta')

        elif self.x1 == self.x2:
            # Pionowa prosta
            plt.scatter([self.x1, self.x2], [self.y1, self.y2], c='hotpink', label='Punkty', marker='x', s=100)
            plt.axline((self.x1, self.x2), (self.y1, self.y2), c='hotpink', label='Prosta')

        else:
            # Standardowy przypadek - rysujemy linię i wyświetlamy równanie
            plt.scatter([self.x1, self.x2], [self.y1, self.y2], c='gold', label='Punkty', marker='*', s=150)
            plt.axline((self.x1, self.y1), slope=self.a, c='hotpink', label='Odcinek')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Wyznaczenie równania prostej, do której należy dany odcinek')
        plt.grid(True)
        plt.legend()
        plt.axis("equal")
        plt.show()

    def kat_miedzy_liniami(self, other):
        w1 = self.punkt2 - self.punkt1
        w2 = other.punkt2 - other.punkt1
        iloczyn_dlugosci = (math.sqrt(w1[0] ** 2 + w1[1] ** 2)) * (math.sqrt(w2[0] ** 2 + w2[1] ** 2))
        iloraz_skalarny = np.dot(w1, w2)
        kat_radian = np.arccos(abs(iloraz_skalarny)/iloczyn_dlugosci)
        kat_stopnie = np.rad2deg(kat_radian)
        print("Kat w stopniach to ", kat_stopnie)

        # rysowanie
        plt.plot([self.punkt1.x, self.punkt2.x], [self.punkt1.y, self.punkt2.y], c='blue', label='Linia 1')
        plt.plot([other.punkt1.x, other.punkt2.x], [other.punkt1.y, other.punkt2.y], c='hotpink', label='Linia 2')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('kat między odcinkami')
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show()

        return kat_stopnie


class Triangle:
    def __init__(self, punkt1, punkt2, punkt3):
        self.x1 = punkt1.x
        self.x2 = punkt2.x
        self.x3 = punkt3.x
        self.y1 = punkt1.y
        self.y2 = punkt2.y
        self.y3 = punkt3.y
        self.punkt1 = punkt1
        self.punkt2 = punkt2
        self.punkt3 = punkt3
        self.dlugosc1 = math.sqrt(math.pow(self.x2 - self.x1, 2) + math.pow(self.y2 - self.y1, 2))
        self.dlugosc2 = math.sqrt(math.pow(self.x3 - self.x2, 2) + math.pow(self.y3 - self.y2, 2))
        self.dlugosc3 = math.sqrt(math.pow(self.x3 - self.x1, 2) + math.pow(self.y3 - self.y1, 2))

    def rysuj_trojkat(self):
        plt.plot([self.x1, self.x2, self.x3, self.x1], [self.y1, self.y2, self.y3, self.y1], color='black')
        x = np.array([self.x1, self.x2, self.x3, self.x1])
        y = np.array([self.y1, self.y2, self.y3, self.y1])
        plt.scatter(x, y, c='gold', label='Punkt', marker='o')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Trojkat')
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show()

    def obwod(self):
        obwod = self.dlugosc1 + self.dlugosc2 + self.dlugosc3
        print("Obwod trojkata to: ", round(obwod, 3))
        return obwod

    def pole_trojkata(self):
        p = ((1/2) * self.obwod())
        pole_trojkata = math.sqrt(p * (p - self.dlugosc1) * (p - self.dlugosc2) * (p - self.dlugosc3))
        print("Pole trojkata to: ", round(pole_trojkata, 3))
        return pole_trojkata

    def czy_punkt_nalezy_pola(self, punkt):
        kawal1 = Triangle(self.punkt1, self.punkt2, punkt)
        kawal2 = Triangle(self.punkt2, self.punkt3, punkt)
        kawal3 = Triangle(self.punkt3, self.punkt1, punkt)
        pole1 = kawal1.pole_trojkata()
        pole2 = kawal2.pole_trojkata()
        pole3 = kawal3.pole_trojkata()
        trzy_pola = pole1 + pole2 + pole3

        if trzy_pola > self.pole_trojkata():
            print("Punkt (", punkt.x, ",", punkt.y, ") nie należy do trójkąta")
        else:
            print("Punkt (", punkt.x, ",", punkt.y, ") należy do trójkąta")

        plt.scatter(punkt.x, punkt.y, c='hotpink', label='Punkt', marker='X', s=150)
        self.rysuj_trojkat()

    def czy_punkt_nalezy_katy(self, punkt):
        linia1 = Linia(self.punkt1, punkt)
        linia2 = Linia(self.punkt2, punkt)
        linia3 = Linia(self.punkt3, punkt)

        kat1 = linia1.kat_miedzy_liniami(linia2)
        kat2 = linia2.kat_miedzy_liniami(linia3)
        kat3 = linia3.kat_miedzy_liniami(linia1)

        trzy_katy = kat1 + kat2 + kat3

        if trzy_katy == 360:
            print("Punkt (", punkt.x, ",", punkt.y, ") należy do trójkąta")

        else:
            print("Punkt (", punkt.x, ",", punkt.y, ") nie należy do trójkąta")

        plt.scatter(punkt.x, punkt.y, c='hotpink', label='Punkt', marker='X', s=150)
        self.rysuj_trojkat()


class Wielokat:
    def __init__(self, *points):
        self.points = points

    def wyswietl_wielokat(self):
        length = len(self.points)
        for i in range(length):
            plt.plot([self.points[i].x, self.points[(i + 1) % length].x],
                     [self.points[i].y, self.points[(i + 1) % length].y], color='hotpink')
        plt.xlabel('Os x')
        plt.ylabel('Os y')
        plt.axis('equal')
        plt.grid(True)
        plt.show()

    def przynaleznosc_punkt_wielokat(self, punkt):
        ilosc_wierzcholkow = len(self.points)
        x, y = punkt.x, punkt.y
        wynik = False
        p1 = self.points[0]

        for i in range(1, ilosc_wierzcholkow + 1):
            # modulo zeby zrobic miedzy ostatnim a 1
            p2 = self.points[i % ilosc_wierzcholkow]

            # czy y w pionowym zakresie boku
            if y > min(p1.y, p2.y):
                if y <= max(p1.y, p2.y):
                    # czy po lewej lub na
                    if x <= max(p1.x, p2.x):
                        # liczymy x przeciecia poziomej z bokiem
                        przeciecie_x = (y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x

                        # no i jesli x jest po lewo lub na to witamy
                        if p1.x == p2.x or x <= przeciecie_x:
                            wynik = not wynik 
            p1 = p2

        if wynik:
            print("Punkt leży w wielokacie")
        else:
            print("Punkt nie leży w wielokacie")

        plt.scatter(punkt.x, punkt.y, c='hotpink', label='Punkt', marker='X', s=150)
        self.wyswietl_wielokat()
        return wynik


def row_ogolne(punkt, linia):
    return ((punkt.y - linia.y1) * (linia.x2 - linia.x1)) - ((linia.y2 - linia.y1) * (punkt.x - linia.x1))


def wizualizacja_punkt_linia(punkt, linia):
    plt.scatter(punkt.x, punkt.y, c='gold', label='Punkt', marker='*', s=150)
    plt.axline((linia.x1, linia.y1), (linia.x2, linia.y2), c='hotpink', label='Linia 1')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Punkt względem prostej')
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.show()


def przyn_punk_pros(punkt, linia):
    row = row_ogolne(punkt, linia)
    if row > 0:
        print("Punkt leży po lewej stronie prostej")
    elif row == 0:
        print("Punkt leży na prostej")
    else:
        print("Punkt leży po prawej stronie prostej")

    wizualizacja_punkt_linia(punkt, linia)


def przyn_punk_odc(punkt, odcinek):
    rown2 = row_ogolne(punkt, odcinek)
    war1 = min(odcinek.x1, odcinek.x2) <= punkt.x <= max(odcinek.x1, odcinek.x2)
    war2 = min(odcinek.y1, odcinek.y2) <= punkt.y <= max(odcinek.y1, odcinek.y2)
    war3 = punkt == odcinek.punkt1 or punkt == odcinek.punkt2
    if rown2 == 0 and (war1 and war2) or war3:
        print("Punkt należy do odcinka")
    else:
        print("Punkt nie należy do odcinka")

    plt.scatter(punkt.x, punkt.y, c='MidnightBlue', label='Punkt', marker='*', s=150)
    plt.plot([odcinek.x1, odcinek.x2], [odcinek.y1, odcinek.y2], c='Maroon', label='Odcinek', marker='o')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Punkt względem odcinka')
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.show()


def transl_odcin_wekt(wektor, odcinek):
    trans_punkt1 = Punkt(odcinek.x1 + wektor.x, odcinek.y1 + wektor.y)
    trans_punkt2 = Punkt(odcinek.x2 + wektor.x, odcinek.y2 + wektor.y)
    # przed translacja
    plt.plot([odcinek.x1, odcinek.x2], [odcinek.y1, odcinek.y2], c='DarkGreen', label='Odcinek', marker='o')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Przesunięcie odcinka o wektor')
    plt.grid(True)
    plt.axis("equal")

    # po translacji
    s = 'Odcinek po translacji'
    plt.plot([trans_punkt1.x, trans_punkt2.x], [trans_punkt1.y, trans_punkt2.y], c='Maroon', label=s, marker='o')
    plt.legend()
    plt.show()


# zaczynamy funkcje lustrzana
def punkt_przeciecia_z_prostopadla(punkt, odcinek):
    row = row_ogolne(punkt, odcinek)
    if row == 0:
        print("Punkt jest w tym samym miejscu")
        przyn_punk_pros(punkt, odcinek)
        return 2
    else:
        if odcinek.a is None:
            prostop_a = 0
            prostop_b = None
        elif odcinek.a == 0:
            prostop_a = None
            prostop_b = 0
        else:
            prostop_a = (-1 / odcinek.a)
            prostop_b = (punkt.y - (prostop_a * punkt.x))

    if odcinek.a is None:
        punkt_przec_x = odcinek.x1
        punkt_przec_y = punkt.y
    elif odcinek.a == 0:
        punkt_przec_x = punkt.x
        punkt_przec_y = odcinek.y1
    else:
        punkt_przec_x = ((prostop_b - odcinek.b) / (odcinek.a - prostop_a))
        punkt_przec_y = (((odcinek.a * prostop_b) - (odcinek.b * prostop_a)) / (odcinek.a - prostop_a))

    punkt_przec = Punkt(punkt_przec_x, punkt_przec_y)
    return punkt_przec


def odleglosc_od_przeciecia(punkt_przec, punkt):
    odl_x = punkt_przec.x - punkt.x
    odl_y = punkt_przec.y - punkt.y
    wektor_odl = Punkt(odl_x, odl_y)
    # print(str(wektor_odl.x) + ' ' + str(wektor_odl.y))
    wektor_odwr = Punkt(-1 * wektor_odl.x, -1 * wektor_odl.y)
    # print( str(wektor_odwr.x) + ' ' + str(wektor_odwr.y))
    return wektor_odwr


def wizualizacja_lustro(odcinek, punkt, punkt_przec, punkt_odwr):
    # prosta przechodząca przez odcinek
    plt.scatter([odcinek.x1, odcinek.x2], [odcinek.y1, odcinek.y2], c='hotpink', label='Krańce odcinka', marker='x',
                s=100)
    plt.axline((odcinek.x1, odcinek.y1), (odcinek.x2, odcinek.y2), c='hotpink', label='Prosta')
    plt.grid(True)

    # prosta prostopadła
    plt.scatter(punkt.x, punkt.y, c='Maroon', label='Punkt', marker='*', s=200)
    plt.scatter(punkt_przec.x, punkt_przec.y, c='Teal', label='Punkt przecięcia prostych', marker='o', s=50)
    plt.scatter(punkt_odwr.x, punkt_odwr.y, c='Orange', label='Punkt odbity', marker='*', s=200)
    plt.axline((punkt_przec.x, punkt_przec.y), (punkt.x, punkt.y), c='Teal', label='Prostopadła')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Odbicie punktu względem odcinka')
    plt.axis("equal")
    plt.legend()
    plt.show()


def odbicie_lustrzane(punkt, odcinek):

    # znalezienie prostej porstopadlej i punktu przecięcia
    punkt_przec = punkt_przeciecia_z_prostopadla(punkt, odcinek)

    # znalezienie odleglosci od przecięcia
    wektor_odwr = odleglosc_od_przeciecia(punkt_przec, punkt)

    # Nowy punkt
    punkt_odwr = Punkt(punkt_przec.x - wektor_odwr.x, punkt_przec.y - wektor_odwr.y)

    # Zaokrąglenie współrzędnych do 2 miejsc po przecinku
    zaok_x = round(punkt_odwr.x, 2)
    zaok_y = round(punkt_odwr.y, 2)
    print("Zaokrąglone współrzędne punktu (x: " + str(zaok_x) + ', y: ' + str(zaok_y) + ") ")

    # wizualizacja
    return wizualizacja_lustro(odcinek, punkt, punkt_przec, punkt_odwr)

# 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222


def wizualizacja_przeciecie(odcinek1_a, odcinek1_b, odcinek2_a, odcinek2_b, punkt_przec):
    # prosta 1
    plt.axline((0, odcinek1_b), slope=odcinek1_a, c='hotpink', label='Prosta1')
    # prosta 2
    plt.axline((0, odcinek2_b), slope=odcinek2_a, c='hotpink', label='Prosta2')
    # punkt
    plt.scatter(punkt_przec.x, punkt_przec.y, c='Teal', label='Punkt przecięcia prostych', marker='o', s=50)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Przeciecie dwoch prostych')
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()


def punkt_przec_dwoch_prostych_wspolczynniki(line1_a, line1_b, line2_a, line2_b):

    # W wersji do cramera rownanie to -ax + 1y = b
    if line1_a is None or line2_a is None:
        print("Tym sposobem nie da sie policzyć wyznacznika dla pionowych prostych (dzielenie przez 0)")
        return "Exception"

    wyznacznik_o = (-line1_a) - (-line2_a)
    wyznacznik_x = (line1_b - line2_b)
    wyznacznik_y = (-line1_a * line2_b) - (-line2_a * line1_b)

    if wyznacznik_o == 0 and wyznacznik_x == 0 and wyznacznik_y == 0:
        print("Proste się pokrywają, nieskończenie wiele punktów przecięcia")
        return "Exception"
    elif wyznacznik_o == 0:
        print("Proste równoległe, brak punktów przecięcia")
        return "Exception"
    else:
        x = wyznacznik_x / wyznacznik_o
        y = wyznacznik_y / wyznacznik_o
        punkt_cramer = Punkt(x, y)

    wizualizacja_przeciecie(line1_a, line1_b, line2_a, line2_b, punkt_cramer)
    print("Wspolrzedne punktu przeciecia to x = ", punkt_cramer.x, ", y = ", punkt_cramer.y)
    return punkt_cramer


def punkt_przec_odcinkow(od1, od2):

    if od1.a is None or od1.b is None or od2.a is None or od2.b is None:
        print("Brak wartosci współczynników dla pionowych lini")
        return
    else:
        # na podstawie dwóch linii o znanym początku i końcu (punkt przecięcia prostych przechodzących przez te linie)
        mianownik = (od1.x1 - od1.x2) * (od2.y1 - od2.y2) - (od2.x1 - od2.x2) * (od1.y1 - od1.y2)
        if mianownik == 0:
            print("Proste sa rownolegle i nie maja punktu przeciecia")
            return
        y = (od1.y2 * (od2.x1 * od2.y2 - od2.x2 * od2.y1) + od1.y1 * (od2.x2 * od2.y1 - od2.x1 * od2.y2) + od1.x2 * od1.y1 * (od2.y2 - od2.y1) + od1.x1 * od1.y2 * (od2.y1 - od2.y2)) / mianownik
        x = (od1.x2 * (od2.x1 * od2.y2 - od2.x2 * od2.y1 + (od2.x2 - od2.x1) * od1.y1) + od1.x1 * (od2.x2 * od2.y1 - od2.x1 * od2.y2 + (od2.x1 - od2.x2) * od1.y2)) / mianownik
        punkt_przec = Punkt(x, y)

        print("Wspolrzedne punktu przeciecia to x = ", punkt_przec.x, ", y = ", punkt_przec.y)
        wizualizacja_przeciecie(od1.a, od1.b, od2.a, od2.b, punkt_przec)


def zmierzenie_odleglosci_miedzy_punktem_linia(point, line):

    # znalezienie punktu przecięcia
    punkt_przec = punkt_przeciecia_z_prostopadla(point, line)
    if punkt_przec == 2:
        return
    new_line = Linia(point, punkt_przec)
    dl = round(new_line.dlugosc, 3)
    print("Dlugosc miedzy punktem a linia to ", dl)
    wizualizacja_punkt_linia(point, line)


def trojkat_z_wspolczynnikow(wsp1_a, wsp1_b, wsp2_a, wsp2_b, wsp3_a, wsp3_b):

    punkt1 = punkt_przec_dwoch_prostych_wspolczynniki(wsp1_a, wsp1_b, wsp2_a, wsp2_b)
    if punkt1 != "Exception":
        punkt2 = punkt_przec_dwoch_prostych_wspolczynniki(wsp2_a, wsp2_b, wsp3_a, wsp3_b)
    else:
        return
    if punkt2 != "Exception":
        punkt3 = punkt_przec_dwoch_prostych_wspolczynniki(wsp1_a, wsp1_b,  wsp3_a, wsp3_b)
    else:
        return
    if punkt3 != "Exception":
        trojkat1 = Triangle(punkt1, punkt2, punkt3)
        trojkat1.rysuj_trojkat()
    else:
        return

# 33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333


# ________________________________________________________________________________________________________________
# Zadanie 1 - Wyznaczenie równania prostej, do której należy dana linia
# Wykres pionowy
punkt_1 = Punkt(0, 0)
punkt_2 = Punkt(0, 9)
prosta1 = Linia(punkt_1, punkt_2)
# prosta1.rown_print()
# prosta1.row_prostej()

# Warunek dwa identyczne punkty
punkt_3 = Punkt(0, 0)
punkt_4 = Punkt(0, 0)
# prosta2 = Linia(punkt_3, punkt_4)
# prosta2.rown_print()
# prosta2.row_prostej()

# Wykres poziomy
punkt_5 = Punkt(5, 3)
punkt_6 = Punkt(0, 3)
prosta3 = Linia(punkt_5, punkt_6)
# prosta3.rown_print()
# prosta3.row_prostej()

# Wykres standardowy
punkt_7 = Punkt(5, 2)
punkt_8 = Punkt(8, 3)
prosta4 = Linia(punkt_7, punkt_8)
# prosta4.rown_print()
# prosta4.row_prostej()
# ________________________________________________________________________________________________________________
# Zadanie 2&4 - Sprawdzenie przynależności punktu do prostej i względem prostej (prawo/lewo)
# Punkt leży na prostej
# przyn_punk_pros(punkt_3, prosta1)

# Punkt leży po prawej
# przyn_punk_pros(punkt_3, prosta4)

# Punkt leży po lewej
# przyn_punk_pros(punkt_5, prosta4)

# ________________________________________________________________________________________________________________
# Zadanie 3 - Sprawdzenie przynależności punktu do linii (odcinka)
# Punkt należy do odcinka jest na skraju
# przyn_punk_odc(punkt_2, prosta1)

# Punkt należy do odcinka w środku
punkt_9 = Punkt(2, 3)
# przyn_punk_odc(punkt_9, prosta3)

# Punkt nie należy do odcinka
# przyn_punk_odc(punkt_2, prosta3)

# ________________________________________________________________________________________________________________
# Zadanie 5 - Dokonanie translacji linii o podany wektor
# zwykly wektor
wektor1 = Punkt(0, 2)
# transl_odcin_wekt(wektor1, prosta4)

# wektor (0,0)
wektor2 = Punkt(0, 0)
# transl_odcin_wekt(wektor2, prosta4)

# ________________________________________________________________________________________________________________
# Zadanie 6 - Dokonanie odbicia danego punktu względem linii
# prosta pionowa, punkt na lini
# odbicie_lustrzane(punkt_6, prosta1)

# prosta pionowa, punkt nie na lini
# odbicie_lustrzane(punkt_8, prosta1)

# prosta pozioma, punkt na lini
# odbicie_lustrzane(punkt_6, prosta3)

# prosta pozioma, punkt nie na lini
# odbicie_lustrzane(punkt_7, prosta3)

# prosta zwykła
# odbicie_lustrzane(punkt_2, prosta4)

# 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
punkt_10 = Punkt(3, 2)
prosta5 = Linia(punkt_9, punkt_10)

# prosta5.rown_print()
# prosta5.row_prostej()
# prosta4.rown_print()
# prosta4.row_prostej()

# punkt_przec_dwoch_prostych_wspolczynniki(prosta4.a, prosta4.b, prosta3.a, prosta3.b)
# punkt_przec_odcinkow(prosta5, prosta4)

# zmierzenie_odleglosci_miedzy_punktem_linia(punkt_1, prosta4)

# trojkat_z_wspolczynnikow(prosta4.a, prosta4.b, prosta5.a, prosta5.b, prosta3.a, prosta3.b)

# 33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

trojkat2 = Triangle(punkt_7, punkt_8, punkt_9)
# Zadanie 1 Dodaj metodę obliczającą pole Trójkąta
# trojkat2.rysuj_trojkat()
# trojkat2.pole_trojkata()

punkt_11 = Punkt(0, 2)
punkt_12 = Punkt(5, 2)
prosta6 = Linia(punkt_11, punkt_12)

punkt_13 = Punkt(0, 2)
punkt_14 = Punkt(5, 8)
prosta7 = Linia(punkt_13, punkt_14)

# Zadanie 2 Dodaj metodę obliczającą polę pomiędzy dwoma liniami
# prosta6.kat_miedzy_liniami(prosta7)

# Zdanie 3 Dodaj metodę sprawdzającą czy należy do niego podany punkt
# sposob I z polami
trojkat2.czy_punkt_nalezy_pola(punkt_3)

# sposob II z katami
# trojkat2.czy_punkt_nalezy_katy(punkt_4)

# Zadanie 4 Wielokat
punkt_1 = Punkt(1, 1)
punkt_2 = Punkt(3, -4)
punkt_3 = Punkt(5, 2)
punkt_4 = Punkt(2, 6)
punkt_5 = Punkt(2, 9)
wielokat1 = Wielokat(punkt_1, punkt_2, punkt_3, punkt_4, punkt_5)
# wielokat1.wyswietl_wielokat()

# Zadanie 5 przynaleznosc punktu do wielokata
punkt_12 = Punkt(3, 8)
punkt_13 = Punkt(2.5, 2)
wielokat1.przynaleznosc_punkt_wielokat(punkt_4)
