"""Plotly chart builders for the Morocco Weather History app."""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.config import get_location_arabic_name
from src.translations import AppText, bi


def _style_chart(
    figure: go.Figure,
    title_english: str,
    title_arabic: str,
    y_axis_english: str,
    y_axis_arabic: str,
) -> go.Figure:
    """Apply bilingual titles, labels, fonts, and formatting."""
    title_text = bi(
        title_english,
        title_arabic,
    )

    figure.update_layout(
        title=title_text,
        xaxis_title=bi(*AppText.date()),
        yaxis_title=bi(
            y_axis_english,
            y_axis_arabic,
        ),
        font={
            "family": "WeatherBilingual, Comfortaa, sans-serif",
            "size": 14,
            "color": "#E5E7EB",
        },
        hoverlabel={
            "font_family": "WeatherBilingual, Comfortaa, sans-serif",
            "font_color": "#E5E7EB",
            "bgcolor": "#111827",
            "bordercolor": "#14B8A6",
        },
        template="plotly_dark",
        height=500,
    )

    return figure

def create_daily_temperature_chart(
    data: pd.DataFrame,
    location: str,
    chart_type: str = "line",
) -> go.Figure:
    """Create a bilingual daily temperature chart."""
    text = AppText
    arabic_location = get_location_arabic_name(location)

    if chart_type == "box":
        temperature_columns = [
            column
            for column in (
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
            )
            if column in data.columns
        ]

        melted = data.melt(
            id_vars=["date"],
            value_vars=temperature_columns,
            var_name="variable",
            value_name="temperature",
        )

        figure = px.box(
            melted,
            x=melted["date"].dt.year,
            y="temperature",
            color="variable",
            points=False,
        )

        figure.update_layout(
            legend_title_text=bi(
                "Temperature type",
                "نوع درجة الحرارة",
            )
        )

    elif chart_type == "area":
        figure = go.Figure()

        if "temperature_2m_max" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["date"],
                    y=data["temperature_2m_max"],
                    mode="lines",
                    name=bi(*text.maximum_temperature()),
                    line={"color": "#F87171", "width": 2},
                    stackgroup="temperature",
                )
            )

        if "temperature_2m_min" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["date"],
                    y=data["temperature_2m_min"],
                    mode="lines",
                    name=bi(*text.minimum_temperature()),
                    line={"color": "#60A5FA", "width": 2},
                    stackgroup="temperature",
                )
            )

    elif chart_type == "bar":
        figure = go.Figure()

        if "temperature_2m_max" in data.columns:
            figure.add_trace(
                go.Bar(
                    x=data["date"],
                    y=data["temperature_2m_max"],
                    name=bi(*text.maximum_temperature()),
                    marker_color="#F87171",
                )
            )

        if "temperature_2m_min" in data.columns:
            figure.add_trace(
                go.Bar(
                    x=data["date"],
                    y=data["temperature_2m_min"],
                    name=bi(*text.minimum_temperature()),
                    marker_color="#60A5FA",
                )
            )

        figure.update_layout(barmode="group")

    else:
        figure = go.Figure()

        if "temperature_2m_max" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["date"],
                    y=data["temperature_2m_max"],
                    mode="lines",
                    name=bi(*text.maximum_temperature()),
                    line={"color": "#F87171", "width": 2},
                )
            )

        if "temperature_2m_min" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["date"],
                    y=data["temperature_2m_min"],
                    mode="lines",
                    name=bi(*text.minimum_temperature()),
                    line={"color": "#60A5FA", "width": 2},
                )
            )

    _apply_dark_bilingual_style(
        figure,
        *text.temperature_history(location),
        *text.date(),
        *text.temperature_celsius(),
    )

    return figure

