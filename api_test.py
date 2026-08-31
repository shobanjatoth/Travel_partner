import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

models = client.models.list()

print("\nAvailable Groq models:\n")

for model in models.data:
    print(model.id)