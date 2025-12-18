import streamlit as st
import os

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Tech Support Expert System",
    page_icon="🧠",
    layout="wide"
)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("⚙️ Navigation")
st.sidebar.info("AI-powered Tech Support Expert System")
st.sidebar.markdown("""
**Features**
- Forward & Backward Chaining
- Multiple Diagnoses
- Confidence Scores
- Conflict Resolution
- Natural Language Input
""")

reasoning_method = st.sidebar.radio(
    "Choose reasoning method",
    (
        "Backward Chaining (Goal-driven)",
        "Forward Chaining (Data-driven)",
        "Both"
    )
)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
# 🧠 Tech Support Expert System
### Intelligent diagnosis for common computer problems
---
""")

# -------------------------
# SYMPTOM INPUT
# -------------------------
col1, col2 = st.columns(2)

symptoms = [
    "no_power", "slow_performance", "overheating", "no_internet",
    "blue_screen", "strange_noise", "battery_not_charging",
    "screen_flickering", "keyboard_not_working", "mouse_not_working",
    "app_crashing", "storage_full", "os_not_booting",
    "wifi_disconnects", "system_freezing"
]

with col1:
    st.subheader("🔍 Select Symptoms")
    selected = st.multiselect("Choose all that apply", symptoms)

with col2:
    st.subheader("📝 Describe the Problem")
    user_text = st.text_area(
        "Use plain English",
        placeholder="e.g. my laptop is slow and keeps crashing",
        height=120
    )

# -------------------------
# NLP HELPER
# -------------------------
def extract_symptoms(text: str):
    text = text.lower()
    mapping = {
        "no power": "no_power",
        "won't turn on": "no_power",
        "slow": "slow_performance",
        "overheat": "overheating",
        "hot": "overheating",
        "no internet": "no_internet",
        "wifi disconnect": "wifi_disconnects",
        "blue screen": "blue_screen",
        "crash": "app_crashing",
        "battery not charging": "battery_not_charging",
        "screen flicker": "screen_flickering",
        "keyboard not working": "keyboard_not_working",
        "mouse not working": "mouse_not_working",
        "storage full": "storage_full",
        "won't boot": "os_not_booting",
        "strange noise": "strange_noise",
        "freezing": "system_freezing",
    }

    found = set()
    for phrase, symptom in mapping.items():
        if phrase in text:
            found.add(symptom)

    return list(found)

# -------------------------
# DIAGNOSE BUTTON
# -------------------------
st.markdown("###")

if st.button("🚀 Diagnose Issue", use_container_width=True):

    # -------- PROLOG SAFE LOAD --------
    try:
        from pyswip import Prolog
        prolog = Prolog()
        prolog.consult("main.pl")
    except Exception as e:
        st.error(
            "❌ SWI-Prolog is not available on Streamlit Cloud.\n\n"
            "✔️ This app works **locally** where SWI-Prolog is installed.\n"
            "ℹ️ Streamlit Cloud does not support native Prolog engines."
        )
        st.stop()

    # -------- RESET KB --------
    list(prolog.query("retractall(has_symptom(_))"))
    list(prolog.query("retractall(derived_problem(_))"))

    # -------- ADD SYMPTOMS --------
    final_symptoms = set(selected)
    final_symptoms.update(extract_symptoms(user_text))

    for s in final_symptoms:
        prolog.assertz(f"has_symptom({s})")

    # -------------------------
    # FORWARD CHAINING
    # -------------------------
    forward_results = []
    if reasoning_method in ("Forward Chaining (Data-driven)", "Both"):
        list(prolog.query("forward_chain_all()"))
        for r in prolog.query("derived_problem(DP)"):
            dp = r["DP"]
            conf = list(prolog.query(f"confidence({dp}, C)"))[0]["C"]
            sol = list(prolog.query(f"solution({dp}, S)"))[0]["S"]

            forward_results.append({
                "Problem": dp.replace("_", " ").title(),
                "Confidence": int(conf * 100),
                "Solution": sol
            })

    # -------------------------
    # BACKWARD CHAINING
    # -------------------------
    backward_results = []
    best_bc = None

    if reasoning_method in ("Backward Chaining (Goal-driven)", "Both"):
        for r in prolog.query("diagnose_all(Problem)"):
            prob = r["Problem"]
            conf = list(prolog.query(f"confidence({prob}, C)"))[0]["C"]
            sol = list(prolog.query(f"solution({prob}, S)"))[0]["S"]

            backward_results.append({
                "Problem": prob.replace("_", " ").title(),
                "Confidence": int(conf * 100),
                "Solution": sol
            })

        best = list(prolog.query("select_highest_confidence(Problem,C)"))[0]
        best_bc = best["Problem"].replace("_", " ").title()

    # -------------------------
    # DISPLAY RESULTS
    # -------------------------
    if forward_results or backward_results:

        st.markdown("### 📊 Reasoning Comparison")

        rows = max(len(forward_results), len(backward_results))
        table = []

        for i in range(rows):
            f = (
                f"{forward_results[i]['Problem']} ({forward_results[i]['Confidence']}%)"
                if i < len(forward_results) else ""
            )
            b = (
                f"{backward_results[i]['Problem']} ({backward_results[i]['Confidence']}%)"
                if i < len(backward_results) else ""
            )
            table.append({"Forward": f, "Backward": b})

        st.table(table)

        st.markdown("### 💡 Recommended Solutions")

        for r in forward_results:
            st.info(f"🔹 Forward: **{r['Problem']}** — {r['Solution']}")

        for r in backward_results:
            tag = " ⭐ Highest Confidence" if r["Problem"] == best_bc else ""
            st.info(f"🔸 Backward: **{r['Problem']}**{tag} — {r['Solution']}")

    else:
        st.warning("⚠️ No diagnosis could be derived from the given symptoms.")

# -------------------------
# FOOTER
# -------------------------
st.markdown("""
---
👨‍💻 **Developed using Prolog + Python + Streamlit**  
🎓 *Academic Expert System Project*
""")

