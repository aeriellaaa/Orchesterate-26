import os
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load datasets
claims = pd.read_csv("../dataset/claims.csv")
history = pd.read_csv("../dataset/user_history.csv")

# First claim only
row = claims.iloc[0]

# User history
user_history = history[
    history["user_id"] == row["user_id"]
].iloc[0]

# Load images and resize
images = []

for path in row["image_paths"].split(";"):
    img = Image.open("../dataset/" + path)

    # Reduce size to avoid Gemini connection issues
    img.thumbnail((1024, 1024))

    images.append(img)

prompt = f"""
You are an insurance evidence reviewer.

Images are the primary source of truth.

Claim:
{row['user_claim']}

Object:
{row['claim_object']}

History Flags:
{user_history['history_flags']}

Return ONLY valid JSON.

{{
    "evidence_standard_met": "",
    "evidence_standard_met_reason": "",
    "risk_flags": "",
    "issue_type": "",
    "object_part": "",
    "claim_status": "",
    "claim_status_justification": "",
    "supporting_image_ids": "",
    "valid_image": "",
    "severity": ""
}}

Allowed claim_status values:
supported
contradicted
not_enough_information

Allowed severity values:
none
low
medium
high
unknown
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt, *images]
)

print(response.text)