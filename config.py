"""
Application configuration.

All sensitive/environment-specific values (database credentials, secret key)
are read from a .env file so they are never hardcoded in the source code.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # --- MySQL / TiDB Cloud connection ---
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "careerready")

    # Allows an explicit override (e.g. for automated testing)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # TiDB Cloud SSL certificate
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": os.path.join(
                    os.path.dirname(__file__),
                    "isrgrootx1.pem"
                )
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False