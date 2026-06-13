# resources.py
# Database of emergency contacts, legal rights, well-being guides, and affirmations for SafeHer.

HELPLINES = {
    "Emergency Helpline (All-in-One)": {
        "number": "112",
        "description": "National emergency response support system for police, fire, and health services."
    },
    "Police Helpline": {
        "number": "100",
        "description": "Direct police assistance hotline."
    },
    "Women's Helpline (Domestic Abuse)": {
        "number": "1091",
        "description": "Dedicated toll-free 24/7 hotline for women in distress or facing domestic violence."
    },
    "Women's Helpline (Alternate)": {
        "number": "181",
        "description": "Direct national support line for women victims of violence."
    },
    "Cybercrime Helpline": {
        "number": "1930",
        "description": "National helpline to report cyber frauds, cyberstalking, and digital harassment immediately."
    },
    "National Commission for Women (NCW)": {
        "number": "011-26944880",
        "description": "NCW helpline for reporting violence against women or seeking legal counsel."
    },
    "Child / Student Helpline": {
        "number": "1098",
        "description": "Toll-free, 24-hour phone outreach service for children in distress."
    },
    "National Human Rights Commission": {
        "number": "144333",
        "description": "Toll-free number to report severe violations of civil rights and human rights."
    }
}

STATE_HELPLINES = [
    {"State": "Andhra Pradesh", "Police": "100 / 112", "Women Helpline": "1091 / 181"},
    {"State": "Bihar", "Police": "100 / 112", "Women Helpline": "1091 / 181"},
    {"State": "Delhi", "Police": "100 / 112", "Women Helpline": "1091 / 181 / 1096"},
    {"State": "Gujarat", "Police": "100 / 112", "Women Helpline": "1091 / 181 (Abhayam)"},
    {"State": "Karnataka", "Police": "100 / 112", "Women Helpline": "1091 / 181"},
    {"State": "Maharashtra", "Police": "100 / 112", "Women Helpline": "1091 / 181"},
    {"State": "Tamil Nadu", "Police": "100 / 112", "Women Helpline": "1091 / 181"},
    {"State": "Telangana", "Police": "100 / 112", "Women Helpline": "1091 / 181 / 100"},
    {"State": "Uttar Pradesh", "Police": "100 / 112", "Women Helpline": "1090 (Women Power Line)"},
    {"State": "West Bengal", "Police": "100 / 112", "Women Helpline": "1091 / 181"}
]

WOMENS_RIGHTS = {
    "Right to Zero FIR": {
        "summary": "A woman can file an FIR at any police station, regardless of where the incident occurred.",
        "details": "A Zero FIR is registered under a temporary serial number '0'. It is subsequently transferred to the police station that has the jurisdiction to investigate the crime. This ensures that the police cannot refuse to file a complaint on jurisdictional grounds, saving crucial time in emergencies."
    },
    "Right to No Arrest after Sunset": {
        "summary": "A woman cannot be arrested after sunset and before sunrise, except under extraordinary circumstances.",
        "details": "Section 46(4) of the Code of Criminal Procedure (CrPC) mandates that a woman cannot be arrested between 6:00 PM and 6:00 AM unless there is an exceptional circumstance and a prior written permission is obtained from a Judicial Magistrate First Class. Additionally, the arrest must be carried out by a woman police officer."
    },
    "Right to Free Legal Aid": {
        "summary": "Women are entitled to free legal counsel and representation in court.",
        "details": "Under Section 12 of the Legal Services Authorities Act, 1987, all women, regardless of their financial status, income, or background, are entitled to free legal services. This includes free legal advice, representation, and filing of documents in court."
    },
    "Right to Privacy & Confidentiality": {
        "summary": "A victim's identity and statements must be kept completely private and confidential.",
        "details": "Under Section 228A of the Indian Penal Code (IPC), disclosing the identity, name, or address of a victim of sexual offenses is a punishable crime. Additionally, statements must be recorded at the victim's residence or a place of choice in the presence of a female police officer and family members."
    },
    "Protection of Women from Domestic Violence Act (2005)": {
        "summary": "Protects women from physical, emotional, sexual, verbal, and economic abuse in domestic relationships.",
        "details": "This civil law protects not just wives, but sisters, mothers, and live-in partners. It provides women with the right to reside in their shared household, protection orders, monetary relief, custody of children, and free medical aid."
    },
    "POSH Act - Workplace Safety (2013)": {
        "summary": "Protects women from sexual harassment at their workplace.",
        "details": "The Prevention of Sexual Harassment (POSH) Act mandates that every organization with 10 or more employees must establish an Internal Complaints Committee (ICC) headed by a woman. The ICC must investigate sexual harassment allegations within 90 days."
    },
    "Maternity Benefit Act": {
        "summary": "Entitles working women to fully paid leave and maternity benefits.",
        "details": "This act regulates the employment of women in certain establishments for certain periods before and after childbirth. It mandates a minimum of 26 weeks of paid maternity leave for women working in companies with 10 or more employees."
    }
}

