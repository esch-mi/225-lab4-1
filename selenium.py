from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest


class TestContactsApp(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_page_loads(self):
        driver = self.driver
        driver.get("http://10.48.228.102")
        h2_text = driver.find_element(By.TAG_NAME, "h2").text
        self.assertEqual("Add Contact", h2_text, "The <h2> tag does not contain 'Add Contact'")

    def test_add_contact(self):
        driver = self.driver
        driver.get("http://10.48.228.102")
        driver.find_element(By.ID, "name").send_keys("Test User")
        driver.find_element(By.ID, "phone").send_keys("555-1234")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("Contact added successfully.", driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
