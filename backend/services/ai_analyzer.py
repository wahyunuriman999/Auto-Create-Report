import os
import json

def generate_report(data_summary: dict, user_notes: str) -> str:
    """
    Generates an analytical report based on the data summary and user notes.
    Uses OpenAI API if OPENAI_API_KEY is set in environment, otherwise falls back to a mock report.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # Compress the summary to save tokens
    context = json.dumps({
        "rows": data_summary["total_rows"],
        "columns": data_summary["columns"],
        "stats": data_summary["basic_stats"]
    })[:1000] # truncate if too long

    if not api_key:
        # Fallback Mock Report
        notes_section = f"\n\n**Additional Insights based on your notes:**\n\"{user_notes}\"" if user_notes else ""
        return f"""### Automated AI Data Report (Mock)

**Notice:** No API Key was detected in the environment (`OPENAI_API_KEY`). This is a simulated report. To enable true dynamic AI analysis, please configure your API key.

#### Overview
The dataset contains **{data_summary['total_rows']} rows** and **{len(data_summary['columns'])} columns**. 

#### Data Structure
* **Numerical Metrics:** {', '.join(data_summary['numerical_columns']) if data_summary['numerical_columns'] else 'None'}
* **Categorical Dimensions:** {', '.join(data_summary['categorical_columns']) if data_summary['categorical_columns'] else 'None'}

#### Initial Findings
Based on the structure, the data appears to track metrics across different categories. A bar chart has been automatically generated to visualize the top categorical distributions against the primary numerical metric.{notes_section}
"""

    # If API key exists, call OpenAI
    import openai
    openai.api_key = api_key

    prompt = f"""
    You are an expert data analyst. I am providing you with a statistical summary of a dataset.
    Please write a professional, concise executive summary report (in Markdown format).
    
    Data Summary (JSON): {context}
    
    User Additional Notes/Instructions: {user_notes or 'Provide a general overview.'}
    
    Ensure the tone is professional, insightful, and formatted with markdown headers and bullet points.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an elite data scientist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"### Error Generating Report\nAn error occurred while contacting the AI provider: {str(e)}"
