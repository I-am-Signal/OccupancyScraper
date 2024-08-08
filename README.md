# Occupancy-Scraper
A Python script for scraping current occupation information from the URLs specified from freely available Google Maps data. This information is then compiled into a single CSV formatted document for easy viewing and use.

## Prerequisites
An installation of Google Chrome is required for this program. You can download Chrome directly from [Google](www.google.com/chrome/dr/download/).

This program requires the use of a Python interpreter. You can download one directly from [python.org](https://www.python.org/downloads/) (ensure you install version 3.9 or newer). Depending on your installation, you may have access to the `pip` tool that will allow you to install these libraries. If you do not have pip installed, please follow a [tutorial](https://www.youtube.com/watch?v=81SHyuNLMOY). 

Once you have a functioning interpreter, you must have the Python libraries Beautiful Soup 4 (bs4), Pandas, and Selenium installed. To begin getting your Python environment set up for this program, you must open the command prompt. Assuming your version of Python has the `pip` tool installed, you can simply type `pip install bs4, pandas, selenium` and press the `Enter` key to install these libraries.

The program can now be ran with default settings at this point. 

## Configuration
By default, this program has the following settings for the configuration variables in the `OccupancyScraper.py` file:
```
OPTIONALS = False
CHECKVPN = True
WAITTIME = 3
LOADTIME = 10
OUTPUTFILENAME = "ScrapedOccupancyInformation.csv"
INPUTFILENAME = "URL_CSV_Documents/TestURLs.csv"
```

* `OPTIONALS`: this variable controls a few settings that may improve the program's ability to access the desired information. By default it is set to `False`.
* `CHECKVPN`: this variable controls the initial VPN check message prompt. It is recommended that you are using a VPN when running this program, however it is not required. You can turn off the initial VPN check message prompt by changing the value of this variable from the default `True` to `False`.
* `WAITTIME`: this variable controls the arbitrary wait time (in seconds) used to get around scraping bot blockers when they are present. By default, this variable is set to the value `3` for 3 seconds.
* `LOADTIME`: this variable controls the amount of time (in seconds) the program times out after waiting for the page to load. By default, this variable is set to the value `10` for 10 seconds.
* `OUTPUTFILENAME`: this variable controls the filename of the output file. By default, this variable is set to the value is `ScrapedOccupancyInformation.csv`.
* `INPUTFILENAME`: this variable controls the filename of the input file that this program will search for. If you wish to change where the program sources its input URLs from, you can change the value to the desired csv file (such as the template file `URLs.csv`). By default, this variable is to the value `URL_CSV_Documents/NewPizzaIndexURLs.csv`.

## Run the Program
Open the command prompt and navigate to the folder containing this document (cd filepath-to-directory/Occupancy-Scraper on Windows). To run the program, type `python OccupancyScraper.py` and press the `Enter` key.

## Provided CSV Files
* `NewPizzaIndex.csv`
    * URLs of gay bars local to government offices around Washington DC. Data about these bars can be used as essentially a new version of the popularized [Pizza Index](https://knowyourmeme.com/memes/pizza-meter-pentagon-pizza-orders). This version uses the knowledge that a significant portion of government workers are of the LGBT community. If there is a reduction in occupancy on a typically highly occupied night, this may or may not be indicative of potential for international government action. The New Pizza Index was the original intent of writing this program, but I realized that this program can be used for any set of Google Maps URLs and may be of use to other people.
* `TestURLs.csv`
    * URLs of a few places (including both 24/7 and limited hour locations) that can be used in testing the program or for demonstration purposes. This is currently the default value for the variable `INPUTFILENAME` in the `OccupancyScraper.py` file and can be changed to the filename you wish to search using.
* `URLs.csv`
    * This file is a template you can use to research occupancy information about places you are interested in.

## Choice of Scraping Libraries
This program uses the `Selenium` library as opposed to the `Requests` library because Google dynamically loads the displayed HTML. `Selenium` acts like a normal user and opens a window (specifically Chrome in this program) to scrape information, allowing the page to be fully loaded before scraping. `Requests` only provides the initial state of the HTML from the request.

Additionally, `Selenium`'s usual methods for finding elements does not work for this program, as Google Maps refuses the request. Instead, this program scrapes the loaded page's HTML source code and from there does an element search using `Beautiful Soup 4` as an HTML parser.