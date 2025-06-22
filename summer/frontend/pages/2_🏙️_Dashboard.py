import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
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
from streamlit_lottie import st_lottie
import json

# DEBUG: Print to Streamlit and log to help diagnose blank page issues
st.write('DEBUG: Dashboard page loaded.')
try:
    st.write('DEBUG: Session state:', dict(st.session_state))
except Exception as e:
    st.write(f'DEBUG: Session state error: {e}')

# Theme switcher
st.sidebar.header("Theme")
theme = st.sidebar.radio("Choose theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #222 !important; color: #eee !important; }
        </style>
    """, unsafe_allow_html=True)

# Custom CSS for a modern, professional look with a darker, softer background
st.markdown('''
    <style>
    .stApp {
        background: linear-gradient(135deg, #232526 0%, #414345 100%) !important;
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-1kyxreq, .css-1dp5vir, .css-1v3fvcr {
        background: rgba(34,36,38,0.92) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.15) !important;
        color: #f3f4f6 !important;
    }
    .st-bb, .st-cq, .st-dg, .st-dh, .st-di, .st-dj, .st-dk, .st-dl, .st-dm, .st-dn, .st-do, .st-dp, .st-dq, .st-dr, .st-ds, .st-dt, .st-du, .st-dv, .st-dw, .st-dx, .st-dy, .st-dz {
        background: transparent !important;
    }
    .stButton>button {
        background-color: #6366f1 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5em 2em !important;
        box-shadow: 0 2px 8px 0 rgba(99,102,241,0.15) !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #4338ca !important;
        color: #fff !important;
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
    </style>
''', unsafe_allow_html=True)

# Add a GenAI-themed background image to the dashboard
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.45);
        z-index: 0;
    }
    .block-container { position: relative; z-index: 1; }
    </style>
    """,
    unsafe_allow_html=True
)

# Store scenario history in session state
if 'scenario_history' not in st.session_state:
    st.session_state['scenario_history'] = []

st.set_page_config(page_title="Smart City Simulation Dashboard", layout="wide")
st.title("🏙️ Smart City Multi-Agent Simulation")

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
scenario = st.sidebar.selectbox("Choose a scenario:", [
    "Normal Operation",
    "Fire in Hospital During Traffic Congestion",
    "Power Outage in Downtown",
    "Pollution Spike During Festival"
])

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
selected_city = st.sidebar.selectbox("Choose a city:", list(cities.keys()), index=0)
city_center = cities[selected_city]["center"]
city_zoom = cities[selected_city]["zoom"]

# Run Simulation button
if st.button("Run Simulation"):
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
            # Status color bar
            bar_color = "#22c55e" if status == "Normal" else ("#facc15" if status == "Alert" else "#ef4444")
            st.markdown(f'<div style="height:6px;width:100%;background:{bar_color};border-radius:4px 4px 0 0;margin-bottom:8px;"></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background-color:#232526;padding:10px;border-radius:10px;">', unsafe_allow_html=True)
            st.markdown(f'<span style="color:{bar_color};font-weight:bold;">Status: {status}</span>', unsafe_allow_html=True)
            if isinstance(log, dict):
                for k, v in log.items():
                    if isinstance(v, dict):
                        for subk, subv in v.items():
                            st.write(f'**{subk}**: {subv}')
                    elif isinstance(v, list):
                        for item in v:
                            if isinstance(item, dict):
                                for subk, subv in item.items():
                                    st.write(f'**{subk}**: {subv}')
                            else:
                                st.write(f'**{k}**: {item}')
                    else:
                        st.write(f'**{k}**: {v}')
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

# Live City Map Visualization
st.subheader("Live City Map")
map_data = []
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    last_logs = st.session_state['scenario_history'][-1]['logs']
    if len(last_logs) > 5:
        if "congestion" in str(last_logs[1]).lower():
            map_data.append({"lat": 28.6139, "lon": 77.2090, "type": "Traffic", "desc": "Main St congestion"})
        if "fire" in str(last_logs[2]).lower():
            map_data.append({"lat": 28.6145, "lon": 77.2100, "type": "Emergency", "desc": "Fire at Hospital"})
        if "pollution" in str(last_logs[5]).lower():
            map_data.append({"lat": 28.6150, "lon": 77.2110, "type": "Pollution", "desc": "Air pollution spike"})
# Add user locations to map
for loc in user_map_data:
    map_data.append({"lat": loc["lat"], "lon": loc["lon"], "type": loc["name"], "desc": loc["desc"]})
