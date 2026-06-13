# app.py
# SafeHer: AI-Powered Women's Safety and Emotional Support Chatbot
# Developed with Python, Streamlit, Custom CSS/HTML, and Ollama.

import streamlit as st
import pandas as pd
import random
import urllib.parse
from styles import CUSTOM_CSS, HUG_HTML
from resources import HELPLINES, STATE_HELPLINES, WOMENS_RIGHTS, CYBERCRIME_STEPS, AFFIRMATIONS, GROUNDING_STEPS
from bot import detect_crisis, generate_response, check_ollama_status

# Page configuration
st.set_page_config(
    page_title="SafeHer - Safety & Support Chatbot",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# State initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "safety"
if "custom_contact_name" not in st.session_state:
    st.session_state.custom_contact_name = "Emergency Contact"
if "custom_contact_phone" not in st.session_state:
    st.session_state.custom_contact_phone = ""
if "crisis_mode" not in st.session_state:
    st.session_state.crisis_mode = False
if "trigger_gps" not in st.session_state:
    st.session_state.trigger_gps = False
if "latitude" not in st.session_state:
    st.session_state.latitude = None
if "longitude" not in st.session_state:
    st.session_state.longitude = None

# Sync coordinates from query parameters
query_params = st.query_params
if "lat" in query_params and "lon" in query_params:
    try:
        st.session_state.latitude = float(query_params["lat"])
        st.session_state.longitude = float(query_params["lon"])
    except ValueError:
        pass

# Sidebar Layout
st.sidebar.markdown("<h2 style='text-align: center; color: #a18cd1; font-family: Playfair Display, serif;'>🌸 SafeHer Panel</h2>", unsafe_allow_html=True)

# Mode Selector
st.sidebar.markdown("### 🎛️ Mode Selector")
mode_choice = st.sidebar.radio(
    "Choose Chatbot Mode:",
    options=["Safety Assistant Mode", "Emotional Support Mode"],
    index=0 if st.session_state.selected_mode == "safety" else 1,
    help="Safety Assistant answers safety/legal questions. Emotional Support Mode offers empathetic comfort."
)
# Update mode in state
new_mode = "safety" if "Safety" in mode_choice else "support"
if new_mode != st.session_state.selected_mode:
    st.session_state.selected_mode = new_mode
    st.rerun()

st.sidebar.markdown("---")

# SOS Contacts configuration
st.sidebar.markdown("### 📞 SOS Emergency Contacts")
contact_name = st.sidebar.text_input("Contact Name (e.g., Parent, Friend)", value=st.session_state.custom_contact_name)
contact_phone = st.sidebar.text_input("Contact Phone Number (with Country Code, e.g., +919876543210)", value=st.session_state.custom_contact_phone)

# Save contacts in state
st.session_state.custom_contact_name = contact_name
st.session_state.custom_contact_phone = contact_phone

# Geolocation Action in Sidebar
st.sidebar.markdown("### 📍 Live GPS Location")
col_gps_1, col_gps_2 = st.sidebar.columns(2)

with col_gps_1:
    if st.button("🛰️ Fetch GPS", help="Acquires live location from your browser"):
        st.session_state.trigger_gps = True

with col_gps_2:
    if st.button("🗑️ Clear GPS", help="Clears stored location data"):
        st.query_params.clear()
        st.session_state.latitude = None
        st.session_state.longitude = None
        st.rerun()

# Display current GPS status in sidebar
if st.session_state.latitude and st.session_state.longitude:
    st.sidebar.success(f"Location Captured!\nLat: {st.session_state.latitude:.4f}, Lon: {st.session_state.longitude:.4f}")
else:
    st.sidebar.info("Location: Not Shared")

# Invisible Iframe to capture geolocation when triggered
if st.session_state.trigger_gps:
    st.components.v1.html(
        """
        <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        const parentUrl = new URL(window.parent.location.href);
                        parentUrl.searchParams.set("lat", lat);
                        parentUrl.searchParams.set("lon", lon);
                        window.parent.location.href = parentUrl.toString();
                    },
                    (error) => {
                        console.error("GPS fetch error", error);
                        alert("Could not fetch location. Please ensure site permissions are granted.");
                    },
                    { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
                );
            } else {
                alert("Geolocation is not supported by your browser.");
            }
        }
        getLocation();
        </script>
        """,
        height=0,
        width=0
    )

st.sidebar.markdown("---")

# Ollama Server Connection Settings
st.sidebar.markdown("### ⚙️ Ollama LLM Configuration")
ollama_url = st.sidebar.text_input("Ollama Server URL", value="http://localhost:11434")

# Check connectivity
ollama_connected = check_ollama_status(ollama_url)

if ollama_connected:
    st.sidebar.markdown("<span style='color:green'>● Connected to Ollama</span>", unsafe_allow_html=True)
    
    # Sensible models available
    available_models = ["gemma3:1b", "qwen3:8b", "phi3:latest"]
    
    # Let user pick model for current mode
    if st.session_state.selected_mode == "safety":
        model_choice_ollama = st.sidebar.selectbox("Ollama Model (Safety Mode)", options=available_models, index=0)
        st.session_state.safety_model = model_choice_ollama
    else:
        model_choice_ollama = st.sidebar.selectbox("Ollama Model (Support Mode)", options=available_models, index=1)
        st.session_state.support_model = model_choice_ollama
else:
    st.sidebar.markdown("<span style='color:orange'>● Ollama Offline (Running in Heuristic Simulator Mode)</span>", unsafe_allow_html=True)
    st.sidebar.caption("To connect, run 'ollama serve' locally on your machine.")

# Main Application Layout
st.markdown("<div class='hero-banner'><h1>SafeHer</h1><p>AI-Powered Women's Safety Counsel & Emotional Well-being Sanctuary</p></div>", unsafe_allow_html=True)

# Tabs
tab_chat, tab_resources, tab_wellbeing = st.tabs([
    "💬 Chat Assistant", 
    "🛡️ Resources & Legal Rights", 
    "🌸 Well-being Space"
])

# Quick Action handler (adds a prompt to history and triggers response)
def trigger_quick_action(prompt_text):
    st.session_state.chat_history.append({"role": "user", "content": prompt_text})
    
    # Check for crisis
    if detect_crisis(prompt_text):
        st.session_state.crisis_mode = True
        response = "Crisis detected. Intercepting and launching SOS panel."
    else:
        selected_model = (st.session_state.safety_model if st.session_state.selected_mode == "safety" 
                          else st.session_state.support_model) if ollama_connected else "fallback"
        response = generate_response(
            prompt=prompt_text,
            history=st.session_state.chat_history[:-1],
            mode=st.session_state.selected_mode,
            model=selected_model,
            url=ollama_url
        )
    
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

# ----------------- TAB 1: CHAT ASSISTANT -----------------
with tab_chat:
    # Manual SOS Button
    col_header_1, col_header_2 = st.columns([8, 2])
    with col_header_2:
        if st.button("🚨 TRIGGER SOS", type="primary", use_container_width=True, help="Immediately open Emergency SOS panel"):
            st.session_state.crisis_mode = True
            st.rerun()
            
    # Crisis Mode Display
    if st.session_state.crisis_mode:
        st.markdown("""
        <div class="sos-banner">
            <h2>🚨 EMERGENCY SOS PANEL TRIGGERED 🚨</h2>
            <p>Your safety is the absolute priority. Please review the emergency links below and call immediately.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid for SOS actions
        col_sos_1, col_sos_2, col_sos_3 = st.columns(3)
        
        # 1. Direct Call Police Button
        with col_sos_1:
            st.markdown(
                '<a href="tel:112" style="text-decoration: none;">'
                '<div style="background: #ff4b2b; color: white; padding: 1.5rem; text-align: center; border-radius: 16px; font-weight: 800; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(255,75,43,0.3);">'
                '📞 CALL POLICE (112)'
                '</div></a>',
                unsafe_allow_html=True
            )
            st.caption("Click to call the national emergency response support system directly.")
            
        # 2. WhatsApp/SMS share with location
        # Construct SMS & WhatsApp message
        location_msg = "EMERGENCY! I need immediate help. "
        if st.session_state.latitude and st.session_state.longitude:
            location_msg += f"My live location is: https://maps.google.com/?q={st.session_state.latitude},{st.session_state.longitude}"
        else:
            location_msg += "(Location not available - please call/check on me immediately!)"
            
        encoded_msg = urllib.parse.quote(location_msg)
        phone = st.session_state.custom_contact_phone if st.session_state.custom_contact_phone else ""
        whatsapp_url = f"https://wa.me/{phone.replace('+', '')}?text={encoded_msg}"
        sms_url = f"sms:{phone}?body={encoded_msg}"
        
        with col_sos_2:
            st.markdown(
                f'<a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">'
                '<div style="background: #25D366; color: white; padding: 1.5rem; text-align: center; border-radius: 16px; font-weight: 800; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(37,211,102,0.3);">'
                '💬 SEND WA SOS'
                '</div></a>',
                unsafe_allow_html=True
            )
            if phone:
                st.caption(f"Send pre-filled SOS WhatsApp to {st.session_state.custom_contact_name} ({phone}).")
            else:
                st.caption("Send SOS location text. Set contact phone in the sidebar first!")
                
        with col_sos_3:
            st.markdown(
                f'<a href="{sms_url}" style="text-decoration: none;">'
                '<div style="background: #007AFF; color: white; padding: 1.5rem; text-align: center; border-radius: 16px; font-weight: 800; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(0,122,255,0.3);">'
                '✉️ SEND SMS SOS'
                '</div></a>',
                unsafe_allow_html=True
            )
            st.caption("Send native SMS text message with coordinates (on mobile).")

        # Map display if location exists
        if st.session_state.latitude and st.session_state.longitude:
            st.markdown("### 📍 Your Captured Live Location")
            map_data = pd.DataFrame({
                'lat': [st.session_state.latitude],
                'lon': [st.session_state.longitude]
            })
            st.map(map_data, zoom=14)
            st.info("Emergency services and your contact can find you using these coordinates.")
        else:
            st.warning("GPS coordinates not captured yet. Click '🛰️ Fetch GPS' in the sidebar to load coordinates onto the map and SOS links.")

        # Help line cards
        st.markdown("### ☎️ Critical Help Numbers")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown("""
            <div class="contact-card">
                <strong>Women Helpline</strong><br/>
                <span style="font-size: 1.3rem; font-weight: bold; color: #ff4b2b;">1091</span><br/>
                Toll-free 24/7 helpline for domestic abuse, harassment, or counseling.
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
            <div class="contact-card">
                <strong>Domestic Violence</strong><br/>
                <span style="font-size: 1.3rem; font-weight: bold; color: #ff4b2b;">181</span><br/>
                Toll-free support for women facing domestic violence.
            </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown("""
            <div class="contact-card">
                <strong>Cyber Crime Cell</strong><br/>
                <span style="font-size: 1.3rem; font-weight: bold; color: #ff4b2b;">1930</span><br/>
                Call for online safety, hacking, cyberstalking, and digital threats.
            </div>
            """, unsafe_allow_html=True)

        if st.button("❌ Close SOS Panel & Return to Chat"):
            st.session_state.crisis_mode = False
            st.rerun()
            
    else:
        # Standard Chat Mode
        if len(st.session_state.chat_history) == 0:
            # Landing page welcome animation
            st.markdown(HUG_HTML, unsafe_allow_html=True)
            
            # Quick Actions Section
            st.markdown("### ⚡ Quick Start Prompts")
            
            if st.session_state.selected_mode == "safety":
                col_q1, col_q2, col_q3 = st.columns(3)
                with col_q1:
                    if st.button("⚖️ What is a Zero FIR?", use_container_width=True):
                        trigger_quick_action("What is a Zero FIR and when can I use it?")
                with col_q2:
                    if st.button("💻 Report Online Harassment", use_container_width=True):
                        trigger_quick_action("How do I report cyber stalking or online harassment?")
                with col_q3:
                    if st.button("🌙 Arrest Rights after Sunset", use_container_width=True):
                        trigger_quick_action("What are my rights regarding arrest after sunset?")
            else:
                col_q1, col_q2, col_q3 = st.columns(3)
                with col_q1:
                    if st.button("🌸 Daily Affirmation", use_container_width=True):
                        trigger_quick_action("Can you give me an uplifting daily affirmation?")
                with col_q2:
                    if st.button("🌬️ Calm My Anxiety", use_container_width=True):
                        trigger_quick_action("I am feeling stressed and anxious. Can you help me calm down?")
                with col_q3:
                    if st.button("⭐ Boost My Confidence", use_container_width=True):
                        trigger_quick_action("I have a big interview/event and I'm feeling insecure. Can you give me a confidence boost?")
        
        # Render chat messages
        for message in st.session_state.chat_history:
            bubble_class = "user" if message["role"] == "user" else "assistant"
            st.markdown(
                f'<div class="chat-bubble {bubble_class}">{message["content"]}</div>', 
                unsafe_allow_html=True
            )
            
        # Chat input
        user_input = st.chat_input("Write your message here...")
        
        if user_input:
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.markdown(f'<div class="chat-bubble user">{user_input}</div>', unsafe_allow_html=True)
            
            # Crisis detection
            if detect_crisis(user_input):
                st.session_state.crisis_mode = True
                st.session_state.chat_history.append({"role": "assistant", "content": "[🚨 Crisis Triggered: Launching SOS Panel]"})
                st.rerun()
            else:
                # Generate AI Response
                with st.spinner("Writing response..."):
                    selected_model = (st.session_state.safety_model if st.session_state.selected_mode == "safety" 
                                      else st.session_state.support_model) if ollama_connected else "fallback"
                    response = generate_response(
                        prompt=user_input,
                        history=st.session_state.chat_history[:-1],
                        mode=st.session_state.selected_mode,
                        model=selected_model,
                        url=ollama_url
                    )
                # Append assistant message
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

# ----------------- TAB 2: RESOURCES & LEGAL RIGHTS -----------------
with tab_resources:
    st.markdown("## 🛡️ Women's Rights & Emergency Resources")
    st.write("Browse legal information, reporting procedures, and contacts directly from our database.")
    
    # Helplines Section
    st.markdown("### 📞 National Support Helplines")
    col_list = list(HELPLINES.keys())
    
    # Grid of helplines
    h_col1, h_col2 = st.columns(2)
    for i, name in enumerate(col_list):
        target_col = h_col1 if i % 2 == 0 else h_col2
        with target_col:
            st.markdown(f"""
            <div class="custom-card" style="padding: 1.2rem;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #7b2cbf;">{name}</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #ff4b2b; margin: 0.2rem 0;">
                    <a href="tel:{HELPLINES[name]['number']}" style="color: #ff4b2b; text-decoration: none;">{HELPLINES[name]['number']}</a>
                </div>
                <div style="font-size: 0.95rem; opacity: 0.8;">{HELPLINES[name]['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    # Legal rights documentation
    st.markdown("### ⚖️ Legal Rights You Should Know")
    for right, details in WOMENS_RIGHTS.items():
        with st.expander(right):
            st.markdown(f"**Summary:** {details['summary']}")
            st.write(details['details'])
            
    # Cybercrime reporting steps
    st.markdown("### 💻 How to Report Cybercrime & Stalking")
    for step in CYBERCRIME_STEPS:
        st.markdown(f"**{step['step']}**")
        st.write(step['action'])
        st.markdown("---")

    # State wise emergency numbers
    st.markdown("### 🏢 State-wise Helpline Directory")
    state_df = pd.DataFrame(STATE_HELPLINES)
    st.dataframe(state_df, use_container_width=True)

# ----------------- TAB 3: WELL-BEING SPACE -----------------
with tab_wellbeing:
    st.markdown("## 🌸 Mental Well-being & Stress Relief Sanctuary")
    st.write("Take a moment to center yourself, breathe, and restore your calm.")
    
    well_tab1, well_tab2, well_tab3 = st.tabs([
        "🌬️ Guided Breathing", 
        "⭐ Positive Affirmations", 
        "🧩 Grounding Exercises (5-4-3-2-1)"
    ])
    
    # Well tab 1: Guided Breathing Bubble
    with well_tab1:
        st.markdown("### 🌬️ Box Breathing Exercise")
        st.write("Box breathing is a technique used to calm the nervous system. Follow the pulsing circle: Inhale as it expands, hold, exhale as it shrinks, and hold.")
        
        # Display the custom CSS-animated breathing visualizer
        st.markdown(
            """
            <div class="breathing-box">
                <div class="breathing-bubble"></div>
                <div class="breathing-text">Inhale slowly...</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    # Well tab 2: Affirmations
    with well_tab2:
        st.markdown("### ⭐ Positive Affirmations")
        st.write("Generate a positive affirmation to build your confidence and offer emotional support.")
        
        # Affirmation space
        if "current_affirmation" not in st.session_state:
            st.session_state.current_affirmation = AFFIRMATIONS[0]
            
        if st.button("🌸 Generate New Affirmation", type="secondary"):
            st.session_state.current_affirmation = random.choice(AFFIRMATIONS)
            
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%); padding: 2.5rem; border-radius: 20px; text-align: center; margin: 1.5rem 0; box-shadow: 0 5px 15px rgba(255, 154, 158, 0.25);">
            <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.6rem; color: #6d1c32; line-height: 1.5;">
                "{st.session_state.current_affirmation}"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Well tab 3: 5-4-3-2-1 grounding
    with well_tab3:
        st.markdown("### 🧩 The 5-4-3-2-1 Grounding Technique")
        st.write(GROUNDING_STEPS["overview"])
        
        st.write("Take a deep breath and work through the steps below, acknowledging each detail in your space:")
        
        for step in GROUNDING_STEPS["steps"]:
            with st.expander(step["title"]):
                st.write(step["desc"])
                st.checkbox("I have observed this", key=f"ground_{step['title']}")
