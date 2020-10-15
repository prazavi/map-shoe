# -*- coding: utf-8 -*-

# Unfortunately I had the same problems with amazon.com as the last project(eventhough I used header form network tab in inspect
# Therefore  I had to use men's shoe section of digikala which has the same features as the amazon site
# I have combined this project with the materials from ch.5
# The first part of the project is the map part and if you press the "part1(map)" button it will show what the first part of the project wanted
# If you press the "part2(shoe)" button,it will show the name of every shoe in the first page of digikala.com/search/category-men-shoes
# If you press the "name selection" button after selecting a shoe name, first it will show a dictionary of sizes and prices(as the project wanted) in the output of the program
# then it will show all the sizes of that shoe in the graphical interface and if you select one and press "size selection" it will give you it's price

import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mapbtn = QtWidgets.QPushButton(self.centralwidget)
        self.mapbtn.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.mapbtn.setObjectName("mapbtn")

        self.sizebtn = QtWidgets.QPushButton(self.centralwidget)
        self.sizebtn.setGeometry(QtCore.QRect(430, 510, 75, 23))
        self.sizebtn.setObjectName("sizebtn")

        self.namebtn = QtWidgets.QPushButton(self.centralwidget)
        self.namebtn.setGeometry(QtCore.QRect(30, 510, 91, 23))
        self.namebtn.setObjectName("namebtn")

        self.shoebtn = QtWidgets.QPushButton(self.centralwidget)
        self.shoebtn.setGeometry(QtCore.QRect(30, 270, 75, 23))
        self.shoebtn.setObjectName("shoebtn")

        self.name = QtWidgets.QListWidget(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(30, 300, 371, 191))
        self.name.setObjectName("name")

        self.sizetext = QtWidgets.QListWidget(self.centralwidget)
        self.sizetext.setGeometry(QtCore.QRect(430, 300, 71, 191))
        self.sizetext.setObjectName("sizetext")

        self.pricetext = QtWidgets.QTextBrowser(self.centralwidget)
        self.pricetext.setGeometry(QtCore.QRect(520, 350, 251, 91))
        self.pricetext.setObjectName("pricetext")

        self.maptext = QtWidgets.QTextBrowser(self.centralwidget)
        self.maptext.setGeometry(QtCore.QRect(30, 60, 256, 192))
        self.maptext.setObjectName("maptext")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.mapbtn.clicked.connect(self.map1)
        self.namebtn.clicked.connect(self.name1)
        self.shoebtn.clicked.connect(self.shoe1)
        self.sizebtn.clicked.connect(self.size1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def map1(self):
        app.processEvents()
        url = 'http://www.dsit.org.ir/?cmd=page&Cid=92&title=Kontakt&lang=fa'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        scr = str(soup.select('iframe')[0]).split('" src="')
        latitude = re.findall("3d([^!]*)", scr[1])[0]
        longitude = re.findall("2d([^!]*)", scr[1])[0]
        url = 'https://www.google.com/maps/place/@%s,%s,14z/data=!4m5!3m4!1s0x0:0x64f4c98dc95c2b8b!8m2!3d%s!4d%s?hl=en-US' % (
        latitude, longitude, latitude, longitude)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        phone = re.findall('[0-9]{3}\s[0-9]{4}\s[0-9]{4}|[0-9]{2}\s[0-9]{4}\s[0-9]{4}', str(soup))[0]
        site = re.findall('http:\/\/www.([a-z A-Z \. 0-9]*)', str(soup))[1]
        address = re.findall('Tehran, [, ، a-z A-Z 0-9 .]+', str(soup))[0]
        self.maptext.insertPlainText('%s\n\n%s\n\n%s'%(address,site,phone))
    def shoe1(self):
        app.processEvents()
        self.name.clear()
        url = 'https://www.digikala.com/search/category-men-clothing/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        frame = soup.select('.c-product-box__content--row a')
        global framedic
        framedic=dict()
        for i in frame:
            framedic.update({re.findall('^[a-zA-Z:\/.\-0-9]*',i['href'])[0]: i.text})
            self.name.addItem(i.text)
    def size1(self):
        app.processEvents()
        selected_size=self.sizetext.selectedItems()
        global sizeToPrice
        global generalIdToPrice
        global sizeToLocalId
        global localIdToGeneralId
        print(localIdToGeneralId)
        print(sizeToLocalId)
        print(generalIdToPrice)
        for i in sizeToLocalId:
            if selected_size[0].text() in i:
                for j in localIdToGeneralId:
                    if i[selected_size[0].text()] in j:
                        for k in generalIdToPrice:
                            if j[i[selected_size[0].text()]] in k:
                                self.pricetext.clear()
                                self.pricetext.insertPlainText(k[j[i[selected_size[0].text()]]])

    def name1(self):
        app.processEvents()
        selected_name=self.name.selectedItems()
        global framedic
        link='https://www.digikala.com/'+list(framedic.keys())[list(framedic.values()).index(selected_name[0].text())]
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'lxml')
        global generalIdToPrice
        global sizeToLocalId
        global localIdToGeneralId
        global sizeToPrice
        generalIdToPrice = []
        sizeToLocalId = []
        localIdToGeneralId = []
        sizeToPrice = {}
        temp = re.findall('"variants":\[\{([^]]*)', soup.get_text())[0].split('}')
        temp.pop()
        for i in temp:
            localIdToGeneralId.append({re.findall('size":([0-9]*)', i)[0]: re.findall('id":([0-9]*)', i)[0]})
        info = soup.select('.js-btn-add-to-cart')
        info.pop(0)
        info2 = soup.select('.c-product__size-dropdown')
        size = (info2[0].get_text()).split('\n')
        j = 0
        localId = re.findall('value="([0-9]*)"', str(info2[0]))
        for i in size:
            if (i.strip()) != '':
                sizeToLocalId.append({i.strip(): localId[j]})
                j = j + 1
        for i in info:
            generalIdToPrice.append(
                {re.findall('add\/([0-9]*)\/', i["href"])[0]: re.findall(' ([0-9]*) \-', i["data-event-label"])[0]})
        self.sizetext.clear()
        for i in sizeToLocalId:
            self.sizetext.addItem(list(i)[0])
            for j in localIdToGeneralId:
                if i[list(i)[0]] in j:
                    for k in generalIdToPrice:
                        if j[i[list(i)[0]]] in k:
                            sizeToPrice.update({list(i)[0]: k[j[i[list(i)[0]]]]})
        print(sizeToPrice)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mapbtn.setText(_translate("MainWindow", "part1(map)"))
        self.sizebtn.setText(_translate("MainWindow", "size selection"))
        self.namebtn.setText(_translate("MainWindow", "name selection"))
        self.shoebtn.setText(_translate("MainWindow", "part2(shoe)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

