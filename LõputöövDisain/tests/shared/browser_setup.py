from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions

def get_browsers():
    browsers = {
        "Chrome": {
            "driver": webdriver.Chrome,
            "options": Options()
        },
        "Firefox": {
            "driver": webdriver.Firefox,
            "options": FirefoxOptions()
        },
#        "Edge": {
#           "driver": webdriver.Edge,
#            "options": EdgeOptions()
#        }
    }

    # Chrome 
    browsers["Chrome"]["options"].add_argument("--ignore-certificate-errors")
    browsers["Chrome"]["options"].add_argument("--disable-logging")
    browsers["Chrome"]["options"].add_argument("--log-level=3")

    # Firefox
    browsers["Firefox"]["options"].add_argument("--ignore-certificate-errors")
    browsers["Firefox"]["options"].add_argument("--disable-logging")
    browsers["Firefox"]["options"].add_argument("--log-level=3")

    # Edge
  # browsers["Edge"]["options"].add_argument("--ignore-certificate-errors")
  # browsers["Edge"]["options"].add_argument("--disable-logging")
  # browsers["Edge"]["options"].add_argument("--log-level=3")
  # browsers["Edge"]["options"].add_argument("--disable-features=EdgeIdentitySignin")
  # browsers["Edge"]["options"].add_argument("--inprivate")
    
   
    return browsers
