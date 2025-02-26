# Microservice-A
Microservice A for CS 361
Communication contract: I am available week days from 9 AM to 5 PM. The primary method to contact me is via Microsoft Teams at depyakr@oregonstate.edu - I receive notifications about teams messages and will reply prompty. As a second form of communication you can reach me through the discord server. If you need to contact me I will respond outside of the hours above, but the response may be slower as I work at night. 
3A. To programatically request data from the microservice send a GET request to http://127.0.0.1:5000/sightword/random. You can also include optional query parameters for category and difficulty. Categories include noun, verb, and adjective. Difficulty includes easy, medium, and hard. 

An example call for a random word is:
import requests
url = "http://127.0.0.1:5000/sightword/random"
response = requests.get(url)
print(response.text)

An example call for a word from the category noun and difficulty easy is:
import requests

params = {
    "category": "noun",
    "difficulty": "easy"
}

url = "http://127.0.0.1:5000/sightword/random"
response = requests.get(url, params=params)

print(response.text)

To receive data from the microservice, the microservice communicates the sight word in JSON format. An example to programmatically receive data from the microservice is:
import requests

url = "http://127.0.0.1:5000/sightword/random"
params = {"category": "noun", "difficulty": "easy"}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Sight Word:", data["word"])
elif response.status_code == 404:
    print("Error:", response.json()["error"])
else:
    print("Unexpected Error:", response.text)

UML Sequence diagram can be found at the following link:
https://github.com/user-attachments/assets/d02ea696-352f-4871-8dbc-564df8c4291c
