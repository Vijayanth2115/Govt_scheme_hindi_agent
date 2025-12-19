from tools import check_eligibility, fetch_scheme_details
from normalizer import normalize_by_state


YES_WORDS = ["हाँ", "हां", "जी", "जी हाँ", "ठीक", "सही", "ok"]
NO_WORDS = ["नहीं", "नही", "गलत", "no"]

class GovtSchemeAgent:
    def __init__(self, memory):
        self.state = "START"
        self.memory = memory
        self.eligible_schemes = []

        self.pending_key = None
        self.pending_value = None
        self.next_state = None

    def is_yes(self, text):
        return any(w in text.lower() for w in YES_WORDS)

    def is_no(self, text):
        return any(w in text.lower() for w in NO_WORDS)

    def step(self, user_input):

        # ---------- START ----------
        if self.state == "START":
            self.state = "INTRO"
            return (
                "नमस्कार। मैं एक सरकारी योजना सहायक हूँ। "
                "मैं आपकी पात्रता के अनुसार योजनाओं की जानकारी दूँगा।"
            )

        if self.state == "INTRO":
            self.state = "ASK_AGE"
            return "सबसे पहले, कृपया अपनी उम्र बताइए।"

        # ---------- AGE ----------
        if self.state == "ASK_AGE":
            
            print("STATE : ASK_AGE")
            value = normalize_by_state(user_input, "ASK_AGE")
            if not value or not value.isdigit():
                return "कृपया अपनी उम्र फिर से बताइए।"

            self.pending_key = "age"
            self.pending_value = int(value)
            self.next_state = "ASK_INCOME"
            self.state = "CONFIRM"
            return f"मैं आपकी उम्र {value} वर्ष मान रहा हूँ। क्या यह सही है?"

        # ---------- INCOME ----------
        if self.state == "ASK_INCOME":
            
            print("STATE : ASK_INCOME")
            value = normalize_by_state(user_input, "ASK_INCOME")
            if not value or not value.isdigit():
                return "धन्यवाद। अब कृपया अपनी वार्षिक आय फिर से बताइए।"

            self.pending_key = "income"
            self.pending_value = int(value)
            self.next_state = "ASK_STATE"
            self.state = "CONFIRM"
            return f"मैं आपकी वार्षिक आय {value} रुपये मान रहा हूँ। क्या यह सही है?"

        # ---------- STATE ----------
        if self.state == "ASK_STATE":
            
            print("STATE : ASK_STATE")
            value = normalize_by_state(user_input, "ASK_STATE")
            if not value:
                return "धन्यवाद। अब कृपया अपना राज्य फिर से बताइए।"

            self.pending_key = "state"
            self.pending_value = value
            self.next_state = "ASK_CATEGORY"
            self.state = "CONFIRM"
            return f"आप {value} राज्य में रहते हैं। क्या यह सही है?"

        # ---------- CATEGORY ----------
        if self.state == "ASK_CATEGORY":
            
            print("STATE : ASK_CATEGORY")
            value = normalize_by_state(user_input, "ASK_CATEGORY")
            if not value:
                return "धन्यवाद। अब कृपया अपनी श्रेणी बताइए (SC, ST, OBC, सामान्य)।"

            self.pending_key = "category"
            self.pending_value = value
            self.next_state = "ASK_GENDER"
            self.state = "CONFIRM"
            return f"आपकी श्रेणी {value.upper()} है। क्या यह सही है?"

        # ---------- GENDER ----------
        if self.state == "ASK_GENDER":
            
            print("STATE : ASK_GENDER")
            value = normalize_by_state(user_input, "ASK_GENDER")
            if not value:
                return "धन्यवाद। अब कृपया अपना लिंग बताइए।"

            self.pending_key = "gender"
            self.pending_value = value
            self.next_state = "ASK_OCCUPATION"
            self.state = "CONFIRM"
            return f"मैं आपका लिंग {value} मान रहा हूँ। क्या यह सही है?"

        # ---------- OCCUPATION ----------
        if self.state == "ASK_OCCUPATION":
            
            print("STATE : ASK_OCCUPATION")
            value = normalize_by_state(user_input, "ASK_OCCUPATION")
            if not value:
                return "धन्यवाद। अब कृपया अपना व्यवसाय बताइए।"

            self.pending_key = "occupation"
            self.pending_value = value
            self.next_state = "CHECK_ELIGIBILITY"
            self.state = "CONFIRM"
            return f"आपका व्यवसाय {value} है। क्या यह सही है?"

        # ---------- CONFIRM ----------
        # if self.state == "CONFIRM":
        #     if self.is_yes(user_input):
        #         self.memory.set(self.pending_key, self.pending_value)
        #         self.state = self.next_state
        #         return "धन्यवाद।"

        #     if self.is_no(user_input):
        #         self.state = f"ASK_{self.pending_key.upper()}"
        #         return "ठीक है, कृपया फिर से बताइए।"

        #     return "कृपया हाँ या नहीं में उत्तर दीजिए।"
        
        # ---------- CONFIRM ----------
        if self.state == "CONFIRM":
            if self.is_yes(user_input):
                self.memory.set(self.pending_key, self.pending_value)
                self.state = self.next_state
                return None   # 🔥 auto-continue

            if self.is_no(user_input):
                self.state = f"ASK_{self.pending_key.upper()}"
                return "ठीक है, कृपया फिर से बताइए।"

            return "कृपया हाँ या नहीं में उत्तर दीजिए।"
        

        # ---------- CHECK ----------
        if self.state == "CHECK_ELIGIBILITY":
            eligible = check_eligibility(self.memory.data)

            print("CHECK_ELIGIBILITY tool called \n")
            
            if not eligible:
                self.state = "END"
                return "क्षमा करें, आप वर्तमान में किसी सरकारी योजना के लिए पात्र नहीं हैं।"

            self.eligible_schemes = eligible
            self.state = "FETCH_ALL"
            return "आप निम्नलिखित सरकारी योजनाओं के लिए पात्र हैं। विवरण बता रहा हूँ।"

        # ---------- FETCH ----------
        if self.state == "FETCH_ALL":
            
            print("FETCH_ALL Tool called \n")
            response = ""
            
            
            for scheme in self.eligible_schemes:
                d = fetch_scheme_details(scheme)
                response += f"\nयोजना का नाम: {d['name']}\n"
                response += "आवश्यक दस्तावेज़:\n"
                for doc in d["documents"]:
                    response += f"- {doc}\n"
                response += "आवेदन प्रक्रिया:\n"
                for s in d["steps"]:
                    response += f"- {s}\n"

            self.state = "END"
            return response