if map_data:
    df_map = pd.DataFrame(map_data)
    fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", color="type", hover_name="desc",
        center=dict(lat=city_center[0], lon=city_center[1]),
        zoom=city_zoom, height=300, mapbox_style="carto-positron")
    fig_map.update_traces(marker=dict(size=14), selector=dict(mode='markers'))
    st.plotly_chart(fig_map, use_container_width=True)
    st.info("Click on a marker in the map legend to highlight and see details.")
    # Show details for each marker below the map
    for i, row in df_map.iterrows():
        with st.expander(f"{row['type']} - {row['desc']}"):
            st.write(f"**Latitude:** {row['lat']}")
            st.write(f"**Longitude:** {row['lon']}")
            st.write(f"**Description:** {row['desc']}")
else:
    st.info("No live events to display on the map.")

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
selected_role = st.sidebar.selectbox("Choose your role:", roles)

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
    st.sidebar.write(f"🌡️ Temp: {weather.get('temperature', 'N/A')}°C, ☁️ Weather: {weather.get('weathercode', 'N/A')}")
except Exception:
    st.sidebar.write("Weather data unavailable.")

# Role-Based Dashboard Customization
if selected_role == "City Planner":
    st.success("You are viewing as a City Planner. Focus: Urban planning, infrastructure, and development proposals.")
elif selected_role == "Emergency Responder":
    st.warning("You are viewing as an Emergency Responder. Focus: Emergency events, hospital/ambulance status, and rapid response.")
elif selected_role == "Energy Manager":
    st.info("You are viewing as an Energy Manager. Focus: Energy grid, green energy, and consumption analytics.")
elif selected_role == "Environment Analyst":
    st.info("You are viewing as an Environment Analyst. Focus: Pollution, air/water quality, and sustainability.")
elif selected_role == "Public Safety Officer":
    st.info("You are viewing as a Public Safety Officer. Focus: Crime prevention, public safety, and law enforcement.")

# Scenario Builder
st.sidebar.header("Scenario Builder")
if 'custom_scenarios' not in st.session_state:
    st.session_state['custom_scenarios'] = []
new_scenario_name = st.sidebar.text_input("Scenario Name", "Custom Scenario 1")
event_steps = st.sidebar.text_area("Events (one per line, e.g. 'Fire at Hospital', 'Power Outage Downtown'):")
if st.sidebar.button("Save Scenario"):
    st.session_state['custom_scenarios'].append({
        'name': new_scenario_name,
        'events': [e.strip() for e in event_steps.split('\n') if e.strip()]
    })
if st.session_state['custom_scenarios']:
    st.sidebar.markdown("**Saved Scenarios:**")
    for i, sc in enumerate(st.session_state['custom_scenarios']):
        st.sidebar.write(f"{i+1}. {sc['name']}: {', '.join(sc['events'])}")

# Agent Customization
st.sidebar.header("Agent Customization")
traffic_light_timing = st.sidebar.slider("Traffic Light Timing (sec)", 10, 120, 60)
hospital_capacity = st.sidebar.slider("Hospital Capacity", 10, 100, 50)

# Pass custom params to orchestrator (example)
orchestrator.traffic.traffic_light_timing = traffic_light_timing
orchestrator.healthcare.hospital_capacity = hospital_capacity

# Event Timeline
st.subheader("Event Timeline")
timeline_events = []
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    for entry in st.session_state['scenario_history']:
        for idx, log in enumerate(entry['logs'][1:]):
            agent_name = AGENT_ORDER[idx]
            if isinstance(log, dict):
                for k, v in log.items():
                    timeline_events.append(dict(Task=agent_name, Start=entry['scenario'], Finish=k, Resource=str(v)))
if timeline_events:
    df_timeline = pd.DataFrame(timeline_events)
    fig_timeline = ff.create_gantt(df_timeline, index_col='Task', show_colorbar=True, group_tasks=True)
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("No events to display on the timeline.")

# Notification Center
st.subheader("Notification Center")
notifications = []
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    for entry in st.session_state['scenario_history']:
        for log in entry['logs'][1:]:
            if "alert" in str(log).lower() or "critical" in str(log).lower() or "emergency" in str(log).lower():
                notifications.append(str(log))
if notifications:
    for note in notifications:
        st.warning(note)
else:
    st.info("No alerts or messages.")

# Download & Share
st.sidebar.header("Download & Share")
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    all_logs = []
    for entry in st.session_state['scenario_history']:
        all_logs.append({'scenario': entry['scenario'], 'logs': entry['logs']})
    df_logs = pd.DataFrame(all_logs)
    csv = df_logs.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download Logs as CSV", csv, "scenario_logs.csv", "text/csv")