CYBERCRIME_STEPS = [
    {
        "step": "1. Save Digital Evidence",
        "action": "Take screenshots, download emails, print chat logs, and save profile URLs of the perpetrators. Do not delete the conversation or block the user immediately without saving proof first."
    },
    {
        "step": "2. File an Online Complaint",
        "action": "Visit the official National Cyber Crime Reporting Portal at https://cybercrime.gov.in and click on 'Report Women/Child Related Crime'. Fill in the details and upload the saved evidence."
    },
    {
        "step": "3. Call the Cyber Helpline",
        "action": "In case of urgent cybercrimes or financial fraud, immediately dial 1930. The call centre will assist in blocking unauthorized transactions or initiating immediate actions."
    },
    {
        "step": "4. Report on the Platform",
        "action": "Use the built-in report/abuse mechanisms of social media platforms (Instagram, Facebook, X, WhatsApp) to report harassment. This helps in quick removal of offensive content."
    },
    {
        "step": "5. Local Police Station",
        "action": "You can also file a written complaint with any local police station or specialized Cyber Crime Cells in your city. Bring a copy of the digital evidence."
    }
]

AFFIRMATIONS = [
    "I am strong, resilient, and capable of overcoming any challenge.",
    "My safety and peace of mind are non-negotiable priorities.",
    "I deserve to feel safe, respected, and valued in every space I enter.",
    "I trust my intuition; it is my inner compass and guide.",
    "I hold the power to shape my future and set healthy boundaries.",
    "I am worthy of love, happiness, peace, and absolute safety.",
    "I am not defined by my past; I am defining my present and future.",
    "I choose to be kind to myself, take deep breaths, and take one step at a time.",
    "My feelings are valid, my voice matters, and my presence is important.",
    "I possess the strength to speak up and seek support whenever I need it."
]

GROUNDING_STEPS = {
    "overview": "The 5-4-3-2-1 technique is a simple, effective grounding exercise that helps quiet the mind and pull you back into the present moment by engaging your 5 senses.",
    "steps": [
        {"title": "👁️ 5 - SEE", "desc": "Look around and name FIVE things you can see in your immediate surroundings. (e.g., a chair, a picture, a glass, a pen, a shadow)."},
        {"title": "👉 4 - TOUCH", "desc": "Identify FOUR things you can touch or feel. Focus on their textures and temperatures. (e.g., your clothes, the desk, the floor, your hair)."},
        {"title": "👂 3 - HEAR", "desc": "Listen closely and name THREE distinct sounds you can hear. (e.g., fan humming, birds chirping, distant traffic, your breathing)."},
        {"title": "👃 2 - SMELL", "desc": "Notice and name TWO things you can smell right now. (e.g., coffee, soap, flowers, fresh air, wood)."},
        {"title": "👅 1 - TASTE", "desc": "Focus on ONE thing you can taste. If nothing is around, focus on the clean taste of water or the natural state of your mouth."}
    ]
}
