from bs4 import BeautifulSoup
import requests
from subprocess import call
import time
from progress.spinner import Spinner
from progress.bar import Bar
import re
from webbrowser import open_new_tab


def clear():
    call("clear", shell=True)
    file = open("splash.txt", "r")
    for line in file:
        print(line.strip("\n")+"\033[1;36;40m")
    print("\u001b[37m")
clear()

def VALUATIONS(page_link):
    global page_content
    # Setup VOA Page
    inc = False
    page_response = requests.get(page_link, timeout=5)
    global page_content
    page_content = BeautifulSoup(page_response.content, "html.parser")
    try:
        recent_val = page_content.find_all("td")[1].text
        recent_val = recent_val.strip("£")
        recent_val = int(recent_val.replace(",", ""))
        previous_val = page_content.find_all("td")[6].text
        previous_val = previous_val.replace(",", "")
        previous_val = int(previous_val.strip('£'))
    except:
        recent_val = 1
        previous_val = 2
    #print(recent_val)
    #print(previous_val)
    if recent_val > previous_val:
        inc = True
    return inc
    
def REQUEST():
    hrefs = []
    postcode = input("Postcode: ")
    print("_" * 20)
    global page_content
    # Setup VOA Page
    page_link = 'https://www.tax.service.gov.uk/business-rates-find/list-valuations?searchBy=Postcode&postCodeQuery='+postcode+'&streetQuery=&townQuery=&primaryCriteria=ADDRESS&baRef=&number=&street=&town=&postCode=&billingAuthority=&specialCategoryCode=&descriptionCode=&from=&to=&listYear=2017'
    page_response = requests.get(page_link, timeout=5)
    global page_content
    page_content = BeautifulSoup(page_response.content, "html.parser")
    for link in page_content.find_all('a', href=True):
        href_temp = "https://www.tax.service.gov.uk"+link["href"]
        hrefs.append(href_temp.replace("summary", "other-properties"))
        
    #Find all addresses
    address = []
    try:
        with Bar('Processing Addresses', max=25) as bar:
            for i in range(9, 34):
                refs = page_content.find_all("a")[i].text
                address.append(refs)
                bar.next()
    except:
        print("WARNING: Few Entries")
        
    try:
        #Find 'Current ratable value', (CRV)
        CRV = []
        with Bar('Processing CRV', max=25) as bar:
            for i in range(2, 27):
                refs = page_content.find_all("span")[5*i + 3].text
                CRV.append(refs)
                bar.next()
    except:
        pass
    print_out = ""
    try:
        with Bar('Evaluating Data', max=24) as bar:
            if len(address) > 0:
                for i in range(len(address) - 1):
                    if VALUATIONS(hrefs[i+9]) == True:
                        print_out = print_out + ("\u001b[31m"+str(i)+") "+address[i]+"  ||  "+CRV[i]+"  ||  "+hrefs[i+9]+"\u001b[37m \n")
                    else:
                        print_out = print_out + (str(i)+") "+address[i]+"  ||  "+CRV[i]+"  ||  "+hrefs[i+9]+"\n")    
                    bar.next()
            else:
                print("No Entries...")
    except:
        pass
    print("")
    print(print_out)
    usr = input("Search: ")
    while usr != "":
        open_new_tab("https://www.google.com/search?q="+address[int(usr)]+"&rlz=1CAEAQE_enGB844&oq="+address[int(usr)]+"&aqs=chrome.0.69i59j46l5.1592j1j9&sourceid=chrome&ie=UTF-8")
        usr = input("Search: ")
    clear()
    REQUEST()

def check_licence(key, epoch):
    tm = epoch
    new_key = key
    if int(key, 16) % 167 != 0 or time.time() > float(epoch) + 2.628e+6:
        while new_key == key:
            print("INVALID LICENCE KEY\nTo get a new key, contact hpdharrison@gmail.com")
            new_key = input("KEY: ")
            tm = time.time()
    file = open("key.txt", "w")
    file.write(new_key+"\n"+str(tm))
    file.close()
    clear()
    REQUEST()
    
content = []    
file = open("key.txt", "r")
for line in file:
    content.append(line.strip("\n"))
check_licence(content[0], content[1])
