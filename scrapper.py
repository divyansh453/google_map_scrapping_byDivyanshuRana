#PROGRAM STARTS HERE
from time import sleep #To give time to browser so that data can be loaded properly, interpreter wait for some time due to it.
from bs4 import BeautifulSoup #Python Library to Parse HTML Content.
from selenium import webdriver #It is used for cross-browser testing.
import re # Regex library to match different patterns
import csv #Python Module for CSV files.

csv_file=open('google_map_scraper.csv','w') #File opens here if it exists then new data overwrites old one otherwise newfile is created.

csv_writer=csv.writer(csv_file) 
csv_writer.writerow(['Business Name','Rating','Reviews Count','Website','Phone Number','Email']) #headers of file

print("Scrapping.....") #Scrappping starts here.

driver = webdriver.Chrome(r"C:\chromedriver_win32\chromedriver.exe") #Using Chrome Browser driver which is stored at the path written inside " "
driver.get("https://www.google.com/maps/search/software+companies/@13.0219722,77.5891393,17z") #To get content from browser
sleep(3) #To give time so that browser can be open and then selenium will scrap the website

SCROLL_PAUSE_TIME = 5 #pause time to stop scrolling for a specific timing
last_height = driver.execute_script("return document.body.scrollHeight") # script of last element is stored in it.
number = 0
while True:
    number = number+1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME) #here program stops for a specific time after which selenium scrolls the webpage
    new_height = driver.execute_script("return document.body.scrollHeight") #new height or the script of current item is assigned to new_height
    if new_height == last_height: #when current item is last item then loop will break
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, "lxml") #Here ,BeautifulSoup will parse the html content ,which we get using selenium

companies=soup.find_all('div',class_='bfdHYd') #here the data of all software companies is stored as elements in a list

for company in companies:
    company_name=company.find("div",class_="qBF1Pd fontHeadlineSmall").text #to get the name of business by using its tag and class

    # Here try except is used because ratings of some companies is not available and it can cause error.
    try:
        ratings=company.find("span",class_="MW4etd").text 
        review_count=company.find("span",class_="UY7F9").text.split(')')[0][1:] #review count is extracted using split methof and indexing
    except:
        ratings=" "
        review_count="No Reviews yet" #if reviews are not available for any company then these values will be assigned to ratings and review_count
    try:
        website=company.find("a",class_="lcr4fd S9kvJb")['href'] #website of some companies is not available that's why I use try and except method here
        #link of website is inside Anchor tag where attribute is href. 
    except:
        website=" "  #If there is no website for any company then empty string will be assigned to website
    
     #phone_number is written at the last of description of company so I reverse the string and then pick last 20 characters using indexing.
     #There were also some spaces in between the digits that's why i take 20 characters and then again reverse it
    Phone_number=company.find("div",class_="Z8fK3b").text[::-1][0:20][::-1]
    phone=re.findall(r'[0-9]+',Phone_number) # Here I use the regex to extract numeric characters which are stored in a list
    phone_number=""
    for number in phone:
        phone_number+=number #Here all the elements of list are concatenated
    if len(phone_number)!=10 and len(phone_number)!=11: #The length of Indian Phone Number is 10 and sometimes some people also attach 0 so it may be 11 sometimes.
        phone_number=" " #If length of the string received after concatentaion id not 11 or 10 then that string can't be a  Indian phone number.
    csv_writer.writerow([company_name,ratings,review_count,website,phone_number,'']) # Data is written to a csv file.As Email is not available for any company in description that's why empty string is assigned to its column


print("File Created.") #Message to know the completion of Process.
csv_file.close() #File is closed.

#END OF PROGRAM