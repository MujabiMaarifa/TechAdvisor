import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Tech Support Expert System",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙️ Navigation")
st.sidebar.info("AI-powered Tech Support Expert System")

reasoning_method = st.sidebar.radio(
    "Choose reasoning method",
    ("Backward Chaining (Goal-driven)", "Forward Chaining (Data-driven)", "Both")
)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
# 🧠 Tech Support Expert System
### Intelligent diagnosis for common computer problems
---
""")

# =========================================================
# INPUTS
# =========================================================
symptoms = [
    "no_power", "slow_performance", "overheating", "no_internet",
    "blue_screen", "strange_noise", "battery_not_charging",
    "screen_flickering", "keyboard_not_working", "mouse_not_working",
    "app_crashing", "storage_full", "os_not_booting",
    "wifi_disconnects", "system_freezing"
]

col1, col2 = st.columns(2)

with col1:
    selected = st.multiselect("🔍 Select Symptoms", symptoms)

with col2:
    user_text = st.text_area(
        "📝 Describe the Problem",
        placeholder="e.g. my laptop is slow and keeps crashing",
        height=120
    )

# =========================================================
# NLP HELPER
# =========================================================
def extract_symptoms(text):
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
        "noise": "strange_noise",
        "freeze": "system_freezing"
    }

    found = set()
    for phrase, sym in mapping.items():
        if phrase in text:
            found.add(sym)
    return list(found)

# =========================================================
# DIAGNOSE BUTTON
# =========================================================
if st.button("🚀 Diagnose Issue", use_container_width=True):

    # -----------------------------------------------------
    # SAFE PROLOG LOADING (NO STREAMLIT CLOUD CRASH)
    # -----------------------------------------------------
    try:
        from pyswip import Prolog
        prolog = Prolog()
        prolog.consult("main.pl")
    except Exception:
        st.error(
            "❌ SWI-Prolog is not available in this environment.\n\n"
            "✔ Works locally\n"
            "❌ Not supported on Streamlit Cloud"
        )
        st.stop()

    # -----------------------------------------------------
    # RESET FACTS
    # -----------------------------------------------------
    list(prolog.query("retractall(has_symptom(_))"))
    list(prolog.query("retractall(derived_problem(_))"))

    # -----------------------------------------------------
    # ADD SYMPTOMS
    # -----------------------------------------------------
    final_symptoms = set(selected)
    final_symptoms.update(extract_symptoms(user_text))

    for s in final_symptoms:
        prolog.assertz(f"has_symptom({s})")

    # =====================================================
    # FORWARD CHAINING (SAFE)
    # =====================================================
    forward_results = []

    if reasoning_method in ("Forward Chaining (Data-driven)", "Both"):
        list(prolog.query("forward_chain_all()"))

        derived = list(prolog.query("derived_problem(P)"))

        for r in derived:
            p = r["P"]

            conf = list(prolog.query(f"confidence({p}, C)"))[0]["C"]
            sol  = list(prolog.query(f"solution({p}, S)"))[0]["S"]

            forward_results.append({
                "Problem": p.replace("_", " ").title(),
                "Confidence": int(conf * 100),
                "Solution": sol
            })

    # =====================================================
    # BACKWARD CHAINING (NO NESTED QUERIES ✅)
    # =====================================================
    backward_results = []

    if reasoning_method in ("Backward Chaining (Goal-driven)", "Both"):

        # IMPORTANT: materialize first
        bc_raw = list(prolog.query("diagnose_all(Problem)"))

        for r in bc_raw:
            prob = r["Problem"]

            conf = list(prolog.query(f"confidence({prob}, C)"))[0]["C"]
            sol  = list(prolog.query(f"solution({prob}, S)"))[0]["S"]

            backward_results.append({
                "Problem": prob.replace("_", " ").title(),
                "Confidence": int(conf * 100),
                "Solution": sol
            })

        # highest confidence (safe single query)
        best = list(prolog.query("select_highest_confidence(P,C)"))[0]
        best_problem = best["P"].replace("_", " ").title()

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================
    if forward_results or backward_results:

        st.markdown("## 📊 Diagnosis Results")

        for r in forward_results:
            st.info(
                f"**Forward Chaining** — {r['Problem']} "
                f"({r['Confidence']}%)\n\n{r['Solution']}"
            )

        for r in backward_results:
            badge = " ⭐ Highest Confidence" if r["Problem"] == best_problem else ""
            st.success(
                f"**Backward Chaining** — {r['Problem']} "
                f"({r['Confidence']}%){badge}\n\n{r['Solution']}"
            )
    else:
        st.warning("⚠️ No diagnosis could be inferred.")

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
---
👩‍💻 **Developed using Prolog + Python + Streamlit**  
🎓 *Academic Expert System Project*
""")
