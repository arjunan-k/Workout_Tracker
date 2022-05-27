import requests
from datetime import datetime
import os

APP_ID = os.environ["NT_APP_ID"]
APP_KEY = os.environ["NT_API_KEY"]

GENDER = "male"
WEIGHT_KG = 45
HEIGHT_CM = 170
AGE = 20

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]

exercise_text = input("Tell me which exercise you did: ")

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    bearer_headers = {
        "Authorization": f"Bearer {os.environ['TOKEN']}"
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)
    print(sheet_response.text)