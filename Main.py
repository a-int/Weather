import datetime
import sys

import pyowm as pm
from PyQt5 import QtWidgets, QtGui


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        #Setting up main window
        QtWidgets.QWidget.__init__(self, parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Weather')
        self.TitleLogo = QtGui.QIcon('.\\icons\\TitleLogo.png')
        self.setWindowIcon(self.TitleLogo)

        #Setting up the lineEdit
        self.lineEdit_searching = QtWidgets.QLineEdit(self)
        self.lineEdit_searching.setPlaceholderText('Enter city')
        self.lineEdit_searching.resize(300,20)
        self.lineEdit_searching.setGeometry(int((self.width()-self.lineEdit_searching.width())//2), int((self.height()-self.lineEdit_searching.height())//2), self.lineEdit_searching.width(), self.lineEdit_searching.height())
        self.lineEdit_searching.textEdited.connect(self.textEdited)
        #Setting up widget that contains suitable citiesTable_widget
        self.citiesTable_widget = QtWidgets.QListView(self)
        self.citiesTable_widget.resize(300, 200)
        self.citiesTable_widget.setGeometry(int((self.width() - self.citiesTable_widget.width()) // 2), int((self.height() - self.lineEdit_searching.height()) // 2 + self.lineEdit_searching.height()), self.citiesTable_widget.width(), self.citiesTable_widget.height())
        self.citiesTable_widget.setMovement(0) #Preventing moving of lines
        self.citiesTable_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.citiesTable_widget.setAlternatingRowColors(True) #Colour of rows alternates
        self.container_for_cities = QtGui.QStandardItemModel(self)
        self.citiesTable_widget.setModel(self.container_for_cities)
        self.citiesTable_widget.hide()
        self.citiesTable_widget.clicked.connect(self.entered)

        #setting Up Owm attributs
        self.City = str()
        self.country = str()
        self.lat = float()
        self.lon = float()
        self.id = int()
        self.suitable_cities = list()
        self.date = str()
        self.day = int()
        self.month = int()
        self.year = int()
        self.sunrise_time = str()
        self.sunset_time = str()

    def find_suitable_cities(self):
        self.suitable_cities = []
        self.city = self.lineEdit_searching.text().title()
        if self.city == '': self.city = '0'

        if  97 <= ord(self.city.lower()[0]) <= 102:
            self.suitable_cities = []
            for string in open('.\\cities_ids\\097-102.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(self.city):
                    self.suitable_cities.append(string)
        if 103 <= ord(self.city.lower()[0]) <= 108:
            self.suitable_cities = []
            for string in open('.\\cities_ids\\103-108.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(self.city):
                    self.suitable_cities.append(string)
        if 109 <= ord(self.city.lower()[0]) <= 114:
            self.suitable_cities = []
            for string in open('.\\cities_ids\\109-114.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(self.city):
                    self.suitable_cities.append(string)
        if 115 <= ord(self.city.lower()[0]) <= 122:
            self.suitable_cities = list()
            for string in open('.\\cities_ids\\115-122.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(self.city):
                    self.suitable_cities.append(string)
        if len(self.suitable_cities) > 50:
            self.suitable_cities = self.suitable_cities[:50]
        i = 0
        for string in self.suitable_cities:
            location = ['' for i in range(5)] #Generate list that looks like [City, id, lat, lon, county]
            index_of_location = 0
            #Clear string that looks like City, La, id, lat, lon, Counry
            for char in string:
                if char == ',': index_of_location += 1
                elif index_of_location == 1 and not char.isdigit(): index_of_location = 0
                elif char != ',' and char != '\n':
                    location[index_of_location] = location[index_of_location] + char
            self.suitable_cities[i] = {"city": str(location[0]), 'id': int(location[1]), 'lat': float(location[2]), 'lon': float(location[3]), 'country': str(location[4])}
            i += 1

    def get_weather(self):
        config_dict = pm.utils.config.get_default_config()
        config_dict['language'] = 'ru'
        owmKey = pm.OWM('41d1b31ac4485832252933721443d6e9', config_dict)
        mgr = owmKey.weather_manager()
        city = self.container_for_cities.data(self.citiesTable_widget.currentIndex())[3:]
        country = self.container_for_cities.data(self.citiesTable_widget.currentIndex())[:2]
        self.lat = owmKey.city_id_registry().locations_for(city)[0].lat
        self.lon = owmKey.city_id_registry().locations_for(city)[0].lon

        one_call = mgr.one_call(self.lat, self.lon)
        for weather in one_call.forecast_daily:
            self.date = weather.reference_time(timeformat='iso')[:-15]  # date[:4] - Year, date[5:7] - Month, date[8:10] - day
            self.day = self.date[8:10]
            self.month = self.date[5:7]
            self.year = self.date[:4]
            self.temp_day = round(weather.temperature('celsius')['day'])
            self.sunrise_time = str(datetime.datetime.fromtimestamp(weather.sunrise_time()).time())[:5]  # I take hours and minutes of sunrise
            self.sunset_time = str(datetime.datetime.fromtimestamp(weather.sunset_time()).time())[:5]  # I take hours and minutes of sunset
            if self.day.startswith('0'): self.day = self.day[1:]
            if self.month.startswith('0'): self.month = self.month[1:]
            if self.sunrise_time.startswith('0'): self.sunrise_time = self.sunrise_time[1:]
            if self.sunset_time.startswith('0'): self.sunset_time = sunset_time[1:]
    #Setting up Actions after choosing a city
    def entered(self, index):
        self.lineEdit_searching.hide()
        self.citiesTable_widget.hide()
        self.get_weather()

    def textEdited(self):
        if self.lineEdit_searching.text() == '':
            self.citiesTable_widget.hide()
        else: self.citiesTable_widget.show()
        self.container_for_cities.clear() #Очищаем таблицу от вариантов
        self.find_suitable_cities()
        #Adding cities to the widget that contains them
        for i in range(50):
            if len(self.suitable_cities) > i:
                city = self.suitable_cities[i]['country'] + '\t' + self.suitable_cities[i]['city']
                flag = QtGui.QIcon('.\\icons\\TitleLogo.png')
                self.container_for_cities.appendRow(QtGui.QStandardItem(flag, city))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
