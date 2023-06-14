import json
import math
import random
import time

import requests


def random_float(*args, **kwargs) -> float:
    """
    Returns a random floating-point number from a uniform distribution
    in the range 1 to 40.
    """
    return round(random.uniform(1, 100), 2)


def nonzero(value) -> float:
    """
    This function returns the input value if it is not zero, otherwise
    it generates a random float value.
    """
    return value if not math.isnan(value) else random_float()


def get_image(*args, **kwargs) -> str:
    """
    This function fetches a random dog image from the website
    'https://random.dog/woof.json' and returns the URL of the image.
    It uses the requests library to make a GET request to the URL
    and then extracts the URL of the image from the JSON response
    using the json library. This function can be used in a program
    to display a random dog image.
    """
    url = 'https://random.dog/woof.json'
    time.sleep(2)
    response = requests.request('GET', url)
    return json.loads(response.text)['url']
