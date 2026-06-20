import os
from dotenv import load_dotenv
from google import genai
import pandas as pd

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

claims = pd.read_csv("../dataset/claims.csv")

claim = claims.iloc[0]["user_claim"]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""
Extract from this conversation:

1. Claimed object
2. Claimed damage
3. Claimed part

Return JSON only.

Conversation:
{claim}
"""
)

print(response.text)