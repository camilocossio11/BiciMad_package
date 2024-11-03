import re

import pandas as pd
from decorators.types_decorator import check_args_types
from UrlEMT.UrlEMT import UrlEMT


class BiciMad:
    def __init__(self, month: int, year: int) -> None:
        self._month = month
        self._year = year
        self._data = BiciMad.get_data(month, year)

    @property
    def month(self) -> int:
        return self._month

    @property
    def year(self) -> int:
        return self._year

    @property
    def data(self) -> int:
        return self._data

    @staticmethod
    @check_args_types
    def get_data(month: int, year: int) -> pd.DataFrame:
        """
        Retrieves data from a CSV related to BiciMad bike usage for a specific month and year,
        processing the information into a DataFrame.

        Args:
            month (int): The month for which to retrieve the data (1-12).
            year (int): The year for which to retrieve the data (21-23).

        Returns:
            pd.DataFrame: A DataFrame containing bike trip data with the following columns:
                - fecha (datetime): The date of the trip.
                - idBike (int): The identifier of the bike.
                - fleet (str): The fleet type of the bike.
                - trip_minutes (float): The duration of the trip in minutes.
                - geolocation_unlock (str): The geolocation where the bike was unlocked.
                - address_unlock (str): The address where the bike was unlocked.
                - unlock_date (datetime): The date and time when the bike was unlocked.
                - locktype (str): The type of lock used.
                - unlocktype (str): The type of unlock used.
                - geolocation_lock (str): The geolocation where the bike was locked.
                - address_lock (str): The address where the bike was locked.
                - lock_date (datetime): The date and time when the bike was locked.
                - station_unlock (int): The ID of the unlock station.
                - unlock_station_name (str): The name of the unlock station.
                - station_lock (int): The ID of the lock station.
                - lock_station_name (str): The name of the lock station.
        """
        csv_file = UrlEMT().get_csv(month, year)
        csv_file.seek(0)
        df = pd.read_csv(
            csv_file,
            sep=";",
            index_col="fecha",
            parse_dates=["fecha", "unlock_date", "lock_date"],
            usecols=[
                "fecha",
                "idBike",
                "fleet",
                "trip_minutes",
                "geolocation_unlock",
                "address_unlock",
                "unlock_date",
                "locktype",
                "unlocktype",
                "geolocation_lock",
                "address_lock",
                "lock_date",
                "station_unlock",
                "unlock_station_name",
                "station_lock",
                "lock_station_name",
            ],
        )
        return df

    def __str__(self) -> str:
        return self.data.__str__()

    def delete_nan_rows(self) -> None:
        """
        Deletes rows where all values are NaN.
        """
        self.data.dropna(how="all", inplace=True)

    @check_args_types
    def float_to_str(self, col: str) -> None:
        """
        Converts a float column to a string column (2.0 -> '2').

        Args:
            col (str): Column name.
        """
        df = self.data
        if col in df.columns and df[col].dtype == float:
            df[col] = df[col].apply(lambda x: str(x).split(".")[0])

    @staticmethod
    @check_args_types
    def format_strings(content: str) -> str:
        """
        Extracts and formats a substring enclosed in single quotes from the input string.
        If no quoted substring is found, the function returns the trimmed version of the input
        string.

        Args:
            content (str): The input string which may contain a substring enclosed in single quotes.

        Returns:
            str: The extracted and trimmed substring if single quotes are found.
                Otherwise, the original string is returned, trimmed of leading and trailing spaces.
        """
        match = re.search(r"'([^']*)'", content)
        if match:
            return match.group(1).strip()
        else:
            return content.strip()

    @check_args_types
    def format_string_col(self, col: str) -> None:
        """
        Formats the values in a specified column of the DataFrame by replacing NaN values
        and applying a string formatting function.

        Args:
            col (str): The name of the column in the DataFrame to format.

        Returns:
            None: The method modifies the DataFrame in place.
        """
        self.data[col] = self.data[col].fillna("not_found")
        self.data[col] = self.data[col].apply(BiciMad.format_strings)

    def clean(self) -> None:
        """
        Cleans the DataFrame by performing several data preparation steps.

        This method executes the following operations:
            - Deletes rows with NaN values from the DataFrame.
            - Fills NaN values in the "trip_minutes" column with 0.
            - Converts specified columns from float to string.
            - Formats specified string columns to handle missing or improperly formatted values.

        Returns:
            None: The method modifies the DataFrame in place.
        """
        self.delete_nan_rows()
        self.data["trip_minutes"] = self.data["trip_minutes"].fillna(0)
        for col in ["fleet", "idBike", "station_lock", "station_unlock"]:
            self.float_to_str(col)
        for col in ["address_unlock", "address_lock"]:
            self.format_string_col(col)

    @check_args_types
    def info_most_popular_stations(self, unlock_st: bool = True) -> pd.DataFrame:
        """
        Retrieves information about the most popular bike stations based on unlock or lock actions.

        This method performs the following steps:
            - Cleans the DataFrame by removing NaN values and formatting columns.
            - Groups the data by station and address based on the specified action (unlock or lock).
            - Counts the number of bike trips associated with each station.
            - Identifies the station(s) with the maximum number of trips.
            - Constructs a descriptive string containing station and address information.

        Args:
            unlock_st (bool): If True, considers unlock actions; if False, considers lock actions.

        Returns:
            pd.DataFrame: A DataFrame containing information about the most popular station(s),
                        including the station ID, address, and a formatted information string.
        """
        self.clean()
        category = "unlock" if unlock_st else "lock"
        action_per_st = self.data.groupby([f"station_{category}", f"address_{category}"]).agg(
            amount=("idBike", "count")
        )
        max_uses = max(action_per_st["amount"])
        most_popular_st = action_per_st[action_per_st["amount"] == max_uses].reset_index()
        most_popular_st["st_info"] = most_popular_st.apply(
            lambda row: f'station: {row[f"station_{category}"]}, dir: {row[f"address_{category}"]}',
            axis=1,
        )
        return most_popular_st

    @check_args_types
    def resume(self, unlock_st: bool = False) -> pd.Series:
        """
        Generates a summary of bike usage data, including total uses, total trip time,
        and information about the most popular station(s).

        This method performs the following steps:
            - Cleans the DataFrame by removing NaN values and formatting columns.
            - Retrieves information about the most popular station(s) based on unlock or lock
            actions.
            - Constructs a summary with total bike uses, total trip time, and details about the
            most popular station(s).

        Args:
            unlock_st (bool): If True, considers unlock actions; if False, considers lock actions.

        Returns:
            pd.Series: A Series containing the summary of bike usage data with the following
            information:
                - total_uses (int): The total number of bike trips recorded.
                - total_time (float): The total trip time in minutes, rounded to two decimal places.
                - most_popular_station (list): A list of formatted strings with information about
                the most popular station(s).
                - uses_from_most_popular (list): A list of counts representing the number of uses
                for the most popular station(s).
        """
        self.clean()
        info_most_popular_st = self.info_most_popular_stations(unlock_st)
        resume_data = {
            "total_uses": self.data.shape[0],
            "total_time": round(sum(self.data["trip_minutes"]), 2),
            "most_popular_station": info_most_popular_st["st_info"].tolist(),
            "uses_from_most_popular": info_most_popular_st["amount"].tolist(),
        }
        return pd.Series(resume_data)

    # C3
    @staticmethod
    @check_args_types
    def sum_hours(series: pd.Series) -> float:
        """
        Converts a Series of trip durations in minutes to hours and calculates the total.

        This function takes a Pandas Series containing durations in minutes,
        converts each duration to hours by dividing by 60,
        and returns the total sum of the durations in hours.

        Args:
            series (pd.Series): A Pandas Series containing trip durations in minutes.

        Returns:
            float: The total duration in hours, calculated from the input Series.
        """
        series = series.apply(lambda x: x / 60)
        return sum(series)

    def day_time(self) -> pd.Series:
        """
        Calculates the total trip duration in hours for each day from the DataFrame.

        This method performs the following steps:
            - Cleans the DataFrame by removing NaN values and formatting columns.
            - Groups the data by date and aggregates the total trip durations for each day.
            - Converts the total trip durations from minutes to hours using `sum_hours`.

        Returns:
            pd.Series: A Series indexed by date, containing the total trip duration in hours for
                        each day, with the name "total_hours".
        """
        self.clean()
        h_per_day = self.data.groupby(self.data.index)["trip_minutes"].agg(BiciMad.sum_hours)
        h_per_day.index = h_per_day.index.date
        h_per_day.name = "total_hours"
        return h_per_day

    # C4
    @staticmethod
    @check_args_types
    def get_weekday(date: pd.Timestamp) -> pd.DataFrame:
        """
        Converts a given date to its corresponding weekday abbreviation.

        Args:
            date (pd.Timestamp): A Pandas Timestamp representing the date.

        Returns:
            str: The abbreviation for the day of the week in Spanish.
        """
        days = {
            "Monday": "L",
            "Tuesday": "M",
            "Wednesday": "X",
            "Thursday": "J",
            "Friday": "V",
            "Saturday": "S",
            "Sunday": "D",
        }
        day = date.day_name()
        return days.get(day)

    def weekday_time(self) -> pd.Series:
        """
        Calculates the total trip duration in hours for each weekday from the DataFrame.

        This method performs the following steps:
            - Cleans the DataFrame by removing NaN values and formatting columns.
            - Creates a copy of the DataFrame and adds a new column for the weekday abbreviations.
            - Groups the data by weekday and aggregates the total trip durations for each weekday.
            - Converts the total trip durations from minutes to hours using `sum_hours` function.

        Returns:
            pd.Series: A Series indexed by weekday abbreviation, containing the total trip duration
                        in hours for each weekday, with the name "total_hours".
        """
        self.clean()
        df_copy = self.data.copy()
        df_copy["weekday"] = df_copy.index.to_series().apply(lambda x: BiciMad.get_weekday(x))
        w_hours = df_copy.groupby("weekday")["trip_minutes"].agg(BiciMad.sum_hours)
        w_hours.name = "total_hours"
        return w_hours

    # C5
    def total_usage_day(self) -> pd.Series:
        """
        Calculates the total number of bike usages per day from the DataFrame.

        This method performs the following steps:
            - Cleans the DataFrame by removing NaN values and formatting columns.
            - Groups the data by date and counts the total number of bike usages for each day.

        Returns:
            pd.Series: A Series indexed by date, containing the total number of bike usages for
            each day, with the name "total_usage".
        """
        self.clean()
        tot_usage = self.data.groupby(self.data.index)["idBike"].count()
        tot_usage.name = "total_usage"
        return tot_usage

    # C6
    def usage_by_date_and_unlock_st(self) -> pd.Series:
        """
        Calculates the number of bike usages per day, grouped by the unlock station.

        This method performs the following steps:
            - Cleans the DataFrame by removing NaN values and formatting columns.
            - Groups the data by date and unlock station, aggregating the total number of bike
            usages for each combination.

        Returns:
            pd.Series: A Series with a multi-index, where the first level is the date (grouped
                        daily)
                        and the second level is the unlock station. Each entry represents the total
                        number of bike usages for the corresponding date and unlock station.
        """
        self.clean()
        return self.data.groupby([pd.Grouper(freq="1D"), "station_unlock"]).agg(
            amount=("idBike", "count")
        )
