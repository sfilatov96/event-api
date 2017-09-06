from os import environ


class Config:
    APP_HOST = environ.get("APP_HOST", default="0.0.0.0")
    APP_PORT = int(environ.get("APP_PORT", default=5000))
    MONGO_HOST = environ.get("MONGO_HOST", default="127.0.0.1")
    MONGO_PORT = int(environ.get("MONGO_PORT", default=27017))