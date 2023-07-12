import requests

def createFetchFn():
    def fetchFn(url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if status is 4xx, 5xx
        return response
    return fetchFn