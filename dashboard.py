# import os
# import io
# import random
# import requests
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas

# st.set_page_config(
#     page_title="FraudGuard AI",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
# DATA_PATH = "data/creditcard.csv"

# # ---------------------------------------------------
# # CSS
# # ---------------------------------------------------
# st.markdown("""
# <style>
# html, body, [class*="css"] {
#     font-family: "Segoe UI", sans-serif;
# }

# .stApp {
#     background:
#         radial-gradient(circle at top left, rgba(16,185,129,0.10), transparent 30%),
#         radial-gradient(circle at bottom right, rgba(245,158,11,0.08), transparent 25%),
#         linear-gradient(135deg, #0b1220 0%, #111827 50%, #0f172a 100%);
#     color: #f8fafc;
# }

# .block-container {
#     max-width: 1450px;
#     padding-top: 1rem;
#     padding-bottom: 2rem;
# }

# section[data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
#     border-right: 1px solid rgba(255,255,255,0.08);
# }

# .topbar {
#     background: linear-gradient(90deg, rgba(16,185,129,0.16), rgba(245,158,11,0.14));
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 20px;
#     padding: 22px;
#     margin-bottom: 18px;
#     box-shadow: 0 10px 28px rgba(0,0,0,0.25);
# }

# .topbar-title {
#     font-size: 34px;
#     font-weight: 800;
#     color: white;
#     margin-bottom: 6px;
# }

# .topbar-sub {
#     font-size: 15px;
#     color: #d1fae5;
#     line-height: 1.7;
# }

# .ribbon {
#     display: inline-block;
#     margin-right: 8px;
#     margin-top: 10px;
#     padding: 7px 12px;
#     border-radius: 999px;
#     font-size: 12px;
#     font-weight: 700;
#     background: rgba(255,255,255,0.08);
#     border: 1px solid rgba(255,255,255,0.08);
#     color: #f8fafc;
# }

# .section-block {
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 20px;
#     padding: 20px;
#     box-shadow: 0 8px 22px rgba(0,0,0,0.20);
# }

# .section-heading {
#     font-size: 22px;
#     font-weight: 800;
#     color: white;
#     margin-bottom: 4px;
# }

# .section-note {
#     font-size: 13px;
#     color: #cbd5e1;
#     margin-bottom: 14px;
# }

# .stat-tile {
#     background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 18px;
#     padding: 16px;
#     min-height: 118px;
# }

# .stat-label {
#     color: #94a3b8;
#     font-size: 12px;
#     margin-bottom: 8px;
#     text-transform: uppercase;
#     letter-spacing: 0.4px;
# }

# .stat-number {
#     color: white;
#     font-size: 28px;
#     font-weight: 800;
# }

# .stat-help {
#     color: #cbd5e1;
#     font-size: 12px;
#     margin-top: 6px;
# }

# .flow-card {
#     text-align: center;
#     padding: 16px;
#     border-radius: 16px;
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.07);
#     font-size: 14px;
#     font-weight: 700;
#     color: #e5e7eb;
# }

# .good-status {
#     padding: 12px 14px;
#     border-radius: 12px;
#     background: rgba(16,185,129,0.16);
#     border: 1px solid rgba(16,185,129,0.30);
#     color: #d1fae5;
#     font-weight: 700;
# }

# .bad-status {
#     padding: 12px 14px;
#     border-radius: 12px;
#     background: rgba(239,68,68,0.16);
#     border: 1px solid rgba(239,68,68,0.30);
#     color: #fee2e2;
#     font-weight: 700;
# }

# .result-card {
#     padding: 14px;
#     border-radius: 14px;
#     border: 1px solid rgba(255,255,255,0.08);
#     background: rgba(255,255,255,0.04);
#     margin-top: 12px;
# }

# .result-title {
#     font-size: 15px;
#     font-weight: 700;
#     color: white;
#     margin-bottom: 6px;
# }

# .result-body {
#     font-size: 13px;
#     line-height: 1.7;
#     color: #e5e7eb;
# }

# .small-muted {
#     color: #94a3b8;
#     font-size: 12px;
#     line-height: 1.7;
# }

# .info-chip {
#     padding: 8px 12px;
#     border-radius: 12px;
#     display: inline-block;
#     margin-right: 8px;
#     margin-bottom: 8px;
#     font-size: 12px;
#     font-weight: 600;
#     background: rgba(255,255,255,0.05);
#     border: 1px solid rgba(255,255,255,0.08);
# }

# .stButton > button {
#     width: 100%;
#     height: 3em;
#     border: none;
#     border-radius: 12px;
#     font-weight: 700;
#     color: white;
#     background: linear-gradient(90deg, #059669, #d97706);
#     box-shadow: 0 8px 20px rgba(5,150,105,0.22);
# }

# .stButton > button:hover {
#     background: linear-gradient(90deg, #047857, #b45309);
#     color: white;
# }

# hr {
#     border: none;
#     height: 1px;
#     background: rgba(255,255,255,0.08);
#     margin: 1.1rem 0;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------
# # HELPERS
# # ---------------------------------------------------
# @st.cache_data
# def load_dataset(path):
#     return pd.read_csv(path)

# def get_transaction(df, mode="random"):
#     if mode == "fraud":
#         filtered = df[df["Class"] == 1]
#     elif mode == "normal":
#         filtered = df[df["Class"] == 0]
#     else:
#         filtered = df

#     row = filtered.sample(n=1).iloc[0].to_dict()
#     actual_class = int(row["Class"])
#     del row["Class"]
#     return row, actual_class

# def get_smart_random(df):
#     if random.random() < 0.5:
#         sample = df[df["Class"] == 1].sample(1)
#     else:
#         sample = df[df["Class"] == 0].sample(1)

#     row = sample.iloc[0].to_dict()
#     actual = int(row["Class"])
#     del row["Class"]
#     return row, actual

# def get_default_transaction():
#     data = {"Time": 10000.0, "Amount": 2500.0}
#     for i in range(1, 29):
#         data[f"V{i}"] = 0.0
#     return data, None

# def class_to_text(value):
#     if value is None:
#         return "Unknown"
#     return "Fraud" if value == 1 else "Legitimate"

# def build_pdf_report(single_result, actual_label_text, dataset_rows, fraud_count, fraud_rate):
#     buffer = io.BytesIO()
#     pdf = canvas.Canvas(buffer, pagesize=A4)
#     y = A4[1] - 50

#     pdf.setFont("Helvetica-Bold", 18)
#     pdf.drawString(50, y, "FraudGuard AI - Prediction Report")
#     y -= 28

#     pdf.setFont("Helvetica", 11)
#     lines = [
#         "Project: Credit Card Fraud Detection System",
#         "Model: XGBoost Classifier",
#         "Imbalance Handling: SMOTE",
#         "Backend: Flask API",
#         "Frontend: Streamlit Dashboard",
#         "",
#         f"Dataset Size: {dataset_rows}",
#         f"Fraud Cases: {fraud_count}",
#         f"Fraud Rate: {fraud_rate:.4f}%",
#         "",
#         f"Predicted Class: {'Fraud' if single_result['fraud_prediction'] == 1 else 'Legitimate'}",
#         f"Fraud Probability: {single_result['fraud_probability']}",
#         f"Risk Level: {single_result['risk_level']}",
#         f"Threshold Used: {single_result['threshold_used']}",
#         f"Actual Dataset Label: {actual_label_text}",
#     ]

#     for line in lines:
#         pdf.drawString(50, y, line)
#         y -= 18

#     pdf.save()
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# def prepare_batch_dataframe(uploaded_df):
#     df2 = uploaded_df.copy()

#     actual_labels = None
#     if "Class" in df2.columns:
#         actual_labels = df2["Class"].copy()
#         df2 = df2.drop(columns=["Class"])

#     required_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]

#     missing_cols = [col for col in required_cols if col not in df2.columns]
#     extra_cols = [col for col in df2.columns if col not in required_cols]

#     for col in missing_cols:
#         df2[col] = 0

#     df2 = df2[required_cols]

#     for col in df2.columns:
#         df2[col] = pd.to_numeric(df2[col], errors="coerce")

#     df2 = df2.fillna(0)

#     return df2, actual_labels, missing_cols, extra_cols

# def backend_health():
#     try:
#         res = requests.get(f"{API_URL}/health", timeout=5)
#         if res.status_code == 200:
#             return True, res.json()
#         return False, {}
#     except Exception:
#         return False, {}

# def plot_probability_gauge(prob):
#     prob_percent = prob * 100
#     remaining = 100 - prob_percent

#     if prob_percent >= 80:
#         color = "#ef4444"
#     elif prob_percent >= 40:
#         color = "#f59e0b"
#     else:
#         color = "#10b981"

#     fig, ax = plt.subplots(figsize=(4.2, 3.0), subplot_kw=dict(aspect="equal"))
#     ax.pie(
#         [prob_percent, remaining],
#         startangle=180,
#         counterclock=False,
#         colors=[color, "#1f2937"],
#         wedgeprops=dict(width=0.35, edgecolor="none")
#     )
#     ax.add_artist(plt.Circle((0, 0), 0.48, color="#111827"))
#     ax.text(0, 0.06, f"{prob_percent:.1f}%", ha="center", va="center", fontsize=20, fontweight="bold", color="white")
#     ax.text(0, -0.16, "Fraud Probability", ha="center", va="center", fontsize=10, color="#cbd5e1")
#     ax.set_xlim(-1.1, 1.1)
#     ax.set_ylim(-1.05, 0.35)
#     ax.axis("off")
#     fig.patch.set_facecolor("#111827")
#     ax.set_facecolor("#111827")
#     return fig

# def get_template_df():
#     cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
#     sample = {col: 0 for col in cols}
#     sample["Time"] = 10000
#     sample["Amount"] = 2500
#     return pd.DataFrame([sample])

# def prediction_box(result):
#     prob = float(result["fraud_probability"])
#     risk = result["risk_level"]
#     pred = result["fraud_prediction"]

#     if risk == "High":
#         color = "#ef4444"
#     elif risk == "Medium":
#         color = "#f59e0b"
#     else:
#         color = "#10b981"

#     return f"""
#     <div class="result-card">
#         <div class="result-title">Prediction Result</div>
#         <div class="result-body">
#             <b>Status:</b> {"Fraud" if pred == 1 else "Legitimate"} <br>
#             <b>Risk Level:</b> <span style="color:{color}; font-weight:700;">{risk}</span> <br>
#             <b>Fraud Probability:</b> {prob:.4f}
#         </div>
#     </div>
#     """

# def render_batch_analysis(result_df):
#     st.markdown("## 📊 Batch Screening Analysis")

#     if result_df is None or result_df.empty:
#         st.info("No batch results available.")
#         return

#     # ---------------- Summary Metrics ----------------
#     c1, c2, c3, c4 = st.columns(4)

#     total_rows = len(result_df)
#     fraud_rows = 0
#     avg_score = 0
#     max_score = 0

#     if "Predicted_Class" in result_df.columns:
#         fraud_rows = int((result_df["Predicted_Class"] == "Fraud").sum())

#     if "Fraud_Probability" in result_df.columns:
#         avg_score = float(result_df["Fraud_Probability"].mean())
#         max_score = float(result_df["Fraud_Probability"].max())

#     with c1:
#         st.metric("Total Rows", total_rows)
#     with c2:
#         st.metric("Predicted Fraud", fraud_rows)
#     with c3:
#         st.metric("Average Fraud Score", f"{avg_score:.4f}")
#     with c4:
#         st.metric("Max Fraud Score", f"{max_score:.4f}")