# Mobile-Friendly UI tweaks
st.markdown('''
    <style>
    @media (max-width: 600px) {
        .stApp { font-size: 1.2em !important; }
        .stButton>button { font-size: 1.1em !important; padding: 1em 2em !important; }
        .stSidebar { font-size: 1.1em !important; }
    }
    </style>
''', unsafe_allow_html=True)

# Voice Commands (browser-based speech-to-text using HTML/JS)
st.sidebar.header("Voice Command")
voice_text = st.sidebar.text_input("Or use your voice (click mic):", "")
st.markdown('''
    <script>
    function startDictation() {
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "en-US";
            recognition.start();
            recognition.onresult = function(e) {
                document.getElementById('voice_input').value = e.results[0][0].transcript;
                recognition.stop();
            };
            recognition.onerror = function(e) {
                recognition.stop();
            }
        }
    }
    </script>
    <input id="voice_input" type="text" style="width:80%;padding:0.5em;" placeholder="Speak here...">
    <button onclick="startDictation()" style="padding:0.5em 1em;margin-left:0.5em;">🎤</button>
''', unsafe_allow_html=True)

# AI Chatbot Assistant
st.sidebar.header("AI Chatbot Assistant")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
chat_input = st.sidebar.text_input("Ask the assistant:")
if st.sidebar.button("Send", key="chat_send") and chat_input:
    # Simple rule-based or LLM placeholder
    if "traffic" in chat_input.lower():
        response = "Traffic is moderate. Main St congestion expected in 15 min."
    elif "emergency" in chat_input.lower():
        response = "Fire at Hospital. Emergency units dispatched."
    else:
        response = "I'm here to help with your smart city simulation!"
    st.session_state['chat_history'].append((chat_input, response))
for q, a in st.session_state['chat_history'][-5:]:
    st.sidebar.write(f"**You:** {q}")
    st.sidebar.write(f"**Assistant:** {a}")

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
    st.bar_chart(df_perf.groupby('Agent')['EventsHandled'].sum())
    st.line_chart(df_perf.groupby('Agent')['ResponseTime'].mean())
else:
    st.info("No performance data yet.")

# Accessibility Features
st.sidebar.header("Accessibility")
high_contrast = st.sidebar.checkbox("High-Contrast Mode")
font_size = st.sidebar.slider("Font Size", 12, 32, 16)

# Remove or comment out high-contrast CSS block to prevent black screen
# (This block is triggered by the high_contrast checkbox)
# if high_contrast:
#     st.markdown('''
#         <style>
#         body, .stApp { background-color: #000 !important; color: #fff !important; }
#         .stApp, .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-1kyxreq, .css-1dp5vir, .css-1v3fvcr {
#             background: #000 !important; color: #fff !important;
#         }
#         .stButton>button { background-color: #FFD600 !important; color: #000 !important; }
#         </style>
#     ''', unsafe_allow_html=True)

st.markdown(f'''<style>html, body, [class^="st"] {{ font-size: {font_size}px !important; }}</style>''', unsafe_allow_html=True)

# Add ARIA labels for screen readers (example for main sections)
st.markdown('<h1 aria-label="Smart City Multi-Agent Simulation Dashboard" style="position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden;">Smart City Multi-Agent Simulation Dashboard</h1>', unsafe_allow_html=True)

# Gamification Features
st.sidebar.header("Gamification & Engagement")
if 'achievements' not in st.session_state:
    st.session_state['achievements'] = set()
if 'leaderboard' not in st.session_state:
    st.session_state['leaderboard'] = []
if 'challenges' not in st.session_state:
    st.session_state['challenges'] = [
        {'name': 'First Simulation', 'desc': 'Run your first scenario.'},
        {'name': 'Crisis Manager', 'desc': 'Resolve a critical event.'},
        {'name': 'Eco Champion', 'desc': 'Achieve 80%+ green energy in a scenario.'}
    ]

# Example: Award achievements based on actions
if 'scenario_history' in st.session_state and st.session_state['scenario_history']:
    if len(st.session_state['scenario_history']) >= 1:
        st.session_state['achievements'].add('First Simulation')
    for entry in st.session_state['scenario_history']:
        for log in entry['logs'][1:]:
            if 'critical' in str(log).lower() or 'emergency' in str(log).lower():
                st.session_state['achievements'].add('Crisis Manager')
            if 'green energy' in str(log).lower() or 'renewable' in str(log).lower():
                st.session_state['achievements'].add('Eco Champion')

# Achievements display
st.sidebar.subheader("Achievements 🏆")
if st.session_state['achievements']:
    for ach in st.session_state['achievements']:
        st.sidebar.success(f"🏅 {ach}")
