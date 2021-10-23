
from selenium import webdriver
import time
import csv
#executeable_path shouldn't be, there's a way to configure your path to have it work(current geckodriver is needed)
#for the sake of doing this quick I used this. You just get deprecated warnings. See link below.
#using Firefox browser
browser = webdriver.Firefox(executable_path=r'D:\coding\pythonScraping\geckodriver-v0.30.0-win64\geckodriver.exe')

#https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path
browser.get('https://www.running2win.com/')
def login():
    #click log in LINK(should be a button)
    browser.find_element_by_link_text("LOG IN").click()

    #input username and password
    user = 'XXXX'
    passw = 'XXX'
    userInput = browser.find_element_by_id('txtUsername')
    passInput = browser.find_element_by_id('txtPassword')
    userInput.send_keys(user)
    passInput.send_keys(passw)
    #Calling the submit() method on any element will have the same result as clicking the Submit button for the form that element is in.
    passInput.submit()

    #some web data takes loading time. Hence the sleeps sprinkled in
    time.sleep(4)
    browser.find_element_by_class_name('r2w-logout-right').click()
    browser.find_element_by_class_name('mar-t10').click()
    time.sleep(4)

    #dropdown select
    el = browser.find_element_by_id('dboYears')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == "2019 - 338 wo's - 1,867.90 miles":
            option.click() # select() in earlier versions of webdriver
            break

    browser.find_element_by_id('btnViewYear').click()
    time.sleep(10)
    allTables = browser.find_elements_by_class_name('encapsule')
    extractData(allTables)

def extractData(tables):
    f = open('D:\coding\pythonScraping\Oney2019runs.csv', 'w', newline='')
    writer = csv.writer(f)

    for t in tables[1:-1]:
        info = []
        p= t.find_element_by_tag_name("tbody")
        p2= p.find_element_by_tag_name("tr")
        p3= p2.find_element_by_tag_name("td")
        p4= p3.find_elements_by_class_name("custom-table")[1]
        p5 = p4.find_element_by_tag_name("tbody")
        #-------------Distance Miles in time [pace]
        p6= p5.find_elements_by_tag_name("tr")[1]
        p7 = p6.find_elements_by_tag_name("td")[1]
        #p8 = p7.find_element_by_tag_name("strong")
        data = p7.find_element_by_tag_name("span")
        info.append(data.text)
        #-------------Comments
        c1 = p5.find_elements_by_tag_name("tr")[2]
        comment = c1.find_elements_by_tag_name("td")[1]
        info.append(comment.text)
        #-------------Date
        d1 = p3.find_elements_by_class_name("custom-table")[0]
        d2 = d1.find_elements_by_tag_name("td")[0]
        #d3 = d1.find_elements_by_tag_name("td")[0]
        if d2.text == "  Workout marked PRIVATE  [Owner Viewing]":
            d2 = d1.find_elements_by_tag_name("td")[1]
            
        info.append(d2.text)

        writer.writerow(info)

    f.close()
    return 0

#start script
login()