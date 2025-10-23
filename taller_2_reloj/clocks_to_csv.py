import pandas as pd
import os


path = "../data-resampled/"

hour_clock = [{}]

for root, dir, files in os.walk(path):
    
    for file in files:
        hour = file[6:8]
        minutes = file[8:10]
        hour_clock.append({
            "hour": hour,
            "minute": minutes,
            "path": os.path.join(root, file)
        })


# Convert list of dict to Dataframe.


data = pd.DataFrame(hour_clock)
data.to_csv("clocks.csv", index=False)
print("✅ Archivo creado")