#     st.markdown("---")

#     # ---------------- Charts Row 1 ----------------
#     g1, g2 = st.columns(2)

#     with g1:
#         st.markdown("### Risk Level Distribution")
#         if "Risk_Level" in result_df.columns:
#             risk_counts = result_df["Risk_Level"].value_counts()

#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.bar(risk_counts.index, risk_counts.values)
#             ax.set_title("Risk Level Count")
#             ax.set_ylabel("Transactions")
#             st.pyplot(fig)
#         else:
#             st.info("Risk_Level column not found.")

#     with g2:
#         st.markdown("### Fraud Probability Distribution")
#         if "Fraud_Probability" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.hist(result_df["Fraud_Probability"], bins=20)
#             ax.set_title("Fraud Score Histogram")
#             ax.set_xlabel("Fraud Probability")
#             ax.set_ylabel("Frequency")
#             st.pyplot(fig)
#         else:
#             st.info("Fraud_Probability column not found.")

#     st.markdown("---")

#     # ---------------- Charts Row 2 ----------------
#     g3, g4 = st.columns(2)

#     with g3:
#         st.markdown("### Amount vs Fraud Score")
#         if "Amount" in result_df.columns and "Fraud_Probability" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.scatter(result_df["Amount"], result_df["Fraud_Probability"], alpha=0.7)
#             ax.set_title("Amount vs Fraud Score")
#             ax.set_xlabel("Amount")
#             ax.set_ylabel("Fraud Probability")
#             st.pyplot(fig)
#         else:
#             st.info("Amount or Fraud_Probability column not found.")

#     with g4:
#         st.markdown("### Fraud Score Trend")
#         if "Fraud_Probability" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.plot(range(len(result_df)), result_df["Fraud_Probability"], marker="o")
#             ax.set_title("Fraud Score by Row Order")
#             ax.set_xlabel("Row Index")
#             ax.set_ylabel("Fraud Probability")
#             st.pyplot(fig)
#         else:
#             st.info("Fraud_Probability column not found.")

#     st.markdown("---")

#     # ---------------- Actual vs Predicted ----------------
#     if "Actual_Label" in result_df.columns and "Predicted_Class" in result_df.columns:
#         st.markdown("### Actual vs Predicted")
#         compare_df = pd.crosstab(result_df["Actual_Label"], result_df["Predicted_Class"])

#         fig, ax = plt.subplots(figsize=(5, 3.2))
#         compare_df.plot(kind="bar", ax=ax)
#         ax.set_title("Actual vs Predicted Class")
#         ax.set_xlabel("Actual Label")
#         ax.set_ylabel("Count")
#         st.pyplot(fig)

#         st.markdown("---")

#     # ---------------- Top 5 Risky Transactions ----------------
#     if "Fraud_Probability" in result_df.columns:
#         st.markdown("### 🔥 Top 5 Risky Transactions")

#         risky_cols = []
#         for col in ["Time", "Amount", "Fraud_Probability", "Predicted_Class", "Risk_Level", "Actual_Label"]:
#             if col in result_df.columns:
#                 risky_cols.append(col)

#         top5 = result_df.sort_values("Fraud_Probability", ascending=False).head(5)[risky_cols]
#         st.dataframe(top5, use_container_width=True)

#     # ---------------- Risk Buckets ----------------
#     if "Fraud_Probability" in result_df.columns:
#         st.markdown("---")
#         st.markdown("### Fraud Score Buckets")

#         bucket_df = result_df.copy()
#         bucket_df["Score_Bucket"] = pd.cut(
#             bucket_df["Fraud_Probability"],
#             bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
#             labels=["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"],
#             include_lowest=True
#         )

#         bucket_counts = bucket_df["Score_Bucket"].value_counts().sort_index()

#         fig, ax = plt.subplots(figsize=(6, 3.2))
#         ax.bar(bucket_counts.index.astype(str), bucket_counts.values)
#         ax.set_title("Fraud Probability Buckets")
#         ax.set_xlabel("Score Bucket")
#         ax.set_ylabel("Count")
#         st.pyplot(fig)

# def compute_feature_impact(input_data, df, top_n=10):
#     feature_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
#     stats_mean = df[feature_cols].mean()
#     stats_std = df[feature_cols].std().replace(0, 1)

#     impacts = []
#     for col in feature_cols:
#         val = float(input_data.get(col, 0))
#         z = abs((val - stats_mean[col]) / stats_std[col])
#         impacts.append((col, z))

#     impact_df = pd.DataFrame(impacts, columns=["Feature", "Impact"]).sort_values("Impact", ascending=False).head(top_n)
#     return impact_df

# def show_report_image(path, title):
#     if os.path.exists(path):
#         st.image(path, caption=title, use_column_width=True)
#     else:
#         st.warning(f"{path} not found.")

# # ---------------------------------------------------
# # LOAD DATA
# # ---------------------------------------------------
# if not os.path.exists(DATA_PATH):
#     st.error(f"Dataset not found at: {DATA_PATH}")
#     st.stop()

# try:
#     df = load_dataset(DATA_PATH)
# except Exception as e:
#     st.error(f"Dataset loading error: {e}")
#     st.stop()

# # ---------------------------------------------------
# # SESSION STATE
# # ---------------------------------------------------
# if "input_data" not in st.session_state:
#     st.session_state.input_data, st.session_state.actual_class = get_default_transaction()

# if "prediction_result" not in st.session_state:
#     st.session_state.prediction_result = None

# if "history" not in st.session_state:
#     st.session_state.history = []

# if "batch_results_df" not in st.session_state:
#     st.session_state.batch_results_df = None

# # ---------------------------------------------------
# # SIDEBAR
# # ---------------------------------------------------
# with st.sidebar:
#     st.markdown("## FraudGuard AI")
#     st.caption("Monitoring Console")

#     if st.button("🎲 Smart Random"):
#         st.session_state.input_data, st.session_state.actual_class = get_smart_random(df)
#         st.session_state.prediction_result = None

#     if st.button("🚨 Fraud Sample"):
#         st.session_state.input_data, st.session_state.actual_class = get_transaction(df, "fraud")
#         st.session_state.prediction_result = None

#     if st.button("✅ Legitimate Sample"):
#         st.session_state.input_data, st.session_state.actual_class = get_transaction(df, "normal")
#         st.session_state.prediction_result = None

#     if st.button("🧪 Default Input"):
#         st.session_state.input_data, st.session_state.actual_class = get_default_transaction()
#         st.session_state.prediction_result = None

#     st.write("")
#     ok, health_data = backend_health()
#     if ok:
#         st.markdown("<div class='good-status'>Backend API Connected</div>", unsafe_allow_html=True)
#         st.caption(f"Threshold: {health_data.get('threshold', 'N/A')}")
#     else:
#         st.markdown("<div class='bad-status'>Backend API Not Reachable</div>", unsafe_allow_html=True)
#         st.caption("Set API_URL env var on Render with your backend service URL")

#     st.write("")
#     st.markdown("### Stack")
#     st.markdown("""
# - **Model**: XGBoost  
# - **Balancing**: SMOTE  
# - **Backend**: Flask  
# - **Frontend**: Streamlit  
# - **Reports**: Matplotlib, ReportLab  
# """)

# # ---------------------------------------------------
# # TOPBAR
# # ---------------------------------------------------
# st.markdown("""
# <div class="topbar">
#     <div class="topbar-title">🛡️ FraudGuard AI</div>
#     <div class="topbar-sub">
#         A cleaner fraud detection dashboard for real-time scoring, batch transaction screening, explainability, and downloadable reporting.
#     </div>
#     <span class="ribbon">Smart Random</span>
#     <span class="ribbon">Batch CSV</span>
#     <span class="ribbon">Explainability</span>
#     <span class="ribbon">Risk Scoring</span>
# </div>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------
# # OVERVIEW
# # ---------------------------------------------------
# ov1, ov2 = st.columns([1.5, 1])

# with ov1:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-heading'>Project Overview</div>", unsafe_allow_html=True)
#     st.markdown("<div class='section-note'>What the system does and how the processing pipeline works.</div>", unsafe_allow_html=True)
#     st.write("""
# This project predicts whether a credit card transaction is **fraudulent** or **legitimate**.

# ### Core flow
# 1. Transaction is selected or uploaded  
# 2. Flask backend receives the data  
# 3. Model preprocessing is applied  
# 4. XGBoost predicts fraud probability  
# 5. Dashboard shows class, probability, and risk level  
# """)
#     st.markdown("</div>", unsafe_allow_html=True)

# with ov2:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-heading'>Conclusion</div>", unsafe_allow_html=True)
#     st.markdown("<div class='section-note'>Short final summary of the project.</div>", unsafe_allow_html=True)
#     st.write("""
# FraudGuard AI demonstrates a complete end-to-end machine learning solution for credit card fraud detection.  
# It combines preprocessing, model inference, real-time prediction, batch screening, and visual reporting in a single workflow.
# """)
#     st.markdown("</div>", unsafe_allow_html=True)

# st.write("")

# # ---------------------------------------------------
# # STATS
# # ---------------------------------------------------
# fraud_count = int(df["Class"].sum())
# normal_count = len(df) - fraud_count
# fraud_rate = (fraud_count / len(df)) * 100

# s1, s2, s3, s4 = st.columns(4)

# with s1:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Total Transactions</div>
#         <div class="stat-number">{len(df):,}</div>
#         <div class="stat-help">Complete dataset size</div>
#     </div>
#     """, unsafe_allow_html=True)

# with s2:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Fraud Cases</div>
#         <div class="stat-number">{fraud_count:,}</div>
#         <div class="stat-help">Minority class</div>
#     </div>
#     """, unsafe_allow_html=True)

# with s3:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Legitimate Cases</div>
#         <div class="stat-number">{normal_count:,}</div>
#         <div class="stat-help">Majority class</div>
#     </div>
#     """, unsafe_allow_html=True)

# with s4:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Fraud Rate</div>
#         <div class="stat-number">{fraud_rate:.4f}%</div>
#         <div class="stat-help">Highly imbalanced</div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # SYSTEM FLOW
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>System Flow</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Simple processing stages of the project.</div>", unsafe_allow_html=True)

# f1, f2, f3, f4 = st.columns(4)
# with f1:
#     st.markdown("<div class='flow-card'>Input</div>", unsafe_allow_html=True)
# with f2:
#     st.markdown("<div class='flow-card'>Preprocess</div>", unsafe_allow_html=True)
# with f3:
#     st.markdown("<div class='flow-card'>Model Score</div>", unsafe_allow_html=True)
# with f4:
#     st.markdown("<div class='flow-card'>Risk Output</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # SINGLE TRANSACTION
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Single Transaction Scoring</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Use one selected transaction and generate a live fraud score.</div>", unsafe_allow_html=True)

# left, right = st.columns([1.2, 1])
# input_data = st.session_state.input_data
# actual_class = st.session_state.actual_class

# with left:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("### Current Transaction")
#     m1, m2, m3 = st.columns(3)
#     with m1:
#         st.metric("Time", f"{input_data.get('Time', 0):.2f}")
#     with m2:
#         st.metric("Amount", f"{input_data.get('Amount', 0):.2f}")
#     with m3:
#         st.metric("Actual Label", class_to_text(actual_class))

