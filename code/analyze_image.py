import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

images = [
    Image.open("../dataset/images/test/case_001/img_1.jpg"),
    Image.open("../dataset/images/test/case_001/img_2.jpg"),
    Image.open("../dataset/images/test/case_001/img_3.jpg"),
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        """
Analyze all images together.

Return:
1. Object type
2. Visible damage
3. Damaged part
4. Severity
5. Which image contains the strongest evidence
        """,
        *images
    ]
)

print(response.text)