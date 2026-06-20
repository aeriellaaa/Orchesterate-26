import os
import json
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

claims = pd.read_csv("../dataset/claims.csv")
history = pd.read_csv("../dataset/user_history.csv")

results = []

for idx, row in claims.iterrows():

    print(f"Processing {idx+1}/{len(claims)}")

    user_history = history[
        history["user_id"] == row["user_id"]
    ].iloc[0]

    images = []

    for path in row["image_paths"].split(";"):

        try:
            img = Image.open("../dataset/" + path)
            img.thumbnail((1024, 1024))
            images.append(img)

        except Exception:
            pass

    prompt = f"""
You are an insurance evidence reviewer.

Images are the PRIMARY source of truth.

Claim:
{row['user_claim']}

Claim Object:
{row['claim_object']}

History Flags:
{user_history['history_flags']}

Return ONLY valid JSON.

{{
"evidence_standard_met":"",
"evidence_standard_met_reason":"",
"risk_flags":"",
"issue_type":"",
"object_part":"",
"claim_status":"",
"claim_status_justification":"",
"supporting_image_ids":"",
"valid_image":"",
"severity":""
}}

Allowed claim_status:
supported
contradicted
not_enough_information
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, *images]
        )

        text = response.text.strip()

        # Remove markdown json fences
        text = text.replace("```json", "")
        text = text.replace("```", "")

        data = json.loads(text)

    except Exception as e:

        print("ERROR:", e)

        data = {
            "evidence_standard_met": "",
            "evidence_standard_met_reason": str(e),
            "risk_flags": "manual_review_required",
            "issue_type": "unknown",
            "object_part": "unknown",
            "claim_status": "not_enough_information",
            "claim_status_justification": "Generation failed",
            "supporting_image_ids": "",
            "valid_image": "",
            "severity": "unknown"
        }

    result = {
        "user_id": row["user_id"],
        "image_paths": row["image_paths"],
        "user_claim": row["user_claim"],
        "claim_object": row["claim_object"],
        **data
    }

    results.append(result)

output = pd.DataFrame(results)

output.to_csv("../dataset/output.csv", index=False)

print("DONE")