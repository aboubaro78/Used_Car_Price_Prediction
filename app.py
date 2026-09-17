import io

import joblib
import pandas as pd
import streamlit as st

# =================================================
# Configuration
# =================================================

st.set_page_config(
    page_title="Used Car Price Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MODEL_COLUMNS = [
    "Kms_Driven",
    "Present_Price",
    "Fuel_Type",
    "Seller_Type",
    "Transmission",
    "Age",
]

FUEL_VALUES = ["Petrol", "Diesel", "CNG"]
SELLER_VALUES = ["Dealer", "Individual"]
TRANS_VALUES = ["Manual", "Automatic"]

FUEL_LABELS = {"Petrol": "Essence", "Diesel": "Diesel", "CNG": "GNC"}
SELLER_LABELS = {"Dealer": "Concession", "Individual": "Particulier"}
TRANS_LABELS = {"Manual": "Manuelle", "Automatic": "Automatique"}

PRESETS = {
    "Citadine": (18_000, 6.2, 3, "Petrol", "Dealer", "Manual"),
    "Berline diesel": (85_000, 8.5, 7, "Diesel", "Individual", "Manual"),
    "Premium auto": (42_000, 12.0, 4, "Petrol", "Dealer", "Automatic"),
}


@st.cache_resource
def load_model():
    return joblib.load("car_price_model.joblib")


def inject_styles() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #eef1f8;
    --surface: #ffffff;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --brand: #4f46e5;
    --brand-2: #2563eb;
    --accent: #06b6d4;
    --ok: #10b981;
}

html, body, [class*="css"] {
    font-family: 'Outfit', system-ui, sans-serif;
}

.stApp {
    background:
        radial-gradient(900px 420px at 8% -5%, rgba(79, 70, 229, 0.14), transparent 55%),
        radial-gradient(700px 380px at 95% 0%, rgba(6, 182, 212, 0.12), transparent 50%),
        var(--bg);
}

.block-container {
    max-width: 1240px;
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 26px;
    padding: 2.1rem 2.4rem;
    margin-bottom: 1.35rem;
    color: #f8fafc;
    background: linear-gradient(125deg, #312e81 0%, #1e40af 45%, #0e7490 100%);
    box-shadow: 0 22px 50px rgba(30, 64, 175, 0.28);
}

.hero::after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
    top: -120px;
    right: -60px;
    pointer-events: none;
}

.hero h1 {
    margin: 0 0 0.45rem;
    font-size: clamp(1.7rem, 3.2vw, 2.35rem);
    font-weight: 800;
    letter-spacing: -0.03em;
}

.hero p {
    margin: 0;
    max-width: 680px;
    color: #dbeafe;
    font-size: 1.02rem;
    line-height: 1.55;
}

.hero-tags {
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.tag {
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.22);
}

div[data-testid="stTabs"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 0.35rem 0.75rem 0.85rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

button[data-baseweb="tab"] {
    font-weight: 700 !important;
    font-size: 0.92rem !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--brand) !important;
}

.panel {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1.2rem 1.25rem;
    box-shadow: 0 6px 22px rgba(15, 23, 42, 0.05);
}

.panel-title {
    margin: 0;
    font-size: 1.08rem;
    font-weight: 700;
    color: var(--ink);
}

.panel-sub {
    margin: 0.25rem 0 0.95rem;
    color: var(--muted);
    font-size: 0.86rem;
    line-height: 1.45;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border-color: #cbd5e1 !important;
    background: #f8fafc !important;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-weight: 600 !important;
    color: #334155 !important;
}

.preset-wrap div.stButton > button {
    background: #f8fafc;
    color: #334155;
    border: 1px solid var(--line);
    border-radius: 11px;
    font-weight: 600;
    font-size: 0.82rem;
    box-shadow: none;
}

.preset-wrap div.stButton > button:hover {
    background: #eef2ff;
    border-color: #c7d2fe;
    color: #3730a3;
}

.cta div.stButton > button {
    border: none;
    border-radius: 14px;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.72rem 1rem;
    background: linear-gradient(90deg, var(--brand), var(--brand-2));
    color: white;
    box-shadow: 0 10px 24px rgba(79, 70, 229, 0.35);
}

