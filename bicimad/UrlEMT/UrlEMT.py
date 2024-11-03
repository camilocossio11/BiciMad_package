import io
import re
import zipfile
from typing import TextIO

import requests
from decorators.types_decorator import check_args_types

from .constants import date_ranges


class UrlEMT:
    # Class constants
    EMT = "https://opendata.emtmadrid.es"
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"

    def __init__(self):
        self._valid_urls: dict = UrlEMT.select_valid_urls()

    @property
    def valid_urls(self) -> dict:
        return self._valid_urls

    @staticmethod
    @check_args_types
    def select_valid_urls() -> dict:
        """
        Fetches HTML content from a specified URL and extracts valid trip CSV links.

        This function sends an HTTP GET request to the base URL for trip data,
        checks for a successful response, and retrieves the HTML content.
        It then calls the `get_links` function to extract valid URLs from the HTML.

        Returns:
            dict: A dictionary mapping date identifiers to their corresponding full URLs of the
                trip CSV files. The format is { 'MM_DD': 'full_url' }.

        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        response = requests.get(f"{UrlEMT.EMT}{UrlEMT.GENERAL}")
        response.raise_for_status()
        html_content = response.text
        return UrlEMT.get_links(html_content)

    @staticmethod
    @check_args_types
    def get_links(html: str) -> dict:
        """
        Extracts valid trip CSV links from the provided HTML string.

        This function uses regular expressions to search for specific patterns in the
        HTML content that match the format of trip CSV links. It returns a dictionary
        where the keys are date identifiers (in the format 'MM_DD') and the values are
        the full URLs of the trip CSV files.

        Args:
            html (str): A string containing the HTML content to search for trip links.

        Returns:
            dict: A dictionary mapping date identifiers to their corresponding full URLs
                of the trip CSV files. The format is { 'MM_DD': 'full_url' }.
        """
        pattern = r"\/[^\s]*trips_\d{2}_\d{2}_\w+\-csv.aspx"
        matches = re.findall(pattern, html)

        key_ptrn = r"(\d{2}_\d{2})"
        valid_urls = {}
        for link in matches:
            key = re.search(key_ptrn, link).group()
            valid_urls[key] = f"{UrlEMT.EMT}{link}"
        return valid_urls

    @staticmethod
    @check_args_types
    def get_file_name_from_url(url: str) -> str:
        """
        Extracts the file name from a given trip CSV URL.

        This function uses a regular expression to search for a specific pattern in the URL,
        extracting the trip file name, which includes the date and additional identifiers.
        If the URL does not match the expected pattern, an empty string is returned.

        Args:
            url (str): A string representing the URL from which to extract the file name.

        Returns:
            str: The extracted file name (format: 'trips_MM_DD_month') if a match is found,
                otherwise an empty string.
        """
        match = re.search(r"/(trips_\d{2}_\d{2}_[A-Za-z]+)-csv\.aspx$", url)
        if match:
            return match.group(1)
        else:
            return ""

    @check_args_types
    def get_url(self, month: int, year: int) -> str:
        """
        Retrieves the URL for the specified month and year from the valid URLs.

        This method checks if the provided month and year are within the valid range.
        If valid, it attempts to retrieve the corresponding URL from the `valid_urls` dictionary.
        If the URL is not found, it raises a ValueError.

        Args:
            month (int): The month for which to retrieve the URL (1-12).
            year (int): The year for which to retrieve the URL (21-23).

        Returns:
            str: The URL corresponding to the specified month and year.

        Raises:
            ValueError: If the month is not in the range of valid months (defined by `date_ranges`),
                        or if the year is not in the range of valid years,
                        or if no data is found for the specified month and year.
        """
        min_month, max_month = date_ranges.get("month")[0], date_ranges.get("month")[1]
        if not (min_month <= month <= max_month):
            raise ValueError(
                f"Month has to be a value between {min_month} and {max_month}, got: {month}"
            )

        min_year, max_year = date_ranges.get("year")[0], date_ranges.get("year")[1]
        if not (min_year <= year <= max_year):
            raise ValueError(
                f"Year has to be a value between {min_year} and {max_year}, got: {year}"
            )

        if self.valid_urls.get(f"{year}_{month:02}"):
            return self.valid_urls.get(f"{year}_{month:02}")
        else:
            raise ValueError(f"Data not fount for month {month} year {year}")

    @check_args_types
    def get_csv(self, month: int, year: int) -> TextIO:
        """
        Retrieves the CSV file corresponding to the specified month and year.

        This method first obtains the URL for the specified month and year using the `get_url`
        method. It then downloads the content at that URL, expecting it to be a ZIP file containing
        the CSV. The method extracts the CSV file and returns it as a StringIO object for further
        processing.

        Args:
            month (int): The month for which to retrieve the CSV (1-12).
            year (int): The year for which to retrieve the CSV (21-23).

        Returns:
            TextIO: A StringIO object containing the contents of the CSV file.

        Raises:
            ValueError: If there is an issue retrieving the URL for the specified month and year.
            HTTPError: If the HTTP request returned an unsuccessful status code when trying to
            download the ZIP file.
            KeyError: If the expected CSV file is not found in the ZIP archive.
        """
        url = self.get_url(month, year)
        file_name = UrlEMT.get_file_name_from_url(url)
        response = requests.get(url)
        response.raise_for_status()
        resp_bytes = io.BytesIO(response.content)
        zip_file = zipfile.ZipFile(resp_bytes)
        with zip_file.open(f"{file_name}.csv") as f:
            contents = f.read()
            content_str = contents.decode("utf-8")
            file_str = io.StringIO(content_str)
        return file_str
