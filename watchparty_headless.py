from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
import math

driver = webdriver.Firefox()
driver.get("https://www.watchparty.me/watch/godly-smoke-launch")

with open("speech-recognition-in-javascript-starter/timecoded_question.json") as f:
    timecode = json.loads(f.read())
    new_timecode = {}
    for t in timecode:
        new_timecode[float(t)] = timecode[t]
    timecode = new_timecode


while True:
    current_time = int(driver.execute_script('return document.querySelector("video").currentTime'))

    distance = {}

    for tc in timecode:
        distance[tc - current_time] = timecode[tc]

    closest = sorted(distance)[0]

    if math.floor(closest) == 0:
        # PAUSE
        driver.execute_script('document.querySelector("i.Controls_control__L161B").click()')


    #closest_time = sorted(timecode.keys(), key=lambda t: t - current_time, reverse=True)[0]

    #print(current_time)

    time.sleep(0.5)
