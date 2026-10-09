"""Morocco Weather History — bilingual Streamlit application."""

import pandas as pd
import streamlit as st

from src.config import (
    APP_NAME_EN,
    APP_NAME_AR,
    APP_RELEASE_DATE,
    APP_VERSION,
    get_location_coordinates,
)
from src.translations import (
    AppText,
    bi,
    bilingual_caption,
    bilingual_error,
    bilingual_heading,
    bilingual_success,
    inject_bilingual_styles,
)
from src.ui import (
    render_charts,
    render_data_table,
    render_export,
    render_metrics,
    render_sidebar,
)
from src.weather_service import WeatherServiceError, fetch_daily_weather



def render_header() -> None:
    """Render the bilingual application header."""
    text = AppText

    bilingual_heading(
        APP_NAME_EN,
        APP_NAME_AR,
        level=1,
    )

    bilingual_caption(
        *text.version(APP_VERSION, APP_RELEASE_DATE)
    )

    st.divider()
    st.write(bi(*text.app_subtitle()))


def load_weather_data(
    location: str,
    start_year: int,
    end_year: int,
    variable_keys: list[str],
) -> pd.DataFrame | None:
    """Load weather data and display bilingual status messages."""
    text = AppText

    latitude, longitude = get_location_coordinates(location)

    try:
        with st.spinner(bi(*text.loading_data())):
            return fetch_daily_weather(
                latitude=latitude,
                longitude=longitude,
                start_year=start_year,
                end_year=end_year,
                variable_keys=tuple(variable_keys),
            )

    except WeatherServiceError as error:
        bilingual_error(*text.data_load_error())
        st.code(str(error), language="text")
        return None


def render_weather_results(
    data: pd.DataFrame,
    location: str,
    variable_keys: list[str],
    start_year: int,
    end_year: int,
) -> None:
    """Render all results for the selected weather data."""
    text = AppText

    bilingual_heading(
        *text.climate_summary(),
        level=2,
    )

    render_metrics(data)
    render_charts(data, location)
    render_data_table(data, variable_keys)

    filename = (
        f"morocco_weather_{location}_{start_year}_{end_year}.csv"
    )

    render_export(data, filename)


def main() -> None:
    st.set_page_config(
        page_title="Morocco Weather History",
        page_icon="🇲🇦",
        layout="wide",
    )
    
    inject_bilingual_styles()
    render_header()

    location, start_year, end_year, variable_keys = render_sidebar()

    if st.sidebar.button(
        label=bi(*AppText.load_data()),
        type="primary",
    ):
        data = load_weather_data(
            location=location,
            start_year=start_year,
            end_year=end_year,
            variable_keys=variable_keys,
        )

        if data is not None and not data.empty:
            st.session_state["weather_data"] = data
            st.session_state["weather_location"] = location
            st.session_state["weather_variables"] = variable_keys
            st.session_state["weather_start_year"] = start_year
            st.session_state["weather_end_year"] = end_year

            bilingual_success(
                *AppText.data_loaded(len(data))
            )

    if "weather_data" not in st.session_state:
        st.info(bi(*AppText.app_subtitle()))
        return

    render_weather_results(
        data=st.session_state["weather_data"],
        location=st.session_state["weather_location"],
        variable_keys=st.session_state["weather_variables"],
        start_year=st.session_state["weather_start_year"],
        end_year=st.session_state["weather_end_year"],
    )

    bilingual_caption(
        *AppText.app_footer(APP_VERSION)
    )


if __name__ == "__main__":
    main()