#     st.write("")
#     st.markdown("### Input Preview")
#     feature_df = pd.DataFrame({
#         "Feature": [f"V{i}" for i in range(1, 29)],
#         "Value": [float(input_data.get(f"V{i}", 0.0)) for i in range(1, 29)]
#     })
#     st.dataframe(feature_df, use_container_width=True, height=360)
#     st.markdown("</div>", unsafe_allow_html=True)

# with right:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("### Prediction")
#     st.markdown("<div class='small-muted'>Run the backend model and review the output in a compact readable format.</div>", unsafe_allow_html=True)

#     if st.button("🔍 Run Prediction"):
#         try:
#             response = requests.post(f"{API_URL}/predict", json=input_data, timeout=15)
#             result = response.json()

#             if response.status_code != 200:
#                 st.error(result.get("error", "Prediction failed"))
#             else:
#                 st.session_state.prediction_result = result
#                 st.session_state.history.insert(0, {
#                     "Predicted Class": "Fraud" if result["fraud_prediction"] == 1 else "Legitimate",
#                     "Fraud Probability": result["fraud_probability"],
#                     "Risk Level": result["risk_level"],
#                     "Actual Label": class_to_text(actual_class)
#                 })
#                 st.session_state.history = st.session_state.history[:10]

#         except requests.exceptions.ConnectionError:
#             st.error("Backend API is not running or API_URL is not set correctly.")
#         except Exception as e:
#             st.error(f"Prediction error: {e}")

#     st.write("")

#     if st.session_state.prediction_result is not None:
#         result = st.session_state.prediction_result

#         x1, x2 = st.columns(2)
#         with x1:
#             st.metric("Predicted Class", "Fraud" if result["fraud_prediction"] == 1 else "Legitimate")
#         with x2:
#             st.metric("Risk Level", result["risk_level"])

#         x3, x4 = st.columns(2)
#         with x3:
#             st.metric("Fraud Probability", f"{result['fraud_probability']:.4f}")
#         with x4:
#             st.metric("Threshold", f"{result['threshold_used']:.2f}")

#         st.pyplot(plot_probability_gauge(float(result["fraud_probability"])), use_container_width=True)
#         st.markdown(prediction_box(result), unsafe_allow_html=True)

#         pdf_bytes = build_pdf_report(
#             result,
#             class_to_text(actual_class),
#             len(df),
#             fraud_count,
#             fraud_rate
#         )

#         st.download_button(
#             label="📄 Download PDF Report",
#             data=pdf_bytes,
#             file_name="fraudguard_prediction_report.pdf",
#             mime="application/pdf"
#         )

#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # EXPLAINABILITY
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Feature Impact View</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>A simple explanation layer based on deviation from dataset averages.</div>", unsafe_allow_html=True)

# impact_df = compute_feature_impact(input_data, df, top_n=10)

# e1, e2 = st.columns([1.1, 1])

# with e1:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     fig_imp, ax_imp = plt.subplots(figsize=(6, 4))
#     ax_imp.barh(impact_df["Feature"], impact_df["Impact"])
#     ax_imp.invert_yaxis()
#     ax_imp.set_title("Top Feature Impact")
#     ax_imp.set_xlabel("Relative Impact")
#     st.pyplot(fig_imp)
#     st.markdown("</div>", unsafe_allow_html=True)

# with e2:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("### Explanation")
#     st.write("""
# This section highlights which input features are most different from the dataset average.

# A larger deviation suggests the feature may be contributing more strongly to the current transaction’s unusual pattern.
# """)
#     for _, row in impact_df.head(5).iterrows():
#         st.markdown(f"<span class='info-chip'>{row['Feature']} • {row['Impact']:.2f}</span>", unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # BATCH SCREENING
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Batch Transaction Screening</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Upload a CSV and run fraud scoring for multiple rows.</div>", unsafe_allow_html=True)

# template_df = get_template_df()
# template_bytes = template_df.to_csv(index=False).encode("utf-8")

# st.download_button(
#     label="⬇️ Download CSV Template",
#     data=template_bytes,
#     file_name="fraudguard_batch_template.csv",
#     mime="text/csv"
# )

# st.markdown("<div class='section-block'>", unsafe_allow_html=True)
# uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])

# if uploaded_file is not None:
#     try:
#         uploaded_df = pd.read_csv(uploaded_file)
#         st.write("### Uploaded File Preview")
#         st.dataframe(uploaded_df.head(), use_container_width=True)

#         batch_df, actual_labels, missing_cols, extra_cols = prepare_batch_dataframe(uploaded_df)

#         b1, b2 = st.columns(2)
#         with b1:
#             if missing_cols:
#                 st.warning(f"Missing columns filled with 0: {missing_cols}")
#             else:
#                 st.success("No required columns missing.")

#         with b2:
#             if extra_cols:
#                 st.info(f"Extra columns ignored: {extra_cols}")
#             else:
#                 st.success("No extra columns detected.")

#         if st.button("📤 Run Batch Screening"):
#             payload = {"records": batch_df.to_dict(orient="records")}
#             response = requests.post(f"{API_URL}/predict_batch", json=payload, timeout=60)
#             result = response.json()

#             if response.status_code != 200:
#                 st.error(result.get("error", "Batch prediction failed"))
#             else:
#                 batch_results = pd.DataFrame(result["results"])

#                 final_df = batch_df.copy()
#                 if not batch_results.empty:
#                     final_df["Predicted_Class"] = batch_results["fraud_prediction"].map({0: "Legitimate", 1: "Fraud"})
#                     final_df["Fraud_Probability"] = batch_results["fraud_probability"]
#                     final_df["Risk_Level"] = batch_results["risk_level"]

#                 if actual_labels is not None:
#                     final_df["Actual_Label"] = actual_labels.map({0: "Legitimate", 1: "Fraud"})

#                 st.session_state.batch_results_df = final_df

#                 if result.get("row_errors"):
#                     st.warning(f"Some rows failed: {result['row_errors']}")

       
#     except Exception as e:
#         st.error(f"CSV processing error: {e}")

# st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # HISTORY
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Prediction History</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Recent predictions generated in the current session.</div>", unsafe_allow_html=True)

# if st.session_state.history:
#     st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, height=250)
# else:
#     st.info("No predictions yet.")

# st.markdown("---")

# # ---------------------------------------------------
# # REPORTS
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Model Reports</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Saved visual artifacts from model training and evaluation.</div>", unsafe_allow_html=True)

# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "Feature Importance",
#     "Confusion Matrix",
#     "ROC Curve",
#     "PR Curve",
#     "SHAP Summary"
# ])

# report_map = {
#     "Feature Importance": "report/feature_importance.png",
#     "Confusion Matrix": "report/confusion_matrix.png",
#     "ROC Curve": "report/roc_curve.png",
#     "PR Curve": "report/pr_curve.png",
#     "SHAP Summary": "report/shap_summary.png"
# }

# with tab1:
#     show_report_image(report_map["Feature Importance"], "Feature Importance")

# with tab2:
#     show_report_image(report_map["Confusion Matrix"], "Confusion Matrix")

# with tab3:
#     show_report_image(report_map["ROC Curve"], "ROC Curve")

# with tab4:
#     show_report_image(report_map["PR Curve"], "PR Curve")

# with tab5:
#     show_report_image(report_map["SHAP Summary"], "SHAP Summary")





# import os
# import io
# import random
# import requests
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas

# st.set_page_config(
#     page_title="FraudGuard AI",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# API_URL = "https://mlproject-1eie.onrender.com"
# DATA_PATH = "data/creditcard.csv"

# # ---------------------------------------------------
# # CSS
# # ---------------------------------------------------
# st.markdown("""
# <style>
# html, body, [class*="css"] {
#     font-family: "Segoe UI", sans-serif;
# }

# .stApp {
#     background:
#         radial-gradient(circle at top left, rgba(16,185,129,0.10), transparent 30%),
#         radial-gradient(circle at bottom right, rgba(245,158,11,0.08), transparent 25%),
#         linear-gradient(135deg, #0b1220 0%, #111827 50%, #0f172a 100%);
#     color: #f8fafc;
# }

# .block-container {
#     max-width: 1450px;
#     padding-top: 1rem;
#     padding-bottom: 2rem;
# }

# section[data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
#     border-right: 1px solid rgba(255,255,255,0.08);
# }

# .topbar {
#     background: linear-gradient(90deg, rgba(16,185,129,0.16), rgba(245,158,11,0.14));
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 20px;
#     padding: 22px;
#     margin-bottom: 18px;
#     box-shadow: 0 10px 28px rgba(0,0,0,0.25);
# }

# .topbar-title {
#     font-size: 34px;
#     font-weight: 800;
#     color: white;
#     margin-bottom: 6px;
# }

# .topbar-sub {
#     font-size: 15px;
#     color: #d1fae5;
#     line-height: 1.7;
# }

# .ribbon {
#     display: inline-block;
#     margin-right: 8px;
#     margin-top: 10px;
#     padding: 7px 12px;
#     border-radius: 999px;
#     font-size: 12px;
#     font-weight: 700;
#     background: rgba(255,255,255,0.08);
#     border: 1px solid rgba(255,255,255,0.08);
#     color: #f8fafc;
# }

# .section-block {
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 20px;
#     padding: 20px;
#     box-shadow: 0 8px 22px rgba(0,0,0,0.20);
# }

# .section-heading {
#     font-size: 22px;
#     font-weight: 800;
#     color: white;
#     margin-bottom: 4px;
# }

# .section-note {
#     font-size: 13px;
#     color: #cbd5e1;
#     margin-bottom: 14px;
# }

# .stat-tile {
#     background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 18px;
#     padding: 16px;
#     min-height: 118px;
# }

# .stat-label {
#     color: #94a3b8;
#     font-size: 12px;
#     margin-bottom: 8px;
#     text-transform: uppercase;
#     letter-spacing: 0.4px;
# }

# .stat-number {
#     color: white;
#     font-size: 28px;
#     font-weight: 800;
# }

# .stat-help {
#     color: #cbd5e1;
#     font-size: 12px;
#     margin-top: 6px;
# }

# .flow-card {
#     text-align: center;
#     padding: 16px;
#     border-radius: 16px;
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.07);
#     font-size: 14px;
#     font-weight: 700;
#     color: #e5e7eb;
# }

# .good-status {
#     padding: 12px 14px;
#     border-radius: 12px;
#     background: rgba(16,185,129,0.16);
#     border: 1px solid rgba(16,185,129,0.30);
#     color: #d1fae5;
#     font-weight: 700;
# }

# .bad-status {
#     padding: 12px 14px;
#     border-radius: 12px;
#     background: rgba(239,68,68,0.16);
#     border: 1px solid rgba(239,68,68,0.30);
#     color: #fee2e2;
#     font-weight: 700;
# }

# .result-card {
#     padding: 14px;
#     border-radius: 14px;
#     border: 1px solid rgba(255,255,255,0.08);
#     background: rgba(255,255,255,0.04);
#     margin-top: 12px;
# }

# .result-title {
#     font-size: 15px;
#     font-weight: 700;
#     color: white;
#     margin-bottom: 6px;
# }

# .result-body {
#     font-size: 13px;
#     line-height: 1.7;
#     color: #e5e7eb;
# }

# .small-muted {
#     color: #94a3b8;
#     font-size: 12px;
#     line-height: 1.7;
# }

