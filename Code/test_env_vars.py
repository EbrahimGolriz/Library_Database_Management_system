import os
from dotenv import load_dotenv

load_dotenv(".env")
db_server = os.environ.get("DB_SERVER")
db_name = os.environ.get("DB_NAME")

print(f"DB_SERVER from env: '{db_server}'")
print(f"DB_NAME from env: '{db_name}'")

if db_server:
    print("DB_SERVER environment variable is set and read successfully.")
else:
    print("DB_SERVER environment variable is NOT set or NOT read.")

if db_name:
    print("DB_NAME environment variable is set and read successfully.")
else:
    print("DB_NAME environment variable is NOT set or NOT read.")