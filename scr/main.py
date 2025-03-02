import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_KEY"])

response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents="list of popular drinks in mexico in spanish",
)

print(response.text)
