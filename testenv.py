import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Kiểm tra biến env: ", os.environ.get("OPENAI_API_KEY"))