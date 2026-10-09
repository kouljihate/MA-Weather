"""Application configuration and Morocco location data."""

from dataclasses import dataclass
from datetime import date


APP_NAME_EN = "Morocco Weather History"
APP_NAME_AR = "سجل الطقس في المغرب"
APP_VERSION = "1.2.0"
APP_RELEASE_DATE = "2026-10-09 15:15"

API_BASE_URL = "https://archive-api.open-meteo.com/v1/era5"
API_TIMEOUT_SECONDS = 30
CACHE_TTL_SECONDS = 3600

DEFAULT_START_YEAR = 1974
EARLIEST_AVAILABLE_YEAR = 1940

LATIN_FONT_URL = "app/static/fonts/Comfortaa-Regular.ttf"
ARABIC_FONT_URL = "app/static/fonts/VIP-RAWY-REGULAR.ttf"
BILINGUAL_FONT_FAMILY = "WeatherBilingual"


@dataclass(frozen=True)
class WeatherVariable:
    """A weather variable supported by the Open-Meteo API."""

    key: str
    english: str
    arabic: str


WEATHER_VARIABLES = (
    WeatherVariable(
        "temperature_2m_max",
        "Maximum temperature",
        "درجة الحرارة القصوى",
    ),
    WeatherVariable(
        "temperature_2m_min",
        "Minimum temperature",
        "درجة الحرارة الدنيا",
    ),
    WeatherVariable(
        "temperature_2m_mean",
        "Mean temperature",
        "متوسط درجة الحرارة",
    ),
    WeatherVariable(
        "precipitation_sum",
        "Total precipitation",
        "مجموع التساقطات",
    ),
    WeatherVariable(
        "wind_speed_10m_max",
        "Maximum wind speed",
        "أقصى سرعة للرياح",
    ),
    WeatherVariable(
        "shortwave_radiation_sum",
        "Solar radiation",
        "الإشعاع الشمسي",
    ),
)

DEFAULT_VARIABLE_KEYS = (
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
)

MOROCCO_LOCATIONS = {
    "Casablanca": (33.5731, -7.5898),
    "Rabat": (34.0209, -6.8416),
    "Marrakech": (31.6295, -7.9811),
    "Fes": (34.0181, -5.0078),
    "Tangier": (35.7595, -5.8340),
    "Agadir": (30.4278, -9.5981),
    "Meknes": (33.8935, -5.5473),
    "Oujda": (34.6867, -1.9114),
    "Kenitra": (34.2610, -6.5802),
    "Tetouan": (35.5889, -5.3626),
    "Safi": (32.2994, -9.2372),
    "Mohammedia": (33.6866, -7.3833),
    "Khouribga": (32.8811, -6.9063),
    "Beni Mellal": (32.3373, -6.3498),
    "El Jadida": (33.2316, -8.5007),
    "Taza": (34.2133, -4.0103),
    "Nador": (35.1681, -2.9287),
    "Settat": (33.0013, -7.5844),
    "Larache": (35.1933, -6.1563),
    "Ksar El Kebir": (35.0017, -5.9078),
    "Khemisset": (33.8242, -6.0661),
    "Guelmim": (28.9870, -10.0574),
    "Berrechid": (33.2651, -7.5844),
    "Ouarzazate": (30.9335, -6.9370),
    "Errachidia": (31.9314, -4.4244),
    "Laayoune": (27.1536, -13.1994),
    "Dakhla": (23.6848, -15.9582),
    "Sefrou": (33.8319, -4.8280),
    "Azghar": (33.6181, -4.7290),
    "Mtarnagha": (33.7222, -4.3914),
}

LOCATION_ARABIC_NAMES = {
    "Casablanca": "الدار البيضاء",
    "Rabat": "الرباط",
    "Marrakech": "مراكش",
    "Fes": "فاس",
    "Tangier": "طنجة",
    "Agadir": "أكادير",
    "Meknes": "مكناس",
    "Oujda": "وجدة",
    "Kenitra": "القنيطرة",
    "Tetouan": "تطوان",
    "Safi": "آسفي",
    "Mohammedia": "المحمدية",
    "Khouribga": "خريبكة",
    "Beni Mellal": "بني ملال",
    "El Jadida": "الجديدة",
    "Taza": "تازة",
    "Nador": "الناظور",
    "Settat": "سطات",
    "Larache": "العرائش",
    "Ksar El Kebir": "القصر الكبير",
    "Khemisset": "الخميسات",
    "Guelmim": "كلميم",
    "Berrechid": "برشيد",
    "Ouarzazate": "ورزازات",
    "Errachidia": "الرشيدية",
    "Laayoune": "العيون",
    "Dakhla": "الداخلة",
    "Sefrou": "صفرو",
    "Azghar": "أزغار",
    "Mtarnagha": "مطَرْناغة",
}


def get_current_year() -> int:
    """Return the current calendar year."""
    return date.today().year


def get_today_iso_date() -> str:
    """Return today's date in ISO format."""
    return date.today().isoformat()


def get_location_coordinates(location: str) -> tuple[float, float]:
    """Return latitude and longitude for a location."""
    return MOROCCO_LOCATIONS[location]


def get_location_arabic_name(location: str) -> str:
    """Return the Arabic display name for a location."""
    return LOCATION_ARABIC_NAMES.get(location, location)


def get_default_variable_keys() -> list[str]:
    """Return the default weather-variable keys."""
    return list(DEFAULT_VARIABLE_KEYS)