# .info-chip {
#     padding: 8px 12px;
#     border-radius: 12px;
#     display: inline-block;
#     margin-right: 8px;
#     margin-bottom: 8px;
#     font-size: 12px;
#     font-weight: 600;
#     background: rgba(255,255,255,0.05);
#     border: 1px solid rgba(255,255,255,0.08);
# }

# .stButton > button {
#     width: 100%;
#     height: 3em;
#     border: none;
#     border-radius: 12px;
#     font-weight: 700;
#     color: white;
#     background: linear-gradient(90deg, #059669, #d97706);
#     box-shadow: 0 8px 20px rgba(5,150,105,0.22);
# }

# .stButton > button:hover {
#     background: linear-gradient(90deg, #047857, #b45309);
#     color: white;
# }

# hr {
#     border: none;
#     height: 1px;
#     background: rgba(255,255,255,0.08);
#     margin: 1.1rem 0;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------
# # HELPERS
# # ---------------------------------------------------
# @st.cache_data
# def load_dataset(path):
#     return pd.read_csv(path)

# def get_transaction(df, mode="random"):
#     if mode == "fraud":
#         filtered = df[df["Class"] == 1]
#     elif mode == "normal":
#         filtered = df[df["Class"] == 0]
#     else:
#         filtered = df

#     row = filtered.sample(n=1).iloc[0].to_dict()
#     actual_class = int(row["Class"])
#     del row["Class"]
#     return row, actual_class

# def get_smart_random(df):
#     if random.random() < 0.5 and len(df[df["Class"] == 1]) > 0:
#         sample = df[df["Class"] == 1].sample(1)
#     else:
#         sample = df[df["Class"] == 0].sample(1)

#     row = sample.iloc[0].to_dict()
#     actual = int(row["Class"])
#     del row["Class"]
#     return row, actual

# def get_default_transaction():
#     data = {"Time": 10000.0, "Amount": 2500.0}
#     for i in range(1, 29):
#         data[f"V{i}"] = 0.0
#     return data, None

# def class_to_text(value):
#     if value is None:
#         return "Unknown"
#     return "Fraud" if value == 1 else "Legitimate"

# def build_pdf_report(single_result, actual_label_text, dataset_rows, fraud_count, fraud_rate):
#     buffer = io.BytesIO()
#     pdf = canvas.Canvas(buffer, pagesize=A4)
#     y = A4[1] - 50

#     pdf.setFont("Helvetica-Bold", 18)
#     pdf.drawString(50, y, "FraudGuard AI - Prediction Report")
#     y -= 28

#     pdf.setFont("Helvetica", 11)
#     lines = [
#         "Project: Credit Card Fraud Detection System",
#         "Model: XGBoost Classifier",
#         "Imbalance Handling: SMOTE",
#         "Backend: Flask API",
#         "Frontend: Streamlit Dashboard",
#         "",
#         f"Dataset Size: {dataset_rows}",
#         f"Fraud Cases: {fraud_count}",
#         f"Fraud Rate: {fraud_rate:.4f}%",
#         "",
#         f"Predicted Class: {'Fraud' if single_result['fraud_prediction'] == 1 else 'Legitimate'}",
#         f"Fraud Probability: {single_result['fraud_probability']}",
#         f"Risk Level: {single_result['risk_level']}",
#         f"Threshold Used: {single_result['threshold_used']}",
#         f"Actual Dataset Label: {actual_label_text}",
#     ]

#     for line in lines:
#         pdf.drawString(50, y, line)
#         y -= 18

#     pdf.save()
#     pdf_bytes = buffer.getvalue()
#     buffer.close()
#     return pdf_bytes

# def prepare_batch_dataframe(uploaded_df):
#     df2 = uploaded_df.copy()

#     actual_labels = None
#     if "Class" in df2.columns:
#         actual_labels = df2["Class"].copy()
#         df2 = df2.drop(columns=["Class"])

#     required_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]

#     missing_cols = [col for col in required_cols if col not in df2.columns]
#     extra_cols = [col for col in df2.columns if col not in required_cols]

#     for col in missing_cols:
#         df2[col] = 0

#     df2 = df2[required_cols]

#     for col in df2.columns:
#         df2[col] = pd.to_numeric(df2[col], errors="coerce")

#     df2 = df2.fillna(0)

#     return df2, actual_labels, missing_cols, extra_cols

# def backend_health():
#     try:
#         res = requests.get(f"{API_URL}/health", timeout=5)
#         if res.status_code == 200:
#             return True, res.json()
#         return False, {}
#     except Exception:
#         return False, {}

# def plot_probability_gauge(prob):
#     prob_percent = prob * 100
#     remaining = 100 - prob_percent

#     if prob_percent >= 80:
#         color = "#ef4444"
#     elif prob_percent >= 40:
#         color = "#f59e0b"
#     else:
#         color = "#10b981"

#     fig, ax = plt.subplots(figsize=(4.2, 3.0), subplot_kw=dict(aspect="equal"))
#     ax.pie(
#         [prob_percent, remaining],
#         startangle=180,
#         counterclock=False,
#         colors=[color, "#1f2937"],
#         wedgeprops=dict(width=0.35, edgecolor="none")
#     )
#     ax.add_artist(plt.Circle((0, 0), 0.48, color="#111827"))
#     ax.text(0, 0.06, f"{prob_percent:.1f}%", ha="center", va="center", fontsize=20, fontweight="bold", color="white")
#     ax.text(0, -0.16, "Fraud Probability", ha="center", va="center", fontsize=10, color="#cbd5e1")
#     ax.set_xlim(-1.1, 1.1)
#     ax.set_ylim(-1.05, 0.35)
#     ax.axis("off")
#     fig.patch.set_facecolor("#111827")
#     ax.set_facecolor("#111827")
#     return fig

# def get_template_df():
#     cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
#     sample = {col: 0 for col in cols}
#     sample["Time"] = 10000
#     sample["Amount"] = 2500
#     return pd.DataFrame([sample])

# def prediction_box(result):
#     prob = float(result["fraud_probability"])
#     risk = result["risk_level"]
#     pred = result["fraud_prediction"]

#     if risk == "High":
#         color = "#ef4444"
#     elif risk == "Medium":
#         color = "#f59e0b"
#     else:
#         color = "#10b981"

#     return f"""
#     <div class="result-card">
#         <div class="result-title">Prediction Result</div>
#         <div class="result-body">
#             <b>Status:</b> {"Fraud" if pred == 1 else "Legitimate"} <br>
#             <b>Risk Level:</b> <span style="color:{color}; font-weight:700;">{risk}</span> <br>
#             <b>Fraud Probability:</b> {prob:.4f}
#         </div>
#     </div>
#     """

# def compute_feature_impact(input_data, df, top_n=10):
#     feature_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
#     stats_mean = df[feature_cols].mean()
#     stats_std = df[feature_cols].std().replace(0, 1)

#     impacts = []
#     for col in feature_cols:
#         val = float(input_data.get(col, 0))
#         z = abs((val - stats_mean[col]) / stats_std[col])
#         impacts.append((col, z))

#     impact_df = pd.DataFrame(impacts, columns=["Feature", "Impact"]).sort_values("Impact", ascending=False).head(top_n)
#     return impact_df

# def render_batch_analysis(result_df):
#     st.markdown("## 📊 Batch Screening Analysis")

#     if result_df is None or result_df.empty:
#         st.info("No batch results available.")
#         return

#     total_rows = len(result_df)
#     fraud_rows = 0
#     avg_score = 0
#     max_score = 0

#     if "Predicted_Class" in result_df.columns:
#         fraud_rows = int((result_df["Predicted_Class"] == "Fraud").sum())

#     if "Fraud_Probability" in result_df.columns:
#         avg_score = float(result_df["Fraud_Probability"].mean())
#         max_score = float(result_df["Fraud_Probability"].max())

#     c1, c2, c3, c4 = st.columns(4)
#     with c1:
#         st.metric("Total Rows", total_rows)
#     with c2:
#         st.metric("Predicted Fraud", fraud_rows)
#     with c3:
#         st.metric("Average Fraud Score", f"{avg_score:.4f}")
#     with c4:
#         st.metric("Max Fraud Score", f"{max_score:.4f}")

#     st.markdown("---")

#     g1, g2 = st.columns(2)

#     with g1:
#         st.markdown("### Risk Level Distribution")
#         if "Risk_Level" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             result_df["Risk_Level"].value_counts().plot(kind="bar", ax=ax)
#             ax.set_title("Risk Level Count")
#             ax.set_ylabel("Transactions")
#             st.pyplot(fig)
#         else:
#             st.info("Risk_Level column not found.")

#     with g2:
#         st.markdown("### Fraud Score Distribution")
#         if "Fraud_Probability" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.hist(result_df["Fraud_Probability"], bins=20)
#             ax.set_title("Fraud Score Histogram")
#             ax.set_xlabel("Fraud Probability")
#             ax.set_ylabel("Frequency")
#             st.pyplot(fig)
#         else:
#             st.info("Fraud_Probability column not found.")

#     st.markdown("---")

#     g3, g4 = st.columns(2)

#     with g3:
#         st.markdown("### Amount vs Fraud Score")
#         if "Amount" in result_df.columns and "Fraud_Probability" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.scatter(result_df["Amount"], result_df["Fraud_Probability"], alpha=0.7)
#             ax.set_title("Amount vs Fraud Score")
#             ax.set_xlabel("Amount")
#             ax.set_ylabel("Fraud Probability")
#             st.pyplot(fig)
#         else:
#             st.info("Amount or Fraud_Probability column not found.")

#     with g4:
#         st.markdown("### Fraud Score Trend")
#         if "Fraud_Probability" in result_df.columns:
#             fig, ax = plt.subplots(figsize=(5, 3.2))
#             ax.plot(range(len(result_df)), result_df["Fraud_Probability"], marker="o")
#             ax.set_title("Fraud Score by Row Order")
#             ax.set_xlabel("Row Index")
#             ax.set_ylabel("Fraud Probability")
#             st.pyplot(fig)
#         else:
#             st.info("Fraud_Probability column not found.")

#     st.markdown("---")

#     if "Actual_Label" in result_df.columns and "Predicted_Class" in result_df.columns:
#         st.markdown("### Actual vs Predicted")
#         compare_df = pd.crosstab(result_df["Actual_Label"], result_df["Predicted_Class"])

#         fig, ax = plt.subplots(figsize=(5, 3.2))
#         compare_df.plot(kind="bar", ax=ax)
#         ax.set_title("Actual vs Predicted Class")
#         ax.set_xlabel("Actual Label")
#         ax.set_ylabel("Count")
#         st.pyplot(fig)

#         st.markdown("---")

#     if "Fraud_Probability" in result_df.columns:
#         st.markdown("### 🔥 Top 5 Risky Transactions")

#         risky_cols = []
#         for col in ["Time", "Amount", "Fraud_Probability", "Predicted_Class", "Risk_Level", "Actual_Label"]:
#             if col in result_df.columns:
#                 risky_cols.append(col)

#         top5 = result_df.sort_values("Fraud_Probability", ascending=False).head(5)[risky_cols]
#         st.dataframe(top5, use_container_width=True)

#     if "Fraud_Probability" in result_df.columns:
#         st.markdown("---")
#         st.markdown("### Fraud Score Buckets")

#         bucket_df = result_df.copy()
#         bucket_df["Score_Bucket"] = pd.cut(
#             bucket_df["Fraud_Probability"],
#             bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
#             labels=["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"],
#             include_lowest=True
#         )

