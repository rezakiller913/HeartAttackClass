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
    "Clinical Decision Support System with **medical guidance for each input**"
)

# =========================
# INPUT FORM
# =========================
with st.form("patient_form"):

    st.markdown("### 🧑‍⚕️ Patient Demographics")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(
            "Age (years)",
            1, 120, 50,
            help="Usia pasien dalam tahun. Risiko penyakit jantung meningkat seiring bertambahnya usia."
        )
    with col2:
        gender = st.selectbox(
            "Gender",
            ["Female", "Male"],
            help="Jenis kelamin biologis pasien. Pria cenderung berisiko lebih tinggi di usia lebih muda."
        )

    st.markdown("### ❤️ Cardiovascular Symptoms")
    col1, col2 = st.columns(2)
    with col1:
        chestpain = st.selectbox(
            "Chest Pain Type (0–3)",
            [0, 1, 2, 3],
            help=(
                "0: Typical angina (nyeri dada khas jantung)\n"
                "1: Atypical angina\n"
                "2: Non-anginal pain\n"
                "3: Asymptomatic (tidak ada nyeri)"
            )
        )
        exerciseangina = st.selectbox(
            "Exercise-induced Angina",
            [0, 1],
            help="Nyeri dada yang muncul saat aktivitas fisik (0 = Tidak, 1 = Ya)."
        )
    with col2:
        oldpeak = st.slider(
            "ST Depression (Oldpeak)",
            0.0, 6.0, 1.0,
            help="Derajat depresi segmen ST pada EKG saat stres. Nilai > 2 menunjukkan risiko tinggi."
        )
        slope = st.selectbox(
            "ST Segment Slope",
            [0, 1, 2],
            help="Kemiringan segmen ST saat latihan. Flat atau menurun lebih berisiko."
        )

    st.markdown("### 🧪 Clinical Measurements")
    col1, col2 = st.columns(2)
    with col1:
        restingBP = st.slider(
            "Resting Blood Pressure (mmHg)",
            50, 250, 120,
            help="Tekanan darah saat istirahat. Nilai ≥140 mmHg termasuk hipertensi."
        )
        serumcholesterol = st.slider(
            "Serum Cholesterol (mg/dL)",
            50, 600, 200,
            help="Kolesterol total darah. ≥240 mg/dL tergolong tinggi."
        )
    with col2:
        fastingbloodsugar = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dL",
            [0, 1],
            help="Menunjukkan apakah gula darah puasa pasien >120 mg/dL (indikasi diabetes)."
        )
        restingelectro = st.selectbox(
            "Resting ECG Result",
            [0, 1, 2],
            help=(
                "0: Normal\n"
                "1: ST-T abnormality\n"
                "2: Left ventricular hypertrophy"
            )
        )

    st.markdown("### 🫀 Cardiac Capacity")
    col1, col2 = st.columns(2)
    with col1:
        maxheartrate = st.slider(
            "Maximum Heart Rate",
            50, 250, 150,
            help="Detak jantung maksimum saat aktivitas. Nilai rendah untuk usia dapat menandakan gangguan."
        )
    with col2:
        noofmajorvessels = st.selectbox(
            "Number of Major Vessels",
            [0, 1, 2, 3],
            help="Jumlah pembuluh darah besar yang tersumbat (hasil angiografi)."
        )

    submit = st.form_submit_button("🔍 Analyze Cardiac Risk")

# =========================
# RULE ENGINE
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
        rules.append("Low maximum heart rate + ST abnormality")

    return votes, rules


def determine_risk(votes):
    score = sum(votes)
    if score >= 2:
        return "HIGH"
    elif score == 1:
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
        st.markdown("**Recommendation:** Immediate referral to cardiologist.")
    elif risk == "MODERATE":
        st.warning("🟠 MODERATE CARDIAC RISK")
        st.markdown("**Recommendation:** Further diagnostic evaluation advised.")
    else:
        st.success("🟢 LOW CARDIAC RISK")
        st.markdown("**Recommendation:** Maintain healthy lifestyle and routine check-ups.")

    
