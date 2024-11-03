import numpy as np
import pandas as pd
import pytest
from BiciMad.BiciMad import BiciMad
from pandas.testing import assert_frame_equal, assert_series_equal


def test_str():
    bicimad_obj = BiciMad(5, 22)
    assert bicimad_obj.__str__() == bicimad_obj.data.__str__()


def test_month():
    bicimad_obj = BiciMad(5, 22)
    assert bicimad_obj.month == 5


def test_year():
    bicimad_obj = BiciMad(5, 22)
    assert bicimad_obj.year == 22


delete_nan_rows_test_cases = [
    (2, 23, 168494),
    (1, 22, 244760),
    (9, 21, 410216),
]


@pytest.mark.parametrize("month, year, expected", delete_nan_rows_test_cases)
def test_delete_nan_rows(month, year, expected):
    bicimad_obj = BiciMad(month, year)
    bicimad_obj.delete_nan_rows()
    assert bicimad_obj.data.shape[0] == expected


float_to_str_test_cases = [
    (2, 23, "fleet", "object"),
    (1, 22, "idBike", "object"),
    (9, 21, "station_lock", "object"),
    (9, 21, 1, TypeError),
]


@pytest.mark.parametrize("month, year, col, expected", float_to_str_test_cases)
def test_float_to_str(month, year, col, expected):
    bicimad_obj = BiciMad(month, year)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            bicimad_obj.float_to_str(col)
    else:
        assert bicimad_obj.data[col].dtype == "float64"
        bicimad_obj.float_to_str(col)
        assert bicimad_obj.data[col].dtype == expected


format_strings_test_cases = [
    ("  'Needs formatting' ", "Needs formatting"),
    ("'address to my house'", "address to my house"),
    ("' Address 1 ' ", "Address 1"),
    (" 'new address    ", "'new address"),
    ("Random sring", "Random sring"),
    (2, TypeError),
    (["str1", "  'str2' "], TypeError),
]


@pytest.mark.parametrize("content, expected", format_strings_test_cases)
def test_format_strings(content, expected):
    bicimad_obj = BiciMad(2, 23)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            bicimad_obj.format_strings(content)
    else:
        result = bicimad_obj.format_strings(content)
        assert result == expected


format_string_col_test_cases = [
    (2, 23, "address_unlock", "'address 1 '", "address 1"),
    (5, 22, "address_lock", " address 3", "address 3"),
    (12, 21, "address_unlock", "address 5", "address 5"),
]


@pytest.mark.parametrize("month, year, col, value, expected", format_string_col_test_cases)
def test_format_string_col(month, year, col, value, expected):
    bicimad_obj = BiciMad(month, year)
    bicimad_obj.delete_nan_rows()
    bicimad_obj.data.iloc[0, bicimad_obj.data.columns.get_loc(col)] = value
    n_nans = int(bicimad_obj.data[col].isna().sum())

    bicimad_obj.format_string_col(col)
    n_not_found = int(bicimad_obj.data[col].value_counts().get("not_found", 0))
    assert n_nans == n_not_found
    assert bicimad_obj.data.iloc[0, bicimad_obj.data.columns.get_loc(col)] == expected


clean_test_cases = [
    (2, 23, 168494),
    (5, 22, 477934),
    (7, 21, 416464),
]


@pytest.mark.parametrize("month, year, expected_size", clean_test_cases)
def test_clean(month, year, expected_size):
    bicimad_obj = BiciMad(month, year)

    bicimad_obj.clean()
    for var in ["fleet", "idBike", "station_lock", "station_unlock"]:
        assert bicimad_obj.data[var].dtype == "object"

    assert bicimad_obj.data.shape[0] == expected_size


info_most_popular_stations_test_cases = [
    (
        7,
        21,
        True,
        pd.DataFrame(
            {
                "station_unlock": "43",
                "address_unlock": "not_found",
                "amount": 4990,
                "st_info": "station: 43, dir: not_found",
            },
            index=[0],
        ),
    ),
    (
        4,
        22,
        False,
        pd.DataFrame(
            {
                "station_lock": "43",
                "address_lock": "Plaza de la Cebada nº 16",
                "amount": 3279,
                "st_info": "station: 43, dir: Plaza de la Cebada nº 16",
            },
            index=[0],
        ),
    ),
    (
        7,
        21,
        True,
        pd.DataFrame(
            {
                "station_unlock": "43",
                "address_unlock": "not_found",
                "amount": 4990,
                "st_info": "station: 43, dir: not_found",
            },
            index=[0],
        ),
    ),
    (7, 21, 1, TypeError),
]


