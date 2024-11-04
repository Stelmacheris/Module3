import requests
from typing import Dict
import aiohttp
class ApiRequest:
    """
    A class to handle synchronous and asynchronous API requests.

    Attributes:
    -----------
    url : str
        The API endpoint URL to request.
    header : Dict
        Headers to include in the request (e.g., authorization).
    params : Dict
        Query parameters to include in the request.

    Methods:
    --------
    make_request():
        Executes a synchronous GET request to the specified URL.
        
    async async_make_request():
        Executes an asynchronous GET request using `aiohttp`.
    """

    def __init__(self, url: str, header: Dict = {}, params: Dict = {}):
        """
        Initializes ApiRequest with the specified URL, headers, and parameters.

        Parameters:
        -----------
        url : str
            The API endpoint URL to request.
        header : Dict, optional
            Headers to include in the request, by default an empty dictionary.
        params : Dict, optional
            Query parameters to include in the request, by default an empty dictionary.
        """
        self.url = url
        self.header = header
        self.params = params

    def make_request(self):
        """
        Executes a synchronous GET request to the specified URL.

        Returns:
        --------
        dict or None
            JSON response from the API if the request is successful; otherwise, `None`.

        Raises:
        -------
        requests.exceptions.RequestException
            If there is an issue with the request, such as network failure or invalid response.

        Example:
        --------
        api = ApiRequest(url="https://api.example.com/data")
        response = api.make_request()
        """
        try:
            response = requests.get(self.url, headers=self.header, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error:", str(e))
            return None

    async def async_make_request(self):
        """
        Executes an asynchronous GET request to the specified URL using `aiohttp`.

        Returns:
        --------
        dict or None
            JSON response from the API if the request is successful; otherwise, `None`.

        Raises:
        -------
        aiohttp.ClientError
            If there is an issue with the request, such as network failure or invalid response.

        Example:
        --------
        import asyncio
        api = ApiRequest(url="https://api.example.com/data")
        response = asyncio.run(api.async_make_request())
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, headers=self.header, params=self.params) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                print("Error:", str(e))
                return None
