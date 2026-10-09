"""Bilingual English/Arabic translation helpers and UI text."""

from html import escape
from typing import Callable

import streamlit as st
from pathlib import Path


def bi(english: str, arabic: str) -> str:
    """Create a bilingual string for Streamlit widgets and Plotly charts."""
    return f"{english} | \u2067{arabic}\u2069"


def bilingual_heading(
    english: str,
    arabic: str,
    level: int = 2,
) -> None:
    """Render a bilingual heading with Arabic above English."""
    level = max(1, min(level, 6))

    st.markdown(
        f"""
        <div class="bilingual-heading bilingual-heading-{level}">
            <div lang="ar" dir="rtl" class="bilingual-arabic">
                {escape(arabic)}
            </div>
            <div lang="en" dir="ltr" class="bilingual-english">
                {escape(english)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def bilingual_caption(english: str, arabic: str) -> None:
    """Render a bilingual caption with Arabic above English."""
    st.markdown(
        f"""
        <div class="bilingual-caption">
            <div lang="ar" dir="rtl" class="bilingual-arabic">
                {escape(arabic)}
            </div>
            <div lang="en" dir="ltr" class="bilingual-english">
                {escape(english)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def bilingual_error(english: str, arabic: str) -> None:
    """Render a bilingual error message."""
    st.error(bi(english, arabic))


def bilingual_success(english: str, arabic: str) -> None:
    """Render a bilingual success message."""
    st.success(bi(english, arabic))


def bilingual_warning(english: str, arabic: str) -> None:
    """Render a bilingual warning message."""
    st.warning(bi(english, arabic))


def bilingual_info(english: str, arabic: str) -> None:
    """Render a bilingual information message."""
    st.info(bi(english, arabic))


CSS_FILE = Path(__file__).resolve().parent.parent / "static" / "css" / "app.css"


PROJECT_ROOT = Path(__file__).resolve().parent.parent

LUMEN_CSS_FILE = (
    PROJECT_ROOT
    / "static"
    / "themes"
    / "bs-lumen.css"
)

APP_CSS_FILE = (
    PROJECT_ROOT
    / "static"
    / "css"
    / "app.css"
)


def _read_css(path: Path) -> str:
    """Read a CSS file and return a helpful error if it is missing."""
    if not path.exists():
        st.warning(
            f"Stylesheet not found: {path.relative_to(PROJECT_ROOT)} | "
            f"لم يتم العثور على ملف التنسيق: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )
        return ""

    return path.read_text(encoding="utf-8")



PROJECT_ROOT = Path(__file__).resolve().parent.parent

LUMEN_CSS_FILE = (
    PROJECT_ROOT
    / "static"
    / "themes"
    / "bs-lumen.css"
)

APP_CSS_FILE = (
    PROJECT_ROOT
    / "static"
    / "css"
    / "app.css"
)


def _read_css(path: Path) -> str:
    """Read a CSS file and return a helpful error if it is missing."""
    if not path.exists():
        st.warning(
            f"Stylesheet not found: {path.relative_to(PROJECT_ROOT)} | "
            f"لم يتم العثور على ملف التنسيق: "
            f"{path.relative_to(PROJECT_ROOT)}"
        )
        return ""

    return path.read_text(encoding="utf-8")


def inject_bilingual_styles() -> None:
    """Load the Lumen theme and bilingual application styles."""
    lumen_css = _read_css(LUMEN_CSS_FILE)
    app_css = _read_css(APP_CSS_FILE)

    st.markdown(
        f"""
        <style>
        {lumen_css}

        {app_css}
        </style>
        """,
        unsafe_allow_html=True,
    )
            
class AppText:
    """Centralized bilingual application text."""

    @staticmethod
    def app_title() -> tuple[str, str]:
        return "Morocco Weather History", "سجل الطقس في المغرب"

    @staticmethod
    def app_subtitle() -> tuple[str, str]:
        return (
            "Historical weather estimates from ERA5 reanalysis.",
            "تقديرات الطقس التاريخية المستمدة من إعادة التحليل ERA5.",
        )

    @staticmethod
    def version(version: str, release_date: str) -> tuple[str, str]:
        return (
            f"Version {version} • Released {release_date}",
            f"الإصدار {version} • تاريخ الإصدار {release_date}",
        )

    @staticmethod
    def sidebar_title() -> tuple[str, str]:
        return "Configuration", "الإعدادات"

    @staticmethod
    def sidebar_version(version: str) -> tuple[str, str]:
        return (
            f"App version: {version}",
            f"إصدار التطبيق: {version}",
        )

    @staticmethod
    def select_location() -> tuple[str, str]:
        return "Select location", "اختر الموقع"

    @staticmethod
    def coordinates(latitude: float, longitude: float) -> tuple[str, str]:
        return (
            f"Coordinates: {latitude:.4f}, {longitude:.4f}",
            f"الإحداثيات: {latitude:.4f}, {longitude:.4f}",
        )

    @staticmethod
    def start_year() -> tuple[str, str]:
        return "Start year", "سنة البداية"

    @staticmethod
    def end_year() -> tuple[str, str]:
        return "End year", "سنة النهاية"

    @staticmethod
    def include_current_year(year: int) -> tuple[str, str]:
        return (
            f"Include {year} (partial year)",
            f"إدراج سنة {year} (سنة غير مكتملة)",
        )

    @staticmethod
    def current_year_warning(year: int, today: str) -> tuple[str, str]:
        return (
            f"⚠️ Data for {year} is available until {today}.",
            f"⚠️ بيانات سنة {year} متوفرة حتى {today}.",
        )

    @staticmethod
    def weather_variables() -> tuple[str, str]:
        return "Weather variables", "متغيرات الطقس"

    @staticmethod
    def load_data() -> tuple[str, str]:
        return "Load Weather Data", "تحميل بيانات الطقس"

    @staticmethod
    def loading_data() -> tuple[str, str]:
        return "Loading weather data...", "جارٍ تحميل بيانات الطقس..."

    @staticmethod
    def data_loaded(record_count: int) -> tuple[str, str]:
        return (
            f"Loaded {record_count:,} daily records.",
            f"تم تحميل {record_count:,} سجل يومي.",
        )

    @staticmethod
    def climate_summary() -> tuple[str, str]:
        return "Climate summary", "ملخص المناخ"

    @staticmethod
    def average_max_temperature() -> tuple[str, str]:
        return (
            "Average maximum temperature",
            "متوسط الحرارة القصوى",
        )

    @staticmethod
    def lowest_temperature() -> tuple[str, str]:
        return "Lowest temperature", "أدنى درجة حرارة"

    @staticmethod
    def highest_temperature() -> tuple[str, str]:
        return "Highest temperature", "أعلى درجة حرارة"

    @staticmethod
    def total_precipitation() -> tuple[str, str]:
        return "Total precipitation", "مجموع التساقطات"

    @staticmethod
    def interactive_charts() -> tuple[str, str]:
        return "Interactive charts", "الرسوم البيانية التفاعلية"

    @staticmethod
    def yearly_trends() -> tuple[str, str]:
        return "Yearly climate trends", "تطور المناخ حسب السنة"

    @staticmethod
    def raw_data() -> tuple[str, str]:
        return "Raw data", "البيانات التفصيلية"

    @staticmethod
    def show_data_table() -> tuple[str, str]:
        return "Show data table", "عرض جدول البيانات"

    @staticmethod
    def export_data() -> tuple[str, str]:
        return "Export data", "تصدير البيانات"

    @staticmethod
    def download_csv() -> tuple[str, str]:
        return "Download CSV", "تحميل ملف CSV"

    @staticmethod
    def data_load_error() -> tuple[str, str]:
        return (
            "Unable to load weather data.",
            "تعذر تحميل بيانات الطقس.",
        )

    @staticmethod
    def no_data_to_show() -> tuple[str, str]:
        return (
            "No data available to show trends.",
            "لا توجد بيانات متاحة لعرض التطور.",
        )

    @staticmethod
    def temperature_history(location: str) -> tuple[str, str]:
        return (
            f"Temperature history — {location}",
            f"سجل درجات الحرارة — {location}",
        )

    @staticmethod
    def precipitation_history(location: str) -> tuple[str, str]:
        return (
            f"Precipitation history — {location}",
            f"سجل التساقطات — {location}",
        )

    @staticmethod
    def yearly_temperature_trends() -> tuple[str, str]:
        return (
            "Yearly average temperature trends",
            "تطور متوسط درجات الحرارة حسب السنة",
        )

    @staticmethod
    def yearly_precipitation_trends() -> tuple[str, str]:
        return (
            "Yearly total precipitation",
            "مجموع التساقطات حسب السنة",
        )

    @staticmethod
    def date() -> tuple[str, str]:
        return "Date", "التاريخ"

    @staticmethod
    def year() -> tuple[str, str]:
        return "Year", "السنة"

    @staticmethod
    def temperature_celsius() -> tuple[str, str]:
        return "Temperature (°C)", "درجة الحرارة (°C)"

    @staticmethod
    def precipitation_mm() -> tuple[str, str]:
        return "Precipitation (mm)", "التساقطات (مم)"

    @staticmethod
    def maximum_temperature() -> tuple[str, str]:
        return (
            "Maximum temperature",
            "درجة الحرارة القصوى",
        )

    @staticmethod
    def minimum_temperature() -> tuple[str, str]:
        return (
            "Minimum temperature",
            "درجة الحرارة الدنيا",
        )

    @staticmethod
    def precipitation() -> tuple[str, str]:
        return "Precipitation", "التساقطات"

    @staticmethod
    def annual_precipitation() -> tuple[str, str]:
        return "Annual precipitation", "التساقطات السنوية"

    @staticmethod
    def app_footer(version: str) -> tuple[str, str]:
        return (
            f"Morocco Weather History • Version {version}",
            f"سجل الطقس في المغرب • الإصدار {version}",
        )
    
    @staticmethod
    def chart_period() -> tuple[str, str]:
        return "Chart period", "فترة الرسم البياني"

    @staticmethod
    def day_by_day() -> tuple[str, str]:
        return "Day by day", "يوم بيوم"

    @staticmethod
    def month_by_month() -> tuple[str, str]:
        return "Month by month", "شهر بشهر"

    @staticmethod
    def chart_type() -> tuple[str, str]:
        return "Chart type", "نوع الرسم البياني"

    @staticmethod
    def line_chart() -> tuple[str, str]:
        return "Line chart", "رسم خطي"

    @staticmethod
    def area_chart() -> tuple[str, str]:
        return "Area chart", "رسم مساحي"

    @staticmethod
    def bar_chart() -> tuple[str, str]:
        return "Bar chart", "رسم أعمدة"

    @staticmethod
    def box_chart() -> tuple[str, str]:
        return "Distribution box plot", "مخطط صندوقي للتوزيع"

    @staticmethod
    def no_monthly_data() -> tuple[str, str]:
        return (
            "No data available for monthly charts.",
            "لا توجد بيانات متاحة للرسوم البيانية الشهرية.",
        )
        