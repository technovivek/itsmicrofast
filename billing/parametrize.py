from unittest.mock import Mock, patch
import pytest
import requests

def myfunction(url):

    try:

        res = requests.get(url)
        print("res", res)
        if res.status_code == 200:
            return "success"
        else:
            return "failure"
    except Exception as e:
        print(e)
        return str(e)

url  = "www.google.com"
myfunction(url)




