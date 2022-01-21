import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests
import configparser
import phonenumbers
from phonenumbers import timezone, carrier, geocoder
from pyowm import *

config = configparser.ConfigParser()
config.read("config.ini")
config_api = config["API"]
api_key = config_api["api_key"]
api_key_weather = config_api["api_key_weather"]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(302, 295)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.submit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.submit_btn.setGeometry(QtCore.QRect(100, 80, 101, 31))
        self.submit_btn.setObjectName("submit_btn")
        self.radioIP = QtWidgets.QRadioButton(self.centralwidget)
        self.radioIP.setGeometry(QtCore.QRect(20, 50, 89, 20))
        self.radioIP.setObjectName("radioIP")
        self.radioNumber = QtWidgets.QRadioButton(self.centralwidget)
        self.radioNumber.setGeometry(QtCore.QRect(120, 50, 101, 20))
        self.radioNumber.setObjectName("radioNumber")
        self.ipnumber = QtWidgets.QLineEdit(self.centralwidget)
        self.ipnumber.setGeometry(QtCore.QRect(20, 10, 261, 31))
        self.ipnumber.setObjectName("ipnumber")
        self.countryLab = QtWidgets.QLabel(self.centralwidget)
        self.countryLab.setGeometry(QtCore.QRect(10, 130, 121, 16))
        self.countryLab.setObjectName("countryLab")
        self.countryCodeLab = QtWidgets.QLabel(self.centralwidget)
        self.countryCodeLab.setGeometry(QtCore.QRect(10, 160, 121, 16))
        self.countryCodeLab.setObjectName("countryCodeLab")
        self.cityLab = QtWidgets.QLabel(self.centralwidget)
        self.cityLab.setGeometry(QtCore.QRect(10, 190, 121, 16))
        self.cityLab.setObjectName("cityLab")
        self.timezoneLab = QtWidgets.QLabel(self.centralwidget)
        self.timezoneLab.setGeometry(QtCore.QRect(10, 220, 121, 16))
        self.timezoneLab.setObjectName("timezoneLab")
        self.providerLab = QtWidgets.QLabel(self.centralwidget)
        self.providerLab.setGeometry(QtCore.QRect(10, 250, 121, 16))
        self.providerLab.setObjectName("providerLab")
        self.latitudeLab = QtWidgets.QLabel(self.centralwidget)
        self.latitudeLab.setGeometry(QtCore.QRect(150, 130, 121, 16))
        self.latitudeLab.setObjectName("latitudeLab")
        self.longitudeLab = QtWidgets.QLabel(self.centralwidget)
        self.longitudeLab.setGeometry(QtCore.QRect(150, 160, 121, 16))
        self.longitudeLab.setObjectName("longitudeLab")
        self.operatorLab = QtWidgets.QLabel(self.centralwidget)
        self.operatorLab.setGeometry(QtCore.QRect(150, 190, 121, 16))
        self.operatorLab.setObjectName("operatorLab")
        self.weather_btn = QtWidgets.QPushButton(self.centralwidget)
        self.weather_btn.setGeometry(QtCore.QRect(150, 230, 101, 31))
        self.weather_btn.setObjectName("weather_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tracksploit GUI"))
        self.submit_btn.setText(_translate("MainWindow", "Execute"))
        self.radioIP.setText(_translate("MainWindow", "IP Adress"))
        self.radioNumber.setText(_translate("MainWindow", "Phone Number"))
        self.countryLab.setText(_translate("MainWindow", "Country: "))
        self.countryCodeLab.setText(_translate("MainWindow", "Country Code: "))
        self.cityLab.setText(_translate("MainWindow", "City: "))
        self.timezoneLab.setText(_translate("MainWindow", "Timezone: "))
        self.providerLab.setText(_translate("MainWindow", "Provider: "))
        self.latitudeLab.setText(_translate("MainWindow", "Latitude: "))
        self.longitudeLab.setText(_translate("MainWindow", "Longitude: "))
        self.operatorLab.setText(_translate("MainWindow", "Operator: "))
        self.weather_btn.setText(_translate("MainWindow", "Show Weather"))

    def get_info(self):
        ip = self.ipnumber.text()
        number = self.ipnumber.text()

        if self.ipnumber.text() == "":
            msg_error_empty = QMessageBox()
            msg_error_empty.setIcon(QMessageBox.Critical)
            msg_error_empty.setText("Empty Input!")
            msg_error_empty.setWindowTitle("Error")
            show = msg_error_empty.exec_()
        else:
            if self.radioIP.isChecked():
                try:
                    data_ip = requests.get(f"http://ip-api.com/json/{ip}")
                    status_ip = data_ip.json()["status"]
                    country_ip = data_ip.json()["country"]
                    langcode_ip = data_ip.json()["countryCode"]
                    city_ip = data_ip.json()["city"]
                    timezone_ip = data_ip.json()["timezone"]
                    provider_ip = data_ip.json()["isp"]
                    latitude_ip = data_ip.json()["lat"]
                    longitude_ip = data_ip.json()["lon"]

                    self.countryLab.setText(f"Country: {country_ip}")
                    self.countryCodeLab.setText(f"Country Code: {langcode_ip}")
                    self.cityLab.setText(f"City: {city_ip}")
                    self.timezoneLab.setText(f"Timezone: {timezone_ip}")
                    self.providerLab.setText(f"Provider: {provider_ip}")
                    self.latitudeLab.setText(f"Latitude: {latitude_ip}")
                    self.longitudeLab.setText(f"Longitude: {longitude_ip}")
                    self.operatorLab.setText("Operator: ")
                except KeyError:
                    msg_error_ip = QMessageBox()
                    msg_error_ip.setIcon(QMessageBox.Critical)
                    msg_error_ip.setText("Invalid IP Adress!")
                    msg_error_ip.setWindowTitle("Error")
                    show = msg_error_ip.exec_()
            elif self.radioNumber.isChecked():
                try:
                    number_details = phonenumbers.parse(number, None)
                    number_timezone = timezone.time_zones_for_number(number_details)
                    number_isvalid = phonenumbers.is_valid_number(number_details)
                    number_operator = carrier.name_for_number(number_details, "en")
                    number_country = geocoder.country_name_for_number(number_details, "en")

                    data_number = requests.get(f"https://htmlweb.ru/geo/api.php?json&telcod={number}&api_key={api_key}")
                    country_data = data_number.json()["country"]
                    countrycode_number = country_data["id"]
                    location_data = data_number.json()["capital"]
                    city_number = location_data["english"]
                    latitude_number = location_data["latitude"]
                    longitude_number = location_data["longitude"]

                    if number_isvalid == False:
                        msg_error_number = QMessageBox()
                        msg_error_number.setIcon(QMessageBox.Critical)
                        msg_error_number.setText("Invalid Phone Number!")
                        msg_error_number.setWindowTitle("Error")
                        show = msg_error_number.exec_()
                    else:
                        try:
                            self.countryLab.setText(f"Country: {number_country}")
                            self.countryCodeLab.setText(f"Country Code: {countrycode_number}")
                            self.cityLab.setText(f"City: {city_number}")
                            self.timezoneLab.setText(f"Timezone: {number_timezone}")
                            self.latitudeLab.setText(f"Latitude: {latitude_number}")
                            self.longitudeLab.setText(f"Longitude: {longitude_number}")
                            self.operatorLab.setText(f"Operator: {number_operator}")
                            self.providerLab.setText("Provider: ")
                        except KeyError:
                            msg_error_limit = QMessageBox()
                            msg_error_limit.setIcon(QMessageBox.Critical)
                            msg_error_limit.setText("Unexpected error. API request limit (20 requests per day) may have been reached")
                            msg_error_limit.setWindowTitle("Error")
                            show = msg_error_mode.exec_()
                except phonenumbers.phonenumberutil.NumberParseException:
                    msg_error_notnumber = QMessageBox()
                    msg_error_notnumber.setIcon(QMessageBox.Critical)
                    msg_error_notnumber.setText("The number you entered did not seem to be a phone number!")
                    msg_error_notnumber.setWindowTitle("Error")
                    show = msg_error_notnumber.exec_()
                except KeyError:
                    pass

                
            else:
                msg_error_mode = QMessageBox()
                msg_error_mode.setIcon(QMessageBox.Critical)
                msg_error_mode.setText("Please, specify track mode")
                msg_error_mode.setWindowTitle("Error")
                show = msg_error_mode.exec_()

    def get_weather(self):
        if self.cityLab.text() == "City: ":
            msg_error_nocity = QMessageBox()
            msg_error_nocity.setIcon(QMessageBox.Critical)
            msg_error_nocity.setText("First we need to get info!")
            msg_error_nocity.setWindowTitle("Error")
            show = msg_error_nocity.exec_()
        else:
            owm = OWM("dca5010d96c210609510a0ce4327f4dd")
            city_from_label = self.cityLab.text().split(': ', 1)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city_from_label[1])
            w = observation.weather

            msg_weather = QMessageBox()
            msg_weather.setIcon(QMessageBox.Information)
            msg_weather.setText(f"Status: {w.detailed_status}\nHumidity: {w.humidity} g/m³\nTemperature: {round(w.temperature('celsius')['temp'], 1)} ℃\nWind Speed: {w.wind()['speed']} m/s               ")
            msg_weather.setWindowTitle(f"Weather in {city_from_label[1]}")
            show_ = msg_weather.exec_()

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
msg_error = QMessageBox().setWindowTitle("Error")
MainWindow.show()

ui.submit_btn.clicked.connect(ui.get_info)
ui.weather_btn.clicked.connect(ui.get_weather)

sys.exit(app.exec_())