#         bucket_counts = bucket_df["Score_Bucket"].value_counts().sort_index()

#         fig, ax = plt.subplots(figsize=(6, 3.2))
#         ax.bar(bucket_counts.index.astype(str), bucket_counts.values)
#         ax.set_title("Fraud Probability Buckets")
#         ax.set_xlabel("Score Bucket")
#         ax.set_ylabel("Count")
#         st.pyplot(fig)

# # ---------------------------------------------------
# # LOAD DATA
# # ---------------------------------------------------
# if not os.path.exists(DATA_PATH):
#     st.error(f"Dataset not found at: {DATA_PATH}")
#     st.stop()

# try:
#     df = load_dataset(DATA_PATH)
# except Exception as e:
#     st.error(f"Dataset loading error: {e}")
#     st.stop()

# # ---------------------------------------------------
# # SESSION STATE
# # ---------------------------------------------------
# if "input_data" not in st.session_state:
#     st.session_state.input_data, st.session_state.actual_class = get_default_transaction()

# if "prediction_result" not in st.session_state:
#     st.session_state.prediction_result = None

# if "history" not in st.session_state:
#     st.session_state.history = []

# if "batch_results_df" not in st.session_state:
#     st.session_state.batch_results_df = None

# # ---------------------------------------------------
# # SIDEBAR
# # ---------------------------------------------------
# with st.sidebar:
#     st.markdown("## FraudGuard AI")
#     st.caption("Monitoring Console")

#     if st.button("🎲 Smart Random"):
#         st.session_state.input_data, st.session_state.actual_class = get_smart_random(df)
#         st.session_state.prediction_result = None

#     if st.button("🚨 Fraud Sample"):
#         st.session_state.input_data, st.session_state.actual_class = get_transaction(df, "fraud")
#         st.session_state.prediction_result = None

#     if st.button("✅ Legitimate Sample"):
#         st.session_state.input_data, st.session_state.actual_class = get_transaction(df, "normal")
#         st.session_state.prediction_result = None

#     if st.button("🧪 Default Input"):
#         st.session_state.input_data, st.session_state.actual_class = get_default_transaction()
#         st.session_state.prediction_result = None

#     st.write("")
#     ok, health_data = backend_health()
#     if ok:
#         st.markdown("<div class='good-status'>Backend API Connected</div>", unsafe_allow_html=True)
#         st.caption(f"Threshold: {health_data.get('threshold', 'N/A')}")
#     else:
#         st.markdown("<div class='bad-status'>Backend API Not Reachable</div>", unsafe_allow_html=True)
#         st.caption("Start Flask first using: python -m src.app")

#     st.write("")
#     st.markdown("### Stack")
#     st.markdown("""
# - **Model**: XGBoost  
# - **Balancing**: SMOTE  
# - **Backend**: Flask  
# - **Frontend**: Streamlit  
# - **Reports**: Matplotlib, ReportLab  
# """)

# # ---------------------------------------------------
# # TOPBAR
# # ---------------------------------------------------
# st.markdown("""
# <div class="topbar">
#     <div class="topbar-title">🛡️ FraudGuard AI</div>
#     <div class="topbar-sub">
#         A cleaner fraud detection dashboard for real-time scoring, batch transaction screening, explainability, and downloadable reporting.
#     </div>
#     <span class="ribbon">Smart Random</span>
#     <span class="ribbon">Batch CSV</span>
#     <span class="ribbon">Explainability</span>
#     <span class="ribbon">Risk Scoring</span>
# </div>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------
# # OVERVIEW
# # ---------------------------------------------------
# ov1, ov2 = st.columns([1.5, 1])

# with ov1:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-heading'>Project Overview</div>", unsafe_allow_html=True)
#     st.markdown("<div class='section-note'>What the system does and how the processing pipeline works.</div>", unsafe_allow_html=True)
#     st.write("""
# This project predicts whether a credit card transaction is **fraudulent** or **legitimate**.

# ### Core flow
# 1. Transaction is selected or uploaded  
# 2. Flask backend receives the data  
# 3. Model preprocessing is applied  
# 4. XGBoost predicts fraud probability  
# 5. Dashboard shows class, probability, and risk level  
# """)
#     st.markdown("</div>", unsafe_allow_html=True)

# with ov2:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("<div class='section-heading'>Conclusion</div>", unsafe_allow_html=True)
#     st.markdown("<div class='section-note'>Short final summary of the project.</div>", unsafe_allow_html=True)
#     st.write("""
# FraudGuard AI demonstrates a complete end-to-end machine learning solution for credit card fraud detection.  
# It combines preprocessing, model inference, real-time prediction, batch screening, and visual reporting in a single workflow.
# """)
#     st.markdown("</div>", unsafe_allow_html=True)

# st.write("")

# # ---------------------------------------------------
# # STATS
# # ---------------------------------------------------
# fraud_count = int(df["Class"].sum())
# normal_count = len(df) - fraud_count
# fraud_rate = (fraud_count / len(df)) * 100

# s1, s2, s3, s4 = st.columns(4)

# with s1:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Total Transactions</div>
#         <div class="stat-number">{len(df):,}</div>
#         <div class="stat-help">Complete dataset size</div>
#     </div>
#     """, unsafe_allow_html=True)

# with s2:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Fraud Cases</div>
#         <div class="stat-number">{fraud_count:,}</div>
#         <div class="stat-help">Minority class</div>
#     </div>
#     """, unsafe_allow_html=True)

# with s3:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Legitimate Cases</div>
#         <div class="stat-number">{normal_count:,}</div>
#         <div class="stat-help">Majority class</div>
#     </div>
#     """, unsafe_allow_html=True)

# with s4:
#     st.markdown(f"""
#     <div class="stat-tile">
#         <div class="stat-label">Fraud Rate</div>
#         <div class="stat-number">{fraud_rate:.4f}%</div>
#         <div class="stat-help">Highly imbalanced</div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # FLOW
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>System Flow</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Simple processing stages of the project.</div>", unsafe_allow_html=True)

# f1, f2, f3, f4 = st.columns(4)
# with f1:
#     st.markdown("<div class='flow-card'>Input</div>", unsafe_allow_html=True)
# with f2:
#     st.markdown("<div class='flow-card'>Preprocess</div>", unsafe_allow_html=True)
# with f3:
#     st.markdown("<div class='flow-card'>Model Score</div>", unsafe_allow_html=True)
# with f4:
#     st.markdown("<div class='flow-card'>Risk Output</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # SINGLE TRANSACTION
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Single Transaction Scoring</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Use one selected transaction and generate a live fraud score.</div>", unsafe_allow_html=True)

# left, right = st.columns([1.2, 1])
# input_data = st.session_state.input_data
# actual_class = st.session_state.actual_class

# with left:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("### Current Transaction")
#     m1, m2, m3 = st.columns(3)
#     with m1:
#         st.metric("Time", f"{input_data.get('Time', 0):.2f}")
#     with m2:
#         st.metric("Amount", f"{input_data.get('Amount', 0):.2f}")
#     with m3:
#         st.metric("Actual Label", class_to_text(actual_class))

#     st.write("")
#     st.markdown("### Input Preview")
#     feature_df = pd.DataFrame({
#         "Feature": [f"V{i}" for i in range(1, 29)],
#         "Value": [float(input_data.get(f"V{i}", 0.0)) for i in range(1, 29)]
#     })
#     st.dataframe(feature_df, use_container_width=True, height=360)
#     st.markdown("</div>", unsafe_allow_html=True)

# with right:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("### Prediction")
#     st.markdown("<div class='small-muted'>Run the backend model and review the output in a compact readable format.</div>", unsafe_allow_html=True)

#     if st.button("🔍 Run Prediction"):
#         try:
#             response = requests.post(f"{API_URL}/predict", json=input_data, timeout=10)
#             result = response.json()

#             if response.status_code != 200:
#                 st.error(result.get("error", "Prediction failed"))
#             else:
#                 st.session_state.prediction_result = result
#                 st.session_state.history.insert(0, {
#                     "Predicted Class": "Fraud" if result["fraud_prediction"] == 1 else "Legitimate",
#                     "Fraud Probability": result["fraud_probability"],
#                     "Risk Level": result["risk_level"],
#                     "Actual Label": class_to_text(actual_class)
#                 })
#                 st.session_state.history = st.session_state.history[:10]

#         except requests.exceptions.ConnectionError:
#             st.error("Backend API is not running. Start it with: python -m src.app")
#         except Exception as e:
#             st.error(f"Prediction error: {e}")

#     st.write("")

#     if st.session_state.prediction_result is not None:
#         result = st.session_state.prediction_result

#         x1, x2 = st.columns(2)
#         with x1:
#             st.metric("Predicted Class", "Fraud" if result["fraud_prediction"] == 1 else "Legitimate")
#         with x2:
#             st.metric("Risk Level", result["risk_level"])

#         x3, x4 = st.columns(2)
#         with x3:
#             st.metric("Fraud Probability", f"{result['fraud_probability']:.4f}")
#         with x4:
#             st.metric("Threshold", f"{result['threshold_used']:.2f}")

#         st.pyplot(plot_probability_gauge(float(result["fraud_probability"])), use_container_width=True)
#         st.markdown(prediction_box(result), unsafe_allow_html=True)

#         pdf_bytes = build_pdf_report(
#             result,
#             class_to_text(actual_class),
#             len(df),
#             fraud_count,
#             fraud_rate
#         )

#         st.download_button(
#             label="📄 Download PDF Report",
#             data=pdf_bytes,
#             file_name="fraudguard_prediction_report.pdf",
#             mime="application/pdf"
#         )

#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # EXPLAINABILITY
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Feature Impact View</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>A simple explanation layer based on deviation from dataset averages.</div>", unsafe_allow_html=True)

# impact_df = compute_feature_impact(input_data, df, top_n=10)

# e1, e2 = st.columns([1.1, 1])

# with e1:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     fig_imp, ax_imp = plt.subplots(figsize=(6, 4))
#     ax_imp.barh(impact_df["Feature"], impact_df["Impact"])
#     ax_imp.invert_yaxis()
#     ax_imp.set_title("Top Feature Impact")
#     ax_imp.set_xlabel("Relative Impact")
#     st.pyplot(fig_imp)
#     st.markdown("</div>", unsafe_allow_html=True)

# with e2:
#     st.markdown("<div class='section-block'>", unsafe_allow_html=True)
#     st.markdown("### Explanation")
#     st.write("""
# This section highlights which input features are most different from the dataset average.

# A larger deviation suggests the feature may be contributing more strongly to the current transaction’s unusual pattern.
# """)
#     for _, row in impact_df.head(5).iterrows():
#         st.markdown(f"<span class='info-chip'>{row['Feature']} • {row['Impact']:.2f}</span>", unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # BATCH SCREENING
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Batch Transaction Screening</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Upload a CSV and run fraud scoring for multiple rows.</div>", unsafe_allow_html=True)

# template_df = get_template_df()
# template_bytes = template_df.to_csv(index=False).encode("utf-8")

# st.download_button(
#     label="⬇️ Download CSV Template",
#     data=template_bytes,
#     file_name="fraudguard_batch_template.csv",
#     mime="text/csv"
# )

# st.markdown("<div class='section-block'>", unsafe_allow_html=True)
# uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])

# if uploaded_file is not None:
#     try:
#         uploaded_df = pd.read_csv(uploaded_file)
#         st.write("### Uploaded File Preview")
#         st.dataframe(uploaded_df.head(), use_container_width=True)

