# Pesa Pulse - Partner Customer Directory API Analysis

A comprehensive exploratory data analysis (EDA) of customer records retrieved from a partner API for **Pesa Pulse**, a Nairobi fintech start-up. This project extracts nested customer data, analyzes geographic and email domain distributions using both core Python data structures and pandas, exports production-ready CSV tables, and produces clean visualizations for executive decision-making.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Nested Data Structure & Deepest Attribute Access](#nested-data-structure--deepest-attribute-access)
3. [Approach & Methodology](#approach--methodology)
4. [Key Findings & Marketing Insights](#key-findings--marketing-insights)
5. [Assumptions](#assumptions)
6. [Repository Structure](#repository-structure)
7. [Installation & How to Run](#installation--how-to-run)
8. [Deliverables & Outputs](#deliverables--outputs)

---

## Project Overview

Before launching regional campaigns in Kenya and neighboring markets, Pesa Pulse's marketing team required insights on:
- How many customer records exist.
- Where customers are located geographically.
- How the data is structured and what marketing angles are supported by the attributes.

This project delivers:
- Robust API consumption with network error and timeout handling.
- Recursive exploration of nested data hierarchies.
- Pure Python data manipulation (sets, dictionary counters, and dictionary comprehensions).
- Validation and tabular analysis with `pandas`.
- Output CSV exports (`customers.csv`, `city_counts.csv`).
- Visualizations (`customer_distribution.png`, `email_domain_distribution.png`).

---

## Nested Data Structure & Deepest Attribute Access

### Nested Attributes Identified
When inspecting the raw customer records from `https://jsonplaceholder.typicode.com/users`, two main top-level attributes contain nested objects:

1. **`address` (dict)**:
   - `street` (str)
   - `suite` (str)
   - `city` (str)
   - `zipcode` (str)
   - **`geo` (dict)**: Nested inside `address`, containing:
     - `lat` (str)
     - `lng` (str)

2. **`company` (dict)**:
   - `name` (str)
   - `catchPhrase` (str)
   - `bs` (str)

### Deepest Nested Attribute Access
The deepest attributes in the record hierarchy are the geographic coordinates **`lat`** (latitude) and **`lng`** (longitude), located at a depth of 3 levels:

```
Customer Record (dict) ──> address (dict) ──> geo (dict) ──> lat / lng (str)
```

To reach and convert them into floating-point numbers:
```python
latitude = float(record["address"]["geo"]["lat"])
longitude = float(record["address"]["geo"]["lng"])
```

---

## Approach & Methodology

1. **API Ingestion (`get_customers`)**:
   Uses `requests.get()` with an explicit `timeout=10` parameter and calls `response.raise_for_status()`. All network exceptions (`requests.exceptions.RequestException`) are caught cleanly to output human-readable messages rather than unhandled tracebacks.

2. **Recursive Data Exploration (`explore`)**:
   Implements a recursive walker that prints each key alongside its Python type (`type(value).__name__`), increasing indentation by 4 spaces per nesting level.

3. **Attribute Extraction & Flattening (`extract_attributes`)**:
   Transforms each nested customer record into a flat dictionary with standardized column names:
   `customer_id`, `name`, `username`, `email`, `email_domain`, `phone`, `city`, `zipcode`, `latitude`, `longitude`, `company`, `website`. Coordinates are converted to `float`, and top-level domains (`email_domain`) are extracted.

4. **Unique Value Isolation (`unique_cities`)**:
   Applies a set comprehension (`{c['city'] for c in customers}`) to isolate all distinct customer cities.

5. **Pure Python Aggregation (`city_counts`, `email_domain_counts`)**:
   - `city_counts()` uses standard `for` loops and dictionary accumulation (`counts.get(city, 0) + 1`) without relying on `collections.Counter` or `pandas`.
   - `email_domain_counts()` uses a clean dictionary comprehension (`{d: domains.count(d) for d in domains}`) to calculate domain frequencies.
   - Both results are sorted descending by frequency, then ascending alphabetically by name.

6. **Tabular Verification with pandas (`to_dataframe`)**:
   Converts flattened records into a DataFrame and asserts that `df['city'].value_counts()` matches the pure Python manual counts.

7. **Export Pipeline (`export_results`)**:
   Generates `output/customers.csv` and `output/city_counts.csv` without DataFrame index headers.

8. **Distribution Visualizations (`plot_distribution`)**:
   Generates two bar charts with data labels and readable rotated ticks:
   - `output/customer_distribution.png` (City distribution)
   - `output/email_domain_distribution.png` (Email domain distribution)

---

## Key Findings & Marketing Insights

1. **Complete Geographic Dispersion (Zero City Clustering)**:
   - There are **10 customers across 10 unique cities** (a 1:1 ratio).
   - *Marketing Implication:* Customer density is completely dispersed with no single city showing dominance. Running expensive localized physical campaigns (such as billboards or in-person pop-up events in a single town) would be ineffective at this stage. Pesa Pulse should prioritize broad digital ad targeting (e.g. Google Search, social media ads) across all covered regions.

2. **Strong B2B Presence via `.biz` Email Domains**:
   - In contrast to the uniform city distribution, email top-level domains show distinct clustering: **30% of customers (3 out of 10) use `.biz`**, with the remaining 7 split across `.ca`, `.info`, `.io`, `.me`, `.net`, `.org`, and `.tv`.
   - *Marketing Implication:* The prominence of `.biz` domains alongside company descriptors indicates that nearly a third of early partner accounts represent commercial or enterprise entities. Marketing should test B2B-oriented copy (e.g., merchant payment gateways, payroll solutions) rather than strictly consumer P2P messaging.

3. **Chart Utility Comparison**:
   - **City Distribution Chart (`customer_distribution.png`):** Every bar has an identical height of 1. While valuable as a proof of dispersion, it provides minimal variance for resource prioritization.
   - **Email Domain Distribution Chart (`email_domain_distribution.png`):** Shows distinct frequency variations (3 vs. 1). **The email domain chart is significantly more useful for marketing strategy** because it reveals customer profile segmentation (commercial B2B vs. personal/creative tech) that informs campaign messaging and product tiering.

---

## Assumptions

1. **API Data Stability:** The mock API endpoint (`https://jsonplaceholder.typicode.com/users`) provides valid JSON representing 10 customer records with standard keys (`address`, `geo`, `company`).
2. **Email Domain Definition:** Per `expected_output.md` specifying `<tld>` under `email_domain`, the domain is parsed as the top-level domain extension (e.g., `biz` from `Sincere@april.biz`).
3. **Missing Value Handling:** Safe `.get()` accessors and default empty strings / 0.0 values are used to ensure the pipeline will not crash if optional fields are omitted in future API updates.
4. **Coordinate Accuracy:** Coordinates provided as strings in `geo.lat` and `geo.lng` represent valid real numbers convertible to Python `float`.

---

## Repository Structure

```
day1-api-analysis/
├── analysis.py                     # Complete end-to-end Python pipeline
├── analysis.ipynb                  # Interactive Jupyter Notebook with documentation
├── output/
│   ├── customers.csv               # Cleaned & flattened customer dataset (10 records, 12 attributes)
│   ├── city_counts.csv             # Aggregated customer counts by city (sorted descending)
│   ├── customer_distribution.png   # Bar chart: Customers by city
│   └── email_domain_distribution.png # Bar chart: Customers by email domain / TLD
├── requirements.txt                # Project dependencies
└── README.md                       # Analysis documentation, findings, and instructions
```

---

## Installation & How to Run

### Prerequisites
- Python 3.9+ (tested on Python 3.14)
- Internet connection (to access the JSONPlaceholder API endpoint)

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd day1-api-analysis
```

### 2. Set Up a Virtual Environment
```bash
# On Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# On Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Python Script
```bash
python analysis.py
```

### 5. Alternatively, Run the Jupyter Notebook
```bash
jupyter notebook analysis.ipynb
```

---

## Deliverables & Outputs

### Console Output
Running `python analysis.py` prints the verification steps and outputs the console findings summary:
```
## Console findings
Customers retrieved : 10
Unique cities       : 10
Most common city    : Aliyaview (1)
Email domains       : {'biz': 3, 'ca': 1, 'info': 1, 'io': 1, 'me': 1, 'net': 1, 'org': 1, 'tv': 1}
Chart saved to      : output/customer_distribution.png
```

### Generated Files in `output/`
- **`customers.csv`**: Contains `customer_id`, `name`, `username`, `email`, `email_domain`, `phone`, `city`, `zipcode`, `latitude`, `longitude`, `company`, `website`.
- **`city_counts.csv`**: Contains `city`, `customer_count` sorted by count descending and city ascending.
- **`customer_distribution.png`**: High-resolution chart depicting the geographic distribution across all cities.
- **`email_domain_distribution.png`**: High-resolution chart showing domain clustering for marketing segmentation.
