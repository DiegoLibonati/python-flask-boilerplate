import os


class DefaultConfig:
    # General
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")
    JSON_AS_ASCII = False

    # Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 5000)

    # Flask general
    DEBUG = False
    TESTING = False
