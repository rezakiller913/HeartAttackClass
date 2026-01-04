import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Cardiac Risk Assessment System",
    page_icon="🫀",
    layout="centered"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
body { background-color: #f4f9ff; }
h1, h2, h3 { color: #0b3c5d; }
.stButton>button {
    background-color: #0b5ed7;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    padding: 10px;
    width: 100%;
}
.section {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("## 🫀 Cardiac Risk Assessment System")
st.markdown(
    "Clinical Decision Support System using **Explainable Rule-Based Knowledge**"
)

# =========================
# INPUT FORM
# =========================
with st.form("patient_form"):

    st.markdown("### 🧑‍⚕️ Patient Demographics")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(
            "Age (years)", 1, 120, 50,
            help="Risk increases with age."
        )
    with col2:
        gender = st.selectbox(
            "Gender", ["Female", "Male"],
            help="Male patients generally have higher risk at younger age."
        )

    st.markdown("### ❤️ Cardiovascular Symptoms")
    col1, col2 = st.columns(2)
    with col1:
        chestpain = st.selectbox(
            "Chest Pain Type",
            [0, 1, 2, 3],
            help="Higher value indicates more severe angina."
        )
        exerciseangina = st.selectbox(
            "Exercise-induced Angina",
            [0, 1],
            help="Chest pain triggered by physical activity."
        )
    with col2:
        oldpeak = st.slider(
            "ST Depression (Oldpeak)", 0.0, 6.0, 1.0,
            help="ST depression > 2 indicates high ischemic risk."
        )
        slope = st.selectbox(
            "ST Segment Slope",
            [0, 1, 2],
            help="Abnormal slope associated with heart disease."
        )

    st.markdown("### 🧪 Clinical Measurements")
    col1, col2 = st.columns(2)
    with col1:
        restingBP = st.slider(
            "Resting Blood Pressure (mmHg)", 50, 250, 120,
            help="≥140 mmHg is considered hypertension."
        )
        serumcholesterol = st.slider(
            "Serum Cholesterol (mg/dL)", 50, 600, 200,
            help="≥240 mg/dL is considered high cholesterol."
        )
    with col2:
        fastingbloodsugar = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dL",
            [0, 1],
            help="Indicator of diabetes."
        )
        restingelectro = st.selectbox(
            "Resting ECG",
            [0, 1, 2],
            help="Abnormal ECG patterns indicate cardiac issues."
        )

    st.markdown("### 🫀 Cardiac Capacity")
    col1, col2 = st.columns(2)
    with col1:
        maxheartrate = st.slider(
            "Maximum Heart Rate", 50, 250, 150,
            help="Low max heart rate relative to age increases risk."
        )
    with col2:
        noofmajorvessels = st.selectbox(
            "Number of Major Vessels",
            [0, 1, 2, 3],
            help="Number of blocked vessels from angiography."
        )

    submit = st.form_submit_button("🔍 Analyze Cardiac Risk")

# =========================
# KNOWLEDGE BASE (RULE ENGINE)
# =========================
def evaluate_rules():
    votes = []
    rules = []

    if chestpain >= 2 and oldpeak > 2 and exerciseangina == 1:
        votes.append(1)
        rules.append("Severe chest pain + high ST depression + exercise angina")

    if noofmajorvessels >= 2 and serumcholesterol > 280:
        votes.append(1)
        rules.append("Multiple blocked vessels + high cholesterol")

    if maxheartrate < 130 and oldpeak > 1:
        votes.append(1)
        rules.append("Low max heart rate + ST abnormality")

    if slope >= 1 and restingelectro >= 1:
        votes.append(1)
        rules.append("Abnormal ST slope + abnormal ECG")

    if age > 55 and restingBP > 150:
        votes.append(1)
        rules.append("Advanced age + hypertension")

    return votes, rules


def determine_risk(votes):
    score = sum(votes)
    if score >= 3:
        return "HIGH"
    elif score == 2:
        return "MODERATE"
    else:
        return "LOW"

# =========================
# OUTPUT
# =========================
if submit:
    votes, active_rules = evaluate_rules()
    risk = determine_risk(votes)

    st.markdown("### 📊 Clinical Assessment Result")

    if risk == "HIGH":
        st.error("🔴 HIGH CARDIAC RISK")
        st.markdown("**Recommendation:** Immediate cardiology referral.")
    elif risk == "MODERATE":
        st.warning("🟠 MODERATE CARDIAC RISK")
        st.markdown("**Recommendation:** Further diagnostic evaluation advised.")
    else:
        st.success("🟢 LOW CARDIAC RISK")
        st.markdown("**Recommendation:** Maintain healthy lifestyle and routine check-ups.")

    st.markdown("### 📌 Activated Clinical Rules")
    if active_rules:
        for r in active_rules:
            st.markdown(f"- {r}")
    else:
        st.markdown("- No high-risk rules activated")
