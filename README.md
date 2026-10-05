# 🏦 Customer Segmentation & Churn Pattern Analytics in European Banking

An interactive **Streamlit** dashboard and research project that explores **customer churn** and **customer segmentation** in a European retail banking dataset of **10,000 customers**. The project turns raw customer records into interpretable segments (age, geography, credit score, tenure, balance, engagement, and customer value) and shows how churn varies across them.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)

> **Data Science Internship Research Project**: includes the full research paper, *Customer Segmentation and Churn Pattern Analytics in European Banking*.

---

## 📌 Table of Contents

- [🏦 Customer Segmentation \& Churn Pattern Analytics in European Banking](#-customer-segmentation--churn-pattern-analytics-in-european-banking)
  - [📌 Table of Contents](#-table-of-contents)
  - [📖 Project Overview](#-project-overview)
  - [🎯 Research Question \& Objectives](#-research-question--objectives)
  - [🔍 Key Findings](#-key-findings)
  - [✨ Dashboard Features](#-dashboard-features)
  - [🧪 Methodology](#-methodology)
  - [🧩 Feature Engineering \& Segments](#-feature-engineering--segments)
  - [🛠 Tech Stack](#-tech-stack)
  - [📂 Project Structure](#-project-structure)
  - [🗃 Dataset](#-dataset)
  - [⚙️ Installation \& Setup](#️-installation--setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. (Optional) Create a virtual environment](#2-optional-create-a-virtual-environment)
    - [3. Install dependencies](#3-install-dependencies)
    - [4. Add the dataset](#4-add-the-dataset)
  - [▶️ Usage](#️-usage)
  - [⚠️ Limitations](#️-limitations)
  - [🚀 Future Work](#-future-work)
  - [🖼 Screenshots](#-screenshots)
  - [👩‍💻 Author](#-author)

---

## 📖 Project Overview

Customer retention is a central concern in retail banking: losing existing customers means losing established relationships and creates the cost of acquiring replacements. This project takes a deliberately **descriptive and diagnostic** approach. It does not claim a production prediction model. Instead it:

- Cleans and validates the banking customer dataset
- Engineers **interpretable customer segments**
- Compares **churn rates** across demographic, geographic, financial, product, and engagement groups
- Identifies **high-value customers** with elevated churn exposure
- Delivers the results in an **interactive Streamlit dashboard** with filters, KPIs, and visualizations

---

## 🎯 Research Question & Objectives

**Research question:** How can customer-level banking data be transformed into interpretable segments that reveal differences in churn behavior and support targeted retention analysis?

**Objectives**

1. Validate and preprocess the European banking customer dataset.
2. Explore distributions and relationships between customer characteristics and churn.
3. Engineer interpretable demographic, financial, tenure, and engagement segments.
4. Compare churn rates across geographic, demographic, and behavioral groups.
5. Identify high-value customer segments with elevated churn exposure.
6. Build an interactive dashboard for segment-level exploration.
7. Translate observed patterns into practical retention recommendations while distinguishing **association from causation**.

---

## 🔍 Key Findings

| Metric | Value |
|--------|-------|
| Customers analysed | **10,000** |
| Churned / Retained | **2,037** / **7,963** |
| Overall churn rate | **20.37%** |
| Active customer rate | **51.51%** |
| Average account balance | **76,485.89** |
| High-value customers | **2,516** (churn rate **25.08%** vs **18.79%** for standard value) |

**Churn by segment**

| Dimension | Highlights |
|-----------|-----------|
| **Geography** | Germany **32.44%** (2,509 customers), Spain **16.67%** (2,477), France **16.15%** (5,014) |
| **Age group** | 46–60 highest at **51.12%**; under 30 lowest at **7.56%** |
| **Tenure** | Smaller differences: Long-term **21.30%**, Established lowest at **18.87%** |
| **Credit score** | Moderate variation; Poor band at **22.02%** |
| **Balance** | Low Balance **34.67%**; Zero Balance **13.82%** |
| **Products** | 3 products **82.71%**; 2 products **7.58%**; 4 products **100%** (very small group, interpret with caution) |
| **Engagement** | Inactive **26.85%** vs Active **14.27%** |
| **Geography × Age** | Germany's 46–60 group peaks at **67.3%** churn |

> ⚠️ These are **observed associations** in a single cross-sectional snapshot. They do not prove causation.

---

## ✨ Dashboard Features

- **Sidebar filters** for Geography, Gender, Age Group, Credit Score Band, Customer Value, and Engagement
- **Top KPI cards**: Total Customers, Churned Customers, Overall Churn Rate, Active Customer Rate, Average Balance
- **Retention vs churn** overview (pie and bar charts)
- **Segment-level churn analysis** charts:
  - Customers and churn rate by Geography
  - Churn rate by Age Group, Tenure Group, Credit Score Band, Balance Segment, Gender, and Number of Products
  - Churn rate for Active vs Inactive customers
- **High-Value Customer Explorer**: dedicated KPIs plus an interactive scatter plot (Balance vs Estimated Salary, sized by Credit Score)
- **Advanced analysis**:
  - Balance distribution: churned vs retained
  - Age vs Balance by churn status
  - Geography × Age Group churn heatmap
- **KPI summary table** that updates with the filters
- **Filtered customer records** viewer (toggle) and **CSV download** of the filtered dataset
- **Auto-generated business insights** that react to the selected filters
- **Cached data loading and preprocessing** for fast performance

---

## 🧪 Methodology

The workflow follows these stages:

```
Data Loading → Data Validation → Cleaning → Exploratory Analysis →
Feature Engineering → Customer Segmentation → Churn Analysis →
KPI Calculation → Interactive Visualization → Business Insights
```

**Data cleaning and pre-processing**

- Duplicate customer records are removed
- The `Surname` column is dropped (not a meaningful behavioral or financial variable); customer identifiers are treated as identifiers, not predictors
- Numeric fields are coerced to numeric types
- Rows with missing critical values are removed
- `Geography` and `Gender` are retained as categorical variables for grouped analysis

**Churn rate** is calculated as the share of customers with `Exited = 1` within each segment. Rates are used rather than raw counts because segment sizes differ.

---

## 🧩 Feature Engineering & Segments

| Engineered Feature | Categories | Purpose |
|--------------------|-----------|---------|
| `Age_Group` | <30, 30-45, 46-60, 60+ | Compare churn across age bands |
| `Credit_Score_Band` | Poor (≤579), Fair (580–669), Good (670–739), Very Good (740–799), Excellent (800+) | Compare financial-risk bands |
| `Tenure_Group` | New (0–2), Mid-term (3–5), Established (6–8), Long-term (9+) | Compare relationship duration |
| `Balance_Segment` | Zero, Low (≤50K), Medium (≤100K), High (≤150K), Very High (>150K) | Compare balance profiles |
| `Customer_Value` | High Value, Standard Value | Identify financially important customers |
| `Engagement_Status` | Active, Inactive | Compare customer activity |
| `Churn_Status` | Churned, Retained | Interpretable target label |

> **High Value definition:** a customer is *High Value* when both `Balance` and `EstimatedSalary` are at or above their dataset medians. This is a portfolio-segmentation rule, **not** a customer lifetime value model.

---

## 🛠 Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| Dashboard | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |

---

## 📂 Project Structure

```
Customer_Segmentation_Churn_Pattern_Analytics/
│
├── app.py                                          # Streamlit dashboard application
├── European_Bank.csv                               # Source dataset (10,000 customers)
├── Customer_Segmentation_Churn_Research_Paper.pdf  # Full research paper
├── requirements.txt                                # Python dependencies
├── README.md                                       # Project documentation
├── .gitignore

```


---

## 🗃 Dataset

`European_Bank.csv` contains **10,000 customer records and 14 original columns**:

| Column | Description |
|--------|-------------|
| `Year` | Year field |
| `CustomerId` | Customer identifier |
| `Surname` | Customer surname (dropped during preprocessing) |
| `CreditScore` | Customer credit score |
| `Geography` | Country (France, Germany, Spain) |
| `Gender` | Customer gender |
| `Age` | Customer age |
| `Tenure` | Years with the bank |
| `Balance` | Account balance |
| `NumOfProducts` | Number of banking products held |
| `HasCrCard` | Credit card ownership (1 = yes, 0 = no) |
| `IsActiveMember` | Active member flag (1 = active, 0 = inactive) |
| `EstimatedSalary` | Estimated salary |
| `Exited` | **Target:** 1 = churned, 0 = retained |

The app expects `European_Bank.csv` in the **same folder as `app.py`**. If it is missing, the dashboard shows an error and stops.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/BRoshini-15/<your-repo-name>.git
cd <your-repo-name>
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, create one with:

```
streamlit
pandas
numpy
plotly
```

### 4. Add the dataset

Place `European_Bank.csv` in the same directory as `app.py`.

---

## ▶️ Usage

```bash
streamlit run app.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`).

1. Use the **sidebar filters** to focus on specific customer groups.
2. Scroll through the KPIs, segment charts, high-value explorer, and heatmap.
3. Review the **Business Insights** panel, which updates with your selection.
4. Toggle **Show filtered customer records** and use **Download Filtered Dataset** to export the data as CSV.

---


## ⚠️ Limitations

- The analysis is **observational** and does not establish causal relationships.
- The data is a **single snapshot**, which limits analysis of churn timing and customer lifecycle.
- The *High Value* segment uses dataset medians, not a formal lifetime value model.
- Some segments (e.g. customers with four products) are small, so extreme rates should be read cautiously.
- No interaction logs, transaction sequences, complaints, marketing exposure, or time-varying features are included.
- The dashboard is for **descriptive and diagnostic analytics**, not production churn prediction.

---

## 🚀 Future Work

- Add time-dependent behavioral data
- Apply formal clustering (e.g. K-Means, DBSCAN)
- Build supervised churn prediction models with explainability
- Run controlled retention experiments
- Deploy on **Streamlit Community Cloud** and add a live demo link

---

## 🖼 Screenshots

> Add screenshots of your dashboard here.

```md
![Overview](screenshots/overview.png)
![Churn by Geography](screenshots/geography.png)
![Geography x Age Heatmap](screenshots/heatmap.png)
```

---

## 👩‍💻 Author

**Baikan Roshini**
B.Tech, Computer Science Engineering | Data Science Intern

🔗 GitHub: [github.com/BRoshini-15](https://github.com/BRoshini-15)

---

⭐ If you found this project useful, consider giving it a star!