from ml.comfort import calculate_comfort

print(
    calculate_comfort(
        air_temp=24,
        radiant_temp=24,
        humidity=50,
        air_speed=0.1,
    )
)