import pandas as pd
import io
import requests

def process_file_data(file_bytes: bytes, filename: str) -> dict:
    """Processes uploaded file bytes into a Pandas DataFrame and extracts insights."""
    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
    elif filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        raise ValueError("Unsupported file format. Please upload CSV or Excel.")
    
    return _analyze_dataframe(df)

def process_url_data(url: str) -> dict:
    """Fetches data from a URL (e.g., Google Sheets public link) and processes it."""
    # Convert standard Google Sheets URL to CSV export URL
    if "docs.google.com/spreadsheets" in url:
        if "/edit" in url:
            url = url.split("/edit")[0] + "/export?format=csv"
        elif "/export" not in url:
            url = url + "/export?format=csv"

    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data from URL. Status code: {response.status_code}")
    
    df = pd.read_csv(io.StringIO(response.text))
    return _analyze_dataframe(df)

def _analyze_dataframe(df: pd.DataFrame) -> dict:
    """Core logic to generate summary, pivot, and chart data from a DataFrame."""
    # 1. Clean Data
    df = df.dropna(how="all", axis=1) # Drop entirely empty columns
    
    # 2. Profile Columns
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    # 3. Generate Summary Profile (for AI and General Info)
    summary = {
        "total_rows": len(df),
        "columns": df.columns.tolist(),
        "numerical_columns": num_cols,
        "categorical_columns": cat_cols,
        "sample_data": df.head(5).fillna("").to_dict(orient="records"),
        "basic_stats": df.describe().fillna(0).to_dict() if num_cols else {}
    }
    
    # 4. Generate Pivot Data
    # For MVP, we automatically pick the first categorical and first numerical to pivot
    pivot_data = {}
    chart_data = {"labels": [], "datasets": []}
    
    if cat_cols and num_cols:
        main_cat = cat_cols[0]
        main_num = num_cols[0]
        
        # Group by the first categorical column, sum the first numerical column
        pivot_df = df.groupby(main_cat)[main_num].sum().reset_index()
        pivot_df = pivot_df.sort_values(by=main_num, ascending=False).head(15) # Top 15 for visualization
        
        pivot_data = {
            "index": main_cat,
            "values": main_num,
            "data": pivot_df.to_dict(orient="records")
        }
        
        # Format for Recharts (Frontend)
        chart_data = {
            "type": "bar",
            "xAxis": main_cat,
            "yAxis": main_num,
            "data": pivot_df.to_dict(orient="records")
        }

    return {
        "summary": summary,
        "pivot_data": pivot_data,
        "chart_data": chart_data,
        "df": df
    }
