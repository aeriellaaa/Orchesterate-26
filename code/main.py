import pandas as pd
from PIL import Image

claims = pd.read_csv("../dataset/claims.csv")

row = claims.iloc[0]

print("\nCLAIM:")
print(row["user_claim"])

print("\nIMAGES:")

for path in row["image_paths"].split(";"):
    print(path)

    img = Image.open("../dataset/" + path)
    img.show()