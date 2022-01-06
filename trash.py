# self.driver.find_element_by_id("downshift-0-label")\
#     .click()
# sleep(2)

# self.driver.find_element(By.ID, "downshift-0-input")\
#     .send_keys("value", "Warszawa")

# self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
#     .send_keys(username)
# self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
#     .send_keys(pw)
# self.driver.find_element_by_xpath('//button[@type="submit"]')\
#     .click()
# sleep(4)
# self.driver.find_element_by_xpath("//button[contains(text(), 'Wyszukaj')]")\
#     .click()
# sleep(2)
# self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
#     .click()
# sleep(3)

def get_unfollowers(self):
	self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)) \
		.click()
	sleep(2)
	self.driver.find_element_by_xpath("//a[contains(@href,'/following')]") \
		.click()
	following = self._get_names()
	self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]") \
		.click()
	followers = self._get_names()
	not_following_back = [user for user in following if user not in followers]
	counter = 0
	for follow in not_following_back:
		counter += 1
		print(counter, follow)


def _get_names(self):
	sleep(2)
	scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
	last_ht, ht = 0, 1
	while last_ht != ht:
		last_ht = ht
		sleep(1)
		ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            return arguments[0].scrollHeight;
            """, scroll_box)
	links = scroll_box.find_elements_by_tag_name('a')
	names = [name.text for name in links if name.text != '']
	# close button
	self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button") \
		.click()
	return names