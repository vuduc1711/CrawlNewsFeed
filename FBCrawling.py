
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

import pandas as pd
import time


class log_in(object):

	def __init__(self,driver_path,user,pw):
		self.driver_path = driver_path
		self.user = user
		self.pw = pw


	def open_fb(self):

		driver = webdriver.Chrome(executable_path=self.driver_path,chrome_options=chrome_options)

		driver.get(
		    "https://www.facebook.com/login" 
		)
		

		# element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbutton"]')))

		print("Đã mở trang Login!")

		time.sleep(1)

		email_box = driver.find_element_by_xpath('//*[@id="email"]')
		pw_box = driver.find_element_by_xpath('//*[@id="pass"]')
		cf_btn =  driver.find_element_by_xpath('//*[@id="loginbutton"]')


		email_box.send_keys(self.user)
		pw_box.send_keys(self.pw)
		time.sleep(1)
		cf_btn.click()

		return driver

class crawl_info(object):
	def __init__(self,driver):
		self.driver=driver


	def crawl_feeling(self,post):
		# aria-label="Xem ai đã bày tỏ cảm xúc về tin này"
		# class="bp9cbjyn j83agx80 b3onmgus"
		
		# aria-label="Thích: 62 người"
		# aria-label="Yêu thích: 27 người"
		# aria-label="Thương thương: 2 người"
		# aria-label="Haha: 1 người"
		# aria-label="Wow: 13 người"
		# aria-label="Buồn: 13K người"
		# aria-label="Phẫn nộ: 1 người"

		# aria-label="Xem ai đã bày tỏ cảm xúc về tin này"

		fl_lis=dict()

		try:
			fl_lis['thich'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Thích')]").get_attribute('aria-label')
		except:
			fl_lis['thich'] = 0

		try:
			fl_lis['yeu'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Yêu thích')]").get_attribute('aria-label')
		except:
			fl_lis['yeu'] = 0

		try:
			fl_lis['thuong_thuong'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Thương thương')]").get_attribute('aria-label')
		except:
			fl_lis['thuong_thuong'] = 0

		try:
			fl_lis['haha'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Haha')]").get_attribute('aria-label')
		except:
			fl_lis['haha'] = 0

		try:	
			fl_lis['wow'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Wow')]").get_attribute('aria-label')
		except:
			fl_lis['wow'] = 0 

		try:
			fl_lis['buon'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Buồn')]").get_attribute('aria-label')
		except:
			fl_lis['buon'] = 0

		try:
			fl_lis['phan_no'] = post.find_element_by_xpath(".//*[contains(@aria-label,'Phẫn nộ')]").get_attribute('aria-label')
		except:
			fl_lis['phan_no'] = 0

		return fl_lis

	def crawl_cnt(self):
		# style="text-align: start;"
		# text() = "Xem thêm"
		# dir="auto"

		cnt_tag = self.driver.find_element_by_xpath('//div[contains(@dir,"auto")]')

		cnt = cnt_tag.text

		whl_cnt = cnt_tag.find_element_by_xpath('..').find_element_by_xpath('..')

		# whl_cnt = cnt_tag.parent

		return cnt, whl_cnt, cnt_tag


	def crawl_cnt_2(self,position):
		all_cnt = self.driver.find_elements_by_xpath('//div[contains(@data-pagelet,"FeedUnit")]')
		whl_cnt = self.driver.find_elements_by_xpath('//div[contains(@data-pagelet,"FeedUnit")]')[position]
		cnt_tag = whl_cnt.find_element_by_xpath('.//*[contains(@class,"ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a")]')

		cnt = cnt_tag.text

		return cnt, whl_cnt, cnt_tag, all_cnt


		# data-ad-comet-preview="message"
		# id="jsc_c_m4"
		# class="ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"
		# class="ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"
		# class="ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a"


	# def crawl_time_of_posting(self):
	# 	# style="text-align: start;"
	# 	# text() = "Xem thêm"
	
	# def scrolling(self):
	# 	# style="text-align: start;"
	# 	# text() = "Xem thêm"

	def crawl_name(self,post):
		# writer = post.find_element_by_xpath(".//*[contains(@id,'jsc_c')]/div/a/strong/span").text
		# writer = post.find_element_by_xpath(".//*[contains(@class,'qzhwtbm6 knvmm38d')]").text
		writer = post.find_element_by_xpath(".//*[contains(@class,'buofh1pr')]/div/div").text
		# post.find_element_by_xpath(".//*[contains(@class,'buofh1pr')]")
		return writer


	def crawl_time(self,post):
		# writer = post.find_element_by_xpath(".//*[contains(@id,'jsc_c')]/div/a/strong/span").text
		# writer = post.find_element_by_xpath(".//*[contains(@class,'qzhwtbm6 knvmm38d') and contains(text(),'phút')]").text
		try:
			time_pas = post.find_element_by_xpath(".//*[contains(text(),'phút')]").text
		except:
			try:
				time_pas = post.find_element_by_xpath(".//*[contains(text(),'giờ')]").text
			except:	
				try:		
					time_pas = post.find_element_by_xpath(".//*[contains(text(),'Vừa')]").text
				except:
					time_pas = post.find_element_by_xpath(".//*[contains(text(),'lúc')]").text
		return time_pas

	def see_more_button(self,post):
		# writer = post.find_element_by_xpath(".//*[contains(@id,'jsc_c')]/div/a/strong/span").text
		# writer = post.find_element_by_xpath(".//*[contains(@class,'qzhwtbm6 knvmm38d') and contains(text(),'phút')]").text
		time_pas = post.find_element_by_xpath(".//*[contains(text(),'Xem thêm')]")


		return time_pas



	def scrolling(self):
		# writer = post.find_element_by_xpath(".//*[contains(@id,'jsc_c')]/div/a/strong/span").text
		# writer = post.find_element_by_xpath(".//*[contains(@class,'qzhwtbm6 knvmm38d') and contains(text(),'phút')]").text
		# element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "tr_header")))
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		return None


		# //*[@id="jsc_c_3d"]/div/a/strong/span


	# Cần ấn xem thêm để xem hết nội dung.
	# FB không hiển thị hết các cảm xúc trong source code, chỉ hiển thị phần lớn.
	# Chưa lấy được tên writer
	# Vẫn lấy thừa feeling ở các post bên dưới