import csv
import json
import requests
import sys

url = "http://localhost:8000/"

userAuthRes = requests.post(url + 'auth/', json={
    "username": sys.argv[1],
    "password": sys.argv[2]
})
userAuth = userAuthRes.json()
headers = {
    'Authorization': 'token ' + userAuth['token']
}

with open('questions.csv', newline='', encoding='utf-8-sig') as csvfile:
    questionReader = csv.DictReader(csvfile, quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    for row in questionReader:
        jsonQuestion = {
            "description": row['question'],
            "level": row['level'],
            "type": row['type of question'],
            "feedback": row['feedback']
        }
        questionRes = requests.post(url + 'questions/', headers=headers, json=jsonQuestion)
        question = questionRes.json()

        for i in range(1, 5):
            answer_key = "%s %d" % ('answer', i)
            jsonQuestionAnswer = {
                "description": row[answer_key],
                "is_correct": row[answer_key] == row['correct answer'],
                "question_id": question['id']
            }
            questionAnswerRes = requests.post(url + 'question-answers/', headers=headers, json=jsonQuestionAnswer)
print('Done')