def create_daily_precipitation_chart(
    data: "pd.DataFrame",
    location: str,
) -> go.Figure:
    """Create a bilingual daily precipitation chart."""
    text = AppText

    fig = go.Figure()

    if "precipitation_sum" in data.columns:
        fig.add_trace(
            go.Bar(
                x=data["date"],
                y=data["precipitation_sum"],
                name=bi(*text.precipitation()),
                marker_color="#4c9be8",
                hovertemplate=(
                    f"<b>%{{x|%Y-%m-%d}}</b><br>"
                    f"{bi(*text.precipitation())}: "
                    "%{y:.1f} mm<extra></extra>"
                ),
            )
        )

    return _style_chart(
        fig,
        *text.precipitation_history(location),
        *text.precipitation_mm(),
    )


def create_yearly_temperature_chart(
    data: "pd.DataFrame",
) -> go.Figure:
    """Create a bilingual yearly temperature trend chart."""
    text = AppText
    fig = go.Figure()

    if "temperature_2m_max" in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data["year"],
                y=data["temperature_2m_max"],
                mode="lines+markers",
                name=bi(*text.maximum_temperature()),
                line={"color": "#d62728", "width": 2},
            )
        )

    if "temperature_2m_min" in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data["year"],
                y=data["temperature_2m_min"],
                mode="lines+markers",
                name=bi(*text.minimum_temperature()),
                line={"color": "#1f77b4", "width": 2},
            )
        )

    fig.update_layout(
        title=bi(*text.yearly_temperature_trends()),
        font={"family": "WeatherBilingual, sans-serif"},
        template="plotly_white",
        height=450,
    )

    fig.update_xaxes(title_text=bi(*text.year()))
    fig.update_yaxes(title_text=bi(*text.temperature_celsius()))

    return fig


def create_yearly_precipitation_chart(
    data: "pd.DataFrame",
) -> go.Figure:
    """Create a bilingual yearly precipitation chart."""
    text = AppText
    fig = go.Figure()

    if "total_precipitation" in data.columns:
        fig.add_trace(
            go.Bar(
                x=data["year"],
                y=data["total_precipitation"],
                name=bi(*text.annual_precipitation()),
                marker_color="#4c9be8",
            )
        )

    fig.update_layout(
        title=bi(*text.yearly_precipitation_trends()),
        font={"family": "WeatherBilingual, sans-serif"},
        template="plotly_white",
        height=450,
    )

    fig.update_xaxes(title_text=bi(*text.year()))
    fig.update_yaxes(title_text=bi(*text.precipitation_mm()))

    return fig

def _apply_dark_bilingual_style(
    figure,
    title_english: str,
    title_arabic: str,
    x_english: str,
    x_arabic: str,
    y_english: str,
    y_arabic: str,
) -> None:
    """Apply the shared dark bilingual chart style."""
    figure.update_layout(
        title=bi(title_english, title_arabic),
        xaxis_title=bi(x_english, x_arabic),
        yaxis_title=bi(y_english, y_arabic),
        font={
            "family": "WeatherBilingual, Comfortaa, sans-serif",
            "size": 14,
            "color": "#E5E7EB",
        },
        hoverlabel={
            "font_family": "WeatherBilingual, Comfortaa, sans-serif",
            "font_color": "#E5E7EB",
            "bgcolor": "#111827",
            "bordercolor": "#14B8A6",
        },
        template="plotly_dark",
        height=500,
        margin=dict(l=40, r=20, t=70, b=50),
    )
    
def create_daily_precipitation_chart(
    data: pd.DataFrame,
    location: str,
    chart_type: str = "bar",
) -> go.Figure:
    """Create a bilingual daily precipitation chart."""
    text = AppText

    if chart_type == "area":
        figure = go.Figure()

        figure.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["precipitation_sum"],
                mode="lines",
                name=bi(*text.precipitation()),
                line={"color": "#38BDF8", "width": 2},
                fill="tozeroy",
                fillcolor="rgba(56, 189, 248, 0.25)",
            )
        )

    elif chart_type == "line":
        figure = go.Figure()

        figure.add_trace(
            go.Scatter(
                x=data["date"],
                y=data["precipitation_sum"],
                mode="lines",
                name=bi(*text.precipitation()),
                line={"color": "#38BDF8", "width": 2},
            )
        )

    else:
        figure = go.Figure()

        figure.add_trace(
            go.Bar(
                x=data["date"],
                y=data["precipitation_sum"],
                name=bi(*text.precipitation()),
                marker_color="#38BDF8",
            )
        )

    _apply_dark_bilingual_style(
        figure,
        *text.precipitation_history(location),
        *text.date(),
        *text.precipitation_mm(),
    )

    return figure

