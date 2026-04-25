import pandas as pd
import random

forests = [
    "Amazon Forest", "Araku Valley", "Nallamala Forest",
    "Seshachalam Hills", "Gir National Park",
    "Kaziranga National Park", "Periyar National Park",
    "Sundarbans", "Ranthambore National Park", "Corbett National Park"
]

rows = []
for i in range(500):
    location = random.choice(forests)
    temp = random.randint(15, 50)
    humidity = random.randint(20, 90)
    wind = random.randint(0, 40)
    rain = random.randint(0, 100)

    # Adjusted rule: easier to trigger fire
    fire = 1 if (temp > 35 and humidity < 50 and wind > 15 and rain < 20) else 0

    rows.append([location, temp, humidity, wind, rain, fire])

df = pd.DataFrame(rows, columns=["Location", "Temperature", "Humidity", "WindSpeed", "Rainfall", "Fire"])
df.to_csv("forest_fire_data.csv", index=False)

print("✅ Balanced dataset created with adjusted fire rule")