@pytest.mark.parametrize("month, year, unlock_str, expected", info_most_popular_stations_test_cases)
def test_info_most_popular_stations(month, year, unlock_str, expected):
    bicimad_obj = BiciMad(month, year)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            bicimad_obj.info_most_popular_stations(unlock_str)
    else:
        result = bicimad_obj.info_most_popular_stations(unlock_str)
        assert_frame_equal(result, expected, check_exact=False, atol=1e-7)


resume_test_cases = [
    (
        1,
        23,
        True,
        pd.Series(
            [295923, 7044801.65, ["station: 57, dir: Calle Valencia nº 1"], [3752]],
            index=["total_uses", "total_time", "most_popular_station", "uses_from_most_popular"],
        ),
    ),
    (
        2,
        22,
        True,
        pd.Series(
            [280375, 5702148.11, ["station: 43, dir: not_found"], [3276]],
            index=["total_uses", "total_time", "most_popular_station", "uses_from_most_popular"],
        ),
    ),
    (
        11,
        22,
        False,
        pd.Series(
            [358394, 8105208.35, ["station: 43, dir: Plaza de la Cebada nº 16"], [4275]],
            index=["total_uses", "total_time", "most_popular_station", "uses_from_most_popular"],
        ),
    ),
    (11, 22, "True", TypeError),
]


@pytest.mark.parametrize("month, year, unlock_str, expected", resume_test_cases)
def test_resume(month, year, unlock_str, expected):
    bicimad_obj = BiciMad(month, year)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            bicimad_obj.resume(unlock_str)
    else:
        result = bicimad_obj.resume(unlock_str)
        assert_series_equal(result, expected, check_exact=False, atol=1e-7)


sum_hours_test_cases = [
    (pd.Series([2, 4, 5, 8, 77]), 1.6),
    (pd.Series([60]), 1.0),
    ([1, 4, 6, 32, 5], TypeError),
]


@pytest.mark.parametrize("input, expected", sum_hours_test_cases)
def test_sum_hours(input, expected):
    bicimad_obj = BiciMad(11, 22)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            bicimad_obj.sum_hours(input)
    else:
        result = bicimad_obj.sum_hours(input)
        assert result == expected


day_time_test_cases = [
    (6, 21, np.float64(201773.85550000134)),
    (8, 21, np.float64(142834.8001666674)),
    (12, 21, np.float64(150893.51050000035)),
]


@pytest.mark.parametrize("month, year, expected", day_time_test_cases)
def test_day_time(month, year, expected):
    bicimad_obj = BiciMad(month, year)
    result = bicimad_obj.day_time().sum()
    assert result == expected


get_weekdays_test_cases = [
    (pd.Timestamp("2024-10-22"), "M"),
    (pd.Timestamp("2024-10-23"), "X"),
    ("2024-10-24", TypeError),
    (1, TypeError),
]


@pytest.mark.parametrize("input, expected", get_weekdays_test_cases)
def test_get_weekday(input, expected):
    bicimad_obj = BiciMad(12, 21)

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            bicimad_obj.get_weekday(input)
    else:
        result = bicimad_obj.get_weekday(input)
        assert result == expected


weekday_time_test_cases = [
    (12, 21, np.float64(150893.51050000018)),
    (10, 22, np.float64(146955.2854999999)),
    (6, 22, np.float64(148653.00649999944)),
]


@pytest.mark.parametrize("month, year, expected", weekday_time_test_cases)
def test_weekday_time(month, year, expected):
    bicimad_obj = BiciMad(month, year)

    result = bicimad_obj.weekday_time().sum()
    assert result == expected


total_usage_day_test_cases = [
    (6, 21, np.int64(493631)),
    (8, 21, np.int64(292704)),
    (4, 22, np.int64(278852)),
]


@pytest.mark.parametrize("month, year, expected", total_usage_day_test_cases)
def test_total_usage_day(month, year, expected):
    bicimad_obj = BiciMad(month, year)

    result = bicimad_obj.total_usage_day().sum()
    assert result == expected


usage_by_date_and_unlock_st_test_cases = [
    (5, 22, 11297),
    (9, 22, 7698),
    (12, 21, 7941),
]


@pytest.mark.parametrize("month, year, expected", usage_by_date_and_unlock_st_test_cases)
def test_usage_by_date_and_unlock_st(month, year, expected):
    bicimad_obj = BiciMad(month, year)

    result = bicimad_obj.usage_by_date_and_unlock_st().shape[0]
    assert result == expected
