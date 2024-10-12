import time
import tkinter as tk
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from tkinter import simpledialog


def add_option_prefs(options): # options to remove the cookie popup to stop possible interference, stop chrome being opened, or minimize it if it does.
    prefs = {
        "profile.default_content_setting_values.cookies": 2  # 2 means block cookies
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-minimized")
    return options

# initialise tkinter
root = tk.Tk()
root.title("Shooting Star Search")
output_label = tk.Label(root, text = "Waiting for user input.")
output_label.pack(pady = 5)
root.update()

# If a user is running this script manually, prompt can be bypassed by commenting out input line and uncommenting string line modified to preference.
#location = "khazard"
location = simpledialog.askstring(title = "Input", prompt="Which star location would you like to search for? Multiple locations can be searched using ;. (e.g falador;port;varrock)").lower()
locations = location.split(sep = ";")
print(locations)
print(f"Searching for {locations} now.")

output_label = tk.Label(root, text = f"Searching for {locations} now.")
output_label.pack(pady = 5)
root.update()


# find users home directory, check chromedriver exists there
home_dir = os.path.expanduser("~")
chrome_filepath = os.path.join(home_dir, "BrowserDriver", "chromedriver.exe")
chrome_file_check = os.path.isfile(chrome_filepath)
firefox_filepath = os.path.join(home_dir, "BrowserDriver", "geckodriver.exe")
firefox_file_check = os.path.isfile(firefox_filepath)
edge_filepath = os.path.join(home_dir, "BrowserDriver", "msedgedriver.exe")
edge_file_check = os.path.isfile(edge_filepath)
window_duration = 15
file_folder_path = os.path.join(home_dir, "BrowserDriver")
download_links = "\nChrome: https://googlechromelabs.github.io/chrome-for-testing/#stable \nFirefox: https://github.com/mozilla/geckodriver/releases \nEdge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH\n"

# assigns variables and loads corresponding driver
if chrome_file_check:
    service = ChromeService(chrome_filepath)
    options = ChromeOptions()
    add_option_prefs(options)
    driver = webdriver.Chrome(service = service, options = options)
    filepath = chrome_filepath
elif firefox_file_check:
    service = FirefoxService(firefox_filepath)
    options = FirefoxOptions()
    add_option_prefs(options)
    driver = webdriver.Firefox(service = service, options = options)
    filepath = firefox_filepath
elif edge_file_check:
    service = EdgeService(edge_filepath)
    options = EdgeOptions()
    add_option_prefs(options)
    driver = webdriver.Edge(service = service, options = options)
    filepath = edge_filepath
else:
    output_label = tk.Label(root, text = f"Browser driver not found. Please download the latest version for your preferred browser from {download_links} and add to {file_folder_path}.")
    output_label.pack(pady = 5)
    print(f"chromedriver.exe is not found. Please download the latest version from {download_links} and add to {file_folder_path}.")
    root.update()
    time.sleep(window_duration)


if chrome_file_check or firefox_file_check or edge_file_check:
    driver.get("https://osrsportal.com/shooting-stars-tracker")
    time.sleep(2)
    root.withdraw()
    root.update()
    for location in locations:
        try:
            xpath_expression = f"//td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{location}')]"
            star_elements = driver.find_elements(By.XPATH, xpath_expression)
            for element in star_elements:
                # Get the parent <tr> of the found element
                row = element.find_element(By.XPATH, "./ancestor::tr")  # Adjust the XPath to your HTML structure
                
                # Extract all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")  # Assuming the data cells are <td> elements
                # Print the text of each cell
                increment = 0
                row_data = ["Last reported: ", "World: ", "Size: ", "Location: ", "Region: ", "Caller: "]
                for increment, cell in enumerate(cells):
                    if increment < len(row_data):
                        row_data[increment] += cell.text
                print(row_data)  # console print
                output_label = tk.Label(root, text=row_data)
                output_label.pack(pady= 5)
                root.update()
            if star_elements == []:
                print(f"No stars matching search parameter {location} have been reported.") # console print
                output_label = tk.Label(root, text=f"No stars matching search parameter {location} have been reported.")
                output_label.pack(pady= 5)
                root.update()
        except Exception as e:
            print("Error finding elements:", e)
    print(f"Search completed at {datetime.now()}.") # console print
    output_label = tk.Label(root, text = f"Search completed at {datetime.now()}. Window will stay open for {window_duration} seconds.")
    output_label.pack(pady = 5)
    root.deiconify()
    root.update()
    time.sleep(window_duration)
    driver.quit

#Todo list:
#Make executable