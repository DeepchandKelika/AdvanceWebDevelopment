import requests, json


url = 'https://michaelgathara.com/api/python-challenge'

response = requests.get(url)

challenges = response.json()
print("Name: Deep Chand Kelika \nBlazerID: dkelika")
for challenge in challenges:
    print( "Answer ",challenge['id']," : ", eval(challenge['problem'][:-1]) )
