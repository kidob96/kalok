#rozszerzenia
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
#klasa Kalkulator, najszerszy element programu
class Kalkulator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()
#tworzenie interfejsu
    def interfejs(self):

        # etykiety
        etykieta1 = QLabel("Kwota:", self)
        etykieta2 = QLabel("Oprocentowanie:", self)
        etykieta3 = QLabel("Okres lokaty:", self)
        etykieta4 = QLabel("Wynik:", self)
        etykieta5 = QLabel("Kapitalizacja odsetek:", self)

        # przypisanie widgetów do układu tabelarycznego
        ukladT = QGridLayout()
        ukladT.addWidget(etykieta1, 0, 0)
        ukladT.addWidget(etykieta2, 0, 1)
        ukladT.addWidget(etykieta3, 0, 2)
        ukladT.addWidget(etykieta4, 0, 3)
        ukladT.addWidget(etykieta5, 1, 0)
#tworzenie pól do wprowadzania danych
  # 1-liniowe pola edycyjne
        self.liczba1Edt = QLineEdit()
        self.liczba2Edt = QLineEdit()
        self.liczba3Edt = QLineEdit()
        self.wynikEdt = QLineEdit()

        self.wynikEdt.readonly = True
#to chyba nie działa ale już nie ruszałem
        self.wynikEdt.setToolTip('Wpisz <b>liczby</b> i wybierz działanie...')
#położenie okienek w oknie kalkulatora
        ukladT.addWidget(self.liczba1Edt, 1, 0)
        ukladT.addWidget(self.liczba2Edt, 1, 1)
        ukladT.addWidget(self.liczba3Edt, 1, 2)
        ukladT.addWidget(self.wynikEdt, 1, 3)

        # przyciski
        miesBtn = QPushButton("&Miesięczna", self)
        kwartBtn = QPushButton("&Kwartalna", self)
        polrBtn = QPushButton("&Półroczna", self)
        roczBtn = QPushButton("&Roczna", self)
        koniecBtn = QPushButton("&Koniec", self)
        koniecBtn.resize(koniecBtn.sizeHint())

        ukladH = QHBoxLayout()
        ukladH.addWidget(miesBtn)
        ukladH.addWidget(kwartBtn)
        ukladH.addWidget(polrBtn)
        ukladH.addWidget(roczBtn)

        ukladT.addLayout(ukladH, 2, 0, 1, 3)
        ukladT.addWidget(koniecBtn, 3, 0, 1, 3)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
        koniecBtn.clicked.connect(self.koniec)
        miesBtn.clicked.connect(self.dzialanie)
        kwartBtn.clicked.connect(self.dzialanie)
        polrBtn.clicked.connect(self.dzialanie)
        roczBtn.clicked.connect(self.dzialanie)
        self.setGeometry(20, 20, 300, 100)
        #obrazek kalkulatora w lewym rogu
        self.setWindowIcon(QIcon('kalkulator.png'))
        #nazwa okna
        self.setWindowTitle("KALOK - Kalkulator lokat")
        self.show()
    #potwierdzenie zamknięcia okna
    def closeEvent(self, event):

        odp = QMessageBox.question(
            self, 'Komunikat',
            "Czy na pewno koniec?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    #umożliwienie zamykania okna przy użyciu ESC
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    #uaktywnienie przycisku zamykania
    def koniec(self):
        self.close()
    #przypisywanie wprowadzonym danym nazw
    def dzialanie(self):

        nadawca = self.sender()

        try:
            kwota = float(self.liczba1Edt.text())
            oprocentowanie = float(self.liczba2Edt.text())
            okres = float(self.liczba3Edt.text())
            wynik = ""
            #pętla z obliczeniami w zależności od wybranego przycisku z kapitalizacją
            if nadawca.text() == "&Miesięczna":
                wynik1 =round( kwota * ((1 + oprocentowanie/12) ** (12 * okres)),2)
                wynik2=(wynik1 - kwota) * 0.81
                wynik=round(wynik2+kwota,2)
            elif nadawca.text() == "&Kwartalna":
                wynik1 =round( kwota * ((1 + oprocentowanie/4) ** (4 * okres)),2)
                wynik2=(wynik1 - kwota) * 0.81
                wynik=round(wynik2+kwota,2)
            elif nadawca.text() == "&Półroczna":
                wynik1 =round( kwota * ((1 + oprocentowanie/2) ** (2 * okres)),2)
                wynik2=(wynik1 - kwota) * 0.81
                wynik=round(wynik2+kwota,2)
            else:  # roczna
                try:
                    wynik1 =round( kwota * ((1 + oprocentowanie) ** (1 * okres)),2)
                    wynik2=(wynik1 - kwota) * 0.81
                    wynik=round(wynik2+kwota,2)
                except ZeroDivisionError:
                    QMessageBox.critical(
                        self, "Błąd", "Zła wartość")
                    return

            self.wynikEdt.setText(str(wynik))

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = Kalkulator()
    sys.exit(app.exec_())