else:
    st.sidebar.info("No achievements yet. Complete challenges to earn badges!")

# Leaderboard (simple: by number of scenarios run)
user = 'You'
if 'leaderboard' in st.session_state:
    found = False
    for entry in st.session_state['leaderboard']:
        if entry['user'] == user:
            entry['score'] = len(st.session_state['scenario_history'])
            found = True
    if not found:
        st.session_state['leaderboard'].append({'user': user, 'score': len(st.session_state['scenario_history'])})
    st.session_state['leaderboard'].sort(key=lambda x: x['score'], reverse=True)
    st.sidebar.subheader("Leaderboard 🥇")
    for idx, entry in enumerate(st.session_state['leaderboard'][:5]):
        st.sidebar.write(f"{idx+1}. {entry['user']} - {entry['score']} runs")

# Simulation Challenges
st.sidebar.subheader("Simulation Challenges 🎯")
for ch in st.session_state['challenges']:
    completed = ch['name'] in st.session_state['achievements']
    st.sidebar.write(f"{'✅' if completed else '⬜️'} **{ch['name']}**: {ch['desc']}")

# --- Real-time Streaming Data (Simulated) ---
st.sidebar.header("Live Data Feed")
import random, time
if 'live_traffic' not in st.session_state:
    st.session_state['live_traffic'] = random.randint(50, 100)
if 'live_pollution' not in st.session_state:
    st.session_state['live_pollution'] = random.randint(20, 80)
if st.sidebar.button("Update Live Data"):
    st.session_state['live_traffic'] = random.randint(50, 100)
    st.session_state['live_pollution'] = random.randint(20, 80)
st.sidebar.write(f"🚦 Traffic Index: {st.session_state['live_traffic']}")
st.sidebar.write(f"🌫️ Pollution Index: {st.session_state['live_pollution']}")

# --- Multi-language Support ---
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "French": "fr",
    "Italian": "it",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Russian": "ru",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Tamil": "ta",
    "Telugu": "te"
}
selected_language = st.sidebar.selectbox("🌐 Language", list(languages.keys()), index=0)

# Simple translation dictionary for scenario builder UI
translations = {
    "Scenario Builder": {
        "hi": "परिदृश्य निर्माता", "bn": "পরিকল্পনা নির্মাতা", "fr": "Générateur de scénario", "it": "Creatore di scenari", "es": "Creador de escenarios", "de": "Szenario-Generator", "zh": "场景生成器", "ja": "シナリオビルダー", "ru": "Создатель сценариев", "ar": "منشئ السيناريو", "pt": "Construtor de Cenários", "ta": "நிகழ்வு உருவாக்கி", "te": "సన్నివేశం బిల్డర్"
    },
    "Enter a scenario in plain English (e.g., 'Fire at hospital during traffic jam'):": {
        "hi": "साधारण अंग्रेज़ी में परिदृश्य दर्ज करें (जैसे, 'ट्रैफिक जाम के दौरान अस्पताल में आग'):",
        "bn": "সহজ ইংরেজিতে একটি পরিকল্পনা লিখুন (যেমন, 'ট্রাফিক জ্যামের সময় হাসপাতালে আগুন'):",
        "fr": "Entrez un scénario en français simple (ex: 'Incendie à l'hôpital pendant un embouteillage'):",
        "it": "Inserisci uno scenario in italiano semplice (es: 'Incendio in ospedale durante un ingorgo'):",
        "es": "Ingrese un escenario en español sencillo (ej: 'Incendio en hospital durante atasco'):",
        "de": "Geben Sie ein Szenario in einfachem Deutsch ein (z.B. 'Feuer im Krankenhaus während Stau'):",
        "zh": "用简单中文输入场景（例如：'交通堵塞期间医院起火'）：",
        "ja": "簡単な日本語でシナリオを入力してください（例：'渋滞中の病院火災'）：",
        "ru": "Введите сценарий на простом русском (например, 'Пожар в больнице во время пробки'):",
        "ar": "أدخل سيناريو باللغة العربية البسيطة (مثال: 'حريق في المستشفى أثناء ازدحام المرور'):",
        "pt": "Insira um cenário em português simples (ex: 'Incêndio no hospital durante engarrafamento'):",
        "ta": "எளிய தமிழில் நிகழ்வை உள்ளிடவும் (எ.கா., 'போக்குவரத்து நெரிசலில் மருத்துவமனையில் தீ'):",
        "te": "సాధారణ తెలుగు లో సన్నివేశాన్ని నమోదు చేయండి (ఉదా: 'ట్రాఫిక్ జామ్ సమయంలో ఆసుపత్రిలో అగ్ని ప్రమాదం'):" 
    },
    "Submit": {
        "hi": "जमा करें", "bn": "জমা দিন", "fr": "Soumettre", "it": "Invia", "es": "Enviar", "de": "Absenden", "zh": "提交", "ja": "送信", "ru": "Отправить", "ar": "إرسال", "pt": "Enviar", "ta": "சமர்ப்பிக்கவும்", "te": "సమర్పించండి"
    },
    "Scenario submitted!": {
        "hi": "परिदृश्य जमा किया गया!", "bn": "পরিকল্পনা জমা হয়েছে!", "fr": "Scénario soumis!", "it": "Scenario inviato!", "es": "¡Escenario enviado!", "de": "Szenario eingereicht!", "zh": "场景已提交！", "ja": "シナリオが送信されました！", "ru": "Сценарий отправлен!", "ar": "تم إرسال السيناريو!", "pt": "Cenário enviado!", "ta": "நிகழ்வு சமர்ப்பிக்கப்பட்டது!", "te": "సన్నివేశం సమర్పించబడింది!"
    },
    "Language": {
        "hi": "भाषा", "bn": "ভাষা", "fr": "Langue", "it": "Lingua", "es": "Idioma", "de": "Sprache", "zh": "语言", "ja": "言語", "ru": "Язык", "ar": "اللغة", "pt": "Idioma", "ta": "மொழி", "te": "భాష"
    }
}
def _(s):
    code = languages[selected_language]
    return translations.get(s, {}).get(code, s)

