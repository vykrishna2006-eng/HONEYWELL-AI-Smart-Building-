from llm.generator import generate


response = generate("""
Temperature : 26°C
Humidity : 60%
Occupancy : 15
Energy Consumption : 145 kWh
Comfort Score : 88%
""")

print(response)