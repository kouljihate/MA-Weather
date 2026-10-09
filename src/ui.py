"""Reusable Streamlit UI components for the weather application."""

import pandas as pd
import streamlit as st

from src.config import (
    APP_NAME_EN,
    APP_VERSION,
    DEFAULT_VARIABLE_KEYS,
    EARLIEST_AVAILABLE_YEAR,
    MOROCCO_LOCATIONS,
    WEATHER_VARIABLES,
    get_current_year,
    get_location_arabic_name,
    get_location_coordinates,
    get_today_iso_date,
)
from src.translations import AppText, bi, bilingual_caption, bilingual_heading
from src.weather_service import WeatherServiceError, fetch_daily_weather
from src.charts import (
    create_daily_precipitation_chart,
    create_daily_temperature_chart,
    create_yearly_precipitation_chart,
    create_yearly_temperature_chart,
)


def _location_label(location: str) -> str:
    """Format a location for bilingual selection."""
    return bi(
        location,
        get_location_arabic_name(location),
    )


def _variable_label(variable) -> str:
    return bi(variable.english, variable.arabic)


def _variable_key(variable) -> str:
    return variable.key


def render_sidebar() -> tuple[str, int, int, list[str]]:
    """Render sidebar controls and return selected app settings."""
    text = AppText
    current_year = get_current_year()

    st.sidebar.header(bi(*text.sidebar_title()))
    bilingual_caption(*text.sidebar_version(APP_VERSION))

    selected_location = st.sidebar.selectbox(
        label=bi(*text.select_location()),
        options=list(MOROCCO_LOCATIONS),
        format_func=_location_label,
    )

    latitude, longitude = get_location_coordinates(selected_location)

    bilingual_caption(*text.coordinates(latitude, longitude))

    start_year = st.sidebar.slider(
        label=bi(*text.start_year()),
        min_value=EARLIEST_AVAILABLE_YEAR,
        max_value=current_year - 1,
        value=max(
            EARLIEST_AVAILABLE_YEAR,
            current_year - 50,
        ),
    )

    include_current_year = st.sidebar.checkbox(
        label=bi(*text.include_current_year(current_year)),
        value=True,
    )

    if include_current_year:
        end_year = current_year
        st.sidebar.warning(
            bi(*text.current_year_warning(
                current_year,
                get_today_iso_date(),
            ))
        )
    else:
        end_year = st.sidebar.slider(
            label=bi(*text.end_year()),
            min_value=start_year,
            max_value=current_year - 1,
            value=current_year - 1,
        )

    variables = st.sidebar.multiselect(
        label=bi(*text.weather_variables()),
        options=list(WEATHER_VARIABLES),
        default=[
            variable
            for variable in WEATHER_VARIABLES
            if variable.key in DEFAULT_VARIABLE_KEYS
        ],
        format_func=_variable_label,
    )

    return (
        selected_location,
        start_year,
        end_year,
        [variable.key for variable in variables],
    )


def render_metrics(data: pd.DataFrame) -> None:
    """Render bilingual climate summary metrics."""
    text = AppText

    col1, col2, col3, col4 = st.columns(4)

    if "temperature_2m_max" in data.columns:
        with col1:
            st.metric(
                label=bi(*text.average_max_temperature()),
                value=f"{data['temperature_2m_max'].mean():.1f} °C",
            )

        with col3:
            st.metric(
                label=bi(*text.highest_temperature()),
                value=f"{data['temperature_2m_max'].max():.1f} °C",
            )

    if "temperature_2m_min" in data.columns:
        with col2:
            st.metric(
                label=bi(*text.lowest_temperature()),
                value=f"{data['temperature_2m_min'].min():.1f} °C",
            )

    if "precipitation_sum" in data.columns:
        with col4:
            total = data["precipitation_sum"].sum(min_count=1)

            st.metric(
                label=bi(*text.total_precipitation()),
                value=f"{total:,.1f} mm",
            )


def render_charts(data: pd.DataFrame, location: str) -> None:
    """Render charts for selected weather variables."""
    text = AppText

    bilingual_heading(*text.interactive_charts())

    if {"temperature_2m_max", "temperature_2m_min"} & set(data.columns):
        st.plotly_chart(
            create_daily_temperature_chart(data, location),
            width="stretch",
            theme=None,
        )

    if "precipitation_sum" in data.columns:
        st.plotly_chart(
            create_daily_precipitation_chart(data, location),
            width="stretch",
            theme=None,
        )

    bilingual_heading(*text.yearly_trends())

    yearly_temperature = _create_yearly_temperature_data(data)

    if not yearly_temperature.empty:
        st.plotly_chart(
            create_yearly_temperature_chart(yearly_temperature),
            width="stretch",
            theme=None,
        )

    yearly_precipitation = _create_yearly_precipitation_data(data)

    if not yearly_precipitation.empty:
        st.plotly_chart(
            create_yearly_precipitation_chart(yearly_precipitation),
            width="stretch",
            theme=None,
        )


def _create_yearly_temperature_data(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate yearly temperature values."""
    temperature_columns = [
        column
        for column in (
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
        )
        if column in data.columns
    ]

    if not temperature_columns:
        return pd.DataFrame()

    return (
        data.groupby("year")[temperature_columns]
        .mean()
        .reset_index()
    )


def _create_yearly_precipitation_data(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate yearly precipitation values."""
    if "precipitation_sum" not in data.columns:
        return pd.DataFrame()

    return (
        data.groupby("year")["precipitation_sum"]
        .sum(min_count=1)
        .reset_index()
        .rename(columns={"precipitation_sum": "total_precipitation"})
    )


def render_data_table(
    data: pd.DataFrame,
    selected_variable_keys: list[str],
) -> None:
    """Render a bilingual raw-data table."""
    from src.config import WEATHER_VARIABLES

    text = AppText

    bilingual_heading(*text.raw_data())

    if not st.checkbox(bi(*text.show_data_table())):
        return

    variable_labels = {
        variable.key: bi(variable.english, variable.arabic)
        for variable in WEATHER_VARIABLES
    }

    display_columns = [
        "date",
        *[
            key
            for key in selected_variable_keys
            if key in data.columns
        ],
    ]

    labels = {
        "date": bi(*text.date()),
        **variable_labels,
    }

    st.dataframe(
        data[display_cols := display_cols].rename(columns=labels),
        width="stretch",
        height=400,
    )


def render_export(data: pd.DataFrame, filename: str) -> None:
    """Render the bilingual CSV export control."""
    text = AppText

    bilingual_heading(*text.export_data())

    st.download_button(
        label=bi(*text.download_csv()),
        data=data.to_csv(index=False).encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv",
    )