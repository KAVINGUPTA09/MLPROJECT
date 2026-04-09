# 💳 FraudGuard AI – Credit Card Fraud Detection System

## 📌 Overview
FraudGuard AI is an end-to-end machine learning system designed to detect fraudulent credit card transactions in real-time and batch mode.

The system uses a trained classification model to analyze transaction data and predict whether a transaction is fraudulent or legitimate.

---

## 🎯 Objectives
- Detect fraudulent transactions with high accuracy
- Handle imbalanced dataset effectively
- Provide real-time and batch prediction
- Generate interpretable results with probability and risk level

---

## ⚙️ Tech Stack

### 🤖 Machine Learning
- XGBoost Classifier
- SMOTE (for imbalance handling)
- Scikit-learn
- Pandas, NumPy

### ⚙️ Backend
- Flask (REST API)
- Joblib (model loading)

### 🎨 Frontend
- Streamlit Dashboard
- Custom CSS UI

### 📊 Visualization & Reporting
- Matplotlib
- SHAP (Explainability)
- ReportLab (PDF generation)

---

## 📊 Dataset

- Source: Credit Card Fraud Dataset (Kaggle)
- Rows: ~284,000
- Fraud Cases: ~492
- Features:
  - Time
  - Amount
  - V1–V28 (PCA transformed features)
  - Class (0 = Legitimate, 1 = Fraud)

---

## 🧠 How the System Works

### Step 1: Data Input
Transaction data is provided via:
- Dashboard (single input)
- CSV upload (batch input)

### Step 2: Preprocessing
- Missing values handled
- Numeric conversion
- Scaling applied (Time, Amount)
- Feature engineering applied

### Step 3: Model Prediction
- XGBoost model predicts fraud probability
- Threshold applied to classify fraud

### Step 4: Output
- Fraud Prediction (0 / 1)
- Fraud Probability
- Risk Level (Low / Medium / High)

---

## 🔍 Features

### ✅ Single Transaction Prediction
- Load random transaction
- Predict fraud in real-time

### ✅ Batch Screening
- Upload CSV file
- Analyze multiple transactions at once

### ✅ PDF Report
- Download prediction report

### ✅ Visualization
- Fraud probability gauge
- Dataset analytics

---

## 📂 Project Structure
