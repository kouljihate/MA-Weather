# app.py - Morocco Weather History (1940-2026)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import requests

APP_NAME = "Morocco Weather History"
APP_VERSION = "1.0.0"
APP_RELEASE_DATE = "2026-10-09"

st.set_page_config(
    page_title=f"{APP_NAME} | v{APP_VERSION}",
    page_icon="🇲🇦",
    layout="wide"
)


# Morocco regions with coordinates
MOROCCO_REGIONS = {
    "Azghar**": (33.6181, -4.7290),
    "Mtarnagha**": (33.7222, -4.3914),
    "Sefrou": (33.8283, -4.8283),
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

@st.cache_data(ttl=3600)
def fetch_weather_data(lat, lon, start_year, end_year, variables):
    """Fetch historical weather data from Open-Meteo ERA5 API"""
    base_url = "https://archive-api.open-meteo.com/v1/era5"
    
    # Get today's date to validate end_year
    today = date.today()
    
    # If end_year is current year, limit to today's date
    if end_year == today.year:
        end_date = today.strftime("%Y-%m-%d")
    else:
        end_date = f"{end_year}-12-31"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": f"{start_year}-01-01",
        "end_date": end_date,
        "daily": variables,
        "timezone": "auto"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Check if data exists
        if 'daily' not in data or 'time' not in data['daily']:
            st.error("No data returned from API")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame({
            'date': pd.to_datetime(data['daily']['time']),
            **{var: data['daily'][var] for var in variables if var in data['daily']}
        })
        
        # Add derived columns
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        
        return df
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}")
        if response.text:
            st.error(f"Response: {response.text}")
        st.error("Tip: Make sure end_date doesn't exceed today's date")
        return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def create_temperature_chart(df, region):
    """Create interactive temperature chart"""
    fig = go.Figure()
    
    if 'temperature_2m_max' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temperature_2m_max'],
            mode='lines',
            name='Max Temp',
            line=dict(color='red', width=1),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Max: %{y:.1f}°C<extra></extra>'
        ))
    
    if 'temperature_2m_min' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['temperature_2m_min'],
            mode='lines',
            name='Min Temp',
            line=dict(color='blue', width=1),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Min: %{y:.1f}°C<extra></extra>'
        ))
    
    fig.update_layout(
        title=f"🌡️ Temperature History - {region}",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        showlegend=True
    )
    
    return fig

def create_precipitation_chart(df, region):
    """Create precipitation chart"""
    fig = go.Figure()
    
    if 'precipitation_sum' in df.columns:
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['precipitation_sum'],
            name='Precipitation',
            marker_color='skyblue',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Rain: %{y:.1f} mm<extra></extra>'
        ))
    
    fig.update_layout(
        title=f"🌧️ Precipitation History - {region}",
        xaxis_title="Date",
        yaxis_title="Precipitation (mm)",
        height=400,
        template='plotly_white'
    )
    
    return fig

# Main app
st.title(f"🇲🇦 {APP_NAME}")
st.caption(
    f"Version {APP_VERSION} • Released {APP_RELEASE_DATE}"
)
st.markdown("""
Historical weather data from **ERA5 reanalysis** - gap-free hourly data from 1940 to present.
Data source: Open-Meteo Historical Weather API (free, no API key required)
""")

# Sidebar controls
st.sidebar.header("⚙️ Configuration")

# Region selection
selected_region = st.sidebar.selectbox(
    "Select Region",
    list(MOROCCO_REGIONS.keys()),
    index=0
)

lat, lon = MOROCCO_REGIONS[selected_region]
st.sidebar.info(f"**Coordinates:** {lat:.4f}, {lon:.4f}")

# Date range - FIXED: Get current year and limit end year
current_year = datetime.now().year
current_month = datetime.now().month

min_year = st.sidebar.slider("Start Year", 1940, current_year - 1, 1974)

# Show warning if selecting current year
if st.sidebar.checkbox(f"Include {current_year} (partial year)", value=True):
    max_year = current_year
    st.sidebar.warning(f"⚠️ {current_year} data only available until {date.today().strftime('%Y-%m-%d')}")
else:
    max_year = st.sidebar.slider("End Year", min_year + 1, current_year - 1, current_year - 1)

# Variables selection
st.sidebar.subheader("Weather Variables")
available_vars = [
    "temperature_2m_max",
    "temperature_2m_min", 
    "temperature_2m_mean",
    "precipitation_sum",
    "windspeed_10m_max",
    "shortwave_radiation_sum",
    "relativehumidity_2m_mean",
    "pressure_msl_mean"
]

