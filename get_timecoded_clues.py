import json
import lxml.html
from thefuzz import fuzz

with open(r"C:\Users\Alex\PycharmProjects\tube\jeopardy_game\Jeopardy - S39E60 - Jeopardy.json") as f:
    data = json.loads(f.read())

with open("J! Archive - Show #8755, aired 2022-12-02.htm") as f:
    root = lxml.html.fromstring(f.read())

all_clues = []

for clue in root.xpath("//td[contains(@id,'clue_') and @class='clue_text']//parent::tr"):
   # print(clue)
    #if not clue.xpath(".//td[@class='clue_text']"):
    #    print(clue)
    if clue.xpath(".//td[@class='clue_text']"):
        answer = clue.xpath(".//td[@class='clue_text']")[0].text_content()
        question = clue.xpath(".//em[@class='correct_response']")[0].text_content()
        all_clues.append({
           "question": question,
           "answer": answer
        })
    #print(clue.xpath(".//td[@class='clue_text']"))


timecode_questions = {}

for clue in all_clues:
    sorted_segments = sorted(list(map(lambda s: (fuzz.ratio(clue["answer"].lower(), s["text"].lower()), s), data["segments"])), key=lambda s: s[0], reverse=True)
    if sorted_segments[0][0] > 75:
        correct_segment = sorted_segments[0]
    else:
        print(f"{clue['answer'][:20]} -> Couldn't find segment")
        continue

    timecode_questions[float(correct_segment[1]["end"])] = clue["question"]
    print(f"{clue['answer'][:20]} -> {correct_segment[1]['text']}")


with open("timecoded_question.json", "w") as f:
    f.write(json.dumps(timecode_questions, indent=4, sort_keys=True))
