# styles.py
# Premium CSS and HTML templates for SafeHer chatbot UI and animations.

# Custom Streamlit styles
CUSTOM_CSS = """
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,600;1,400&display=swap');

    /* Apply Typography and custom background variables */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header Gradient & Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 50%, #A18CD1 100%);
        padding: 3rem 2rem;
        border-radius: 24px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(161, 140, 209, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-banner h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .hero-banner p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        color: #ffffff !important;
        text-shadow: 0 1px 5px rgba(0,0,0,0.15);
    }
    
    /* Sleek card container */
    .custom-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 1.8rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.05);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(161, 140, 209, 0.15);
        border-color: rgba(161, 140, 209, 0.3);
    }

    /* Dark mode support card */
    [data-theme="dark"] .custom-card {
        background: rgba(25, 20, 35, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* SOS Emergency Banner */
    .sos-banner {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(255, 75, 43, 0.35);
        animation: pulseSOS 2s infinite alternate;
        margin-bottom: 2rem;
    }
    
    .sos-banner h2 {
        color: white !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .sos-banner p {
        color: #ffe8e8 !important;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    @keyframes pulseSOS {
        0% { box-shadow: 0 10px 30px rgba(255, 75, 43, 0.35); }
        100% { box-shadow: 0 10px 40px rgba(255, 75, 43, 0.6); }
    }

    /* Custom Chat Bubbles */
    .chat-bubble {
        padding: 1.2rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        max-width: 85%;
        line-height: 1.5;
        font-size: 1.05rem;
        display: flex;
        flex-direction: column;
        animation: slideUp 0.4s ease;
    }
    
    .chat-bubble.user {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        color: white !important;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(161, 140, 209, 0.2);
    }
    
    .chat-bubble.assistant {
        background: #f1f3f9;
        color: #2e3b4e !important;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    [data-theme="dark"] .chat-bubble.assistant {
        background: #231e2d;
        color: #e2e8f0 !important;
        border-color: rgba(255, 255, 255, 0.05);
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* SOS/Emergency Contact List Style */
    .contact-card {
        border-left: 5px solid #ff4b2b;
        background: rgba(255, 75, 43, 0.05);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.8rem;
    }

    /* Interactive Breathing Bubble */
    .breathing-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        background: rgba(161, 140, 209, 0.08);
        border-radius: 30px;
        border: 1px dashed rgba(161, 140, 209, 0.3);
        margin: 2rem auto;
        max-width: 400px;
        text-align: center;
    }

    .breathing-bubble {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #a18cd1 100%);
        border-radius: 50%;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(161, 140, 209, 0.4);
        animation: breathingCycle 16s infinite ease-in-out;
        position: relative;
    }

    .breathing-bubble::after {
        content: "";
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border-radius: 50%;
        border: 2px solid rgba(161, 140, 209, 0.2);
        animation: pulseRing 4s infinite linear;
    }

    .breathing-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #7b2cbf;
        margin-top: 1rem;
        min-height: 2.5rem;
        animation: textBreathing 16s infinite ease-in-out;
    }
    
    [data-theme="dark"] .breathing-text {
        color: #d8b4fe;
    }

    /* 16s Cycle: 4s Inhale, 4s Hold, 4s Exhale, 4s Hold */
    @keyframes breathingCycle {
        0%, 100% { transform: scale(1.0); box-shadow: 0 10px 25px rgba(161, 140, 209, 0.3); }
        25% { transform: scale(1.8); box-shadow: 0 20px 45px rgba(161, 140, 209, 0.7), 0 0 20px rgba(254, 207, 239, 0.8); }
        50% { transform: scale(1.8); box-shadow: 0 20px 45px rgba(161, 140, 209, 0.7), 0 0 30px rgba(161, 140, 209, 0.9); }
        75% { transform: scale(1.0); box-shadow: 0 10px 25px rgba(161, 140, 209, 0.3); }
    }

    @keyframes pulseRing {
        0% { transform: scale(1.0); opacity: 1; }
        100% { transform: scale(1.3); opacity: 0; }
    }

    @keyframes textBreathing {
        0%, 100% { content: "Hold (Breath Out)"; opacity: 0.8; }
        1%, 24% { content: "Inhale slowly..."; opacity: 1; }
        25%, 49% { content: "Hold breath..."; opacity: 1; }
        50%, 74% { content: "Exhale gently..."; opacity: 1; }
        75%, 99% { content: "Hold (Empty)..."; opacity: 1; }
    }

    /* Interactive Hug Animation Styling */
    .hug-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2.5rem;
        background: rgba(254, 207, 239, 0.15);
        border-radius: 24px;
        border: 1px solid rgba(254, 207, 239, 0.4);
        margin: 1rem 0 2rem 0;
        text-align: center;
        animation: fadeIn 1s ease;
    }
    
    [data-theme="dark"] .hug-container {
        background: rgba(161, 140, 209, 0.05);
        border-color: rgba(161, 140, 209, 0.15);
    }

    .hug-svg {
        width: 150px;
        height: 150px;
    }

    .hug-heart {
        fill: #ff4b72;
        transform-origin: center;
        animation: heartPulse 2.5s infinite ease-in-out;
    }

    .hug-arm-left {
        stroke: #fbc2eb;
        stroke-width: 8;
        stroke-linecap: round;
        fill: none;
        transform-origin: 40px 75px;
        animation: leftHug 3s infinite alternate ease-in-out;
    }

    .hug-arm-right {
        stroke: #fbc2eb;
        stroke-width: 8;
        stroke-linecap: round;
        fill: none;
        transform-origin: 110px 75px;
        animation: rightHug 3s infinite alternate ease-in-out;
    }

    @keyframes heartPulse {
        0%, 100% { transform: scale(1.0); }
        35% { transform: scale(1.15); }
        70% { transform: scale(1.05); }
    }

    @keyframes leftHug {
        0% { transform: rotate(-15deg); }
        100% { transform: rotate(18deg) translate(8px, -4px); }
    }

    @keyframes rightHug {
        0% { transform: rotate(15deg); }
        100% { transform: rotate(-18deg) translate(-8px, -4px); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
"""

# HTML template for the landing page animated Hug
HUG_HTML = """<div class="hug-container"><svg class="hug-svg" viewBox="0 0 150 150"><path class="hug-heart" d="M 75 45 C 50 15, 20 30, 20 60 C 20 95, 75 130, 75 130 C 75 130, 130 95, 130 60 C 130 30, 100 15, 75 45 Z" /><path class="hug-arm-left" d="M 15 80 Q 35 110, 60 90 Q 65 85, 62 80" /><path class="hug-arm-right" d="M 135 80 Q 115 110, 90 90 Q 85 85, 88 80" /></svg><div style="font-size: 1.3rem; font-weight: 600; color: #ff4b72; margin-top: 1rem;">You are safe, heard, and supported here.</div><div style="font-size: 0.95rem; opacity: 0.8; margin-top: 0.2rem; max-width: 400px; line-height: 1.4;">Welcome to SafeHer. We are here to listen, offer a calming hug, guide you on safety, or help with emotional comfort. Select a topic below or send a message to begin.</div></div>"""

