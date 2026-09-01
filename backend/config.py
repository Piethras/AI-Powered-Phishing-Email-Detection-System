import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Example: mysql+pymysql://user:password@localhost/phishing_db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:password@localhost/phishing_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
