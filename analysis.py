"""
Pesa Pulse Customer Data API Analysis
Author: Junior Data Analyst
Description:
    Retrieves customer directory data from JSONPlaceholder API,
    explores nested data structures, flattens customer attributes,
    analyzes geographic and email domain distributions with pure Python and pandas,
    exports CSV reports, and generates presentation-ready visualizations.
"""

import os
from typing import Any, Dict, List, Set
import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_customers(url: str, timeout: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve customer data from the given API endpoint with timeout handling.
    
    Args:
        url: The API endpoint URL.
        timeout: Request timeout in seconds.
        
    Returns:
        A list of customer dictionaries, or an empty list if a network error occurs.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching customer data from {url}: {e}")
        return []


def explore(record: Any, indent: int = 0) -> None:
    """
    Recursively inspect and print keys and Python types of a nested record.
    
    Args:
        record: The dictionary, list, or primitive data item to explore.
        indent: Current indentation depth in spaces.
    """
    spacing = " " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{spacing}{key}: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 4)
    elif isinstance(record, list):
        for index, item in enumerate(record):
            print(f"{spacing}[{index}]: {type(item).__name__}")
            if isinstance(item, (dict, list)):
                explore(item, indent + 4)


def extract_attributes(customers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract and flatten nested customer attributes into a clean list of dictionaries.
    
    Fields extracted:
        - customer_id: int
        - name: str
        - username: str
        - email: str
        - email_domain: str (TLD extracted from email)
        - phone: str
        - city: str
        - zipcode: str
        - latitude: float
        - longitude: float
        - company: str
        - website: str
    """
    flattened = []
    for c in customers:
        address = c.get("address", {})
        geo = address.get("geo", {})
        company = c.get("company", {})
        email = c.get("email", "")
        # Extract top-level domain (TLD) as specified in expected output
        tld = email.split(".")[-1] if "." in email else ""

        row = {
            "customer_id": int(c.get("id")),
            "name": c.get("name", ""),
            "username": c.get("username", ""),
            "email": email,
            "email_domain": tld,
            "phone": c.get("phone", ""),
            "city": address.get("city", ""),
            "zipcode": address.get("zipcode", ""),
            "latitude": float(geo.get("lat", 0.0)),
            "longitude": float(geo.get("lng", 0.0)),
            "company": company.get("name", ""),
            "website": c.get("website", ""),
        }
        flattened.append(row)
    return flattened


def unique_cities(customers: List[Dict[str, Any]]) -> Set[str]:
    """
    Extract the set of unique customer cities using a set comprehension.
    Works with both flattened records and raw customer dictionaries.
    """
    return {
        c.get("city") or (c.get("address", {}).get("city") if isinstance(c.get("address"), dict) else "")
        for c in customers
    }


def city_counts(customers: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Count customers by city using standard loops and dictionaries (without Counter or pandas).
    Returns the counts sorted by count descending, then alphabetically by city name.
    """
    counts: Dict[str, int] = {}
    for c in customers:
        city = c.get("city") or (c.get("address", {}).get("city") if isinstance(c.get("address"), dict) else "")
        if city:
            counts[city] = counts.get(city, 0) + 1
    # Sort descending by count, then ascending alphabetically by city
    sorted_counts = dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
    return sorted_counts


def email_domain_counts(customers: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Count customers by email domain (TLD) using a dictionary comprehension.
    Returns the counts sorted by count descending, then alphabetically by domain.
    """
    domains = [
        c.get("email_domain") if "email_domain" in c else c.get("email", "").split(".")[-1]
        for c in customers
    ]
    # Pure dict comprehension for frequency aggregation
    counts = {domain: domains.count(domain) for domain in domains if domain}
    # Sort descending by count, then ascending alphabetically by domain
    sorted_counts = dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
    return sorted_counts


def to_dataframe(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert flattened rows into a pandas DataFrame and print shape and dtypes.
    """
    df = pd.DataFrame(rows)
    return df


def export_results(
    df: pd.DataFrame,
    city_counts_dict: Dict[str, int],
    output_dir: str = "output"
) -> None:
    """
    Export cleaned customer records and city counts to CSV without index.
    
    Files created:
        - {output_dir}/customers.csv
        - {output_dir}/city_counts.csv
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Export customers.csv
    customers_path = os.path.join(output_dir, "customers.csv")
    columns_order = [
        "customer_id", "name", "username", "email", "email_domain",
        "phone", "city", "zipcode", "latitude", "longitude",
        "company", "website"
    ]
    df[columns_order].to_csv(customers_path, index=False)
    print(f"Exported customer records to: {customers_path}")

    # 2. Export city_counts.csv (sorted descending by customer_count, then city)
    city_counts_path = os.path.join(output_dir, "city_counts.csv")
    city_df = pd.DataFrame([
        {"city": city, "customer_count": count}
        for city, count in city_counts_dict.items()
    ])
    # Ensure sorting matches requirements: customer_count desc, city asc
    city_df = city_df.sort_values(by=["customer_count", "city"], ascending=[False, True])
    city_df.to_csv(city_counts_path, index=False)
    print(f"Exported city counts to: {city_counts_path}")


def plot_distribution(
    counts: Dict[str, int],
    path: str,
    title: str = "Customer Distribution by City",
    xlabel: str = "City",
    ylabel: str = "Customer Count"
) -> None:
    """
    Save a presentation-ready bar chart of customer distribution with readable labels.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    categories = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color="#1f77b4", edgecolor="#0e4b75", width=0.6)

    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel(xlabel, fontsize=12, labelpad=10)
    plt.ylabel(ylabel, fontsize=12, labelpad=10)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(range(0, max(values) + 2, 1), fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Annotate integer count on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"{int(height)}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Chart saved to: {path}")


def main() -> None:
    print("=" * 60)
    print("Pesa Pulse - Customer Directory API Analysis")
    print("=" * 60)

    # Task 1: Retrieve customer data with Requests
    url = "https://jsonplaceholder.typicode.com/users"
    print(f"\n[1] Fetching customer data from: {url} ...")
    raw_customers = get_customers(url)
    if not raw_customers:
        print("Failed to retrieve customers. Terminating analysis.")
        return
    print(f"Successfully retrieved {len(raw_customers)} customer records.")

    # Task 2: Explore nested dictionaries and lists
    print("\n[2] Exploring nested structure of customer record #1:")
    print("-" * 50)
    explore(raw_customers[0])
    print("-" * 50)

    # Task 3: Extract customer attributes into flat dictionaries
    print("\n[3] Extracting flattened attributes...")
    flattened_customers = extract_attributes(raw_customers)
    print(f"Extracted {len(flattened_customers)} flat records with {len(flattened_customers[0])} attributes each.")

    # Task 4: Use sets to find unique cities
    print("\n[4] Analyzing unique cities with sets...")
    cities = unique_cities(flattened_customers)
    num_customers = len(flattened_customers)
    num_cities = len(cities)
    print(f"Total customers: {num_customers}")
    print(f"Unique cities  : {num_cities}")
    print(f"Marketing Insight: Because there are {num_cities} unique cities across {num_customers} customers (a 1:1 ratio), customers are completely dispersed geographically with zero market concentration, requiring broad digital campaigns rather than localized city-specific activations.")

    # Task 5: Count customers by city and email domain
    print("\n[5] Calculating frequency distributions...")
    c_counts = city_counts(flattened_customers)
    d_counts = email_domain_counts(flattened_customers)
    
    print("\nCity Counts (sorted descending):")
    for city, count in c_counts.items():
        print(f"  {city:20s}: {count}")

    print("\nEmail Domain Counts (sorted descending):")
    for domain, count in d_counts.items():
        print(f"  .{domain:19s}: {count}")

    # Task 6: Convert data into a DataFrame and verify counts
    print("\n[6] Moving cleaned data into pandas DataFrame...")
    df = to_dataframe(flattened_customers)
    print(f"DataFrame Shape: {df.shape}")
    print("\nDataFrame dtypes:")
    print(df.dtypes)
    
    # Confirm pandas matches handwritten counts
    pandas_city_counts = df["city"].value_counts().to_dict()
    assert pandas_city_counts == c_counts, "Pandas city counts do not match hand-written counts!"
    print("\nVerification Passed: pandas value_counts() matches hand-written counts exactly.")

    # Task 7: Export results to CSV
    print("\n[7] Exporting CSV reports...")
    output_dir = "output"
    export_results(df, c_counts, output_dir=output_dir)

    # Task 8: Visualize customer distribution
    print("\n[8] Visualizing distributions...")
    city_chart_path = os.path.join(output_dir, "customer_distribution.png")
    plot_distribution(
        c_counts,
        city_chart_path,
        title="Customer Distribution by City (Pesa Pulse)",
        xlabel="City",
        ylabel="Number of Customers"
    )

    domain_chart_path = os.path.join(output_dir, "email_domain_distribution.png")
    plot_distribution(
        d_counts,
        domain_chart_path,
        title="Customer Distribution by Email Domain / TLD (Pesa Pulse)",
        xlabel="Email Domain (TLD)",
        ylabel="Number of Customers"
    )

    # Console findings block exactly as specified in expected_output.md
    most_common_city = list(c_counts.keys())[0]
    most_common_count = list(c_counts.values())[0]

    print("\n" + "=" * 60)
    print("## Console findings")
    print(f"Customers retrieved : {len(flattened_customers)}")
    print(f"Unique cities       : {len(cities)}")
    print(f"Most common city    : {most_common_city} ({most_common_count})")
    print(f"Email domains       : {d_counts}")
    print(f"Chart saved to      : {city_chart_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
