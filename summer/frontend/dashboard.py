import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from backend.orchestrator import SmartCityOrchestrator
from streamlit_extras.badges import badge
from streamlit_extras.let_it_rain import rain
import plotly.express as px
from streamlit_extras.stoggle import stoggle
import pandas as pd
import requests
import io
import base64
import plotly.figure_factory as ff
import streamlit.components.v1 as components
import random
import time

def get_live_data(name):
    if name == "Traffic":
        return f"Traffic: {random.choice(['Light', 'Moderate', 'Heavy'])}"
    elif name == "Pollution":
        return f"Current AQI: {random.randint(80, 200)}"
    elif name == "Emergency":
        return f"Response Time: {random.randint(2, 7)} min"
    return None

# Theme switcher
st.sidebar.header("Theme")
theme = st.sidebar.radio("Choose theme:", ["Light", "Dark"])
if 'last_theme' not in st.session_state:
    st.session_state['last_theme'] = theme
if theme != st.session_state['last_theme']:
    st.toast(f"Theme changed to {theme}!", icon="🎨")
    st.session_state['last_theme'] = theme
if theme == "Dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #222 !important; color: #eee !important; }
        </style>
    """, unsafe_allow_html=True)

# Custom CSS for a modern, professional look with a darker, softer background
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    html, body, .stApp {
        font-family: 'Montserrat', sans-serif !important;
        background: linear-gradient(135deg, #232526 0%, #2563eb 100%) !important;
        min-height: 100vh;
        overflow-x: hidden;
        animation: fadeInMain 1.2s cubic-bezier(.4,2,.6,1);
    }
    @keyframes fadeInMain {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .st-expander, .st-cq, .st-dg, .st-dh, .st-di, .st-dj, .st-dk, .st-dl, .st-dm, .st-dn, .st-do, .st-dp, .st-dq, .st-dr, .st-ds, .st-dt, .st-du, .st-dv, .st-dw, .st-dx, .st-dy, .st-dz {
        background: rgba(255,255,255,0.22) !important;
        box-shadow: 0 8px 32px 0 rgba(34,197,94,0.18) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(34,197,94,0.18) !important;
        backdrop-filter: blur(10px) !important;
        transition: box-shadow 0.2s;
    }
    .st-expander:hover {
        box-shadow: 0 12px 32px 0 #22c55e55 !important;
    }
    .stButton>button, .stSidebar .stButton>button {
        background: linear-gradient(90deg, #22c55e 0%, #a5b4fc 100%) !important;
        color: #fff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 12px 0 #22c55e33 !important;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .stButton>button:hover, .stSidebar .stButton>button:hover,
    #voice-btn:hover, #stop-btn:hover {
        background: #065f46 !important;
        color: #fff !important;
        transform: scale(1.09);
        box-shadow: 0 0 0 4px #a5b4fc;
        /* animation: hoverPop 0.18s cubic-bezier(.4,2,.6,1); */
    }
    /* Remove hoverPop animation from selectboxes, text inputs, sliders, and text areas */
    .stSidebar .stSelectbox:hover, .stSidebar .stTextInput:hover, .stSidebar .stSlider:hover, .stSidebar .stTextArea:hover,
    .stSelectbox:hover, .stTextInput:hover, .stSlider:hover, .stTextArea:hover {
        box-shadow: 0 0 0 2px #a5b4fc;
        /* animation: hoverPop 0.18s cubic-bezier(.4,2,.6,1); */
    }
    /* Optionally, you can remove the @keyframes hoverPop if not used anywhere else */
    .stButton>button:active, .stSidebar .stButton>button:active {
        animation: clickPop 0.18s cubic-bezier(.4,2,.6,1);
    }
    @keyframes clickPop {
        0% { transform: scale(1); }
        50% { transform: scale(0.93); }
        100% { transform: scale(1.08); }
    }
    .stSidebar .stSelectbox, .stSidebar .stTextInput, .stSidebar .stSlider, .stSidebar .stTextArea {
        border-radius: 10px !important;
        box-shadow: 0 2px 8px 0 #22c55e22 !important;
        transition: box-shadow 0.1s;
    }
    .stSidebar .stSelectbox:focus, .stSidebar .stTextInput:focus, .stSidebar .stSlider:focus, .stSidebar .stTextArea:focus {
        box-shadow: 0 0 0 2px #22c55e;
    }
    .stSidebar .stSelectbox:hover, .stSidebar .stTextInput:hover, .stSidebar .stSlider:hover, .stSidebar .stTextArea:hover,
    .stSelectbox:hover, .stTextInput:hover, .stSlider:hover, .stTextArea:hover {
        box-shadow: 0 0 0 2px #a5b4fc;
        /* animation: hoverPop 0.18s cubic-bezier(.4,2,.6,1); */
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-1kyxreq, .css-1dp5vir, .css-1v3fvcr {
        background: rgba(34,36,38,0.92) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.15) !important;
        color: #f3f4f6 !important;
    }
    .stSidebar {
        background: linear-gradient(135deg, #232526 0%, #6366f1 100%) !important;
        color: #fff !important;
    }
    .stSidebar .css-1v3fvcr {
        background: transparent !important;
    }
    .st-expanderHeader {
        font-size: 1.1em !important;
        font-weight: 700 !important;
        color: #a5b4fc !important;
    }
    .st-expanderContent {
        background: #232526 !important;
        border-radius: 0 0 12px 12px !important;
        color: #f3f4f6 !important;
    }
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #232526 0%, #2563eb 100%) !important;
    }
    /* Sidebar widget boxes */
    .stSidebar .stSelectbox, .stSidebar .stTextInput, .stSidebar .stTextArea, .stSidebar .stSlider, .stSidebar .stRadio, .stSidebar .stButton, .stSidebar .stDownloadButton, .stSidebar .stCheckbox {
        background: #232526 !important;
        color: #FFD700 !important;
        border-radius: 12px !important;
        border: 1.5px solid #2563eb !important;
        box-shadow: 0 2px 12px 0 #23252633 !important;
        margin-bottom: 0.7em !important;
    }
    .stSidebar label, .stSidebar span, .stSidebar div, .stSidebar input, .stSidebar select, .stSidebar textarea {
        color: #FFD700 !important;
    }
    /* Optionally, style selectbox dropdowns */
    .stSelectbox [data-baseweb="select"] {
        background: #232526 !important;
        color: #FFD700 !important;
    }
    /* Main page input boxes (text_input, text_area) */
    .stTextInput, .stTextArea {
        background: #232526 !important;
        color: #FFD700 !important;
        border-radius: 12px !important;
        border: 1.5px solid #2563eb !important;
        box-shadow: 0 2px 12px 0 #23252633 !important;
    }
    .stTextInput input, .stTextArea textarea {
        color: #FFD700 !important;
        background: #232526 !important;
    }
    </style>
    ''', unsafe_allow_html=True)

# Welcome/info banner
st.markdown("""
<div style='background: linear-gradient(90deg, #6366f1 0%, #a5b4fc 100%); color: #fff; border-radius: 16px; padding: 1.2em 2em; margin-bottom: 1.5em; box-shadow: 0 4px 24px 0 rgba(99,102,241,0.15); text-align:center; font-size:1.3em; font-weight:600;'>
  👋 Welcome to the <span style='color:#FFD700;'>Smart City Multi-Agent Simulation</span>!<br>
  <span style='font-size:0.95em; font-weight:400;'>Explore, interact, and learn how AI agents can shape the cities of tomorrow.<br>Try different scenarios, chat with the AI, and visualize real-time data!</span>
