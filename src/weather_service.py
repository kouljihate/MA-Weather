"""Service for retrieving historical weather data from Open-Meteo."""

from datetime import date

import pandas as pd
import requests
import streamlit as st

from src.config import (
    API_BASE_URL,
    API_TIMEOUT_SECONDS,
    CACHE_TTL_SECONDS,
)


class WeatherServiceError(Exception):
    """Raised when historical weather data cannot be retrieved."""


def _resolve_end_date(end_year: int) -> str:
    """Return a valid end date accepted by the historical API."""
    current_year = date.today().year

    if end_year >= current_year:
        return date.today().isoformat()

    return f"{end_year}-12-31"


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_daily_weather(
    latitude: float,
    longitude: float,
    start_year: int,
    end_year: int,
    variable_keys: tuple[str, ...],
) -> pd.DataFrame:
    """Fetch daily historical weather data and return a DataFrame."""
    response = None

    try:
        response = requests.get(
            API_BASE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": f"{start_year}-01-01",
                "end_date": _resolve_end_date(end_year),
                "daily": list(variable_keys := variable_keys),
                "timezone": "auto",
            },
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        payload = response.json()

        if "daily" not in payload or "time" not in payload["daily"]:
            raise WeatherServiceError(
                "The weather API did not return daily data."
            )

        daily = payload["daily"]

        data = {"date": pd.to_datetime(daily["time"])}

        for key in variable_keys:
            if key in daily:
                data[key] = daily[key]

        frame = pd.DataFrame(data)

        frame["year"] = frame["date"].dt.year
        frame["month"] = frame["date"].dt.month
        frame["day"] = frame["date"].dt.day

        return frame

    except requests.HTTPError as error:
        detail = response.text if response is not None else ""
        raise WeatherServiceError(
            f"Open-Meteo API request failed: {error}. {detail}"
        ) from error

    except (requests.RequestException, ValueError) as error:
        raise WeatherServiceError(
            f"Unable to retrieve weather data: {error}"
        ) from error