.cta div.stButton > button:hover {
    color: white;
    border: none;
    transform: translateY(-1px);
}

.result-hero {
    margin-top: 1rem;
    border-radius: 20px;
    padding: 1.6rem 1.4rem;
    text-align: center;
    color: white;
    background: linear-gradient(130deg, #059669 0%, #10b981 55%, #34d399 100%);
    box-shadow: 0 14px 36px rgba(16, 185, 129, 0.28);
}

.result-hero h3 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    opacity: 0.95;
}

.result-hero h1 {
    margin: 0.35rem 0 0;
    font-size: clamp(2.2rem, 4.5vw, 3rem);
    font-weight: 800;
    letter-spacing: -0.03em;
}

.result-hero p {
    margin: 0.55rem 0 0;
    font-size: 0.88rem;
    opacity: 0.92;
}

.metric-grid [data-testid="stMetric"] {
    background: #f8fafc;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 0.85rem 0.95rem;
    box-shadow: none;
}

.model-card {
    background: linear-gradient(160deg, #0f172a, #1e293b);
    color: #e2e8f0;
    border-radius: 18px;
    padding: 1.2rem 1.25rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.model-card h4 {
    margin: 0 0 0.45rem;
    color: #f8fafc;
    font-size: 1rem;
}

.model-card p, .model-card li {
    color: #cbd5e1;
    font-size: 0.86rem;
    line-height: 1.55;
}

.model-card ul {
    margin: 0.4rem 0 0.8rem;
    padding-left: 1.1rem;
}

.csv-tip {
    background: #eff6ff;
    border: 1px dashed #93c5fd;
    color: #1e3a8a;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-size: 0.86rem;
    line-height: 1.55;
    margin-bottom: 0.85rem;
}

.disclaimer {
    margin-top: 0.85rem;
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
    border-radius: 12px;
    padding: 0.75rem 0.9rem;
    font-size: 0.84rem;
}
</style>
""",
        unsafe_allow_html=True,
    )


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {col: col.strip() for col in df.columns}
    df = df.rename(columns=renamed)
    alias_map = {
        "kms_driven": "Kms_Driven",
        "present_price": "Present_Price",
        "fuel_type": "Fuel_Type",
        "seller_type": "Seller_Type",
        "transmission": "Transmission",
        "age": "Age",
        "selling_price": "Selling_Price",
    }
    lower_to_std = {k: v for k, v in alias_map.items()}
    new_names = {}
    for col in df.columns:
        key = col.strip().lower().replace(" ", "_")
        if key in lower_to_std:
            new_names[col] = lower_to_std[key]
    return df.rename(columns=new_names)


def validate_input_frame(df: pd.DataFrame) -> tuple[pd.DataFrame | None, list[str]]:
    errors: list[str] = []
    missing = [col for col in MODEL_COLUMNS if col not in df.columns]
    if missing:
        errors.append(f"Colonnes manquantes : {', '.join(missing)}")
        return None, errors

    work = df[MODEL_COLUMNS].copy()

    for col in ["Kms_Driven", "Present_Price", "Age"]:
        work[col] = pd.to_numeric(work[col], errors="coerce")
        if work[col].isna().any():
            errors.append(f"Valeurs non numériques détectées dans `{col}`.")

    for col, allowed in [
        ("Fuel_Type", FUEL_VALUES),
        ("Seller_Type", SELLER_VALUES),
        ("Transmission", TRANS_VALUES),
    ]:
        invalid = ~work[col].astype(str).isin(allowed)
        if invalid.any():
            bad = work.loc[invalid, col].astype(str).unique()[:5]
            errors.append(
                f"Valeurs invalides dans `{col}` : {', '.join(bad)}. "
                f"Attendu : {', '.join(allowed)}."
            )

    if (work["Kms_Driven"] < 0).any() or (work["Present_Price"] < 0).any() or (work["Age"] < 0).any():
        errors.append("Kilométrage, prix actuel et âge doivent être ≥ 0.")

    if errors:
        return None, errors
    return work, errors


def run_predictions(model, feature_df: pd.DataFrame) -> pd.Series:
    preds = model.predict(feature_df)
    return pd.Series(preds, name="Predicted_Selling_Price")


def render_hero() -> None:
    st.markdown(
        """
<div class="hero">
  <h1>Used Car Price Prediction</h1>
  <p>
    Interface élégante pour estimer le prix de revente d'une voiture d'occasion —
    saisie manuelle ou import CSV pour des prédictions en lot.
  </p>
  <div class="hero-tags">
    <span class="tag">Random Forest</span>
    <span class="tag">Scikit-learn Pipeline</span>
    <span class="tag">Prédiction unitaire & CSV</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_model_card() -> None:
    st.markdown(
        """
<div class="model-card">
  <h4>Modèle & pipeline</h4>
  <p>Random Forest retenu après comparaison avec XGBoost, Decision Tree et régressions linéaires.</p>
  <ul>
    <li>Prétraitement : Pipeline Scikit-learn</li>
    <li>Encodage catégoriel : OneHotEncoder</li>
    <li>Scaling : RobustScaler</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )


inject_styles()
render_hero()

try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "Fichier `car_price_model.joblib` introuvable. "
        "Placez-le à la racine du projet puis relancez l'application."
    )
    st.stop()

tab_single, tab_csv = st.tabs(["Prédiction manuelle", "Prédiction par CSV"])

# =================================================
# Onglet : une voiture
# =================================================

with tab_single:
    left, right = st.columns([1.65, 1], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(
            '<p class="panel-title">Informations véhicule</p>'
            '<p class="panel-sub">Renseignez les caractéristiques ou chargez un profil type.</p>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="preset-wrap">', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        preset_clicked = None
        with p1:
            if st.button("Citadine", use_container_width=True):
                preset_clicked = "Citadine"
        with p2:
            if st.button("Berline diesel", use_container_width=True):
                preset_clicked = "Berline diesel"
        with p3:
            if st.button("Premium auto", use_container_width=True):
                preset_clicked = "Premium auto"
        st.markdown("</div>", unsafe_allow_html=True)

        if preset_clicked:
            kms, price, age, fuel, seller, trans = PRESETS[preset_clicked]
            st.session_state["kms"] = kms
            st.session_state["price"] = price
            st.session_state["age"] = age
            st.session_state["fuel"] = fuel
            st.session_state["seller"] = seller
            st.session_state["trans"] = trans
            st.rerun()

        c1, c2 = st.columns(2)
        with c1:
            kms_driven = st.number_input(
                "Kilométrage (km)",
                min_value=0,
                step=1000,
                key="kms",
            )
            present_price = st.number_input(
                "Prix actuel (k$)",
                min_value=0.0,
                step=0.1,
                format="%.2f",
                key="price",
            )
            age = st.number_input("Âge (années)", min_value=0, step=1, key="age")

        with c2:
            fuel_type = st.selectbox(
                "Carburant",
                FUEL_VALUES,
                key="fuel",
                format_func=lambda x: FUEL_LABELS[x],
            )
            seller_type = st.selectbox(
                "Vendeur",
                SELLER_VALUES,
                key="seller",
                format_func=lambda x: SELLER_LABELS[x],
            )
            transmission = st.selectbox(
                "Transmission",
                TRANS_VALUES,
                key="trans",
                format_func=lambda x: TRANS_LABELS[x],
            )

        st.markdown('<div class="cta">', unsafe_allow_html=True)
        predict = st.button("Prédire le prix", use_container_width=True, type="primary")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with right:
        render_model_card()

    if predict:
        input_data = pd.DataFrame(
            [
                {
                    "Kms_Driven": kms_driven,
                    "Present_Price": present_price,
                    "Fuel_Type": fuel_type,
                    "Seller_Type": seller_type,
                    "Transmission": transmission,
                    "Age": age,
                }
            ]
        )
        prediction = float(model.predict(input_data)[0])
        diff = prediction - present_price
        diff_pct = (diff / present_price * 100) if present_price > 0 else 0.0

        st.markdown(
            f"""
<div class="result-hero">
  <h3>Prix de vente estimé</h3>
  <h1>{prediction:.2f} k$</h1>
  <p>Écart vs prix actuel : {diff:+.2f} k$ ({diff_pct:+.1f} %)</p>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Kilométrage", f"{kms_driven:,} km")
        m2.metric("Prix actuel", f"{present_price:.2f} k$")
        m3.metric("Âge", f"{age} ans")
        m4.metric("Carburant", FUEL_LABELS[fuel_type])
        m5.metric("Vendeur", SELLER_LABELS[seller_type])
        m6.metric("Transmission", TRANS_LABELS[transmission])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="disclaimer">Estimation indicative produite par le modèle. '
            "Elle ne remplace pas une expertise professionnelle.</div>",
            unsafe_allow_html=True,
        )

# =================================================
# Onglet : CSV
# =================================================

with tab_csv:
    st.markdown(
        """
<div class="csv-tip">
  <b>Format attendu :</b> un fichier CSV avec les colonnes
  <code>Kms_Driven</code>, <code>Present_Price</code>, <code>Fuel_Type</code>,
  <code>Seller_Type</code>, <code>Transmission</code>, <code>Age</code>.
  La colonne <code>Selling_Price</code> est optionnelle (utile pour comparer avec la réalité).
</div>
""",
        unsafe_allow_html=True,
    )

    sample = pd.DataFrame(
        [
            {
                "Kms_Driven": 27000,
                "Present_Price": 5.59,
                "Fuel_Type": "Petrol",
                "Seller_Type": "Dealer",
                "Transmission": "Manual",
                "Age": 6,
            },
            {
                "Kms_Driven": 43000,
                "Present_Price": 9.54,
                "Fuel_Type": "Diesel",
                "Seller_Type": "Dealer",
                "Transmission": "Manual",
                "Age": 7,
            },
        ]
    )
    sample_buffer = io.StringIO()
    sample.to_csv(sample_buffer, index=False)
    st.download_button(
        label="Télécharger un modèle CSV",
        data=sample_buffer.getvalue(),
        file_name="modele_prediction_voitures.csv",
        mime="text/csv",
        use_container_width=False,
    )

    uploaded = st.file_uploader(
        "Importer votre fichier CSV",
        type=["csv"],
        help="Le fichier sera analysé localement dans cette session Streamlit.",
    )

    if uploaded is not None:
        try:
            raw_df = pd.read_csv(uploaded)
        except Exception as exc:
            st.error(f"Impossible de lire le CSV : {exc}")
            st.stop()

        raw_df = normalize_columns(raw_df)
        st.markdown("#### Aperçu des données importées")
        st.dataframe(raw_df.head(10), use_container_width=True, hide_index=True)

        valid_df, errors = validate_input_frame(raw_df)
        if errors:
            for err in errors:
                st.error(err)
        else:
            st.success(f"{len(valid_df)} ligne(s) prête(s) pour la prédiction.")

            if st.button("Lancer la prédiction CSV", type="primary", use_container_width=False):
                preds = run_predictions(model, valid_df)
                output_df = raw_df.copy()
                output_df["Predicted_Selling_Price"] = preds.values

                if "Selling_Price" in output_df.columns:
                    actual = pd.to_numeric(output_df["Selling_Price"], errors="coerce")
                    output_df["Prediction_Error"] = output_df["Predicted_Selling_Price"] - actual
                    output_df["Prediction_Error_Abs"] = output_df["Prediction_Error"].abs()

                st.markdown("#### Résultats")
                st.dataframe(output_df, use_container_width=True, hide_index=True)

                c1, c2, c3 = st.columns(3)
                c1.metric("Nombre de prédictions", len(output_df))
                c2.metric("Prix moyen prédit", f"{preds.mean():.2f} k$")
                c3.metric("Prix min / max", f"{preds.min():.2f} / {preds.max():.2f} k$")

                if "Prediction_Error_Abs" in output_df.columns:
                    mae = output_df["Prediction_Error_Abs"].mean()
                    st.info(f"Erreur absolue moyenne vs `Selling_Price` : {mae:.2f} k$")

                csv_bytes = output_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Télécharger les résultats (CSV)",
                    data=csv_bytes,
                    file_name="predictions_voitures.csv",
                    mime="text/csv",
                    type="primary",
                    use_container_width=True,
                )
