import requests
import dotenv
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import Dict
import aiohttp


class ApiRequest:
    """
    A class to handle synchronous and asynchronous requests to the Gold API.

    Attributes:
        url (str): The URL to query from the API.
        header (Dict): Optional headers for the request.
        params (Dict): Optional parameters for the request.
    """

    def __init__(self, url: str, header: Dict = {}, params: Dict = {}):
        self.url = url
        self.header = header
        self.params = params

    def make_request(self):
        """Makes a synchronous HTTP GET request to the API."""
        try:
            response = requests.get(self.url, headers=self.header, params=self.params)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print("Error:", str(e))
            return None

    async def async_make_request(self):
        """Makes an asynchronous HTTP GET request to the API."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.header, params=self.params) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                return None