#         batch_df, actual_labels, missing_cols, extra_cols = prepare_batch_dataframe(uploaded_df)

#         b1, b2 = st.columns(2)
#         with b1:
#             if missing_cols:
#                 st.warning(f"Missing columns filled with 0: {missing_cols}")
#             else:
#                 st.success("No required columns missing.")

#         with b2:
#             if extra_cols:
#                 st.info(f"Extra columns ignored: {extra_cols}")
#             else:
#                 st.success("No extra columns detected.")

#         if st.button("📤 Run Batch Screening"):
#             payload = {"records": batch_df.to_dict(orient="records")}
#             response = requests.post(f"{API_URL}/predict_batch", json=payload, timeout=60)
#             result = response.json()

#             if response.status_code != 200:
#                 st.error(result.get("error", "Batch prediction failed"))
#             else:
#                 batch_results = pd.DataFrame(result["results"])

#                 final_df = batch_df.copy()
#                 if not batch_results.empty:
#                     final_df["Predicted_Class"] = batch_results["fraud_prediction"].map({0: "Legitimate", 1: "Fraud"})
#                     final_df["Fraud_Probability"] = batch_results["fraud_probability"]
#                     final_df["Risk_Level"] = batch_results["risk_level"]

#                 if actual_labels is not None:
#                     final_df["Actual_Label"] = actual_labels.map({0: "Legitimate", 1: "Fraud"})

#                 st.session_state.batch_results_df = final_df

#                 if result.get("row_errors"):
#                     st.warning(f"Some rows failed: {result['row_errors']}")

#         if st.session_state.batch_results_df is not None:
#             st.write("### Batch Results")
#             st.dataframe(st.session_state.batch_results_df, use_container_width=True, height=350)

#             csv_bytes = st.session_state.batch_results_df.to_csv(index=False).encode("utf-8")
#             st.download_button(
#                 label="⬇️ Download Results CSV",
#                 data=csv_bytes,
#                 file_name="fraudguard_batch_results.csv",
#                 mime="text/csv"
#             )

#             render_batch_analysis(st.session_state.batch_results_df)

#     except Exception as e:
#         st.error(f"CSV processing error: {e}")
# st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("---")

# # ---------------------------------------------------
# # HISTORY
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Prediction History</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Recent predictions generated in the current session.</div>", unsafe_allow_html=True)

# if st.session_state.history:
#     st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, height=250)
# else:
#     st.info("No predictions yet.")
# st.markdown("---")

# # ---------------------------------------------------
# # MODEL REPORTS
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Model Reports</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Saved visual artifacts from model training and evaluation.</div>", unsafe_allow_html=True)

# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "Feature Importance",
#     "Confusion Matrix",
#     "ROC Curve",
#     "PR Curve",
#     "SHAP Summary"
# ])

# report_map = {
#     "Feature Importance": "report/feature_importance.png",
#     "Confusion Matrix": "report/confusion_matrix.png",
#     "ROC Curve": "report/roc_curve.png",
#     "PR Curve": "report/pr_curve.png",
#     "SHAP Summary": "report/shap_summary.png"
# }

# with tab1:
#     path = report_map["Feature Importance"]
#     if os.path.exists(path):
#         st.image(path, width=900)
#     else:
#         st.warning(f"{path} not found.")

# with tab2:
#     path = report_map["Confusion Matrix"]
#     if os.path.exists(path):
#         st.image(path, width=900)
#     else:
#         st.warning(f"{path} not found.")

# with tab3:
#     path = report_map["ROC Curve"]
#     if os.path.exists(path):
#         st.image(path, width=900)
#     else:
#         st.warning(f"{path} not found.")

# with tab4:
#     path = report_map["PR Curve"]
#     if os.path.exists(path):
#         st.image(path, width=900)
#     else:
#         st.warning(f"{path} not found.")

# with tab5:
#     path = report_map["SHAP Summary"]
#     if os.path.exists(path):
#         st.image(path, width=900)
#     else:
#         st.warning(f"{path} not found.")







import os
import io
import random
import json
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# IMPORTANT
# local:
API_URL = "http://127.0.0.1:5000"
# deployed:
# API_URL = "https://your-backend-url.onrender.com"
# -------------------------------
# API_URL = "https://mlproject-1eie.onrender.com"
DATA_PATH = "data/creditcard.csv"

# API_URL = "https://mlproject-1eie.onrender.com"
# DATA_PATH = "data/creditcard.csv"
# ---------------------------------------------------
# CSS
# ---------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(16,185,129,0.10), transparent 30%),
        radial-gradient(circle at bottom right, rgba(245,158,11,0.08), transparent 25%),
        linear-gradient(135deg, #0b1220 0%, #111827 50%, #0f172a 100%);
    color: #f8fafc;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.topbar {
    background: linear-gradient(90deg, rgba(16,185,129,0.16), rgba(245,158,11,0.14));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.25);
}

.topbar-title {
    font-size: 34px;
    font-weight: 800;
    color: white;
    margin-bottom: 6px;
}

.topbar-sub {
    font-size: 15px;
    color: #d1fae5;
    line-height: 1.7;
}

.ribbon {
    display: inline-block;
    margin-right: 8px;
    margin-top: 10px;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    color: #f8fafc;
}

.section-block {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.20);
}

.section-heading {
    font-size: 22px;
    font-weight: 800;
    color: white;
    margin-bottom: 4px;
}

.section-note {
    font-size: 13px;
    color: #cbd5e1;
    margin-bottom: 14px;
}

.stat-tile {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 16px;
    min-height: 118px;
}

.stat-label {
    color: #94a3b8;
    font-size: 12px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.stat-number {
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.stat-help {
    color: #cbd5e1;
    font-size: 12px;
    margin-top: 6px;
}

.flow-card {
    text-align: center;
    padding: 16px;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    font-size: 14px;
    font-weight: 700;
    color: #e5e7eb;
}

.good-status {
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(16,185,129,0.16);
    border: 1px solid rgba(16,185,129,0.30);
    color: #d1fae5;
    font-weight: 700;
}

.bad-status {
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(239,68,68,0.16);
    border: 1px solid rgba(239,68,68,0.30);
    color: #fee2e2;
    font-weight: 700;
}

.result-card {
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    margin-top: 12px;
}

.result-title {
    font-size: 15px;
    font-weight: 700;
    color: white;
    margin-bottom: 6px;
}

.result-body {
    font-size: 13px;
    line-height: 1.7;
    color: #e5e7eb;
}

.small-muted {
    color: #94a3b8;
    font-size: 12px;
    line-height: 1.7;
}

.info-chip {
    padding: 8px 12px;
    border-radius: 12px;
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
    font-size: 12px;
    font-weight: 600;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}

.stButton > button {
    width: 100%;
    height: 3em;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg, #059669, #d97706);
    box-shadow: 0 8px 20px rgba(5,150,105,0.22);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #047857, #b45309);
    color: white;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 1.1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
@st.cache_data
def load_dataset(path):
    return pd.read_csv(path)

def get_transaction(df, mode="random"):
    if mode == "fraud":
        filtered = df[df["Class"] == 1]
    elif mode == "normal":
        filtered = df[df["Class"] == 0]
    else:
        filtered = df

    row = filtered.sample(n=1).iloc[0].to_dict()
    actual_class = int(row["Class"])
    del row["Class"]
    return row, actual_class

def get_smart_random(df):
    if random.random() < 0.5 and len(df[df["Class"] == 1]) > 0:
        sample = df[df["Class"] == 1].sample(1)
    else:
        sample = df[df["Class"] == 0].sample(1)

    row = sample.iloc[0].to_dict()
    actual = int(row["Class"])
    del row["Class"]
    return row, actual

def get_default_transaction():
    data = {"Time": 10000.0, "Amount": 2500.0}
    for i in range(1, 29):
        data[f"V{i}"] = 0.0
    return data, None

def class_to_text(value):
    if value is None:
        return "Unknown"
    return "Fraud" if value == 1 else "Legitimate"

def build_pdf_report(single_result, actual_label_text, dataset_rows, fraud_count, fraud_rate, model_used):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    y = A4[1] - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "FraudGuard AI - Prediction Report")
    y -= 28

    pdf.setFont("Helvetica", 11)
    lines = [
        "Project: Credit Card Fraud Detection System",
        f"Model Used: {model_used}",
        "Frontend: Streamlit Dashboard",
        "Backend: Flask API",
        "",
        f"Dataset Size: {dataset_rows}",
        f"Fraud Cases: {fraud_count}",
        f"Fraud Rate: {fraud_rate:.4f}%",
        "",
        f"Predicted Class: {'Fraud' if single_result['fraud_prediction'] == 1 else 'Legitimate'}",
        f"Fraud Probability: {single_result['fraud_probability']}",
        f"Risk Level: {single_result['risk_level']}",
        f"Actual Dataset Label: {actual_label_text}",
    ]

    if "threshold_used" in single_result:
        lines.append(f"Threshold Used: {single_result['threshold_used']}")

    for line in lines:
        pdf.drawString(50, y, line)
        y -= 18

    pdf.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def prepare_batch_dataframe(uploaded_df):
    df2 = uploaded_df.copy()

    actual_labels = None
    if "Class" in df2.columns:
        actual_labels = df2["Class"].copy()
        df2 = df2.drop(columns=["Class"])

    required_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]

    missing_cols = [col for col in required_cols if col not in df2.columns]
    extra_cols = [col for col in df2.columns if col not in required_cols]

    for col in missing_cols:
        df2[col] = 0

    df2 = df2[required_cols]

    for col in df2.columns:
        df2[col] = pd.to_numeric(df2[col], errors="coerce")

    df2 = df2.fillna(0)

    return df2, actual_labels, missing_cols, extra_cols

def backend_health():
    try:
        res = requests.get(f"{API_URL}/health", timeout=5)
        if res.status_code == 200:
            return True, res.json()
        return False, {}
    except Exception:
        return False, {}

def plot_probability_gauge(prob):
    prob_percent = prob * 100
    remaining = 100 - prob_percent

    if prob_percent >= 80:
        color = "#ef4444"
    elif prob_percent >= 40:
        color = "#f59e0b"
    else:
        color = "#10b981"

    fig, ax = plt.subplots(figsize=(4.2, 3.0), subplot_kw=dict(aspect="equal"))
    ax.pie(
        [prob_percent, remaining],
        startangle=180,
        counterclock=False,
        colors=[color, "#1f2937"],
        wedgeprops=dict(width=0.35, edgecolor="none")
    )
    ax.add_artist(plt.Circle((0, 0), 0.48, color="#111827"))
    ax.text(0, 0.06, f"{prob_percent:.1f}%", ha="center", va="center", fontsize=20, fontweight="bold", color="white")
    ax.text(0, -0.16, "Fraud Probability", ha="center", va="center", fontsize=10, color="#cbd5e1")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.05, 0.35)
    ax.axis("off")
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    return fig

def get_template_df():
    cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    sample = {col: 0 for col in cols}
    sample["Time"] = 10000
    sample["Amount"] = 2500
    return pd.DataFrame([sample])

