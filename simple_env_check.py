
import environ
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()

print(f"Checking .env at: {BASE_DIR / '.env'}")
# Mimic base.py logic
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    print("Reading .env file...")
    env.read_env(str(BASE_DIR / ".env"))
else:
    print("NOT reading .env file.")

print(f"EMAIL_HOST_USER: {env('DJANGO_EMAIL_HOST_USER', default='NOT_SET')}")
