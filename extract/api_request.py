import requests
import dotenv
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import Dict

class ApiRequest:
    """
    A class to handle synchronous and asynchronous requests to the Gold API.

    Attributes:
        ticker (str): The ticker symbol representing the asset to query from the API.
    """

    def __init__(self, url: str, header: Dict = {}):
        """
        Initializes the ApiRequest instance with a specified ticker symbol.

        Args:
            ticker (str): The ticker symbol for the asset (e.g., 'XAU' for gold).
        """
        self.url = url
        self.header = header

    def make_request(self):
        """
        Makes a synchronous HTTP GET request to the Gold API using the provided ticker.

        Returns:
            str: The API response text if the request is successful.
            None: If an error occurs during the request.

        Raises:
            requests.exceptions.RequestException: If the HTTP request fails.
        """
        
        url = self.url

        header = self.header

        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print("Error:", str(e))
            return None