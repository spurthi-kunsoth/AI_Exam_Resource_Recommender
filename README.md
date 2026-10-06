# 🎯 AI-Based Competitive Exam Resource Recommendation System

An AI-powered web application that recommends suitable study resources for competitive exam preparation based on the user's **exam, subject, preparation level, and resource type**.

The system uses **TF-IDF Vectorization** and **Cosine Similarity** to rank resources according to the user's selected requirements.

---

## 📌 Project Overview

Preparing for competitive examinations can be difficult because students have access to a large number of books, practice materials, previous-year papers, and mock tests.

This project provides a simple recommendation system that helps students find relevant study resources based on their preparation requirements.

The user selects:

- 🎯 Competitive Exam
- 📚 Subject
- 📊 Preparation Level
- 📖 Resource Type

The system then analyzes the available resources and displays the most relevant recommendations.

---

## ✨ Features

- 🎯 Supports multiple competitive examinations
- 📚 Subject-wise resource recommendations
- 📖 Filter resources by type
- 📊 Beginner, Intermediate, and Advanced levels
- 🤖 AI-based recommendation using TF-IDF
- 🔍 Cosine Similarity-based ranking
- ⭐ AI Match Score for each recommendation
- 💡 Explanation of why a resource is recommended
- 📋 Clean and simple Streamlit interface
- 📂 CSV-based resource dataset

---

## 📝 Supported Examinations

The current dataset includes resources for:

- SSC CGL
- SBI PO
- IBPS PO
- UPSC
- NDA
- GATE

---

## 📚 Resource Types

The system provides different types of preparation resources:

- 📘 Books
- ✏️ Practice Sets
- 📄 Previous Year Papers
- 📝 Mock Tests

---

## 🧠 Recommendation Method

The recommendation system uses **Natural Language Processing (NLP)** techniques.

### 1. TF-IDF Vectorization

TF-IDF (Term Frequency-Inverse Document Frequency) converts the resource information into numerical vectors.

The system considers information such as:

- Resource title
- Exam
- Subject
- Resource type
- Preparation level
- Description

### 2. Cosine Similarity

Cosine Similarity measures how closely the user's selected requirements match each available resource.

Resources with higher similarity are ranked higher.

### 3. Preference-Based Scoring

The system also considers:

- Selected preparation level
- Subject relevance
- Resource type
- Title relevance
- Description relevance

The final score is used to rank the recommendations.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Streamlit | Web application interface |
| Pandas | Dataset handling |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF and Cosine Similarity |
| Requests | HTTP/API requests |
| Python-dotenv | Environment variable management |
| Flask | Backend/API support |

---

## 📂 Project Structure

```text
AI_Exam_Resource_Recommender/
│
├── app.py
├── recommender.py
├── resources.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── venv/