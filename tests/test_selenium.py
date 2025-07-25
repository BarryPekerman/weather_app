from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(options=options)

driver.get("http://localhost:80")

title = driver.title

driver.implicitly.wait(0.5)

driver.quit()
