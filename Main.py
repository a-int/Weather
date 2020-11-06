import datetime
import sys

import pyowm as pm
from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        #Setting up main window
        QtWidgets.QWidget.__init__(self, parent)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Weather')
        self.TitleLogo = QtGui.QIcon('.\\icons\\TitleLogo.png')
        self.setWindowIcon(self.TitleLogo)

        #Setting up widgets
        self.lineEdit_searching = QtWidgets.QLineEdit(self)
        self.lineEdit_searching.setPlaceholderText('Enter city')
        self.lineEdit_searching.setFixedSize(300,20)
        lineEdit_searching_X_geo =int((self.width()-self.lineEdit_searching.width())//2)
        lineEdit_searching_Y_geo =int((self.height()-self.lineEdit_searching.height())//2)
        self.lineEdit_searching.setGeometry(lineEdit_searching_X_geo,lineEdit_searching_Y_geo , self.lineEdit_searching.width(), self.lineEdit_searching.height())
        self.lineEdit_searching.textEdited.connect(self.textEdited)

        self.citiesTable_widget = QtWidgets.QListView(self)
        self.citiesTable_widget.setFixedSize(300,200)
        citiesTable_widget_x_geo = int((self.width() - self.citiesTable_widget.width()) // 2)
        citiesTable_widget_Y_geo = int((self.height() - self.lineEdit_searching.height())// 2 + self.lineEdit_searching.height())
        self.citiesTable_widget.setGeometry(citiesTable_widget_x_geo, citiesTable_widget_Y_geo , self.citiesTable_widget.width(), self.citiesTable_widget.height())
        self.citiesTable_widget.setMovement(0) #Preventing moving of lines
        self.citiesTable_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.citiesTable_widget.setAlternatingRowColors(True) #Colour of rows alternates
        self.container_for_cities = QtGui.QStandardItemModel(self)
        self.citiesTable_widget.setModel(self.container_for_cities)
        self.citiesTable_widget.hide()
        self.citiesTable_widget.clicked.connect(self.entered)

        self.cityLabel = QtWidgets.QLabel(self)
        self.cityLabel.setFixedSize(100,40)
        self.cityLabel.setWordWrap(True)
        self.cityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cityLabel.setStyleSheet(""" 
                                        font: bold italic;
                                        color: black;
                                        background-opacity: 1;
                                    """)
        self.cityLabel.setGeometry(10, 10, self.cityLabel.width(), self.cityLabel.height())
        self.cityLabel.hide()

        self.status_of_today = QtWidgets.QLabel(self)
        self.status_of_today.setWordWrap(True)
        self.status_of_today.setFixedSize(100, 40)
        self.status_of_today.setAlignment(QtCore.Qt.AlignCenter)
        self.status_of_today.setStyleSheet("""  """)
        self.status_of_today.setGeometry(13, 50, self.status_of_today.width(), self.status_of_today.height())
        self.status_of_today.hide()

        self.temperature_now = QtWidgets.QLabel(self)
        self.temperature_now.setWordWrap(True)
        self.temperature_now.setFixedSize(100, 100)
        self.temperature_now.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature_now.setStyleSheet(""" """)
        self.temperature_now.setGeometry(10, 90, self.status_of_today.width(), self.status_of_today.height())
        self.temperature_now.hide()

        self.sunrise_time = QtWidgets.QLabel(self)
        self.sunrise_time.setWordWrap(True)
        self.sunrise_time.setFixedSize(200, 40)
        self.sunrise_time.setAlignment(QtCore.Qt.AlignCenter)
        self.sunrise_time.setStyleSheet("""  """)
        sunrise_time_X_geo = self.width() - 2 * self.sunrise_time.width()
        sunrise_time_Y_geo = 53
        self.sunrise_time.setGeometry(sunrise_time_X_geo, sunrise_time_Y_geo, self.sunrise_time.width(), self.sunrise_time.height())
        self.sunrise_time.hide()

        self.sunset_time = QtWidgets.QLabel(self)
        self.sunset_time.setWordWrap(True)
        self.sunset_time.setFixedSize(200, 40)
        self.sunset_time.setAlignment(QtCore.Qt.AlignCenter)
        self.sunset_time.setStyleSheet("""  """)
        sunset_time_X_geo = self.width() -  self.sunrise_time.width()
        sunset_time_Y_geo = 53
        self.sunset_time.setGeometry(sunset_time_X_geo, sunset_time_Y_geo, self.sunset_time.width(),self.sunset_time.height())
        self.sunset_time.hide()

        self.feels_like_of_today = QtWidgets.QLabel(self)
        self.feels_like_of_today.setWordWrap(True)
        self.feels_like_of_today.setFixedSize(200, 40)
        self.feels_like_of_today.setAlignment(QtCore.Qt.AlignCenter)
        self.feels_like_of_today.setStyleSheet("""  """)
        feels_like_of_today_X_geo = self.width() - 2 * self.feels_like_of_today.width()
        feels_like_of_today_Y_geo = self.feels_like_of_today.height()+ sunset_time_Y_geo
        self.feels_like_of_today.setGeometry(feels_like_of_today_X_geo, feels_like_of_today_Y_geo, self.feels_like_of_today.width(), self.feels_like_of_today.height())
        self.feels_like_of_today.hide()

        self.wind_speed = QtWidgets.QLabel(self)
        self.wind_speed.setWordWrap(True)
        self.wind_speed.setFixedSize(200, 40)
        self.wind_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.wind_speed.setStyleSheet("""  """)
        wind_speed_X_geo = self.width() - self.wind_speed.width()
        wind_speed_Y_geo = self.wind_speed.height() + sunset_time_Y_geo
        self.wind_speed.setGeometry(wind_speed_X_geo, wind_speed_Y_geo, self.wind_speed.width(), self.wind_speed.height())
        self.wind_speed.hide()

        #setting Up Owm attributs
        self.city = str()
        self.country = str()
        self.lat = float()
        self.lon = float()
        self.id = int()
        self.suitable_cities = list()
        self.date = list()
        self.day = list()
        self.daily_weather_status = list()
        self.daily_max_temps = list()
        self.daily_min_temps = list()

        weekday_now = datetime.datetime.isoweekday(datetime.datetime.today())
        day_of_week = {1: 'Monday', 2:'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    def find_suitable_cities(self):
        self.suitable_cities = []
        city = self.lineEdit_searching.text().title()
        if city == '': city = '0'

        if  97 <= ord(city.lower()[0]) <= 102:
            self.suitable_cities = []
            for string in open('.\\cities_ids\\097-102.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(city):
                    self.suitable_cities.append(string)
        if 103 <= ord(city.lower()[0]) <= 108:
            self.suitable_cities = []
            for string in open('.\\cities_ids\\103-108.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(city):
                    self.suitable_cities.append(string)
        if 109 <= ord(city.lower()[0]) <= 114:
            self.suitable_cities = []
            for string in open('.\\cities_ids\\109-114.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(city):
                    self.suitable_cities.append(string)
        if 115 <= ord(city.lower()[0]) <= 122:
            self.suitable_cities = list()
            for string in open('.\\cities_ids\\115-122.txt', 'r', encoding='UTF8').readlines():
                if string.startswith(city):
                    self.suitable_cities.append(string)
        if len(self.suitable_cities) > 50:
            self.suitable_cities = self.suitable_cities[:50]
        i = 0
        for string in self.suitable_cities:
            location = ['' for i in range(5)] #Generate list that looks like [city, id, lat, lon, county]
            index_of_location = 0
            #Clear string that looks like city, La, id, lat, lon, Counry
            for char in string:
                if char == ',': index_of_location += 1
                elif index_of_location == 1 and not char.isdigit(): index_of_location = 0
                elif char != ',' and char != '\n':
                    location[index_of_location] = location[index_of_location] + char
            self.suitable_cities[i] = {"city": str(location[0]), 'id': int(location[1]), 'lat': float(location[2]), 'lon': float(location[3]), 'country': str(location[4])}
            i += 1

    def get_weather(self):
        self.city = self.container_for_cities.data(self.citiesTable_widget.currentIndex())[3:]
        self.country = self.container_for_cities.data(self.citiesTable_widget.currentIndex())[:2]
        for i in range(len(self.suitable_cities)):
            if self.suitable_cities[i]['city'] == self.city and self.suitable_cities[i]['country'] == self.country:
                index = i
        self.lat = self.suitable_cities[index]['lat']
        self.lon = self.suitable_cities[index]['lon']
        config_dict = pm.utils.config.get_default_config()
        config_dict['language'] = 'ru'
        owmKey = pm.OWM('41d1b31ac4485832252933721443d6e9', config_dict)
        mgr = owmKey.weather_manager()
        self.temperature_now.setNum(mgr.weather_at_place(self.city).weather.temperature('celsius')['temp']) #Get today's temperature
        self.sunrise_time.setText('Sunrise time\n'+str(datetime.datetime.fromtimestamp(mgr.weather_at_place(self.city).weather.sunrise_time()).time())[:5])
        self.sunset_time.setText('Sunset time\n'+str(datetime.datetime.fromtimestamp(mgr.weather_at_place(self.city).weather.sunset_time()).time())[:5])
        self.feels_like_of_today.setText('Feels like\n'+str(round(mgr.weather_at_place(self.city).weather.temperature('celsius')['feels_like'])))
        self.wind_speed.setText('Wind speed\n' + str(mgr.weather_at_place(self.city).weather.wind()['speed']))
        one_call = mgr.one_call(self.lat, self.lon)
        i = 0
        for weather in one_call.forecast_daily:
            self.date.append(weather.reference_time(timeformat='iso')[:-15])  # date[:4] - Year, date[5:7] - Month, date[8:10] - day
            self.day.append(self.date[i][8:10])
            self.temp_day = round(weather.temperature('celsius')['day'])
            self.daily_weather_status.append(weather.detailed_status)
            self.daily_min_temps.append(round(weather.temperature('celsius')['min']))
            self.daily_max_temps.append(round(weather.temperature('celsius')['max']))
            if self.day[i].startswith('0'): self.day[i] = self.day[i][1:]
            i+=1

    #Setting up Actions after choosing a city
    def entered(self, index):
        self.lineEdit_searching.hide()
        self.citiesTable_widget.hide()
        self.get_weather()
        self.cityLabel.setText(self.city)
        self.cityLabel.show()
        self.status_of_today.setText(self.daily_weather_status[0])
        self.status_of_today.show()
        self.temperature_now.show()
        self.sunrise_time.show()
        self.sunset_time.show()
        self.feels_like_of_today.show()
        self.wind_speed.show()

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