</div>
""", unsafe_allow_html=True)

# Store scenario history in session state
if 'scenario_history' not in st.session_state:
    st.session_state['scenario_history'] = []

st.set_page_config(page_title="Smart City Simulation Dashboard", layout="wide")

# Dashboard Title (deep yellow with animated color)
st.markdown("""
<style>
@keyframes colorChange {
  0% { color: #FFD600; }
  20% { color: #22c55e; }
  40% { color: #2563eb; }
  60% { color: #e1306c; }
  80% { color: #facc15; }
  100% { color: #FFD600; }
}
#custom-dashboard-title {
  font-size: 3.2em !important;
  font-weight: 900 !important;
  /* color: #FFD600 !important;  removed !important to allow animation */
  letter-spacing: 2px !important;
  text-shadow: 2px 2px 8px #23252655 !important;
  text-align: center !important;
  margin-bottom: 1.5em !important;
  animation: colorChange 3s infinite linear;
}
</style>
<div id='custom-dashboard-title'>
  🏙️ Smart City Multi-Agent Simulation
</div>
""", unsafe_allow_html=True)

AGENT_ICONS = {
    "TrafficAgent": "🚦",
    "EmergencyAgent": "🚨",
    "SmartEnergyGridAgent": "⚡",
    "HealthcareInfrastructureAgent": "🏥",
    "EnvironmentalPollutionAgent": "🌫️",
    "GreenEnergySustainabilityAgent": "🌱",
    "SmartBuildingInfrastructureAgent": "🏢",
    "PublicSafetyCrimePreventionAgent": "👮",
    "UrbanPlanningDevelopmentAgent": "🏗️"
}

AGENT_TITLES = {
    "TrafficAgent": "Traffic Control & Optimization",
    "EmergencyAgent": "Emergency Detection & Response",
    "SmartEnergyGridAgent": "Smart Energy Grid",
    "HealthcareInfrastructureAgent": "Healthcare Infrastructure",
    "EnvironmentalPollutionAgent": "Environmental & Pollution Control",
    "GreenEnergySustainabilityAgent": "Green Energy & Sustainability",
    "SmartBuildingInfrastructureAgent": "Smart Building & Infrastructure",
    "PublicSafetyCrimePreventionAgent": "Public Safety & Crime Prevention",
    "UrbanPlanningDevelopmentAgent": "Urban Planning & Development"
}

AGENT_ORDER = [
    "TrafficAgent", "EmergencyAgent", "SmartEnergyGridAgent", "HealthcareInfrastructureAgent",
    "EnvironmentalPollutionAgent", "GreenEnergySustainabilityAgent", "SmartBuildingInfrastructureAgent",
    "PublicSafetyCrimePreventionAgent", "UrbanPlanningDevelopmentAgent"
]

st.sidebar.header("Simulation Scenarios")
if 'last_scenario' not in st.session_state:
    st.session_state['last_scenario'] = "Normal Operation"
scenario = st.sidebar.selectbox("Choose a scenario:", [
    "Normal Operation",
    "Fire in Hospital During Traffic Congestion",
    "Power Outage in Downtown",
    "Pollution Spike During Festival"
])
if scenario != st.session_state['last_scenario']:
    st.toast(f"Scenario changed to: {scenario}", icon="🚦")
    st.session_state['last_scenario'] = scenario

# User input section
st.sidebar.header("User Input")
user_message = st.sidebar.text_input("Send a message or command to the agents:")

st.sidebar.header("Agent Status")
st.sidebar.write("(Agent status and logs will appear here)")

st.header(f"Scenario: {scenario}")
st.write("---")

st.subheader("Live City Map & Agent Visualizations")
st.info("Visualizations and agent outputs will be shown here.")

st.subheader("Event Log")

orchestrator = SmartCityOrchestrator()

# Run Simulation button
if st.button("Run Simulation"):
    st.toast("Agents are running now!", icon="🤖")
    logs = orchestrator.run_scenario(scenario, user_message)
    st.session_state['scenario_history'].append({
        'scenario': scenario,
        'logs': logs
    })
    # City summary visualization (example: pie chart for energy usage)
    energy_data = logs[3]['energy_data'] if isinstance(logs[3], dict) and 'energy_data' in logs[3] else None
    if energy_data:
        fig = px.pie(names=list(energy_data.keys()), values=list(energy_data.values()), title="Energy Usage by Zone")
        st.plotly_chart(fig, use_container_width=True)
    # Agent output cards with status badges and collapsible sections
    for idx, log in enumerate(logs[1:]):  # skip scenario title
        agent_name = AGENT_ORDER[idx]
        icon = AGENT_ICONS[agent_name]
        title = AGENT_TITLES[agent_name]
        # Determine status (simple logic for demo)
        status = "Normal"
        color = "green"
        if "alert" in str(log).lower() or "fire" in str(log).lower() or "congestion" in str(log).lower():
            status = "Alert"
            color = "orange"
        if "critical" in str(log).lower() or "emergency" in str(log).lower():
            status = "Critical"
            color = "red"
        with st.expander(f"{icon} {title}"):
            # Status color bar with animated fill (CSS only, no JS)
            bar_color = "#22c55e" if status == "Normal" else ("#facc15" if status == "Alert" else "#ef4444")
            st.markdown(f'''
                <div style="width:100%;height:18px;background:#232526;border-radius:8px;margin-bottom:8px;overflow:hidden;position:relative;">
                  <div class="bar-anim" style="height:100%;width:100%;background:{bar_color};border-radius:8px;"></div>
                </div>
                <style>
                  @keyframes fillBar {{
                    from {{ transform:scaleX(0); }}
                    to {{ transform:scaleX(1); }}
                  }}
                  .bar-anim {{
                    transform:scaleX(1);
                    transform-origin:left;
                    animation:fillBar 1.2s cubic-bezier(.4,2,.6,1);
                  }}
                </style>
            ''', unsafe_allow_html=True)
            st.markdown(f'<div style="background-color:#232526;padding:10px;border-radius:10px;">', unsafe_allow_html=True)
            st.markdown(f'<span style="color:{bar_color};font-weight:bold;">Status: {status}</span>', unsafe_allow_html=True)
            # Feature highlight for each agent
            feature_highlights = {
                "TrafficAgent": "<b style='color:#000;'>🚦 Feature Highlight:</b> <span style='color:#000;'>Live congestion heatmap & smart rerouting for emergency vehicles.</span>",
                "EmergencyAgent": "<b style='color:#000;'>🚨 Feature Highlight:</b> <span style='color:#000;'>Fastest route calculation and real-time emergency alerts.</span>",
                "SmartEnergyGridAgent": "<b style='color:#000;'>⚡ Feature Highlight:</b> <span style='color:#000;'>Grid load balancing and outage prediction with renewable integration.</span>",
                "HealthcareInfrastructureAgent": "<b style='color:#000;'>🏥 Feature Highlight:</b> <span style='color:#000;'>Live hospital bed/ambulance tracking and emergency triage analytics.</span>",
                "EnvironmentalPollutionAgent": "<b style='color:#000;'>🌫️ Feature Highlight:</b> <span style='color:#000;'>Air quality index, pollution source detection, and forecasting.</span>",
                "GreenEnergySustainabilityAgent": "<b style='color:#000;'>🌱 Feature Highlight:</b> <span style='color:#000;'>Solar/wind stats, CO₂ savings, and green project highlights.</span>",
                "SmartBuildingInfrastructureAgent": "<b style='color:#000;'>🏢 Feature Highlight:</b> <span style='color:#000;'>Energy savings, occupancy analytics, and smart building controls.</span>",
                "PublicSafetyCrimePreventionAgent": "<b style='color:#000;'>👮 Feature Highlight:</b> <span style='color:#000;'>Crime heatmap, patrol optimization, and real-time alert system.</span>",
                "UrbanPlanningDevelopmentAgent": "<b style='color:#000;'>🏗️ Feature Highlight:</b> <span style='color:#000;'>Zoning suggestions, growth forecast, and citizen feedback integration.</span>"
            }
            st.markdown(f"<div style='background:linear-gradient(90deg,#facc15 0%,#f472b6 100%);border-radius:8px;padding:0.7em 1em;margin:0.7em 0 1em 0;box-shadow:0 2px 8px #facc1555;'>{feature_highlights.get(agent_name,'')}</div>", unsafe_allow_html=True)
            # --- Enhanced details ---
            if isinstance(log, dict):
                st.write('**Agent Output Details:**')
                st.json(log, expanded=False)
                # Show event count and last event time if available
                if 'events' in log and isinstance(log['events'], list):
                    st.write(f"Events handled: {len(log['events'])}")
                    if log['events']:
                        st.write(f"Last event: {log['events'][-1]}")
                # Mini chart for numeric data
                numeric_data = {k: v for k, v in log.items() if isinstance(v, (int, float))}
                if numeric_data:
                    st.bar_chart(numeric_data)
                # Collapsible logs/history
                if 'history' in log and isinstance(log['history'], list):
                    with st.expander('Show Agent History'):
                        for h in log['history']:
                            st.write(h)
            else:
                st.write(log)
            st.markdown('</div>', unsafe_allow_html=True)
    # Simulated agent-to-agent messages (demo)
    st.subheader("Agent-to-Agent Messages")
    st.info("TrafficAgent → EmergencyAgent: Main St congestion, reroute emergency vehicles.\nEmergencyAgent → TrafficAgent: Fire at Hospital, clear route.")
    rain(emoji="🌟", font_size=20, falling_speed=5, animation_length="infinite")
else:
    st.info("Click 'Run Simulation' to start the scenario.")

# User-defined map locations
st.sidebar.header("Custom Map Locations")
custom_names = st.sidebar.text_area(
    "Names (one per line):",
    "Hospital\nCentral Park"
)
custom_lats = st.sidebar.text_area(
    "Latitudes (one per line):",
    "28.6145\n28.6150"
)
custom_lons = st.sidebar.text_area(
    "Longitudes (one per line):",
    "77.2100\n77.2110"
)
custom_descs = st.sidebar.text_area(
    "Descriptions (one per line):",
    "Main Hospital\nPark Area"
)
user_map_data = []
name_lines = [n.strip() for n in custom_names.strip().split("\n") if n.strip()]
lat_lines = [l.strip() for l in custom_lats.strip().split("\n") if l.strip()]
lon_lines = [l.strip() for l in custom_lons.strip().split("\n") if l.strip()]
desc_lines = [d.strip() for d in custom_descs.strip().split("\n") if d.strip()]
for i in range(min(len(name_lines), len(lat_lines), len(lon_lines), len(desc_lines))):
    try:
        user_map_data.append({
            "name": name_lines[i],
            "lat": float(lat_lines[i]),
            "lon": float(lon_lines[i]),
            "desc": desc_lines[i]
        })
    except Exception:
        continue

# City selection sidebar
st.sidebar.header("City Selection")
cities = {
    "Delhi": {"center": [28.6139, 77.2090], "zoom": 12},
    "Mumbai": {"center": [19.0760, 72.8777], "zoom": 11},
    "Bangalore": {"center": [12.9716, 77.5946], "zoom": 12},
    "Kolkata": {"center": [22.5726, 88.3639], "zoom": 12},
    "Chennai": {"center": [13.0827, 80.2707], "zoom": 12},
    "Ahmedabad": {"center": [23.0225, 72.5714], "zoom": 12},
    "Goa": {"center": [15.2993, 74.1240], "zoom": 11},
    "Hyderabad": {"center": [17.3850, 78.4867], "zoom": 12},
    "Pune": {"center": [18.5204, 73.8567], "zoom": 12},
    "Jaipur": {"center": [26.9124, 75.7873], "zoom": 12},
    "London": {"center": [51.5074, -0.1278], "zoom": 10},
    "New York": {"center": [40.7128, -74.0060], "zoom": 10}
}
if 'last_city' not in st.session_state:
    st.session_state['last_city'] = list(cities.keys())[0]
selected_city = st.sidebar.selectbox("Choose a city:", list(cities.keys()), index=0)
if selected_city != st.session_state['last_city']:
    st.toast(f"City changed to {selected_city}!", icon="🌆")
    st.session_state['last_city'] = selected_city
city_center = cities[selected_city]["center"]
city_zoom = cities[selected_city]["zoom"]

# Language selection sidebar (moved here)
st.sidebar.header("Language")
languages = ["English", "Hindi", "Bengali", "Spanish", "French", "Tamil", "Italian"]
if 'last_language' not in st.session_state:
    st.session_state['last_language'] = languages[0]
selected_language = st.sidebar.selectbox("Choose a language:", languages, index=0)
if selected_language != st.session_state['last_language']:
    st.toast(f"Language changed to {selected_language}!", icon="🌐")
    st.session_state['last_language'] = selected_language

# Predefined interesting places for each city
CITY_PLACES = {
    "Delhi": [
        {"name": "Hospital", "lat": 28.6145, "lon": 77.2100, "desc": "Main Hospital"},
        {"name": "Central Park", "lat": 28.6150, "lon": 77.2110, "desc": "Park Area"},
        {"name": "Connaught Place", "lat": 28.6315, "lon": 77.2167, "desc": "Shopping & Business Hub"},
        {"name": "India Gate", "lat": 28.6129, "lon": 77.2295, "desc": "Historic Monument"}
    ],
    "Mumbai": [
        {"name": "Marine Drive", "lat": 18.9430, "lon": 72.8238, "desc": "Scenic Promenade"},
        {"name": "Chhatrapati Shivaji Terminus", "lat": 18.9402, "lon": 72.8356, "desc": "Historic Railway Station"},
        {"name": "Juhu Beach", "lat": 19.0988, "lon": 72.8267, "desc": "Popular Beach"}
    ],
    "Bangalore": [
        {"name": "MG Road", "lat": 12.9758, "lon": 77.6055, "desc": "Shopping & Nightlife"},
        {"name": "Lalbagh Botanical Garden", "lat": 12.9507, "lon": 77.5848, "desc": "Botanical Garden"},
        {"name": "Electronic City", "lat": 12.8452, "lon": 77.6600, "desc": "IT Hub"},
        {"name": "Cubbon Park", "lat": 12.9763, "lon": 77.5929, "desc": "Green Space"}
    ],
    "Kolkata": [
        {"name": "Victoria Memorial", "lat": 22.5448, "lon": 88.3426, "desc": "Historic Monument"},
        {"name": "Howrah Bridge", "lat": 22.5850, "lon": 88.3468, "desc": "Iconic Bridge"},
        {"name": "Park Street", "lat": 22.5535, "lon": 88.3520, "desc": "Dining & Nightlife"},
        {"name": "Science City", "lat": 22.5392, "lon": 88.4137, "desc": "Science Museum"}
    ],
    # Add more cities and places as needed
}

# Fun facts and images for Delhi landmarks (expand for other cities as needed)
PLACE_DETAILS = {
    "Hospital": {
        "emoji": "🏥", "badge": "Healthcare", "color": "#22c55e",
        "link": "https://goo.gl/maps/6Qw2vQw2vQw2", "image": "https://cdn.pixabay.com/photo/2016/03/31/19/56/hospital-1294464_1280.png",
        "facts": ["Main Hospital is the largest in Delhi.", "It has over 1000 beds.", "Known for its emergency care."]
    },
    "Central Park": {
        "emoji": "🌳", "badge": "Park", "color": "#22d3ee",
        "link": "https://goo.gl/maps/8Qw2vQw2vQw2", "image": "https://cdn.pixabay.com/photo/2017/01/20/00/30/park-1990260_1280.jpg",
        "facts": ["Central Park hosts music festivals.", "It's a popular jogging spot.", "Home to rare plant species."]
    },
    "Connaught Place": {
        "emoji": "🏬", "badge": "Landmark", "color": "#facc15",
        "link": "https://en.wikipedia.org/wiki/Connaught_Place,_New_Delhi", "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Connaught_Place%2C_New_Delhi.jpg",
        "facts": ["Built in 1933.", "Major shopping and business hub.", "Circular design inspired by Royal Crescent, Bath."]
    },
    "India Gate": {
        "emoji": "🗼", "badge": "Landmark", "color": "#facc15",
        "link": "https://en.wikipedia.org/wiki/India_Gate", "image": "https://upload.wikimedia.org/wikipedia/commons/5/5d/India_Gate_in_New_Delhi_03-2016.jpg",
        "facts": ["War memorial built in 1931.", "Height: 42 meters.", "Names of 13,300 soldiers inscribed."]
    },
    # Add more places as needed
}

# Add details for event types (Traffic, Emergency, Pollution)
PLACE_DETAILS.update({
    "Traffic": {
        "emoji": "🚦", "badge": "Traffic Event", "color": "#f59e42",
        "link": "https://en.wikipedia.org/wiki/Traffic_congestion", "image": "https://cdn.pixabay.com/photo/2016/11/29/09/32/traffic-1865307_1280.jpg",
        "facts": ["Smart rerouting helps reduce congestion.", "Traffic lights are AI-optimized.", "Congestion is highest during rush hour."]
    },
    "Emergency": {
        "emoji": "🚨", "badge": "Emergency", "color": "#ef4444",
        "link": "https://en.wikipedia.org/wiki/Emergency_management", "image": "https://cdn.pixabay.com/photo/2017/06/20/19/22/ambulance-2426782_1280.jpg",
        "facts": ["Emergency response time is under 5 minutes.", "AI helps dispatch ambulances faster.", "Critical alerts are sent citywide."]
    },
    "Pollution": {
        "emoji": "🌫️", "badge": "Pollution Alert", "color": "#6366f1",
        "link": "https://en.wikipedia.org/wiki/Air_pollution", "image": "https://cdn.pixabay.com/photo/2017/01/20/00/30/park-1990260_1280.jpg",
        "facts": ["Air quality is monitored in real time.", "Pollution spikes during festivals.", "Green zones help reduce city pollution."]
    }
})

# Live City Map Visualization (Debugged)
st.subheader("Live City Map")
map_data = []
# Add predefined places for the selected city
if selected_city in CITY_PLACES:
    for place in CITY_PLACES[selected_city]:
        map_data.append({"lat": place["lat"], "lon": place["lon"], "type": f"📍 {place['name']}", "desc": place["desc"]})
# Add scenario/user events as before
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    last_logs = st.session_state['scenario_history'][-1]['logs']
    if len(last_logs) > 5:
        if "congestion" in str(last_logs[1]).lower():
            map_data.append({"lat": 28.6139, "lon": 77.2090, "type": "Traffic", "desc": "🚦 Main St congestion"})
        if "fire" in str(last_logs[2]).lower():
            map_data.append({"lat": 28.6145, "lon": 77.2100, "type": "Emergency", "desc": "🔥 Fire at Hospital"})
        if "pollution" in str(last_logs[5]).lower():
            map_data.append({"lat": 28.6150, "lon": 77.2110, "type": "Pollution", "desc": "🌫️ Air pollution spike"})
# Remove duplicate user locations if already in CITY_PLACES
city_place_names = set([place['name'] for place in CITY_PLACES.get(selected_city, [])])
for loc in user_map_data:
    if loc["name"] not in city_place_names:
        map_data.append({"lat": loc["lat"], "lon": loc["lon"], "type": f"📍 {loc['name']}", "desc": loc["desc"]})

if map_data:
    df_map = pd.DataFrame(map_data)
    st.info(f"Loaded {len(df_map)} locations for the map.")
    st.write(df_map)  # Debug: Show the data being plotted
    fig_map = px.scatter_mapbox(
        df_map, lat="lat", lon="lon", color="type", hover_name="desc",
        center=dict(lat=city_center[0], lon=city_center[1]),
        zoom=city_zoom, height=500, mapbox_style="open-street-map"
    )
    fig_map.update_traces(marker=dict(size=16, opacity=0.85))
    st.plotly_chart(fig_map, use_container_width=True)
    st.info("Click on a marker in the map legend to highlight and see details.")
    for i, row in df_map.iterrows():
        name = row['type'].replace('📍 ', '') if row['type'].startswith('📍') else row['type']
        details = PLACE_DETAILS.get(name, None)
        with st.expander(f"{row['type']} - {row['desc']}"):
            # Badge
            if details:
                st.markdown(f"<span style='background:{details['color']};color:#232526;padding:0.3em 0.8em;border-radius:8px;font-weight:700;font-size:1em;margin-right:0.7em;'>{details['badge']}</span>", unsafe_allow_html=True)
            # Image
            if details and details.get('image'):
                st.image(details['image'], width=220)
            # Google Maps/Wikipedia link
            if details and details.get('link'):
                st.markdown(f"<a href='{details['link']}' target='_blank' style='color:#2563eb;font-weight:700;'>More Info</a>", unsafe_allow_html=True)
            # Fun fact
            if details and details.get('facts'):
                st.info(f"Fun Fact: {random.choice(details['facts'])}")
            # Popularity/Rating (random for demo)
            if details:
                stars = '⭐' * random.randint(3, 5)
                st.markdown(f"<span style='font-size:1.2em;color:#facc15;'>{stars}</span> <span style='color:#22c55e;font-weight:600;'>Popularity</span>", unsafe_allow_html=True)
            # Live data for traffic, pollution, emergency (now robust)
            live_value = get_live_data(name)
            if live_value:
                st.markdown(f"<span style='background:#e0f2fe;color:#2563eb;padding:0.3em 0.8em;border-radius:8px;font-weight:700;font-size:1em;margin-right:0.7em;'>🔴 Live: {live_value}</span>", unsafe_allow_html=True)
            # Animated effect for emergencies (pulsing dot)
            if name == "Emergency":
                st.markdown('''<span style="display:inline-block;width:16px;height:16px;background:#ef4444;border-radius:50%;box-shadow:0 0 8px 4px #ef444488;animation:pulse 1s infinite;"></span>
                <style>@keyframes pulse {0%{box-shadow:0 0 8px 4px #ef444488;}50%{box-shadow:0 0 16px 8px #ef4444aa;}100%{box-shadow:0 0 8px 4px #ef444488;}}</style>''', unsafe_allow_html=True)
            # User comments (session-based)
            comment_key = f"comment_{i}_{name}"
            if f'user_comments' not in st.session_state:
                st.session_state['user_comments'] = {}
            user_comment = st.text_input("Leave a comment or tip:", value=st.session_state['user_comments'].get(comment_key, ''), key=comment_key)
            if user_comment:
                st.session_state['user_comments'][comment_key] = user_comment
                st.success("Comment saved!")
            # Share button (Google Maps link)
            if details and details.get('link'):
                share_url = details['link']
                st.markdown(f"<a href='https://twitter.com/intent/tweet?text=Check+out+this+place:+{share_url}' target='_blank' style='background:#22c55e;color:#fff;padding:0.4em 1em;border-radius:8px;font-weight:700;text-decoration:none;display:inline-block;margin-top:0.7em;'>Share on Twitter</a>", unsafe_allow_html=True)
else:
    st.warning("No data available for the map. Please check your city selection or scenario.")

# Notification popups for critical events
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    last_logs = st.session_state['scenario_history'][-1]['logs']
    for log in last_logs[1:]:
        if "critical" in str(log).lower() or "emergency" in str(log).lower():
            st.toast("Critical event detected! Check agent details.", icon="🚨")

# Scenario history sidebar
st.sidebar.header("Scenario History")
for i, entry in enumerate(st.session_state['scenario_history']):
    st.sidebar.markdown(f"**{i+1}. {entry['scenario']}**")
    for log in entry['logs'][1:]:
        if isinstance(log, dict):
            for k, v in log.items():
                st.sidebar.write(f'{k}: {v}')

# Role-Based Views
st.sidebar.header("Role Selection")
roles = ["City Planner", "Emergency Responder", "Energy Manager", "Environment Analyst", "Public Safety Officer"]
if 'last_role' not in st.session_state:
    st.session_state['last_role'] = roles[0]
selected_role = st.sidebar.selectbox("Choose your role:", roles)
if selected_role != st.session_state['last_role']:
    st.toast(f"Role changed to: {selected_role}", icon="🛡️")
    st.session_state['last_role'] = selected_role

# Real-Time Data Integration (Weather Example)
st.sidebar.header("Real-Time Weather (Open-Meteo)")
city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Ahmedabad": (23.0225, 72.5714),
    "Goa": (15.2993, 74.1240),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873),
    "London": (51.5074, -0.1278),
    "New York": (40.7128, -74.0060)
}
lat, lon = city_coords[selected_city]
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
try:
    weather = requests.get(weather_url, timeout=5).json().get("current_weather", {})
    temp = weather.get('temperature', 'N/A')
    weathercode = weather.get('weathercode', 'N/A')
    st.sidebar.markdown(f"🌡️ Temp: <span style='color:#2563eb;font-weight:bold;'>{temp}°C</span>, ☁️ Weather: {weathercode}", unsafe_allow_html=True)
except Exception:
    st.sidebar.write("Weather data unavailable.")

# Accessibility: High Contrast Mode and Font Size (in sidebar)
st.sidebar.header("Accessibility")
high_contrast = st.sidebar.checkbox("High Contrast Mode", key="high_contrast_mode")
font_size = st.sidebar.slider("Font Size", 12, 32, 16, key="font_size_slider")

# Apply accessibility styles
accessibility_css = f'''
    <style>
    .stApp * {{
        font-size: {font_size}px !important;
    }}
    {'body, .stApp, .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-1kyxreq, .css-1dp5vir, .css-1v3fvcr { background: #000 !important; color: #FFD700 !important; } .stSidebar { background: #000 !important; color: #FFD700 !important; } .stButton>button { background-color: #FFD700 !important; color: #000 !important; } .stButton>button:hover { background-color: #FFA500 !important; color: #000 !important; }' if high_contrast else ''}
    </style>
'''
st.markdown(accessibility_css, unsafe_allow_html=True)

# Voice Command (Speech-to-Text) for Chatbot with notification and stop button
st.sidebar.markdown("<b>🎤 Voice Command</b>", unsafe_allow_html=True)
voice_input_placeholder = st.sidebar.empty()

# Add a placeholder for live speech transcript beside the voice command buttons
speech_transcript = st.sidebar.empty()

components.html('''
  <div id="voice-assistant-container" style="text-align:center; font-weight:800; font-size:1.2em; color:#FFD600; margin-bottom:0.3em;display:flex;align-items:center;justify-content:center;gap:0.5em; border-radius:18px; box-shadow:0 4px 24px #6366f155; background:linear-gradient(90deg,#232526 0%,#2563eb 100%); border:3px solid #FFD600; animation:glow 2s infinite alternate; padding:1em 0.5em 1.2em 0.5em; position:relative;">
    <span style="font-size:1.3em;display:flex;align-items:center;gap:0.5em;">
      <span id="mic-emoji" style="transition:filter 0.3s;">🎤</span>
      Voice Assistant
    </span>
    <span id="voice-status" style="margin-left:10px;color:#6366f1;font-weight:600;"></span>
    <style>
      @keyframes glow {
        from { box-shadow:0 0 16px #FFD60055, 0 0 32px #2563eb33; }
        to { box-shadow:0 0 32px #FFD600, 0 0 48px #2563eb; }
      }
      @keyframes wave {
        0% { background-position:0% 50%; }
        100% { background-position:100% 50%; }
      }
      #live-transcript.capturing {
        background: linear-gradient(90deg,#a5b4fc 0%,#22c55e 100%);
        color:#000;
        animation: wave 1.2s linear infinite alternate;
        background-size:200% 100%;
      }
      #voice-btn {
        background:linear-gradient(90deg,#22c55e 0%,#6366f1 100%);
        color:#fff;
        border:none;
        padding:0.5em 1.2em;
        border-radius:8px;
        font-size:1.1em;
        cursor:pointer;
        font-weight:700;
        box-shadow:0 2px 12px #22c55e33;
        margin-right:0.5em;
        transition:transform 0.1s,box-shadow 0.1s;
      }
      #voice-btn.listening {
        filter:drop-shadow(0 0 8px #22c55e);
        background:linear-gradient(90deg,#22c55e 0%,#a5b4fc 100%);
        animation:glow 1s infinite alternate;
      }
      #stop-btn {
        background:linear-gradient(90deg,#ef4444 0%,#6366f1 100%);
        color:#fff;
        border:none;
        padding:0.5em 1.2em;
        border-radius:8px;
        font-size:1.1em;
        cursor:pointer;
        font-weight:700;
        box-shadow:0 2px 12px #ef444433;
        transition:transform 0.1s,box-shadow 0.1s;
      }
      #stop-btn:active, #voice-btn:active {
        transform:scale(0.97);
      }
    </style>
  </div>
  <div style="display:flex;align-items:center;gap=10px;justify-content:center;margin-bottom:0.5em;">
    <button id="voice-btn">🎤 Start</button>
    <button id="stop-btn">⏹️ Stop</button>
  </div>
  <div id="live-transcript" style="margin-top:0.7em; min-height:2.2em; background:#2563eb; color:#000; border-radius:8px; box-shadow:0 2px 8px #6366f122; padding:0.5em 1em; font-size:1.1em; font-weight:600; display:inline-block; transition:background 0.3s;"></div>
  <div style="margin-top:0.5em;font-size:0.95em;color:#FFD600;font-weight:500;text-align:center;">
    💡 <span id="voice-tip">Try: "Show me the latest traffic updates" or "What is the air quality now?"</span>
  </div>
  <script>
    const btn = document.getElementById('voice-btn');
    const stopBtn = document.getElementById('stop-btn');
    const status = document.getElementById('voice-status');
    const transcriptDiv = document.getElementById('live-transcript');
    const micEmoji = document.getElementById('mic-emoji');
    let recognition;
    if ('webkitSpeechRecognition' in window) {
      recognition = new webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      btn.onclick = function() {
        recognition.start();
        status.textContent = '🎤 Listening...';
        status.style.color = '#22c55e';
        transcriptDiv.textContent = '';
        transcriptDiv.classList.add('capturing');
        btn.classList.add('listening');
        micEmoji.style.filter = 'drop-shadow(0 0 8px #22c55e)';
      };
      stopBtn.onclick = function() {
        recognition.stop();
        status.textContent = '⏹️ Stopped';
        status.style.color = '#ef4444';
        transcriptDiv.classList.remove('capturing');
        btn.classList.remove('listening');
        micEmoji.style.filter = '';
      };
      recognition.onresult = function(event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        transcriptDiv.textContent = transcript;
        window.parent.postMessage({ isStreamlitMessage: true, voiceInput: transcript }, '*');
      };
      recognition.onend = function() {
        transcriptDiv.classList.remove('capturing');
        btn.classList.remove('listening');
        micEmoji.style.filter = '';
      };
    } else {
      btn.disabled = true;
      stopBtn.disabled = true;
      status.textContent = 'Not supported';
      status.style.color = '#ef4444';
    }
    window.addEventListener('message', (event) => {
      if (event.data && event.data.isStreamlitMessage && event.data.voiceInput) {
        const streamlitInput = window.parent.document.querySelector('input[type="text"][aria-label="Ask the assistant:"]');
        if (streamlitInput) {
          streamlitInput.value = event.data.voiceInput;
          streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
      }
    });
  </script>
''', height=200)

# AI Chatbot Assistant with vertical quick actions and safe fallback
st.sidebar.header("AI Chatbot Assistant 🤖")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
chat_input = st.sidebar.text_input("Ask the assistant:")
summarize = st.sidebar.button("Summarize", key="summarize_btn")
explain = st.sidebar.button("Explain", key="explain_btn")
suggest = st.sidebar.button("Suggest", key="suggest_btn")
chat_response = None
try:
    from utils.llm_utils import gemini_llm
    llm_enabled = True
except Exception:
    llm_enabled = False
if st.sidebar.button("Send", key="chat_send") and chat_input:
    if llm_enabled:
        chat_response = gemini_llm(chat_input)
    else:
        chat_response = "[LLM functionality is disabled. Please install google-generativeai to enable Gemini integration.]"
    st.session_state['chat_history'].append((chat_input, chat_response))
if summarize and chat_input:
    if llm_enabled:
        chat_response = gemini_llm(f"Summarize this: {chat_input}")
    else:
        chat_response = "[LLM functionality is disabled. Please install google-generativeai to enable Gemini integration.]"
    st.session_state['chat_history'].append((f"Summarize: {chat_input}", chat_response))
if explain and chat_input:
    if llm_enabled:
        chat_response = gemini_llm(f"Explain this: {chat_input}")
    else:
        chat_response = "[LLM functionality is disabled. Please install google-generativeai to enable Gemini integration.]"
    st.session_state['chat_history'].append((f"Explain: {chat_input}", chat_response))
if suggest and chat_input:
    if llm_enabled:
        chat_response = gemini_llm(f"Suggest improvement for: {chat_input}")
    else:
        chat_response = "[LLM functionality is disabled. Please install google-generativeai to enable Gemini integration.]"
    st.session_state['chat_history'].append((f"Suggest: {chat_input}", chat_response))
for q, a in st.session_state['chat_history'][-5:]:
    st.sidebar.write(f"**You:** {q}")
    st.sidebar.write(f"**Assistant:** {a}")

# --- Voice-to-Chatbot Integration ---
# (Feature removed as requested. Voice command now only fills the chat input box. No automatic chatbot trigger.)

# Performance Analytics
st.subheader("Performance Analytics")
perf_data = []
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    for entry in st.session_state['scenario_history']:
        for idx, log in enumerate(entry['logs'][1:]):
            agent_name = AGENT_ORDER[idx]
            perf_data.append({
                'Agent': agent_name,
                'Scenario': entry['scenario'],
                'ResponseTime': 1 + idx * 0.5,  # Demo: fake response time
                'EventsHandled': len(str(log))
            })
if perf_data:
    df_perf = pd.DataFrame(perf_data)
    st.markdown("#### Agent Performance Table")
    st.dataframe(df_perf)

    st.markdown("#### Events Handled by Agent (Bar Chart)")
    st.bar_chart(df_perf.groupby('Agent')['EventsHandled'].sum())

    st.markdown("#### Average Response Time by Agent (Line Chart)")
    st.line_chart(df_perf.groupby('Agent')['ResponseTime'].mean())

    st.markdown("#### Events Handled Distribution (Pie Chart)")
    import plotly.express as px
    pie_fig = px.pie(df_perf, names='Agent', values='EventsHandled', title='Events Handled Distribution')
    st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("#### Response Time Heatmap (Agent vs Scenario)")
    import plotly.figure_factory as ff
    heatmap_data = df_perf.pivot_table(index='Agent', columns='Scenario', values='ResponseTime', fill_value=0)
    heatmap_fig = px.imshow(heatmap_data, text_auto=True, color_continuous_scale='Blues', aspect='auto',
        labels=dict(x="Scenario", y="Agent", color="Response Time"), title="Response Time Heatmap")
    st.plotly_chart(heatmap_fig, use_container_width=True)
else:
    st.info("No performance data yet.")

# Accessibility: High Contrast Mode and Font Size (already present)
# Removed duplicate accessibility controls to avoid StreamlitDuplicateElementKey error

st.markdown("""
<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css'>
<div style='width:100vw;display:flex;justify-content:center;align-items:center;position:fixed;left:0;right:0;bottom:0;z-index:1000;'>
  <div class='custom-footer-enhanced' style='background: linear-gradient(90deg, #2563eb 0%, #22c55e 100%); border-radius: 22px 22px 0 0; padding: 1.1em 2.5em 0.7em 2.5em; box-shadow: 0 -4px 24px 0 #23252655; font-size: 1.18em; text-align: center; color: #fff; position: relative; overflow: hidden;'>
    <span style=\"font-size:1.5em;vertical-align:middle;animation:footerPulse 2s infinite alternate;\">🌆</span>
    <span style=\"font-weight: 800; letter-spacing: 1px; margin-left: 0.5em;\">Made with <span style='color:#facc15;'>❤️</span> by your Smart City Team</span>
    <span style=\"margin-left:1.2em;font-size:1.1em;\">|</span>
    <span style=\"margin-left:1.2em;font-weight:700;\">💻 Creator: Srijan Roy, IEM Kolkata</span>
    <span style=\"margin-left:1.2em;\">
      <a href=\"https://github.com/SrijanRoy12\" target=\"_blank\" style=\"color:#fff;margin:0 0.4em;\"><i class=\"fa-brands fa-github\"></i></a>
      <a href=\"https://www.linkedin.com/in/srijan-roy-29bb19256?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app\" target=\"_blank\" style=\"color:#fff;margin:0 0.4em;\"><i class=\"fa-brands fa-linkedin-in\"></i></a>
      <a href=\"https://mail.google.com/mail/?view=cm&fs=1&to=roysrijan53@gmail.com\" target=\"_blank\" style=\"color:#fff;margin:0 0.4em;\"><i class=\"fa-regular fa-envelope\"></i></a>
      <a href=\"https://www.instagram.com/its_ur_roy123/\" target=\"_blank\" style=\"color:#fff;margin:0 0.4em;\"><i class=\"fa-brands fa-instagram\"></i></a>
      <a href=\"https://x.com/home\" target=\"_blank\" style=\"color:#fff;margin:0 0.4em;\"><i class=\"fa-brands fa-x-twitter\"></i></a>
    </span>
  </div>
</div>
<style>
@keyframes footerPulse {
  from { filter: drop-shadow(0 0 8px #22c55e); }
  to { filter: drop-shadow(0 0 18px #facc15); }
}
.custom-footer-enhanced {
  animation: footerFadeIn 1.2s cubic-bezier(.4,2,.6,1);
}
@keyframes footerFadeIn {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (max-width: 600px) {
  .custom-footer-enhanced {
    font-size: 0.95em !important;
    padding: 0.7em 0.5em !important;
  }
}
</style>
""", unsafe_allow_html=True)

# Floating social media buttons (bottom right)
st.markdown('''
<style>
.fab-social-float {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 2000;
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.fab-social-float a {
    background: #222;
    color: #fff;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18);
    font-size: 2rem;
    transition: background 0.2s, transform 0.25s cubic-bezier(.4,2,.6,1), box-shadow 0.2s;
    text-decoration: none;
    will-change: transform;
}
.fab-social-float a:hover {
    transform: scale(1.18) rotate(-8deg);
    box-shadow: 0 8px 24px rgba(0,0,0,0.22);
}
.fab-social-float a.linkedin { background: #0077b5; }
.fab-social-float a.linkedin:hover { background: #005983; }
.fab-social-float a.github { background: #333; }
.fab-social-float a.github:hover { background: #24292e; }
.fab-social-float a.mail { background: #ea4335; }
.fab-social-float a.mail:hover { background: #b31412; }
.fab-social-float a.insta { background: #e1306c; }
.fab-social-float a.insta:hover { background: #b92d5c; }
.fab-social-float a.twitter { background: #1da1f2; }
.fab-social-float a.twitter:hover { background: #0d8ddb; }
</style>
<div class="fab-social-float">
    <a href="https://www.linkedin.com/in/srijan-roy-29bb19256?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank" class="linkedin"><i class="fa-brands fa-linkedin-in"></i></a>
    <a href="https://github.com/SrijanRoy12" target="_blank" class="github"><i class="fa-brands fa-github"></i></a>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=roysrijan53@gmail.com" target="_blank" class="mail"><i class="fa-regular fa-envelope"></i></a>
    <a href="https://www.instagram.com/its_ur_roy123/" target="_blank" class="insta"><i class="fa-brands fa-instagram"></i></a>
    <a href="https://x.com/home" target="_blank" class="twitter"><i class="fa-brands fa-x-twitter"></i></a>
</div>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
''', unsafe_allow_html=True)

# --- Download & Share: Export scenario results, logs, or visualizations ---
st.sidebar.header("Download & Share")
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    last_entry = st.session_state['scenario_history'][-1]
    logs = last_entry['logs']
    # Export logs as CSV
    import pandas as pd
    flat_logs = []
    for log in logs:
        if isinstance(log, dict):
            flat_logs.append({k: str(v) for k, v in log.items()})
        else:
            flat_logs.append({'log': str(log)})
    df_logs = pd.DataFrame(flat_logs)
    csv_data = df_logs.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download Logs as CSV", csv_data, file_name="scenario_logs.csv", mime="text/csv")
    # Export logs as PDF
    try:
        from fpdf import FPDF
        import tempfile
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Scenario: {last_entry['scenario']}", ln=True)
        for log in logs:
            pdf.multi_cell(0, 10, txt=str(log))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf.output(tmp_pdf.name)
            tmp_pdf.seek(0)
            st.sidebar.download_button("Download Logs as PDF", tmp_pdf.read(), file_name="scenario_logs.pdf", mime="application/pdf")
    except Exception as e:
        st.sidebar.info("Install 'fpdf' for PDF export: pip install fpdf")
    # Export visualization as image (if available)
    if 'fig' in locals():
        img_bytes = fig.to_image(format="png")
        st.sidebar.download_button("Download Visualization as Image", img_bytes, file_name="visualization.png", mime="image/png")
    st.sidebar.info("You can download the latest scenario logs as CSV or PDF, and the visualization as an image.")
else:
    st.sidebar.info("Run a scenario to enable downloads.")

# --- Feedback & Support Section (Enhanced) ---
st.sidebar.markdown('''
    <div style="background: linear-gradient(90deg, #facc15 0%, #f472b6 100%); border-radius: 14px; padding: 1em 1em 0.5em 1em; margin-bottom: 1.2em; box-shadow: 0 2px 12px 0 #facc1555; text-align:center;">
        <span style="font-size:1.3em; font-weight:700; color:#2563eb !important;">💬 Feedback & Support</span><br>
        <span style="font-size:1em; color:#22c55e !important;">We value your feedback and are here to help!</span>
    </div>
''', unsafe_allow_html=True)
with st.sidebar.form(key="feedback_form_sidebar"):
    feedback_email = st.text_input("Your email (optional):", key="sidebar_feedback_email")
    feedback_text = st.text_area("Your feedback or suggestion:", key="sidebar_feedback_text")
    feedback_submitted = st.form_submit_button("Submit Feedback")
    if feedback_submitted:
        st.session_state['show_feedback_notification'] = True

# Show floating notification in main app area if feedback was submitted
if st.session_state.get('show_feedback_notification', False):
    st.markdown('''
        <div style="position:fixed;bottom:100px;right:40px;z-index:99999;background:linear-gradient(90deg,#22c55e 0%,#facc15 100%);color:#111;padding:1em 2em;border-radius:16px;box-shadow:0 4px 24px #22c55e55;font-weight:700;font-size:1.1em;animation:fadeInNotif 0.7s;">
            ✅ Thank you for your feedback! We appreciate your input.
        </div>
        <style>@keyframes fadeInNotif {from{opacity:0;transform:translateY(40px);}to{opacity:1;transform:translateY(0);}}</style>
    ''', unsafe_allow_html=True)
    # Reset after showing
    st.session_state['show_feedback_notification'] = False

