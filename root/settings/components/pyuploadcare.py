import os

UPLOADCARE = {
    'pub_key': os.getenv("UPLOADCARE_PUB_KEY"),
    'secret': os.getenv("UPLOADCARE_API_KEY"),
}
