import os
import json
import time
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
output = pd.read_csv("../dataset/output.csv")

failed_rows = output[
    output["severity"].astype(str).str.lower() == "unknown"
]

print("Rows to reprocess:", len(failed_rows))

for idx in failed_rows.index:

    row = claims.iloc[idx]

    print(f"\nReprocessing row {idx}")

    try:

        user_history = history[
            history["user_id"] == row["user_id"]
        ].iloc[0]

        images = []

        for path in row["image_paths"].split(";"):

            try:
                img = Image.open("../dataset/" + path)
                img.thumbnail((1024, 1024))
                images.append(img)

            except Exception as e:
                print("Image load error:", e)

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

        response = None

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=[prompt, *images]
                )

                break

            except Exception as e:

                print(f"Retry {attempt+1}/3:", e)
                time.sleep(15)

        if response is None:
            print("Skipped row", idx)
            continue

        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        try:
            data = json.loads(text)

        except Exception:
            print("Bad JSON response")
            print(text[:500])
            continue

        for key, value in data.items():

            if isinstance(value, (list, dict)):
                value = json.dumps(value)

            output.at[idx, key] = str(value)

        # SAVE IMMEDIATELY AFTER SUCCESS
        output.to_csv("../dataset/output.csv", index=False)

        print("Success")

    except Exception as e:

        print("FAILED:", idx, e)

# final save
output.to_csv("../dataset/output.csv", index=False)

print("\nDONE")