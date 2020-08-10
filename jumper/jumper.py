import time
from selenium import webdriver
import threading
from Crypto.Hash import keccak
import random
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from judge import judge
from bs4 import BeautifulSoup
from urllib.parse import urlparse

#global variable
visited = {}
MAX_DEPTH = 3
THRESHOLD_LCS = 0.87
lock = threading.Lock()
seedtag = []
ward = ""
maxRank = 0

#crawler
def crawler(url, keyword, depth, min, max) :
    o = urlparse(url)
    url = o.geturl()
    print(url)
    global MAX_DEPTH
    global THRESHOLD_LCS
    global ward, maxRank
    if depth >= MAX_DEPTH :
        print("reach Max!")
        return True;
    global visited
    global keccak_hash
    global lock
    global seedtag
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(url.encode('utf-8'))
    
    lock.acquire()
    if keccak_hash.hexdigest() in visited :
        lock.release()
        return True
    visited[keccak_hash.hexdigest()] = url
    lock.release()

    driver = webdriver.Chrome('/WebDriver/bin/chromedriver')
    driver.get(url);
    time.sleep(4+depth)
    # webdriver.ActionChains(driver).click(box[0]).perform()
    if depth != 0 :
        soup = BeautifulSoup(driver.page_source,"html.parser")
        mytag = [tag.name for tag in soup.findAll()]
        score = judge.lcs_similarity(seedtag, mytag)
        print(score,"  ",url)
        if score >= THRESHOLD_LCS :
            f = open("../evidence/" + keccak_hash.hexdigest() + ".png","wb")
            tmp = driver.get_screenshot_as_png()
            f.write(tmp)
            f.close()

    if depth == 0 :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        box = driver.find_elements_by_tag_name('a')
        soup = BeautifulSoup(driver.page_source,"html.parser")
        seedtag = [tag.name for tag in soup.findAll()]

    elif depth+1 < MAX_DEPTH:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        box = driver.find_elements_by_partial_link_text(keyword)
        if maxRank < len(box) :
            maxRank = len(box)
            ward = url
    else : 
        print(depth," is depth")
        box = []

    for i in range (len(box)) :
        nexturl = box[i].get_attribute("href")
        tmp = urlparse(nexturl)
        nexturl = tmp.geturl()
        if type(nexturl) is str and nexturl.startswith("http") :
            keccak_hashnew = keccak.new(digest_bits=256)
            keccak_hashnew.update(nexturl.encode('utf-8'))
            lock.acquire()
            if keccak_hashnew.hexdigest() not in visited :
                lock.release()
                time.sleep(7 + random.randint(min,max))
                thread = threading.Thread(target=crawler, args = (nexturl, keyword, depth+1, min + 7, max + 15))
                thread.start()
            else :
                lock.release()
                print("Already visited")
    driver.quit()

def printexit() :
    global ward, maxRank
    print("Ward : ", ward, " Max :" , maxRank)
