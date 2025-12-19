def check_eligibility(memory: dict):
    """
    Determine eligible government schemes
    based on collected user details.
    """
    schemes = []

    age = memory.get("age")
    income = memory.get("income")
    gender = memory.get("gender")
    occupation = memory.get("occupation")
    category = memory.get("category")
    state = memory.get("state")

    # ---------- Age + Income based schemes ----------
    if age is not None and income is not None:
        if age >= 18 and income <= 300000:
            schemes.append("PMAY")

        if income <= 500000:
            schemes.append("AYUSHMAN_BHARAT")

    # ---------- Occupation based ----------
    if occupation == "farmer":
        schemes.append("PM_KISAN")

    # ---------- Gender + Age ----------
    if gender == "female" and age is not None and age < 10:
        schemes.append("SUKANYA_SAMRIDDHI")

    # ---------- Category-based example ----------
    if category in ["sc", "st"] and income is not None and income <= 250000:
        schemes.append("SCHOLARSHIP_SC_ST")

    # ---------- State-based (example placeholder) ----------
    if state == "uttar_pradesh" and income is not None and income <= 200000:
        schemes.append("UP_SCHOLARSHIP")

    # Remove duplicates
    return list(set(schemes))


def fetch_scheme_details(scheme: str):
    """
    Fetch detailed information for a scheme
    (Hindi output for user consumption)
    """
    schemes = {

        "PMAY": {
            "name": "प्रधानमंत्री आवास योजना",
            "documents": [
                "आधार कार्ड",
                "आय प्रमाण पत्र",
                "निवास प्रमाण पत्र"
            ],
            "steps": [
                "pmaymis.gov.in वेबसाइट पर जाएँ",
                "ऑनलाइन आवेदन फॉर्म भरें",
                "आवश्यक दस्तावेज़ अपलोड करें",
                "आवेदन सबमिट करें"
            ]
        },

        "AYUSHMAN_BHARAT": {
            "name": "आयुष्मान भारत योजना",
            "documents": [
                "आधार कार्ड",
                "राशन कार्ड"
            ],
            "steps": [
                "pmjay.gov.in वेबसाइट पर जाएँ",
                "लाभार्थी पात्रता जाँचें",
                "नज़दीकी अस्पताल से संपर्क करें"
            ]
        },

        "PM_KISAN": {
            "name": "प्रधानमंत्री किसान सम्मान निधि",
            "documents": [
                "आधार कार्ड",
                "भूमि दस्तावेज़",
                "बैंक खाता विवरण"
            ],
            "steps": [
                "pmkisan.gov.in वेबसाइट पर जाएँ",
                "किसान पंजीकरण करें",
                "बैंक विवरण अपडेट करें"
            ]
        },

        "SUKANYA_SAMRIDDHI": {
            "name": "सुकन्या समृद्धि योजना",
            "documents": [
                "बालिका जन्म प्रमाण पत्र",
                "अभिभावक का आधार कार्ड"
            ],
            "steps": [
                "नज़दीकी डाकघर या बैंक जाएँ",
                "खाता खोलने का फॉर्म भरें",
                "न्यूनतम राशि जमा करें"
            ]
        },

        "SCHOLARSHIP_SC_ST": {
            "name": "एससी/एसटी छात्रवृत्ति योजना",
            "documents": [
                "जाति प्रमाण पत्र",
                "आय प्रमाण पत्र",
                "शैक्षणिक प्रमाण पत्र"
            ],
            "steps": [
                "राज्य छात्रवृत्ति पोर्टल पर जाएँ",
                "ऑनलाइन आवेदन करें",
                "दस्तावेज़ अपलोड करें"
            ]
        },

        "UP_SCHOLARSHIP": {
            "name": "उत्तर प्रदेश छात्रवृत्ति योजना",
            "documents": [
                "आधार कार्ड",
                "आय प्रमाण पत्र",
                "निवास प्रमाण पत्र"
            ],
            "steps": [
                "scholarship.up.gov.in वेबसाइट पर जाएँ",
                "पंजीकरण करें",
                "आवेदन फॉर्म भरें"
            ]
        }
    }

    return schemes.get(scheme)