def prediction_box(result):
    prob = float(result["fraud_probability"])
    risk = result["risk_level"]
    pred = result["fraud_prediction"]

    if risk == "High":
        color = "#ef4444"
    elif risk == "Medium":
        color = "#f59e0b"
    else:
        color = "#10b981"

    return f"""
    <div class="result-card">
        <div class="result-title">Prediction Result</div>
        <div class="result-body">
            <b>Status:</b> {"Fraud" if pred == 1 else "Legitimate"} <br>
            <b>Risk Level:</b> <span style="color:{color}; font-weight:700;">{risk}</span> <br>
            <b>Fraud Probability:</b> {prob:.4f}
        </div>
    </div>
    """

def compute_feature_impact(input_data, df, top_n=10):
    feature_cols = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]
    stats_mean = df[feature_cols].mean()
    stats_std = df[feature_cols].std().replace(0, 1)

    impacts = []
    for col in feature_cols:
        val = float(input_data.get(col, 0))
        z = abs((val - stats_mean[col]) / stats_std[col])
        impacts.append((col, z))

    impact_df = pd.DataFrame(impacts, columns=["Feature", "Impact"]).sort_values("Impact", ascending=False).head(top_n)
    return impact_df

def render_batch_analysis(result_df):
    st.markdown("## 📊 Batch Screening Analysis")

    if result_df is None or result_df.empty:
        st.info("No batch results available.")
        return

    total_rows = len(result_df)
    fraud_rows = 0
    avg_score = 0
    max_score = 0

    if "Predicted_Class" in result_df.columns:
        fraud_rows = int((result_df["Predicted_Class"] == "Fraud").sum())

    if "Fraud_Probability" in result_df.columns:
        avg_score = float(result_df["Fraud_Probability"].mean())
        max_score = float(result_df["Fraud_Probability"].max())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Rows", total_rows)
    with c2:
        st.metric("Predicted Fraud", fraud_rows)
    with c3:
        st.metric("Average Fraud Score", f"{avg_score:.4f}")
    with c4:
        st.metric("Max Fraud Score", f"{max_score:.4f}")

    st.markdown("---")

    g1, g2 = st.columns(2)

    with g1:
        st.markdown("### Risk Level Distribution")
        if "Risk_Level" in result_df.columns:
            fig, ax = plt.subplots(figsize=(5, 3.2))
            result_df["Risk_Level"].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("Risk Level Count")
            ax.set_ylabel("Transactions")
            st.pyplot(fig)
        else:
            st.info("Risk_Level column not found.")

    with g2:
        st.markdown("### Fraud Score Distribution")
        if "Fraud_Probability" in result_df.columns:
            fig, ax = plt.subplots(figsize=(5, 3.2))
            ax.hist(result_df["Fraud_Probability"], bins=20)
            ax.set_title("Fraud Score Histogram")
            ax.set_xlabel("Fraud Probability")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        else:
            st.info("Fraud_Probability column not found.")

    st.markdown("---")

    g3, g4 = st.columns(2)

    with g3:
        st.markdown("### Amount vs Fraud Score")
        if "Amount" in result_df.columns and "Fraud_Probability" in result_df.columns:
            fig, ax = plt.subplots(figsize=(5, 3.2))
            ax.scatter(result_df["Amount"], result_df["Fraud_Probability"], alpha=0.7)
            ax.set_title("Amount vs Fraud Score")
            ax.set_xlabel("Amount")
            ax.set_ylabel("Fraud Probability")
            st.pyplot(fig)
        else:
            st.info("Amount or Fraud_Probability column not found.")

    with g4:
        st.markdown("### Fraud Score Trend")
        if "Fraud_Probability" in result_df.columns:
            fig, ax = plt.subplots(figsize=(5, 3.2))
            ax.plot(range(len(result_df)), result_df["Fraud_Probability"], marker="o")
            ax.set_title("Fraud Score by Row Order")
            ax.set_xlabel("Row Index")
            ax.set_ylabel("Fraud Probability")
            st.pyplot(fig)
        else:
            st.info("Fraud_Probability column not found.")

    st.markdown("---")

    if "Actual_Label" in result_df.columns and "Predicted_Class" in result_df.columns:
        st.markdown("### Actual vs Predicted")
        compare_df = pd.crosstab(result_df["Actual_Label"], result_df["Predicted_Class"])

        fig, ax = plt.subplots(figsize=(5, 3.2))
        compare_df.plot(kind="bar", ax=ax)
        ax.set_title("Actual vs Predicted Class")
        ax.set_xlabel("Actual Label")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.markdown("---")

    if "Fraud_Probability" in result_df.columns:
        st.markdown("### 🔥 Top 5 Risky Transactions")

        risky_cols = []
        for col in ["Time", "Amount", "Fraud_Probability", "Predicted_Class", "Risk_Level", "Actual_Label", "Model_Used"]:
            if col in result_df.columns:
                risky_cols.append(col)

        top5 = result_df.sort_values("Fraud_Probability", ascending=False).head(5)[risky_cols]
        st.dataframe(top5, use_container_width=True)

    if "Fraud_Probability" in result_df.columns:
        st.markdown("---")
        st.markdown("### Fraud Score Buckets")

        bucket_df = result_df.copy()
        bucket_df["Score_Bucket"] = pd.cut(
            bucket_df["Fraud_Probability"],
            bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
            labels=["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"],
            include_lowest=True
        )

        bucket_counts = bucket_df["Score_Bucket"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(6, 3.2))
        ax.bar(bucket_counts.index.astype(str), bucket_counts.values)
        ax.set_title("Fraud Probability Buckets")
        ax.set_xlabel("Score Bucket")
        ax.set_ylabel("Count")
        st.pyplot(fig)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
if not os.path.exists(DATA_PATH):
    st.error(f"Dataset not found at: {DATA_PATH}")
    st.stop()

try:
    df = load_dataset(DATA_PATH)
except Exception as e:
    st.error(f"Dataset loading error: {e}")
    st.stop()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "input_data" not in st.session_state:
    st.session_state.input_data, st.session_state.actual_class = get_default_transaction()

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "history" not in st.session_state:
    st.session_state.history = []

if "batch_results_df" not in st.session_state:
    st.session_state.batch_results_df = None

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## FraudGuard AI")
    st.caption("Monitoring Console")

    model_choice = st.selectbox(
        "🤖 Select ML Model",
        ["logistic", "random_forest", "xgboost"],
        index=2
    )

    if st.button("🎲 Smart Random"):
        st.session_state.input_data, st.session_state.actual_class = get_smart_random(df)
        st.session_state.prediction_result = None

    if st.button("🚨 Fraud Sample"):
        st.session_state.input_data, st.session_state.actual_class = get_transaction(df, "fraud")
        st.session_state.prediction_result = None

    if st.button("✅ Legitimate Sample"):
        st.session_state.input_data, st.session_state.actual_class = get_transaction(df, "normal")
        st.session_state.prediction_result = None

    if st.button("🧪 Default Input"):
        st.session_state.input_data, st.session_state.actual_class = get_default_transaction()
        st.session_state.prediction_result = None

    st.write("")
    ok, health_data = backend_health()
    if ok:
        st.markdown("<div class='good-status'>Backend API Connected</div>", unsafe_allow_html=True)
        st.caption(f"Available Models: {', '.join(health_data.get('available_models', []))}")
    else:
        st.markdown("<div class='bad-status'>Backend API Not Reachable</div>", unsafe_allow_html=True)
        st.caption("Start Flask first using: python -m src.app")

    st.write("")
    st.markdown("### Stack")
    st.markdown("""
- **Models**: Logistic, Random Forest, XGBoost  
- **Balancing**: SMOTE  
- **Backend**: Flask  
- **Frontend**: Streamlit  
- **Reports**: Matplotlib, ReportLab  
""")

# ---------------------------------------------------
# TOPBAR
# ---------------------------------------------------
st.markdown("""
<div class="topbar">
    <div class="topbar-title">🛡️ FraudGuard AI</div>
    <div class="topbar-sub">
        A multi-model fraud detection dashboard for real-time scoring, batch transaction screening, model comparison, and downloadable reporting.
    </div>
    <span class="ribbon">Model Selection</span>
    <span class="ribbon">Batch CSV</span>
    <span class="ribbon">Comparison</span>
    <span class="ribbon">Risk Scoring</span>
</div>
""", unsafe_allow_html=True)

# # ---------------------------------------------------
# # MODEL COMPARISON
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Model Comparison</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Compare multiple machine learning models and identify the best one.</div>", unsafe_allow_html=True)

# try:
#     metrics_response = requests.get(f"{API_URL}/metrics", timeout=10)
#     metrics_json = metrics_response.json()

#     if isinstance(metrics_json, dict) and len(metrics_json) > 0:
#         metrics_df = pd.DataFrame(metrics_json).T.reset_index()
#         metrics_df = metrics_df.rename(columns={"index": "Model"})
#         st.dataframe(metrics_df, use_container_width=True)

#         best_model = None
#         score_col = None

#         if "f1_score" in metrics_df.columns:
#             score_col = "f1_score"
#         elif "F1" in metrics_df.columns:
#             score_col = "F1"

#         if score_col:
#             best_model = metrics_df.sort_values(score_col, ascending=False).iloc[0]["Model"]
#             st.success(f"Best Model based on F1 Score: {best_model}")

#             fig, ax = plt.subplots(figsize=(6, 3))
#             ax.bar(metrics_df["Model"], metrics_df[score_col])
#             ax.set_title("F1 Score Comparison")
#             ax.set_ylabel("F1 Score")
#             st.pyplot(fig)

# except Exception as e:
#     st.warning(f"Could not load model comparison: {e}")

# st.markdown("---")

# ---------------------------------------------------
# MODEL COMPARISON
# ---------------------------------------------------
st.markdown("<div class='section-heading'>Model Comparison</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>Compare multiple machine learning models and identify the best one.</div>", unsafe_allow_html=True)

try:
    metrics_response = requests.get(f"{API_URL}/metrics", timeout=15)

    # first check response code
    if metrics_response.status_code != 200:
        st.warning(f"Could not load model comparison: HTTP {metrics_response.status_code}")
    else:
        # check content
        raw_text = metrics_response.text.strip()

        if not raw_text:
            st.warning("Could not load model comparison: empty response from backend.")
        else:
            try:
                metrics_json = metrics_response.json()
            except Exception:
                st.warning(f"Could not load model comparison: backend returned non-JSON response.\n\n{raw_text[:300]}")
                metrics_json = None

            if metrics_json:
                if isinstance(metrics_json, dict) and "error" in metrics_json:
                    st.warning(f"Could not load model comparison: {metrics_json['error']}")
                elif isinstance(metrics_json, dict) and len(metrics_json) > 0:
                    metrics_df = pd.DataFrame(metrics_json).T.reset_index()
                    metrics_df = metrics_df.rename(columns={"index": "Model"})
                    st.dataframe(metrics_df, use_container_width=True)

                    score_col = None
                    if "f1_score" in metrics_df.columns:
                        score_col = "f1_score"
                    elif "F1" in metrics_df.columns:
                        score_col = "F1"

                    if score_col:
                        best_model = metrics_df.sort_values(score_col, ascending=False).iloc[0]["Model"]
                        st.success(f"Best Model based on F1 Score: {best_model}")

                        fig, ax = plt.subplots(figsize=(6, 3))
                        ax.bar(metrics_df["Model"], metrics_df[score_col])
                        ax.set_title("F1 Score Comparison")
                        ax.set_ylabel("F1 Score")
                        st.pyplot(fig)
                else:
                    st.warning("Model comparison data is empty.")

except Exception as e:
    st.warning(f"Could not load model comparison: {e}")

st.markdown("---")

