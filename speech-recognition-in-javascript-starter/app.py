from flask import Flask, jsonify, render_template, request
import threading
import time
from thefuzz import fuzz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import math

app = Flask(__name__)


active_question = None


def run_watch_party():
    global active_question
    print("starting ff")
    driver = webdriver.Firefox()
    driver.get("https://www.watchparty.me/watch/godly-smoke-launch")

    with open("timecoded_question.json") as f:
        timecode = json.loads(f.read())
        new_timecode = {}
        for t in timecode:
            new_timecode[float(t)] = timecode[t]
        timecode = new_timecode

    while True:
        current_time = int(driver.execute_script('return document.querySelector("video").currentTime'))

        distance = {}

        for tc in timecode:
            distance[abs(tc - current_time)] = tc, timecode[tc]

        closest = sorted(distance)[0]

        print(closest)

        if math.floor(closest) == 0:
            print(closest)

            chat_element = driver.find_element("xpath", "//input[@placeholder='Enter a message...']")

            chat_element.send_keys(f"Question ended. Pausing for 5 seconds.")
            chat_element.send_keys(Keys.ENTER)
            #chat_element.click()

            question = distance[closest][1]

            active_question = question

            # PAUSE
            driver.execute_script('document.querySelector("i.Controls_control__L161B").click()')

            del timecode[distance[closest][0]]

            # Wait 5 seconds
            time.sleep(5)

            # Resume
            driver.execute_script('document.querySelector("i.Controls_control__L161B").click()')
            continue

        # closest_time = sorted(timecode.keys(), key=lambda t: t - current_time, reverse=True)[0]

        # print(current_time)

        time.sleep(0.5)


@app.route("/question", methods=["POST"])
def hello_world():
    if active_question:
        massaged_player_question = request.json["question"].lower().replace("what is", "").replace("who is", "").replace("what are", "").replace("who are", "").strip()
        massaged_active_question = active_question.lower().replace("what is", "").replace("who is", "").replace("what are", "").replace("who are", "").strip()
        ratio = fuzz.ratio(massaged_active_question, massaged_player_question)
        print(f"{massaged_active_question} -> {massaged_player_question} -> {ratio}")

        if ratio > 80:
            return jsonify({"correct": True})
        else:
            return jsonify({"correct": False})
    else:
        return jsonify({"active": False})


@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    y = threading.Thread(target=run_watch_party)
    y.start()

    app.run(debug=False)