variables = st.sidebar.multiselect(
    "Select variables to display",
    available_vars,
    default=["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
)

# Fetch data button
if st.sidebar.button("🔄 Load Weather Data", type="primary"):
    with st.spinner(f"Loading {max_year - min_year + 1} years of data for {selected_region}..."):
        weather_df = fetch_weather_data(lat, lon, min_year, max_year, variables)
        
        if weather_df is not None and len(weather_df) > 0:
            st.session_state['weather_data'] = weather_df
            st.session_state['region'] = selected_region
            st.success(f"✅ Loaded {len(weather_df):,} daily records ({min_year}-{max_year})")

# Display data if available
if 'weather_data' in st.session_state:
    df = st.session_state['weather_data']
    region = st.session_state['region']
    
    # Key metrics
    st.subheader(f"📊 Climate Summary for {region}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'temperature_2m_max' in df.columns:
            avg_temp = df['temperature_2m_max'].mean()
            st.metric("Avg Max Temp", f"{avg_temp:.1f}°C")
    
    with col2:
        if 'temperature_2m_min' in df.columns:
            min_temp = df['temperature_2m_min'].min()
            st.metric("Lowest Temp", f"{min_temp:.1f}°C")
    
    with col3:
        if 'temperature_2m_max' in df.columns:
            max_temp = df['temperature_2m_max'].max()
            st.metric("Highest Temp", f"{max_temp:.1f}°C")
    
    with col4:
        if 'precipitation_sum' in df.columns:
            total_rain = df['precipitation_sum'].sum()
            st.metric("Total Precipitation", f"{total_rain:,.0f} mm")
    
    # Interactive charts
    st.subheader("📈 Interactive Charts")
    
    # Temperature chart
    if 'temperature_2m_max' in df.columns or 'temperature_2m_min' in df.columns:
        temp_fig = create_temperature_chart(df, region)
        st.plotly_chart(temp_fig, width='stretch')
    
    # Precipitation chart
    if 'precipitation_sum' in df.columns:
        precip_fig = create_precipitation_chart(df, region)
        st.plotly_chart(precip_fig, width='stretch')
    
    # Yearly trends - FIXED: Show only selected variables
    st.subheader("📅 Yearly Climate Trends")
    
    # Build aggregation dict based on selected variables
    agg_dict = {}
    show_temp_chart = False
    
    if 'temperature_2m_max' in df.columns:
        agg_dict['temperature_2m_max'] = 'mean'
        show_temp_chart = True
    if 'temperature_2m_min' in df.columns:
        agg_dict['temperature_2m_min'] = 'mean'
        show_temp_chart = True
    if 'temperature_2m_mean' in df.columns:
        agg_dict['temperature_2m_mean'] = 'mean'
        show_temp_chart = True
    
    # Only create yearly data if we have columns to aggregate
    if agg_dict:
        yearly_data = df.groupby('year').agg(agg_dict).reset_index()
        
        # Add precipitation if available
        if 'precipitation_sum' in df.columns:
            yearly_precip = df.groupby('year')['precipitation_sum'].sum().reset_index()
            yearly_precip.columns = ['year', 'total_precipitation']
            yearly_data = yearly_data.merge(yearly_precip, on='year', how='outer')
        
        # Show temperature trend chart ONLY if temperature data exists
        if show_temp_chart:
            fig_trend = go.Figure()
            
            if 'temperature_2m_max' in yearly_data.columns:
                fig_trend.add_trace(go.Scatter(
                    x=yearly_data['year'],
                    y=yearly_data['temperature_2m_max'],
                    mode='lines+markers',
                    name='Avg Max Temp',
                    line=dict(color='red', width=2)
                ))
            
            if 'temperature_2m_min' in yearly_data.columns:
                fig_trend.add_trace(go.Scatter(
                    x=yearly_data['year'],
                    y=yearly_data['temperature_2m_min'],
                    mode='lines+markers',
                    name='Avg Min Temp',
                    line=dict(color='blue', width=2)
                ))
            
            fig_trend.update_layout(
                title="🌡️ Yearly Average Temperature Trends",
                xaxis_title="Year",
                yaxis_title="Temperature (°C)",
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_trend, width='stretch')
        
        # Show precipitation trend chart if precipitation data exists
        if 'precipitation_sum' in df.columns:
            fig_precip_trend = go.Figure()
            
            fig_precip_trend.add_trace(go.Bar(
                x=yearly_data['year'],
                y=yearly_data['total_precipitation'],
                name='Annual Precipitation',
                marker_color='skyblue'
            ))
            
            fig_precip_trend.update_layout(
                title="🌧️ Yearly Total Precipitation",
                xaxis_title="Year",
                yaxis_title="Precipitation (mm)",
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_precip_trend, width='stretch')
    
    else:
        st.warning("No data available to show trends")
    
    # Data table
    st.subheader("📋 Raw Data")
    
    if st.checkbox("Show raw data table"):
        display_cols = ['date'] + [col for col in variables if col in df.columns]
        st.dataframe(
            df[display_cols],
            width='stretch',
            height=400
        )
    
    # Download option
    st.subheader("💾 Export Data")
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"morocco_weather_{region}_{min_year}_{max_year}.csv",
        mime="text/csv"
    )
    
else:
    st.info("👈 Select your preferences in the sidebar and click 'Load Weather Data' to begin.")

# Footer
st.markdown("---")
st.markdown("""
**Data Source:** Open-Meteo Historical Weather API (ERA5 reanalysis)  
**Endpoint:** `https://archive-api.open-meteo.com/v1/era5`  
**Coverage:** 1940 to present (updated daily with ~5 day delay)  
**License:** CC BY 4.0 - Free for commercial and non-commercial use with attribution  
**Note:** This app uses reanalysis data (model-based), not measured station data.
""")