# ---------------------------------------------------
# OVERVIEW
# ---------------------------------------------------
ov1, ov2 = st.columns([1.5, 1])

with ov1:
    st.markdown("<div class='section-block'>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Project Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>What the system does and how the processing pipeline works.</div>", unsafe_allow_html=True)
    st.write("""
This project predicts whether a credit card transaction is **fraudulent** or **legitimate**.

### Core flow
1. User selects a machine learning model  
2. Transaction is selected or uploaded  
3. Flask backend receives the data  
4. Model preprocessing is applied  
5. Selected model predicts fraud probability  
6. Dashboard shows class, probability, and risk level  
""")
    st.markdown("</div>", unsafe_allow_html=True)

with ov2:
    st.markdown("<div class='section-block'>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Conclusion</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>Short final summary of the project.</div>", unsafe_allow_html=True)
    st.write("""
FraudGuard AI now supports multiple machine learning models, user-driven model selection, comparative evaluation, real-time prediction, and batch fraud screening in one workflow.
""")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# STATS
# ---------------------------------------------------
fraud_count = int(df["Class"].sum())
normal_count = len(df) - fraud_count
fraud_rate = (fraud_count / len(df)) * 100

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-label">Total Transactions</div>
        <div class="stat-number">{len(df):,}</div>
        <div class="stat-help">Complete dataset size</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-label">Fraud Cases</div>
        <div class="stat-number">{fraud_count:,}</div>
        <div class="stat-help">Minority class</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-label">Legitimate Cases</div>
        <div class="stat-number">{normal_count:,}</div>
        <div class="stat-help">Majority class</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-label">Fraud Rate</div>
        <div class="stat-number">{fraud_rate:.4f}%</div>
        <div class="stat-help">Highly imbalanced</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")


# ---------------------------------------------------
# FLOW
# ---------------------------------------------------
st.markdown("<div class='section-heading'>System Flow</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>Simple processing stages of the project.</div>", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
with f1:
    st.markdown("<div class='flow-card'>Model Select</div>", unsafe_allow_html=True)
with f2:
    st.markdown("<div class='flow-card'>Input</div>", unsafe_allow_html=True)
with f3:
    st.markdown("<div class='flow-card'>Predict</div>", unsafe_allow_html=True)
with f4:
    st.markdown("<div class='flow-card'>Compare & Output</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# SINGLE TRANSACTION
# ---------------------------------------------------
st.markdown("<div class='section-heading'>Single Transaction Scoring</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>Use one selected transaction and generate a live fraud score using the selected model.</div>", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])
input_data = st.session_state.input_data
actual_class = st.session_state.actual_class

with left:
    st.markdown("<div class='section-block'>", unsafe_allow_html=True)
    st.markdown("### Current Transaction")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Time", f"{input_data.get('Time', 0):.2f}")
    with m2:
        st.metric("Amount", f"{input_data.get('Amount', 0):.2f}")
    with m3:
        st.metric("Actual Label", class_to_text(actual_class))

    st.write("")
    st.markdown("### Input Preview")
    feature_df = pd.DataFrame({
        "Feature": [f"V{i}" for i in range(1, 29)],
        "Value": [float(input_data.get(f"V{i}", 0.0)) for i in range(1, 29)]
    })
    st.dataframe(feature_df, use_container_width=True, height=360)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-block'>", unsafe_allow_html=True)
    st.markdown("### Prediction")
    st.markdown("<div class='small-muted'>Run the selected backend model and review the output.</div>", unsafe_allow_html=True)

    if st.button("🔍 Run Prediction"):
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json={**input_data, "model": model_choice},
                timeout=10
            )
            result = response.json()

            if response.status_code != 200:
                st.error(result.get("error", "Prediction failed"))
            else:
                st.session_state.prediction_result = result
                st.session_state.history.insert(0, {
                    "Model Used": result.get("model_used", model_choice),
                    "Predicted Class": "Fraud" if result["fraud_prediction"] == 1 else "Legitimate",
                    "Fraud Probability": result["fraud_probability"],
                    "Risk Level": result["risk_level"],
                    "Actual Label": class_to_text(actual_class)
                })
                st.session_state.history = st.session_state.history[:10]

        except requests.exceptions.ConnectionError:
            st.error("Backend API is not running. Start it with: python -m src.app")
        except Exception as e:
            st.error(f"Prediction error: {e}")

    st.write("")

    if st.session_state.prediction_result is not None:
        result = st.session_state.prediction_result

        st.info(f"Model Used: {result.get('model_used', model_choice)}")

        x1, x2 = st.columns(2)
        with x1:
            st.metric("Predicted Class", "Fraud" if result["fraud_prediction"] == 1 else "Legitimate")
        with x2:
            st.metric("Risk Level", result["risk_level"])

        x3, x4 = st.columns(2)
        with x3:
            st.metric("Fraud Probability", f"{result['fraud_probability']:.4f}")
        with x4:
            if "threshold_used" in result:
                st.metric("Threshold", f"{result['threshold_used']:.2f}")
            else:
                st.metric("Threshold", "0.50")

        st.pyplot(plot_probability_gauge(float(result["fraud_probability"])), use_container_width=True)
        st.markdown(prediction_box(result), unsafe_allow_html=True)

        pdf_bytes = build_pdf_report(
            result,
            class_to_text(actual_class),
            len(df),
            fraud_count,
            fraud_rate,
            result.get("model_used", model_choice)
        )

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="fraudguard_prediction_report.pdf",
            mime="application/pdf"
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# EXPLAINABILITY STYLE VIEW
# ---------------------------------------------------

st.markdown("<div class='section-heading'>Feature Impact View</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>A simple explanation layer based on deviation from dataset averages.</div>", unsafe_allow_html=True)

impact_df = compute_feature_impact(input_data, df, top_n=10)

e1, e2 = st.columns([1.1, 1])

with e1:
    st.markdown("<div class='section-block'>", unsafe_allow_html=True)
    fig_imp, ax_imp = plt.subplots(figsize=(6, 4))
    ax_imp.barh(impact_df["Feature"], impact_df["Impact"])
    ax_imp.invert_yaxis()
    ax_imp.set_title("Top Feature Impact")
    ax_imp.set_xlabel("Relative Impact")
    st.pyplot(fig_imp)
    st.markdown("</div>", unsafe_allow_html=True)

with e2:
    st.markdown("<div class='section-block'>", unsafe_allow_html=True)
    st.markdown("### Explanation")
    st.write("""
This section shows the most unusual features compared to the dataset average.
It helps explain why a transaction may appear suspicious, regardless of the selected model.
""")
    for _, row in impact_df.head(5).iterrows():
        st.markdown(f"<span class='info-chip'>{row['Feature']} • {row['Impact']:.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# BATCH SCREENING
# ---------------------------------------------------
st.markdown("<div class='section-heading'>Batch Transaction Screening</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>Upload a CSV and run fraud scoring for multiple rows using the selected model.</div>", unsafe_allow_html=True)

template_df = get_template_df()
template_bytes = template_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download CSV Template",
    data=template_bytes,
    file_name="fraudguard_batch_template.csv",
    mime="text/csv"
)

st.markdown("<div class='section-block'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])

if uploaded_file is not None:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        st.write("### Uploaded File Preview")
        st.dataframe(uploaded_df.head(), use_container_width=True)

        batch_df, actual_labels, missing_cols, extra_cols = prepare_batch_dataframe(uploaded_df)

        b1, b2 = st.columns(2)
        with b1:
            if missing_cols:
                st.warning(f"Missing columns filled with 0: {missing_cols}")
            else:
                st.success("No required columns missing.")

        with b2:
            if extra_cols:
                st.info(f"Extra columns ignored: {extra_cols}")
            else:
                st.success("No extra columns detected.")

        if st.button("📤 Run Batch Screening"):
            payload = {
                "model": model_choice,
                "records": batch_df.to_dict(orient="records")
            }

            response = requests.post(f"{API_URL}/predict_batch", json=payload, timeout=60)
            result = response.json()

            if response.status_code != 200:
                st.error(result.get("error", "Batch prediction failed"))
            else:
                batch_results = pd.DataFrame(result["results"])

                final_df = batch_df.copy()
                if not batch_results.empty:
                    final_df["Model_Used"] = batch_results["model_used"]
                    final_df["Predicted_Class"] = batch_results["fraud_prediction"].map({0: "Legitimate", 1: "Fraud"})
                    final_df["Fraud_Probability"] = batch_results["fraud_probability"]
                    final_df["Risk_Level"] = batch_results["risk_level"]

                if actual_labels is not None:
                    final_df["Actual_Label"] = actual_labels.map({0: "Legitimate", 1: "Fraud"})

                st.session_state.batch_results_df = final_df

                if result.get("row_errors"):
                    st.warning(f"Some rows failed: {result['row_errors']}")

        if st.session_state.batch_results_df is not None:
            st.info(f"Batch prediction executed using model: {model_choice}")

            st.write("### Batch Results")
            st.dataframe(st.session_state.batch_results_df, use_container_width=True, height=350)

            csv_bytes = st.session_state.batch_results_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Results CSV",
                data=csv_bytes,
                file_name="fraudguard_batch_results.csv",
                mime="text/csv"
            )

            render_batch_analysis(st.session_state.batch_results_df)

    except Exception as e:
        st.error(f"CSV processing error: {e}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# HISTORY
# ---------------------------------------------------
st.markdown("<div class='section-heading'>Prediction History</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>Recent predictions generated in the current session.</div>", unsafe_allow_html=True)

if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, height=250)
else:
    st.info("No predictions yet.")

st.markdown("---")

# # ---------------------------------------------------
# # HISTORY
# # ---------------------------------------------------
# st.markdown("<div class='section-heading'>Prediction History</div>", unsafe_allow_html=True)
# st.markdown("<div class='section-note'>Recent predictions generated in the current session.</div>", unsafe_allow_html=True)

# if st.session_state.history:
#     st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, height=250)
# else:
#     st.info("No predictions yet.")

# st.markdown("---")

# ---------------------------------------------------
# REPORTS
# ---------------------------------------------------
st.markdown("<div class='section-heading'>Model Reports</div>", unsafe_allow_html=True)
st.markdown("<div class='section-note'>Saved visual artifacts from model training and evaluation.</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Feature Importance",
    "Confusion Matrix",
    "ROC Curve",
    "PR Curve",
    "SHAP Summary"
])

report_map = {
    "Feature Importance": "report/feature_importance.png",
    "Confusion Matrix": "report/confusion_matrix.png",
    "ROC Curve": "report/roc_curve.png",
    "PR Curve": "report/pr_curve.png",
    "SHAP Summary": "report/shap_summary.png"
}

with tab1:
    path = report_map["Feature Importance"]
    if os.path.exists(path):
        st.image(path, width=900)
    else:
        st.warning(f"{path} not found.")

with tab2:
    path = report_map["Confusion Matrix"]
    if os.path.exists(path):
        st.image(path, width=900)
    else:
        st.warning(f"{path} not found.")

with tab3:
    path = report_map["ROC Curve"]
    if os.path.exists(path):
        st.image(path, width=900)
    else:
        st.warning(f"{path} not found.")

with tab4:
    path = report_map["PR Curve"]
    if os.path.exists(path):
        st.image(path, width=900)
    else:
        st.warning(f"{path} not found.")

with tab5:
    path = report_map["SHAP Summary"]
    if os.path.exists(path):
        st.image(path, width=900)
    else:
        st.warning(f"{path} not found.")