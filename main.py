from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import statistics


# oblicza cene za metr kwadratowy z podanej listy
def get_flat_price_per_m2(flat):
	price = flat.find_element(By.CLASS_NAME, "css-1bq5zfe.e1uhhet014")
	meters = flat.find_elements(By.CLASS_NAME, "css-1q7zgjd.e1uhhet015")[1]

	# convert to number
	meters_convert = meters.text.replace(" m²", "")
	price_convert = price.text \
		.replace(" ", "") \
		.replace("zł", "").replace(',', "")

	# sprawdz czy uda sie przekonwertowac na zmiennoprzeciwnkowa
	try:
		meters_number = float(meters_convert)
		price_number = float(price_convert)
	except ValueError:
		return -1

	return round(float(price_number) / float(meters_number))


class Bot:
	all_avg_list = []
	page = 1

	def __init__(self):
		self.driver = webdriver.Chrome()

		self.driver.get("https://otodom.pl")
		sleep(2)

		self.driver.find_element(By.ID, "onetrust-accept-btn-handler") \
			.click()

		self.driver.find_element(By.XPATH, "//button[contains(text(), 'Wyszukaj')]") \
			.click()
		sleep(6)

		avg = 0
		while self.page < 10:

			# glowne dzialania
			self._mainLoop()

			if not len(self.all_avg_list):
				break

			# nastepna strona
			self.page += 1

			print(len(self.all_avg_list))
			avg = statistics.mean(self.all_avg_list)
			print("srednia po {} stronie: {} zł".format(self.page - 1, avg))

			# z powodu problematycznego dojscia do przycisku
			# dodajemy nastepna strone poprzez query param
			self.driver.get(self._set_query_param())
			sleep(5)

		print("Razem: {} zł/m2".format(round(avg)))

	def _mainLoop(self):

		# pobiera liste ogloszen
		flat_list = self.driver.find_elements(By.CLASS_NAME, "css-e87esy.e1uhhet017")

		# jesli cos poszlo nie tak zwraca blad
		if not flat_list:
			print("empty list")
			return

		# lista na cene/m2
		prices = []

		# przechodzi przez kazde ogloszenie
		for flat in flat_list:

			# cena na metr kwadratowy
			price_per_meter = get_flat_price_per_m2(flat)

			# jesli jest blad to pomija
			if price_per_meter == -1:
				break

			# dodanie do listy w tej funkcji
			prices.append(price_per_meter)

		# srednia cena za metr kwadradowy z aktualnej listy
		avg = sum(prices) / len(prices)

		# dodaj do listy srednich z kazdej strony
		self.all_avg_list.append(avg)

	def _set_query_param(self):

		# jesli ustawiona jest nastepna strona jako 2 to dodaje query param
		if self.page == 2:
			url = "{}?page={}".format(self.driver.current_url, str(self.page))
		else:
			url = self.driver.current_url[0:-1] + str(self.page)

		return url


if __name__ == '__main__':
	my_bot = Bot()

