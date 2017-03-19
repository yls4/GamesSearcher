from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import urllib2
import time
import csv
import sys
import os
from pip._vendor.distlib.compat import raw_input
from _io import open
from locale import str

def main():
    if os.path.isfile("list.txt") == False:
        print "list.txt not found"
        sys.exit()
        
    print "These games will be used:"
    file = open("list.txt", 'r')
    for line in file:
        print line,
        if 'str' in line:
            break
    raw_input("\nPress Enter to continue...")
    print "Please wait..."
    
    # Creates output folder
    if not os.path.exists(os.getcwd() + "/output"):
        os.mkdir(os.getcwd() + "/output")
    data = open(os.getcwd() + "/output/" + "data.xml", 'w')
    data.write(u"<data>\n")
    driver = webdriver.Firefox()
    file = open("list.txt", 'r')
    for line in file:
        try:
            if line == "":
                continue
            print "Now parsing through: " + line,
            line = line.strip()
            # Searching Facebook
            print "\Waiting..."
            driver.get("https://www.google.com/search?q=" + line + " game")
            time.sleep(10)
            print "\Checking..."
            RHS = driver.find_elements_by_css_selector("A._hvg")
            data.write("\t<entry>\n\t<name>" + line + "</name>\n\t")
            # Retrieving ratings
            for ele in RHS:
                data.write("<rating>" + ele.text + "</rating>\n\t")
                print "Writing " + ele.text
                    
            # Retrieving platforms and initial release
            platforms = driver.find_elements_by_css_selector("DIV._mr.kno-fb-ctx")
            for ele in platforms:
                if "Initial release date:" in ele.text:
                    print "Writing " + ele.text
                    data.write("<release>" + ele.text.replace("Initial release date: ", "") + "</release>\n\t")
                if "Platforms:" in ele.text or "Platform: in ele.text":
                    print "Writing " + ele.text
                    data.write("<platforms>" + ele.text.replace("Platforms: ", "") + "</platforms>\n\t")
            data.write(u"\t</entry>\n")
        except:
            continue;
       
    data.write(u"</data>")
    data.close()
    driver.close()
    print "\nOutput written to text"
    
def check_exists_by_css(driver, classDom):
    try:
        driver.find_element_by_css_selector(classDom)
    except:
        return False
    return True
     
if __name__ == '__main__':
    main()