def create_monthly_temperature_chart(
    data: pd.DataFrame,
    location: str,
    chart_type: str = "line",
) -> go.Figure:
    """Create a bilingual monthly temperature chart."""
    text = AppText

    figure = go.Figure()

    if chart_type == "bar":
        if "temperature_2m_max" in data.columns:
            figure.add_trace(
                go.Bar(
                    x=data["month"],
                    y=data["temperature_2m_max"],
                    name=bi(*text.maximum_temperature()),
                    marker_color="#F87171",
                )
            )

        if "temperature_2m_min" in data.columns:
            figure.add_trace(
                go.Bar(
                    x=data["month"],
                    y=data["temperature_2m_min"],
                    name=bi(*text.minimum_temperature()),
                    marker_color="#60A5FA",
                )
            )

        figure.update_layout(barmode="group")

    elif chart_type == "area":
        if "temperature_2m_max" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["month"],
                    y=data["temperature_2m_max"],
                    mode="lines",
                    name=bi(*text.maximum_temperature()),
                    line={"color": "#F87171", "width": 2},
                    stackgroup="temperature",
                )
            )

        if "temperature_2m_min" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["month"],
                    y=data["temperature_2m_min"],
                    mode="lines",
                    name=bi(*text.minimum_temperature()),
                    line={"color": "#60A5FA", "width": 2},
                    stackgroup="temperature",
                )
            )

    else:
        if "temperature_2m_max" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["month"],
                    y=data["temperature_2m_max"],
                    mode="lines+markers",
                    name=bi(*text.maximum_temperature()),
                    line={"color": "#F87171", "width": 2},
                )
            )

        if "temperature_2m_min" in data.columns:
            figure.add_trace(
                go.Scatter(
                    x=data["month"],
                    y=data["temperature_2m_min"],
                    mode="lines+markers",
                    name=bi(*text.minimum_temperature()),
                    line={"color": "#60A5FA", "width": 2},
                )
            )

    _apply_dark_bilingual_style(
        figure,
        *text.temperature_history(location),
        *text.date(),
        *text.temperature_celsius(),
    )

    return figure

def create_monthly_precipitation_chart(
    data: pd.DataFrame,
    location: str,
    chart_type: str = "bar",
) -> go.Figure:
    """Create a bilingual monthly precipitation chart."""
    text = AppText

    if chart_type == "area":
        figure = go.Figure()

        figure.add_trace(
            go.Scatter(
                x=data["month"],
                y=data["total_precipitation"],
                mode="lines",
                name=bi(*text.annual_precipitation()),
                line={"color": "#38BDF8", "width": 2},
                fill="tozeroy",
                fillcolor="rgba(56, 189, 248, 0.25)",
            )
        )

    elif chart_type == "line":
        figure = go.Figure()

        figure.add_trace(
            go.Scatter(
                x=data["month"],
                y=data["total_precipitation"],
                mode="lines+markers",
                name=bi(*text.annual_precipitation()),
                line={"color": "#38BDF8", "width": 2},
            )
        )

    else:
        figure = go.Figure()

        figure.add_trace(
            go.Bar(
                x=data["month"],
                y=data["total_precipitation"],
                name=bi(*text.annual_precipitation()),
                marker_color="#38BDF8",
            )
        )

    _apply_dark_bilingual_style(
        figure,
        *text.precipitation_history(location),
        *text.date(),
        *text.precipitation_mm(),
    )

    return figure

