import pandas as pd
import serial

# Load the cleaned dataset
df = pd.read_csv("cleaned_plants.csv")

# Setup serial communication (Adjust 'COM3' to match your Arduino port)
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)

def get_plant_recommendation(plant_name):
    plant_info = df[df['Plant Name'].str.lower() == plant_name.lower()]
    if plant_info.empty:
        return "Plant not found."

    sunlight = plant_info.iloc[0]['Sunlight']
    watering = plant_info.iloc[0]['Watering']
    return f"Sunlight:{sunlight}, Watering:{watering}"

while True:
    if arduino.in_waiting > 0:
        plant_name = arduino.readline().decode().strip()
        response = get_plant_recommendation(plant_name)
        arduino.write((response + "\n").encode())