# --- Natural Language Scenario Builder ---
st.sidebar.header(_("Scenario Builder"))
nl_scenario = st.sidebar.text_area(_("Enter a scenario in plain English (e.g., 'Fire at hospital during traffic jam'):"), "")
if st.sidebar.button(_("Submit"), key="nl_scenario_submit"):
    if nl_scenario:
        st.session_state['custom_scenarios'].append({'name': nl_scenario, 'events': [nl_scenario]})
        st.sidebar.success(_("Scenario submitted!"))

# Remove Lottie, animated overlays, and card animation CSS
# (Restore previous dashboard look)

# Remove Lottie animation and animated gradient overlay
# (Uncomment to restore Lottie animation)
# lottie_ai = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_2glqweqs.json")  # GenAI/AI themed animation

# Place Lottie animation in sidebar (top) only if loaded successfully
# with st.sidebar:
#     if lottie_ai:
#         st_lottie(lottie_ai, height=120, key="ai_lottie", speed=1, loop=True)
#     else:
#         st.info("[AI Animation Unavailable]")

# Add animated gradient overlay to background (lower z-index, pointer-events: none)
# st.markdown('''
#     <style>
#     .stApp::after {
#         content: "";
#         position: fixed;
#         top: 0; left: 0; width: 100vw; height: 100vh;
#         pointer-events: none;
#         z-index: 0;
#         background: linear-gradient(270deg, #6366f1 0%, #a5b4fc 50%, #6366f1 100%);
#         opacity: 0.18;
#         background-size: 400% 400%;
#         animation: gradientMove 18s ease-in-out infinite;
#     }
#     @keyframes gradientMove {
#         0% { background-position: 0% 50%; }
#         50% { background-position: 100% 50%; }
#         100% { background-position: 0% 50%; }
#     }
#     </style>
# ''', unsafe_allow_html=True)

# Remove card entrance/hover and status animation CSS
# st.markdown('''
#     <style>
#     .stExpander {
#         animation: fadeInUp 0.8s cubic-bezier(.23,1.01,.32,1) both;
#         transition: box-shadow 0.2s;
#     }
#     .stExpander:hover {
#         box-shadow: 0 0 0 4px #6366f133, 0 4px 24px 0 rgba(99,102,241,0.15);
#         transform: translateY(-2px) scale(1.01);
#     }
#     @keyframes fadeInUp {
#         0% { opacity: 0; transform: translateY(40px); }
#         100% { opacity: 1; transform: translateY(0); }
#     }
#     .status-animated {
#         animation: pulseStatus 1.2s infinite alternate;
#     }
#     @keyframes pulseStatus {
#         0% { filter: brightness(1); }
#         100% { filter: brightness(1.5); }
#     }
#     </style>
# ''', unsafe_allow_html=True)

# Restore original status line in agent output cards
# (This was modified in the code block to be removed)
# st.markdown(f'<span style="color:{bar_color};font-weight:bold;">Status: {status}</span>', unsafe_allow_html=True)
