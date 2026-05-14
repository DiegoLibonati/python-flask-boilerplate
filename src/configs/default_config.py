import os


class DefaultConfig:
    # General
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")

    # Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))

    # Flask general
    DEBUG = False
    TESTING = False

    # App seeding
    SEED_DEFAULTS = False
