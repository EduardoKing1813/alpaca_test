import colorama
from colorama import Fore, Style
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

PATH_TO_DRIVER = "C:\Program Files (x86)/chromedriver.exe"



class TestCase:
    
    def __init__(self, name : str, result : bool):
        self.name = name
        self.result = result
        
    def __repr__(self):
        if self.result:
            return f'{self.name} - {Fore.GREEN}{self.result}{Style.RESET_ALL}\n'
        else:
            return f'{self.name} - {Fore.RED}{self.result}{Style.RESET_ALL}\n'
            
        

class TestReport:
    
    def __init__(self, name):
        self.name = name
        self.test_cases = []
    
    def add_case(self, testcase : TestCase):
        self.test_cases.append(testcase)
        
    
    def __repr__(self):
        return  self.name + '\n' + ''.join([test.__repr__() for test in self.test_cases]) + '\n'

        


def test_A() -> TestReport:
    report = TestReport('Test A')
    
    #Setup driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(PATH_TO_DRIVER, options=options)
    
    #Get to google.com
    driver.get("https://google.com")
    
    #Accept cookies
    accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="L2AGLb"]/div')
    accept_cookies_button.click()
    
    QUERY = "CyberAlpaca"
    TARGET = "www.cyberalpaca.com"
    
    #Type our query to search bar
    search_bar = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    search_bar.send_keys(QUERY)
    
    #Click search button
    search_button = driver.find_element(by=By.XPATH, value= '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
    search_button.click()
    
    
    #Search for results
    n_pages = 2
    links = []
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + QUERY + "&start=" +      str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            #Get link
            link = h.a.get('href')
            
            #Format link
            link = link.replace('https://', '')
            link = link.replace('http://', '')
            link = link[:-1] if link.endswith('/') else link
            
            #Add link to results
            links.append(link)

    #Quit browser
    driver.close()

    result = TARGET in links
    report.add_case( TestCase('www.cyberalpaca.com in search results', result) )
    
    return report

    

def test_B() -> TestReport:
    report = TestReport('Test B')
    
    #Setup driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(PATH_TO_DRIVER, options=options)
    
    driver.get("https://www.cyberalpaca.com")
    
    services_tab = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/a[3]')
    services_tab.click()
    
    try:
        our_services_label = driver.find_element(by=By.XPATH, value='//*[@id="root"]/main/section[1]/div[1]/div/div[1]/h1')
        result = True
    except NoSuchElementException:
        result = False
    finally:
        report.add_case(TestCase('“Our Services” is displayed at the top', result))
    
    
    #Sqish logo test
    
    #Must be
    
    try:
        autogui_testing_logo_path = '/html/body/div/main/section[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/a'
        autogui_sqish = driver.find_element(by=By.XPATH, value=autogui_testing_logo_path)
        result = True
    except NoSuchElementException:
        result = False
    finally:
        report.add_case(TestCase('Squish logo is shown for autogui testing', result))
        
    
    try:
        embedded_testing_logo_path = '/html/body/div/main/section[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/a'
        embedded_sqish = driver.find_element(by=By.XPATH, value=embedded_testing_logo_path)
        result = True
    except NoSuchElementException:
        result = False
    finally:
        report.add_case(TestCase('Squish logo is shown for embedded testing', result))
    
    #I don't know how to test if logo is not shown, sorry(
    
    
    return report


def run_tests(tests : list) -> None:
    reports = []
    
    for test in tests:
        reports.append(test())

    print(
        '''
        ########
        #REPORT#
        ########
        '''
    )
        
    for report in reports:
        print(report)


def main():
    tests = [test_A, test_B]
    
    run_tests(tests)
    
    
    
if __name__ == '__main__':
    colorama.init()
    main()