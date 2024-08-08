from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup
from sys import exit

def getPercentagesFromGoogleMaps(URLs: pd.DataFrame, loadtime=10, waittime=3, optionals=False):
    """
    Returns the current and typical percentage values for each URL in the DataFrame.
    URLS: DataFrame with columns 'Link Name' and 'URL'
    loadtime: Maximum time to wait for the page to load (default: 10)
    waittime: Implicit wait time for Selenium (default: 5)
    optionals: Boolean to determine whether to use optional Chrome options (default: False)
    returns: list[list[str]]
    """

    CSSSELECTORCLASS = ".dpoVLd"
    
    # may be necessary sometimes
    chrome_options = webdriver.ChromeOptions()
    if optionals:
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    percentagesList = []

    # extract info from each URL
    for index, row in URLs.iterrows():
        linkName = row['Link Name']
        print("Attempting to locate information for", linkName)
        currentURL = row['URL']

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(currentURL)
        try:
            WebDriverWait(driver, loadtime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSSSELECTORCLASS))
            )

            # may be necessary sometimes 
            if optionals: driver.implicitly_wait(waittime)
            
            # normal Selenium methods did not work, so had to scrape just the HTML source instead
            foundCurrentPercentages = False
            parsedHTML = BeautifulSoup(driver.page_source, features="html.parser")
            for element in parsedHTML.select(CSSSELECTORCLASS):
                aria_label = element.get("aria-label")
                if aria_label and "Currently" in aria_label:
                    foundCurrentPercentages = True
                    aria_label = aria_label.split(" ")
                    percentagesList.append(["\"" + linkName + "\"", aria_label[1].replace('%', ''), aria_label[4].replace('%', '')])
            if not foundCurrentPercentages:
                percentagesList.append(["\"" + linkName + "\"", "", "", "", "Unable to find current percentages. Potentially closed or current occupancy is unavailable."])
            
            driver.quit()
        except TimeoutException as t:
            print("Error: Page timed out before the CSS selector could be found, potentially indicative of the element not being publicly displayed.")
            percentagesList.append(["\"" + linkName + "\"", "", "", "", "Page timed out before CSS selector was found. Potentially the occupancy values are not shown"])
        except Exception as e:
            print("Issue occurred for", linkName,"\n", e)
            percentagesList.append(["\"" + linkName + "\"", "", "", "", "An error occurred"])
            continue
    
    return percentagesList


def printToCSV(percentagesList, filename="ScrapedOccupancyInformation.csv"):
    """
    Formats and writes the content of percentagesList to a csv named by the filename parameter
    percentagesList: List[List[str]]
    filename: str (default:\"ScrapedOccupancyInformation.csv\")
    """

    columns = "\"Link Name\",\"Current\",\"Typical\",\"Ratio (%)\",\"Notes\"\n"
    rows = ""
    for row in percentagesList:
        if len(row) > 4: # when percentages could not be found
            rows += f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"
        else:
            rows += f"{row[0]},{row[1]},{row[2]},{round(int(row[1])/int(row[2])*100, 2)}\n"
    write = columns + rows
    with open(filename, "w") as f:
        f.write(write)
    print("Data was written to the file", filename)


if __name__=="__main__":
    # Settings Configurations
    OPTIONALS = False # options that can help with getting the info (False by default)
    CHECKVPN = True # whether to prompt VPN check (for bypassing scraping restrictions)
    WAITTIME = 3 # (in seconds) wait time used to get around potential scraper bot restrictions
    LOADTIME = 10 # (in seconds) the amount of time the program times out after waiting for page to load
    OUTPUTFILENAME = "ScrapedOccupancyInformation.csv" # the output filename
    INPUTFILENAME = "URL_CSV_Documents/TestURLs.csv" # the input filename

    # there are free functional VPNs out there if you don't have one, such as Privado
    if CHECKVPN and input("Are you currently running a VPN (Y/N)? ").lower() != 'y':
        if input("A VPN is recommended but not required. Continue (Y/N)? ").lower() != 'y':
            exit()

    URLDF = pd.read_csv(INPUTFILENAME)
    printToCSV(getPercentagesFromGoogleMaps(URLs=URLDF, loadtime=LOADTIME, waittime=WAITTIME, optionals=OPTIONALS), filename=OUTPUTFILENAME)