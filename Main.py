import datetime
import sys

import pyowm as pm
from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        #Setting up main window
        QtWidgets.QWidget.__init__(self)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Weather')
        self.TitleLogo = QtGui.QIcon('.\\icons\\TitleLogo.png')
        self.setWindowIcon(self.TitleLogo)
        self.time = datetime.datetime.now().hour
        if 6 <= self.time <= 20:
            self.setStyleSheet('''
                                background-color: #FFFFFF;
                                font-color: black;''')
        else:self.setStyleSheet('''
                                background-color: #1A1A1A;
                                color: white''')

        CSS = """
            .QLabel{
                    font: Verdana;
                    font-size: 15px;
                    font-weight: bold;
            }
            .QLabel#City{
                        font: Verdana;
                        font-size: 50px;
            }
            .QLabel#status{
                    font-weight:bold;
                    font-size: 13px;
            }
            .QLabel#temp_now{
                        font: Verdana;
                        font-size: 150px;
                        background-color: rgba(0,0,0,0);
            }
        """

        #Setting up widgets
        self.search_lineEdit = QtWidgets.QLineEdit(self)
        self.search_lineEdit.setPlaceholderText('Enter city')
        self.search_lineEdit.setFixedSize(300, 20)
        search_lineEdit_X_geo =int((self.width() - self.search_lineEdit.width()) // 2)
        search_lineEdit_Y_geo =int((self.height() - self.search_lineEdit.height()) // 2)
        self.search_lineEdit.setGeometry(search_lineEdit_X_geo, search_lineEdit_Y_geo, self.search_lineEdit.width(), self.search_lineEdit.height())
        self.search_lineEdit.textEdited.connect(self.textEdited)

        self.citiesTable_widget = QtWidgets.QListView(self)
        self.citiesTable_widget.setFixedSize(300,200)
        citiesTable_widget_x_geo = int((self.width() - self.citiesTable_widget.width()) // 2)
        citiesTable_widget_Y_geo = int((self.height() - self.search_lineEdit.height()) // 2 + self.search_lineEdit.height())
        self.citiesTable_widget.setGeometry(citiesTable_widget_x_geo, citiesTable_widget_Y_geo , self.citiesTable_widget.width(), self.citiesTable_widget.height())
        self.citiesTable_widget.setMovement(0) #Preventing moving of lines
        self.citiesTable_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #self.citiesTable_widget.setAlternatingRowColors(True) #Colour of rows alternates
        self.container_for_cities = QtGui.QStandardItemModel(self)
        self.citiesTable_widget.setModel(self.container_for_cities)
        self.citiesTable_widget.hide()
        self.citiesTable_widget.clicked.connect(self.entered)

        self.cityLabel = QtWidgets.QLabel(self, objectName = 'City')
        #self.cityLabel.setFixedSize(350,80)
        self.cityLabel.setStyleSheet(CSS)
        self.cityLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.cityLabel.setWordWrap(True)
        self.cityLabel.setGeometry(10, 0, self.cityLabel.width(), self.cityLabel.height())
        self.cityLabel.hide()

        self.status_of_today = QtWidgets.QLabel(self, objectName = "status")
        self.status_of_today.setWordWrap(True)
        self.status_of_today.resize(100, 30)
        self.status_of_today.setAlignment(QtCore.Qt.AlignHCenter)
        self.status_of_today.setStyleSheet(CSS)
        self.status_of_today.hide()

        self.temperature_now = QtWidgets.QLabel(self, objectName = 'temp_now')
        self.temperature_now.setAlignment(QtCore.Qt.AlignHCenter)
        self.temperature_now.setStyleSheet(CSS)
        self.temperature_now.resize(176,160)
        #self.temperature_now.setGeometry(0, 0, self.status_of_today.width(), self.status_of_today.height())
        self.temperature_now.hide()

        self.sunrise_time = QtWidgets.QLabel(self, objectName = "sunrice_time")
        self.sunrise_time.setWordWrap(True)
        self.sunrise_time.setFixedSize(100, 40)
        self.sunrise_time.setAlignment(QtCore.Qt.AlignCenter)
        self.sunrise_time.setStyleSheet(CSS)
        self.sunrise_time.setGeometry(580, 130, self.sunrise_time.width(), self.sunrise_time.height())
        self.sunrise_time.hide()

        self.sunset_time = QtWidgets.QLabel(self, objectName = "sunset_time")
        self.sunset_time.setWordWrap(True)
        self.sunset_time.setFixedSize(100, 40)
        self.sunset_time.setAlignment(QtCore.Qt.AlignCenter)
        self.sunset_time.setStyleSheet(CSS)
        self.sunset_time.setGeometry(680,130, self.sunset_time.width(),self.sunset_time.height())
        self.sunset_time.hide()

        self.feels_like_of_today = QtWidgets.QLabel(self, objectName = 'feels_like')
        self.feels_like_of_today.setWordWrap(True)
        self.feels_like_of_today.setFixedSize(100, 40)
        self.feels_like_of_today.setAlignment(QtCore.Qt.AlignCenter)
        self.feels_like_of_today.setStyleSheet(CSS)
        self.feels_like_of_today.setGeometry(580, 200, self.feels_like_of_today.width(), self.feels_like_of_today.height())
        self.feels_like_of_today.hide()

        self.wind_speed = QtWidgets.QLabel(self, objectName = 'wind_speed')
        self.wind_speed.setWordWrap(True)
        self.wind_speed.setFixedSize(100, 40)
        self.wind_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.wind_speed.setStyleSheet(CSS)

        self.wind_speed.setGeometry(680, 200, self.wind_speed.width(), self.wind_speed.height())
        self.wind_speed.hide()

        #Setup similar widgets
        weekday_now = datetime.datetime.weekday(datetime.datetime.today())
        day_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        self.day1, self.day2, self.day3, self.day4, self.day5, self.day6, self.day7 = QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day")
        self.day1.setGeometry(10,330,100,40), self.day2.setGeometry(10,370,100,40), self.day3.setGeometry(10,410,100,40), self.day4.setGeometry(10,450,100,40), self.day5.setGeometry(10,490,100,40), self.day6.setGeometry(10,530,100,40), self.day7.setGeometry(10,570,100,40)
        self.day1.setStyleSheet(CSS),self.day2.setStyleSheet(CSS), self.day3.setStyleSheet(CSS), self.day4.setStyleSheet(CSS), self.day5.setStyleSheet(CSS), self.day6.setStyleSheet(CSS), self.day7.setStyleSheet(CSS)
        self.day1.setAlignment(QtCore.Qt.AlignLeft),self.day2.setAlignment(QtCore.Qt.AlignLeft), self.day3.setAlignment(QtCore.Qt.AlignLeft), self.day4.setAlignment(QtCore.Qt.AlignLeft), self.day5.setAlignment(QtCore.Qt.AlignLeft), self.day6.setAlignment(QtCore.Qt.AlignLeft), self.day7.setAlignment(QtCore.Qt.AlignLeft)
        self.day1.setText(day_of_week[(weekday_now+1)%7]), self.day2.setText(day_of_week[(weekday_now+2)%7]), self.day3.setText(day_of_week[(weekday_now+3)%7]), self.day4.setText(day_of_week[(weekday_now+4)%7]), self.day5.setText(day_of_week[(weekday_now+5)%7]), self.day6.setText(day_of_week[(weekday_now+6)%7]), self.day7.setText(day_of_week[(weekday_now+7)%7])
        self.day1.hide(), self.day2.hide(), self.day3.hide(), self.day4.hide(), self.day5.hide(), self.day6.hide(), self.day7.hide()

        self.day_status1, self.day_status2, self.day_status3, self.day_status4, self.day_status5, self.day_status6, self.day_status7 = QtWidgets.QLabel(self), QtWidgets.QLabel(self), QtWidgets.QLabel(self), QtWidgets.QLabel(self), QtWidgets.QLabel(self), QtWidgets.QLabel(self), QtWidgets.QLabel(self)
        self.day_status1.setGeometry(390, 330,30,30), self.day_status2.setGeometry(390, 370,30,30), self.day_status3.setGeometry(390, 410,30,30), self.day_status4.setGeometry(390, 450,30,30), self.day_status5.setGeometry(390, 490,30,30), self.day_status6.setGeometry(390, 530, 30, 30), self.day_status7.setGeometry(390, 570, 30, 30)
        self.day_status1.hide(), self.day_status2.hide(), self.day_status3.hide(), self.day_status4.hide(), self.day_status5.hide(), self.day_status6.hide(), self.day_status7.hide()

        self.day_mx_temp1, self.day_mx_temp2, self.day_mx_temp3, self.day_mx_temp4, self.day_mx_temp5, self.day_mx_temp6, self.day_mx_temp7 = QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"),  QtWidgets.QLabel(self, objectName = "Week's_day"),  QtWidgets.QLabel(self, objectName = "Week's_day"),  QtWidgets.QLabel(self, objectName = "Week's_day"),  QtWidgets.QLabel(self, objectName = "Week's_day"),  QtWidgets.QLabel(self, objectName = "Week's_day")
        self.day_mx_temp1.setGeometry(620, 330, 20, 20),self.day_mx_temp2.setGeometry(620, 370, 20,20), self.day_mx_temp3.setGeometry(620, 410, 20,20), self.day_mx_temp4.setGeometry(620, 450, 20,20), self.day_mx_temp5.setGeometry(620, 490, 20,20), self.day_mx_temp6.setGeometry(620, 530, 20,20), self.day_mx_temp7.setGeometry(620, 570, 20,20)
        self.day_mx_temp1.setStyleSheet(CSS),self.day_mx_temp2.setStyleSheet(CSS), self.day_mx_temp3.setStyleSheet(CSS), self.day_mx_temp4.setStyleSheet(CSS), self.day_mx_temp5.setStyleSheet(CSS), self.day_mx_temp6.setStyleSheet(CSS), self.day_mx_temp7.setStyleSheet(CSS)
        self.day_mx_temp1.setAlignment(QtCore.Qt.AlignCenter),self.day_mx_temp2.setAlignment(QtCore.Qt.AlignCenter), self.day_mx_temp3.setAlignment(QtCore.Qt.AlignCenter), self.day_mx_temp4.setAlignment(QtCore.Qt.AlignCenter), self.day_mx_temp5.setAlignment(QtCore.Qt.AlignCenter), self.day_mx_temp6.setAlignment(QtCore.Qt.AlignCenter), self.day_mx_temp7.setAlignment(QtCore.Qt.AlignCenter)
        self.day_mx_temp1.hide(),self.day_mx_temp2.hide(), self.day_mx_temp3.hide(), self.day_mx_temp4.hide(), self.day_mx_temp5.hide(), self.day_mx_temp6.hide(), self.day_mx_temp7.hide()

        self.day_mn_temp1, self.day_mn_temp2, self.day_mn_temp3, self.day_mn_temp4, self.day_mn_temp5, self.day_mn_temp6, self.day_mn_temp7 = QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day"), QtWidgets.QLabel(self, objectName = "Week's_day")
        self.day_mn_temp1.setGeometry(720, 330, 20, 20), self.day_mn_temp2.setGeometry(720, 370, 20, 20), self.day_mn_temp3.setGeometry(720, 410, 20, 20), self.day_mn_temp4.setGeometry(720, 450, 20, 20), self.day_mn_temp5.setGeometry(720, 490,20,20), self.day_mn_temp6.setGeometry(720, 530, 20, 20), self.day_mn_temp7.setGeometry(720, 570, 20, 20)
        self.day_mn_temp1.setStyleSheet(CSS),self.day_mn_temp2.setStyleSheet(CSS), self.day_mn_temp3.setStyleSheet(CSS), self.day_mn_temp4.setStyleSheet(CSS), self.day_mn_temp5.setStyleSheet(CSS), self.day_mn_temp6.setStyleSheet(CSS), self.day_mn_temp7.setStyleSheet(CSS)
        self.day_mn_temp1.setAlignment(QtCore.Qt.AlignCenter), self.day_mn_temp2.setAlignment(QtCore.Qt.AlignCenter), self.day_mn_temp3.setAlignment(QtCore.Qt.AlignCenter), self.day_mn_temp4.setAlignment(QtCore.Qt.AlignCenter), self.day_mn_temp5.setAlignment(QtCore.Qt.AlignCenter), self.day_mn_temp6.setAlignment(QtCore.Qt.AlignCenter), self.day_mn_temp7.setAlignment(QtCore.Qt.AlignCenter)
        self.day_mn_temp1.hide(), self.day_mn_temp2.hide(), self.day_mn_temp3.hide(), self.day_mn_temp4.hide(), self.day_mn_temp5.hide(), self.day_mn_temp6.hide(), self.day_mn_temp7.hide()

        self.resetBtn = QtWidgets.QPushButton(self, objectName = 'reset')
        self.resetBtn.setGeometry(740, 20, 30, 30)
        self.resetBtn.setIcon(QtGui.QIcon('.\\icons\\reset.jpg'))
        self.resetBtn.setIconSize(QtCore.QSize(30,30))
        self.resetBtn.hide()
        self.resetBtn.clicked.connect(self.reset)

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

    def find_suitable_cities(self):
        self.suitable_cities = []
        city = self.search_lineEdit.text().title()
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
            self.suitable_cities = self.suitable_cities[:30]
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
        owmKey = pm.OWM('41d1b31ac4485832252933721443d6e9')
        mgr = owmKey.weather_manager()
        self.temperature_now.setNum(int(mgr.weather_at_coords(int(self.lat), int(self.lon)).weather.temperature('celsius')['temp'])) #Get today's temperature
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
            self.daily_min_temps.append(int(weather.temperature('celsius')['min']))
            self.daily_max_temps.append(int(weather.temperature('celsius')['max']))
            if self.day[i].startswith('0'): self.day[i] = self.day[i][1:]
            i+=1
    #Setting up Actions after choosing a city
    def entered(self, index):
        self.search_lineEdit.hide()
        self.citiesTable_widget.hide()
        self.get_weather()

        self.cityLabel.setText(self.city)
        if len(self.city)<6:
            self.cityLabel.resize(176,60)
        elif 5 <  len(self.city) <= 13:
            self.cityLabel.resize(len(self.city)*35, 60)
        else:
            self.cityLabel.resize(400,120)
        self.cityLabel.show()
        self.status_of_today.setText(self.daily_weather_status[0])
        self.status_of_today.setGeometry((self.cityLabel.width()-self.status_of_today.width())//2, self.cityLabel.height(), 100, 50)
        self.temperature_now.setGeometry((self.cityLabel.width()-self.temperature_now.width())//2, self.cityLabel.height()+self.status_of_today.height()-20, 176, 160)
        self.sunrise_time.setGeometry(580, self.cityLabel.height()+self.status_of_today.height()+10, 100, 40)
        self.sunset_time.setGeometry(680, self.cityLabel.height()+self.status_of_today.height()+10, 100, 40)
        self.feels_like_of_today.setGeometry(580,self.cityLabel.height()+self.status_of_today.height()+70 ,100,40)
        self.wind_speed.setGeometry(680, self.cityLabel.height()+self.status_of_today.height()+70, 100, 40)
        self.status_of_today.show()
        self.temperature_now.show()
        self.sunrise_time.show()
        self.sunset_time.show()
        self.feels_like_of_today.show()
        self.wind_speed.show()
        self.resetBtn.show()

        self.day1.show(), self.day2.show(), self.day3.show(), self.day4.show(), self.day5.show(), self.day6.show(), self.day7.show()
        for i in range(7):
            if self.daily_weather_status[i] == 'clear sky':
                Pixmap = QtGui.QPixmap('.\\icons\\clear_morn.jpg')
            elif self.daily_weather_status[i] == 'few clouds':
                Pixmap = QtGui.QPixmap('.\\icons\\few_clouds_morn.jpg')
            elif self.daily_weather_status[i] == 'scatted clouds':
                Pixmap = QtGui.QPixmap('.\\icons\\scattered_clouds.jpg')
            elif self.daily_weather_status[i] in ['broken clouds', "overcast clouds"]:
                Pixmap = QtGui.QPixmap(".\\icons\\broken_clouds.jpg")
            elif self.daily_weather_status[i] in ['mist', 'smoke', 'haze', 'sand', 'fog', 'dust', 'volcanic ash', 'squalls', 'tornado']:
                Pixmap = QtGui.QPixmap('.\\icons\\mist.jpg')
            elif self.daily_weather_status[i] in ['light snow', 'snow', 'heavy snow', 'sleet', 'light shower sleet', 'shower sleet', 'light rain and snow', 'rain and snow', 'light shower snow', 'shower snow', 'heavy shower snow', 'freezing rain']:
                Pixmap = QtGui.QPixmap(".\\icons\\snow.jpg")
            elif self.daily_weather_status[i] in ['light intensity drizzle', 'drizzle', 'heavy intensity drizzle', 'light intensity drizzle rain', 'drizzle rain', 'heavy intensity drizzle rain', 'shower rain and drizzle', 'heavi shower rain and drizzle', 'shower drizzle', 'light intensity shower rain' , 'shower rain', 'heavi intensity shower rain', 'ragged shower rain']:
                Pixmap = QtGui.QPixmap('.\\icons\\shower_rain.jpg')
            elif self.daily_weather_status[i] in ['light rain', 'moderate rain', 'heavy intensity rain', 'very heavy rain', 'extreme rain']:
                Pixmap = QtGui.QPixmap('.\\icons\\rain_morn.jpg')
            elif self.daily_weather_status[i] in ['thunderstorm with light rain', 'thinderstorm with rain', 'thunderstorm with heavy rain', 'light thunderstorm', 'heavy thunderstorm', 'thunderstorm', 'ragged thunderstorm', 'thunderstorm with light drizzle', 'thunderstorm with drizzle', 'thunderstorm with heavy drizzle']:
                Pixmap = QtGui.QPixmap('.\\icons\\thunderstorm.jpg')
            if i == 0:
                self.day_status1.setPixmap(Pixmap)
            if i == 1:
                self.day_status2.setPixmap(Pixmap)
            if i == 2:
                self.day_status3.setPixmap(Pixmap)
            if i == 3:
                self.day_status4.setPixmap(Pixmap)
            if i == 4:
                self.day_status5.setPixmap(Pixmap)
            if i == 5:
                self.day_status6.setPixmap(Pixmap)
            if i == 6:
                self.day_status7.setPixmap(Pixmap)
        self.day_status1.show(), self.day_status2.show(), self.day_status3.show(), self.day_status4.show(), self.day_status5.show(), self.day_status6.show(), self.day_status7.show()
        self.day_mx_temp1.setNum(self.daily_max_temps[1]),self.day_mx_temp2.setNum(self.daily_max_temps[2]), self.day_mx_temp3.setNum(self.daily_max_temps[3]), self.day_mx_temp4.setNum(self.daily_max_temps[4]), self.day_mx_temp5.setNum(self.daily_max_temps[5]), self.day_mx_temp6.setNum(self.daily_max_temps[6]), self.day_mx_temp7.setNum(self.daily_max_temps[7]),
        self.day_mx_temp1.show(),self.day_mx_temp2.show(), self.day_mx_temp3.show(), self.day_mx_temp4.show(), self.day_mx_temp5.show(), self.day_mx_temp6.show(), self.day_mx_temp7.show()
        self.day_mn_temp1.setNum(self.daily_min_temps[1]), self.day_mn_temp2.setNum(self.daily_min_temps[2]), self.day_mn_temp3.setNum(self.daily_min_temps[3]), self.day_mn_temp4.setNum(self.daily_min_temps[4]), self.day_mn_temp5.setNum(self.daily_min_temps[5]), self.day_mn_temp6.setNum(self.daily_min_temps[6]), self.day_mn_temp7.setNum(self.daily_min_temps[7]),
        self.day_mn_temp1.show(), self.day_mn_temp2.show(), self.day_mn_temp3.show(), self.day_mn_temp4.show(), self.day_mn_temp5.show(), self.day_mn_temp6.show(), self.day_mn_temp7.show()
    def textEdited(self):
        if self.search_lineEdit.text() == '':
            self.citiesTable_widget.hide()
        else: self.citiesTable_widget.show()
        self.container_for_cities.clear() #Очищаем таблицу от вариантов
        self.find_suitable_cities()
        #Adding cities to the widget that contains them
        for i in range(30):
            if len(self.suitable_cities) > i:
                city = str(self.suitable_cities[i]['country'] + '\t' + self.suitable_cities[i]['city'])
                if city.startswith('AF'):
                    flag = QtGui.QIcon('.\\icons\\png\\afghanistan.png')
                elif city.startswith('AL'):
                    flag = QtGui.QIcon('.\\icons\\png\\albania.png')
                elif city.startswith('DZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\algeria.png')
                elif city.startswith('AD'):
                    flag = QtGui.QIcon('.\\icons\\png\\andorra.png')
                elif city.startswith('AO'):
                    flag = QtGui.QIcon('.\\icons\\png\\angola.png')
                elif city.startswith('AG'):
                    flag = QtGui.QIcon('.\\icons\\png\\antigua-and-barbuda.png')
                elif city.startswith('AR'):
                    flag = QtGui.QIcon('.\\icons\\png\\argentina.png')
                elif city.startswith('AU'):
                    flag = QtGui.QIcon('.\\icons\\png\\australia.png')
                elif city.startswith('AM'):
                    flag = QtGui.QIcon('.\\icons\\png\\armenia.png')
                elif city.startswith('AT'):
                    flag = QtGui.QIcon('.\\icons\\png\\austria.png')
                elif city.startswith('AZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\azerbaijan.png')
                elif city.startswith('BS'):
                    flag = QtGui.QIcon('.\\icons\\png\\bahamas.png')
                elif city.startswith('BH'):
                    flag = QtGui.QIcon('.\\icons\\png\\bahrain.png')
                elif city.startswith('BD'):
                    flag = QtGui.QIcon('.\\icons\\png\\bangladesh.png')
                elif city.startswith('BB'):
                    flag = QtGui.QIcon('.\\icons\\png\\barbados.png')
                elif city.startswith('BY'):
                    flag = QtGui.QIcon('.\\icons\\png\\belarus.png')
                elif city.startswith('BE'):
                    flag = QtGui.QIcon('.\\icons\\png\\belgium.png')
                elif city.startswith('BZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\belize.png')
                elif city.startswith('BJ'):
                    flag = QtGui.QIcon('.\\icons\\png\\benin.png')
                elif city.startswith('BT'):
                    flag = QtGui.QIcon('.\\icons\\png\\bhutan.png')
                elif city.startswith('BO'):
                    flag = QtGui.QIcon('.\\icons\\png\\bolivia.png')
                elif city.startswith('BA'):
                    flag = QtGui.QIcon('.\\icons\\png\\bosnia-and-herzegovina.png')
                elif city.startswith('BW'):
                    flag = QtGui.QIcon('.\\icons\\png\\botswana.png')
                elif city.startswith('BR'):
                    flag = QtGui.QIcon('.\\icons\\png\\brazil.png')
                elif city.startswith('BN'):
                    flag = QtGui.QIcon('.\\icons\\png\\brunei.png')
                elif city.startswith('BG'):
                    flag = QtGui.QIcon('.\\icons\\png\\bulgaria.png')
                elif city.startswith('BF'):
                    flag = QtGui.QIcon('.\\icons\\png\\burkina-faso.png')
                elif city.startswith('BI'):
                    flag = QtGui.QIcon('.\\icons\\png\\burundi.png')
                elif city.startswith('CV'):
                    flag = QtGui.QIcon('.\\icons\\png\\cape-verde.png')
                elif city.startswith('KH'):
                    flag = QtGui.QIcon('.\\icons\\png\\cambodia.png')
                elif city.startswith('CM'):
                    flag = QtGui.QIcon('.\\icons\\png\\cameroon.png')
                elif city.startswith('CA'):
                    flag = QtGui.QIcon('.\\icons\\png\\canada.png')
                elif city.startswith('CF'):
                    flag = QtGui.QIcon('.\\icons\\png\\central-african-republic.png')
                elif city.startswith('TD'):
                    flag = QtGui.QIcon('.\\icons\\png\\chad.png')
                elif city.startswith('CL'):
                    flag = QtGui.QIcon('.\\icons\\png\\chile.png')
                elif city.startswith('CN'):
                    flag = QtGui.QIcon('.\\icons\\png\\china.png')
                elif city.startswith('CO'):
                    flag = QtGui.QIcon('.\\icons\\png\\colombia.png')
                elif city.startswith('KM'):
                    flag = QtGui.QIcon('.\\icons\\png\\comoros.png')
                elif city.startswith('CK'):
                    flag = QtGui.QIcon('.\\icons\\png\\cook-islands.png')
                elif city.startswith('CR'):
                    flag = QtGui.QIcon('.\\icons\\png\\costa-rica.png')
                elif city.startswith('HR'):
                    flag = QtGui.QIcon('.\\icons\\png\\croatia.png')
                elif city.startswith('CU'):
                    flag = QtGui.QIcon('.\\icons\\png\\cuba.png')
                elif city.startswith('CY'):
                    flag = QtGui.QIcon('.\\icons\\png\\cyprus.png')
                elif city.startswith('CZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\czech-republic.png')
                elif city.startswith('KP'):
                    flag = QtGui.QIcon('.\\icons\\png\\south-korea.png')
                elif city.startswith('CD'):
                    flag = QtGui.QIcon('.\\icons\\png\\democratic-republic-of-congo.png')
                elif city.startswith('DK'):
                    flag = QtGui.QIcon('.\\icons\\png\\denmark.png')
                elif city.startswith('DJ'):
                    flag = QtGui.QIcon('.\\icons\\png\\djibouti.png')
                elif city.startswith('DM'):
                    flag = QtGui.QIcon('.\\icons\\png\\dominica.png')
                elif city.startswith('DOMDO'):
                    flag = QtGui.QIcon('.\\icons\\png\\dominican-republic.png')
                elif city.startswith('EC'):
                    flag = QtGui.QIcon('.\\icons\\png\\ecuador.png')
                elif city.startswith('EG'):
                    flag = QtGui.QIcon('.\\icons\\png\\egypt.png')
                elif city.startswith('SV'):
                    flag = QtGui.QIcon('.\\icons\\png\\salvador.png')
                elif city.startswith('GQ'):
                    flag = QtGui.QIcon('.\\icons\\png\\equatorial-guinea.png')
                elif city.startswith('ER'):
                    flag = QtGui.QIcon('.\\icons\\png\\eritrea.png')
                elif city.startswith('EE'):
                    flag = QtGui.QIcon('.\\icons\\png\\estonia.png')
                elif city.startswith('ET'):
                    flag = QtGui.QIcon('.\\icons\\png\\ethiopia.png')
                elif city.startswith('FO'):
                    flag = QtGui.QIcon('.\\icons\\png\\faroe-islands.png')
                elif city.startswith('FJ'):
                    flag = QtGui.QIcon('.\\icons\\png\\fiji.png')
                elif city.startswith('FI'):
                    flag = QtGui.QIcon('.\\icons\\png\\finland.png')
                elif city.startswith('FR'):
                    flag = QtGui.QIcon('.\\icons\\png\\france.png')
                elif city.startswith('GA'):
                    flag = QtGui.QIcon('.\\icons\\png\\gabon.png')
                elif city.startswith('GM'):
                    flag = QtGui.QIcon('.\\icons\\png\\gambia.png')
                elif city.startswith('GE'):
                    flag = QtGui.QIcon('.\\icons\\png\\georgia.png')
                elif city.startswith('DE'):
                    flag = QtGui.QIcon('.\\icons\\png\\germany.png')
                elif city.startswith('GH'):
                    flag = QtGui.QIcon('.\\icons\\png\\ghana.png')
                elif city.startswith('GR'):
                    flag = QtGui.QIcon('.\\icons\\png\\greece.png')
                elif city.startswith('GD'):
                    flag = QtGui.QIcon('.\\icons\\png\\grenada.png')
                elif city.startswith('GT'):
                    flag = QtGui.QIcon('.\\icons\\png\\guinea.png')
                elif city.startswith('GW'):
                    flag = QtGui.QIcon('.\\icons\\png\\guinea-bissau.png')
                elif city.startswith('GY'):
                    flag = QtGui.QIcon('.\\icons\\png\\guyana.png')
                elif city.startswith('HT'):
                    flag = QtGui.QIcon('.\\icons\\png\\haiti.png')
                elif city.startswith('HN'):
                    flag = QtGui.QIcon('.\\icons\\png\\honduras.png')
                elif city.startswith('HU'):
                    flag = QtGui.QIcon('.\\icons\\png\\hungary.png')
                elif city.startswith('IS'):
                    flag = QtGui.QIcon('.\\icons\\png\\iceland.png')
                elif city.startswith('IN'):
                    flag = QtGui.QIcon('.\\icons\\png\\india.png')
                elif city.startswith('ID'):
                    flag = QtGui.QIcon('.\\icons\\png\\indonesia.png')
                elif city.startswith('IR'):
                    flag = QtGui.QIcon('.\\icons\\png\\iran.png')
                elif city.startswith('IQ'):
                    flag = QtGui.QIcon('.\\icons\\png\\iraq.png')
                elif city.startswith('IE'):
                    flag = QtGui.QIcon('.\\icons\\png\\ireland.png')
                elif city.startswith('IL'):
                    flag = QtGui.QIcon('.\\icons\\png\\israel.png')
                elif city.startswith('IT'):
                    flag = QtGui.QIcon('.\\icons\\png\\italy.png')
                elif city.startswith('JM'):
                    flag = QtGui.QIcon('.\\icons\\png\\jamaica.png')
                elif city.startswith('CP'):
                    flag = QtGui.QIcon('.\\icons\\png\\japan.png')
                elif city.startswith('JO'):
                    flag = QtGui.QIcon('.\\icons\\png\\jordan.png')
                elif city.startswith('KZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\kazakhstan.png')
                elif city.startswith('KE'):
                    flag = QtGui.QIcon('.\\icons\\png\\kenya.png')
                elif city.startswith('KI'):
                    flag = QtGui.QIcon('.\\icons\\png\\kiribati.png')
                elif city.startswith('KW'):
                    flag = QtGui.QIcon('.\\icons\\png\\kuwait.png')
                elif city.startswith('KG'):
                    flag = QtGui.QIcon('.\\icons\\png\\kyrgyzstan.png')
                elif city.startswith('LA'):
                    flag = QtGui.QIcon('.\\icons\\png\\laos.png')
                elif city.startswith('LV'):
                    flag = QtGui.QIcon('.\\icons\\png\\latvia.png')
                elif city.startswith('LB'):
                    flag = QtGui.QIcon('.\\icons\\png\\lebanon.png')
                elif city.startswith('LS'):
                    flag = QtGui.QIcon('.\\icons\\png\\lesotho.png')
                elif city.startswith('LR'):
                    flag = QtGui.QIcon('.\\icons\\png\\liberia.png')
                elif city.startswith('LY'):
                    flag = QtGui.QIcon('.\\icons\\png\\libya.png')
                elif city.startswith('LT'):
                    flag = QtGui.QIcon('.\\icons\\png\\lithuania.png')
                elif city.startswith('LU'):
                    flag = QtGui.QIcon('.\\icons\\png\\luxembourg.png')
                elif city.startswith('MG'):
                    flag = QtGui.QIcon('.\\icons\\png\\madagascar.png')
                elif city.startswith('MW'):
                    flag = QtGui.QIcon('.\\icons\\png\\malawi.png')
                elif city.startswith('MY'):
                    flag = QtGui.QIcon('.\\icons\\png\\malaysia.png')
                elif city.startswith('MV'):
                    flag = QtGui.QIcon('.\\icons\\png\\maldives.png')
                elif city.startswith('ML'):
                    flag = QtGui.QIcon('.\\icons\\png\\mali.png')
                elif city.startswith('MT'):
                    flag = QtGui.QIcon('.\\icons\\png\\malta.png')
                elif city.startswith('MH'):
                    flag = QtGui.QIcon('.\\icons\\png\\marshall-island.png')
                elif city.startswith('MR'):
                    flag = QtGui.QIcon('.\\icons\\png\\mauritania.png')
                elif city.startswith('MU'):
                    flag = QtGui.QIcon('.\\icons\\png\\mauritius.png')
                elif city.startswith('MX'):
                    flag = QtGui.QIcon('.\\icons\\png\\mexico.png')
                elif city.startswith('FM'):
                    flag = QtGui.QIcon('.\\icons\\png\\micronesia.png')
                elif city.startswith('MC'):
                    flag = QtGui.QIcon('.\\icons\\png\\monaco.png')
                elif city.startswith('MN'):
                    flag = QtGui.QIcon('.\\icons\\png\\mongolia.png')
                elif city.startswith('ME'):
                    flag = QtGui.QIcon('.\\icons\\png\\montenegro.png')
                elif city.startswith('MA'):
                    flag = QtGui.QIcon('.\\icons\\png\\morocco.png')
                elif city.startswith('MZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\myanmar.png')
                elif city.startswith('NA'):
                    flag = QtGui.QIcon('.\\icons\\png\\namibia.png')
                elif city.startswith('NR'):
                    flag = QtGui.QIcon('.\\icons\\png\\nauru.png')
                elif city.startswith('NP'):
                    flag = QtGui.QIcon('.\\icons\\png\\nepal.png')
                elif city.startswith('NL'):
                    flag = QtGui.QIcon('.\\icons\\png\\netherlands.png')
                elif city.startswith('NZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\new-zealand.png')
                elif city.startswith('NI'):
                    flag = QtGui.QIcon('.\\icons\\png\\nicaragua.png')
                elif city.startswith('NE'):
                    flag = QtGui.QIcon('.\\icons\\png\\niger.png')
                elif city.startswith('NG'):
                    flag = QtGui.QIcon('.\\icons\\png\\nigeria.png')
                elif city.startswith('NU'):
                    flag = QtGui.QIcon('.\\icons\\png\\niue.png')
                elif city.startswith('MK'):
                    flag = QtGui.QIcon('.\\icons\\png\\republic-of-macedonia.png')
                elif city.startswith('NO'):
                    flag = QtGui.QIcon('.\\icons\\png\\norway.png')
                elif city.startswith('OM'):
                    flag = QtGui.QIcon('.\\icons\\png\\oman.png')
                elif city.startswith('PK'):
                    flag = QtGui.QIcon('.\\icons\\png\\pakistan.png')
                elif city.startswith('PW'):
                    flag = QtGui.QIcon('.\\icons\\png\\palau.png')
                elif city.startswith('PA'):
                    flag = QtGui.QIcon('.\\icons\\png\\panama.png')
                elif city.startswith('PG'):
                    flag = QtGui.QIcon('.\\icons\\png\\papua-new-guinea.png')
                elif city.startswith('PY'):
                    flag = QtGui.QIcon('.\\icons\\png\\paraguay.png')
                elif city.startswith('PE'):
                    flag = QtGui.QIcon('.\\icons\\png\\peru.png')
                elif city.startswith('PH'):
                    flag = QtGui.QIcon('.\\icons\\png\\philippines.png')
                elif city.startswith('PL'):
                    flag = QtGui.QIcon('.\\icons\\png\\republic-of-poland.png')
                elif city.startswith('PT'):
                    flag = QtGui.QIcon('.\\icons\\png\\portugal.png')
                elif city.startswith('QA'):
                    flag = QtGui.QIcon('.\\icons\\png\\qatar.png')
                elif city.startswith('KR'):
                    flag = QtGui.QIcon('.\\icons\\png\\north-korea.png')
                elif city.startswith('MD'):
                    flag = QtGui.QIcon('.\\icons\\png\\moldova.png')
                elif city.startswith('RO'):
                    flag = QtGui.QIcon('.\\icons\\png\\romania.png')
                elif city.startswith('RU'):
                    flag = QtGui.QIcon('.\\icons\\png\\russia.png')
                elif city.startswith('RW'):
                    flag = QtGui.QIcon('.\\icons\\png\\rwanda.png')
                elif city.startswith('KN'):
                    flag = QtGui.QIcon('.\\icons\\png\\saint-kitts-and-nevis.png')
                elif city.startswith('LC'):
                    flag = QtGui.QIcon('.\\icons\\png\\st-lucia.png')
                elif city.startswith('VC'):
                    flag = QtGui.QIcon('.\\icons\\png\\st-vincent-and-the-grenadines.png')
                elif city.startswith('WS'):
                    flag = QtGui.QIcon('.\\icons\\png\\samoa.png')
                elif city.startswith('SM'):
                    flag = QtGui.QIcon('.\\icons\\png\\san-marino.png')
                elif city.startswith('ST'):
                    flag = QtGui.QIcon('.\\icons\\png\\sao-tome-and-principe.png')
                elif city.startswith('SA'):
                    flag = QtGui.QIcon('.\\icons\\png\\saudi-arabia.png')
                elif city.startswith('SN'):
                    flag = QtGui.QIcon('.\\icons\\png\\senegal.png')
                elif city.startswith('RS'):
                    flag = QtGui.QIcon('.\\icons\\png\\serbia.png')
                elif city.startswith('SC'):
                    flag = QtGui.QIcon('.\\icons\\png\\seychelles.png')
                elif city.startswith('SL'):
                    flag = QtGui.QIcon('.\\icons\\png\\sierra-leone.png')
                elif city.startswith('SG'):
                    flag = QtGui.QIcon('.\\icons\\png\\singapore.png')
                elif city.startswith('SK'):
                    flag = QtGui.QIcon('.\\icons\\png\\slovakia.png')
                elif city.startswith('SI'):
                    flag = QtGui.QIcon('.\\icons\\png\\slovenia.png')
                elif city.startswith('SB'):
                    flag = QtGui.QIcon('.\\icons\\png\\solomon-islands.png')
                elif city.startswith('SO'):
                    flag = QtGui.QIcon('.\\icons\\png\\somalia.png')
                elif city.startswith('ZA'):
                    flag = QtGui.QIcon('.\\icons\\png\\south-africa.png')
                elif city.startswith('SS'):
                    flag = QtGui.QIcon('.\\icons\\png\\south-sudan.png')
                elif city.startswith('ES'):
                    flag = QtGui.QIcon('.\\icons\\png\\spain.png')
                elif city.startswith('LK'):
                    flag = QtGui.QIcon('.\\icons\\png\\sri-lanka.png')
                elif city.startswith('SD'):
                    flag = QtGui.QIcon('.\\icons\\png\\sudan.png')
                elif city.startswith('SR'):
                    flag = QtGui.QIcon('.\\icons\\png\\suriname.png')
                elif city.startswith('SE'):
                    flag = QtGui.QIcon('.\\icons\\png\\sweden.png')
                elif city.startswith('CH'):
                    flag = QtGui.QIcon('.\\icons\\png\\switzerland.png')
                elif city.startswith('SY'):
                    flag = QtGui.QIcon('.\\icons\\png\\syria.png')
                elif city.startswith('TJ'):
                    flag = QtGui.QIcon('.\\icons\\png\\tajikistan.png')
                elif city.startswith('Th'):
                    flag = QtGui.QIcon('.\\icons\\png\\thailand.png')
                elif city.startswith('TL'):
                    flag = QtGui.QIcon('.\\icons\\png\\east-timor.png')
                elif city.startswith('TG'):
                    flag = QtGui.QIcon('.\\icons\\png\\togo.png')
                elif city.startswith('TK'):
                    flag = QtGui.QIcon('.\\icons\\png\\tokelau.png')
                elif city.startswith('TO'):
                    flag = QtGui.QIcon('.\\icons\\png\\tonga.png')
                elif city.startswith('TT'):
                    flag = QtGui.QIcon('.\\icons\\png\\trinidad-and-tobago.png')
                elif city.startswith('TN'):
                    flag = QtGui.QIcon('.\\icons\\png\\tunisia.png')
                elif city.startswith('TR'):
                    flag = QtGui.QIcon('.\\icons\\png\\turkey.png')
                elif city.startswith('TM'):
                    flag = QtGui.QIcon('.\\icons\\png\\turkmenistan.png')
                elif city.startswith('TV'):
                    flag = QtGui.QIcon('.\\icons\\png\\tuvalu.png')
                elif city.startswith('UG'):
                    flag = QtGui.QIcon('.\\icons\\png\\uganda.png')
                elif city.startswith('UA'):
                    flag = QtGui.QIcon('.\\icons\\png\\ukraine.png')
                elif city.startswith('AE'):
                    flag = QtGui.QIcon('.\\icons\\png\\united-arab-emirates.png')
                elif city.startswith('GB'):
                    flag = QtGui.QIcon('.\\icons\\png\\united-kingdom.png')
                elif city.startswith('TZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\tanzania.png')
                elif city.startswith('US'):
                    flag = QtGui.QIcon('.\\icons\\png\\united-states-of-america.png')
                elif city.startswith('UY'):
                    flag = QtGui.QIcon('.\\icons\\png\\uruguay.png')
                elif city.startswith('UZ'):
                    flag = QtGui.QIcon('.\\icons\\png\\uzbekistn.png')
                elif city.startswith('VU'):
                    flag = QtGui.QIcon('.\\icons\\png\\vanuatu.png')
                elif city.startswith('VE'):
                    flag = QtGui.QIcon('.\\icons\\png\\venezuela.png')
                elif city.startswith('VN'):
                    flag = QtGui.QIcon('.\\icons\\png\\vietnam.png')
                elif city.startswith('YE'):
                    flag = QtGui.QIcon('.\\icons\\png\\yemen.png')
                elif city.startswith('ZM'):
                    flag = QtGui.QIcon('.\\icons\\png\\zambia.png')
                elif city.startswith('ZW'):
                    flag = QtGui.QIcon('.\\icons\\png\\zimbabwe.png')
                else: flag = QtGui.QIcon('.\\icons\\TitleLogo.png')
                self.container_for_cities.appendRow(QtGui.QStandardItem(flag, city))

    def reset(self):
        self.cityLabel.hide()
        self.status_of_today.hide()
        self.temperature_now.hide()
        self.sunrise_time.hide()
        self.sunset_time.hide()
        self.feels_like_of_today.hide()
        self.wind_speed.hide()
        self.resetBtn.hide()
        self.day1.hide(),self.day2.hide(),self.day3.hide(),self.day4.hide(),self.day5.hide(),self.day6.hide(),self.day7.hide()
        self.day_status1.hide(),self.day_status2.hide(), self.day_status3.hide(), self.day_status4.hide(), self.day_status5.hide(), self.day_status6.hide(), self.day_status7.hide()
        self.day_mx_temp1.hide(),self.day_mx_temp2.hide(), self.day_mx_temp3.hide(), self.day_mx_temp4.hide(), self.day_mx_temp5.hide(), self.day_mx_temp6.hide(), self.day_mx_temp7.hide()
        self.day_mn_temp1.hide(),self.day_mn_temp2.hide(), self.day_mn_temp3.hide(), self.day_mn_temp4.hide(), self.day_mn_temp5.hide(), self.day_mn_temp6.hide(), self.day_mn_temp7.hide()
        self.search_lineEdit.clear()
        self.search_lineEdit.show()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())