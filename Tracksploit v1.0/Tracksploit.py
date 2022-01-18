import requests
import configparser
from colorama import init, Fore, Back, Style
import phonenumbers
from phonenumbers import timezone, carrier, geocoder

config = configparser.ConfigParser()
config.read("config.ini")
config_api = config["API"]
api_key = config_api["api_key"]

print(Fore.CYAN + "Welcome to tracksploit! Developer Discord: Flumy#0802")
print()
print()
print(Fore.RED + "Choose an action:")
print(Fore.GREEN + "A: Get info from number")
print(Fore.GREEN + "B: Get info from ip adress")
print(Fore.GREEN + "C: Exit")
print()

choice = input(Fore.YELLOW + "Enter your choice: ")

def get_info_number():
	print()
	print(Fore.RED + "WARNING: If an error occurs while executing the program, the API request limit (20 requests per day) may have been reached")
	number = input(Fore.YELLOW + "Enter any number with country code (example: +7925*******): ")

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

	print()
	print(Fore.WHITE + f"Results for {number}:")
	print(number_details)
	print(f"Is number valid: {number_isvalid}")
	print()
	print(Fore.GREEN + f"Timezone: {number_timezone}")
	print(f"Operator: {number_operator}")
	print(f"Country: {number_country}")
	print(f"Country Code: {countrycode_number}")
	print(f"City: {city_number}")
	print(f"Latitude: {latitude_number}")
	print(f"Longitude: {longitude_number}")

def get_info_ip():
	try:	
		print()
		ip = input(Fore.YELLOW + "Enter any ip adress: ")

		data_ip = requests.get(f"http://ip-api.com/json/{ip}")
		status_ip = data_ip.json()["status"]
		country_ip = data_ip.json()["country"]
		langcode_ip = data_ip.json()["countryCode"]
		city_ip = data_ip.json()["city"]
		timezone_ip = data_ip.json()["timezone"]
		provider_ip = data_ip.json()["isp"]
		latitude_ip = data_ip.json()["lat"]
		longitude_ip = data_ip.json()["lon"]

		print()
		print(Fore.WHITE + f"Results for {ip}:")
		print(Fore.GREEN + f"Status: {status_ip}")
		print(Fore.GREEN + f"Country: {country_ip}")
		print(Fore.GREEN + f"Country Code: {langcode_ip}")
		print(Fore.GREEN + f"City: {city_ip}")
		print(Fore.GREEN + f"Timezone: {timezone_ip}")
		print(Fore.GREEN + f"Provider: {provider_ip}")
		print(Fore.GREEN + f"Latitude: {latitude_ip}")
		print(Fore.GREEN + f"Longitude: {longitude_ip}")
	except KeyError:
		print()
		print(Fore.WHITE + f"Results for {ip}:")
		print(Fore.RED + f"Status: {status_ip}")
		print(Fore.RED + "Reason: Invalid IP Adress!")

if choice == "A":
	get_info_number()
elif choice == "B":
	get_info_ip()
else:
	exit()