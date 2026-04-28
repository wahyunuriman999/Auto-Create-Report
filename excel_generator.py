import pandas as pd
import io

def generate_premium_excel(pivot_data: dict) -> bytes:
    """
    Generates a beautifully formatted Excel file with a native Excel chart.
    Returns bytes of the Excel file.
    """
    if not pivot_data or "data" not in pivot_data:
        return b""

    # Convert pivot_data back to DataFrame
    df = pd.DataFrame(pivot_data["data"])
    cat_col = pivot_data["index"]
    num_col = pivot_data["values"]

    output = io.BytesIO()
    
    # Use xlsxwriter as the engine for premium formatting and charts
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook  = writer.book
        
        # 1. Create a "Dashboard" Sheet
        dash_sheet = workbook.add_worksheet("Dashboard")
        dash_sheet.hide_gridlines(2) # Hide gridlines for a clean look
        
        # Formats
        title_format = workbook.add_format({'bold': True, 'font_size': 20, 'font_color': '#ffffff', 'bg_color': '#1f2937', 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'font_color': '#ffffff', 'bg_color': '#3b82f6', 'border': 1})
        cell_format = workbook.add_format({'border': 1})
        num_format = workbook.add_format({'border': 1, 'num_format': '#,##0'})
        
        # Set column widths
        dash_sheet.set_column('B:B', 25)
        dash_sheet.set_column('C:C', 15)
        
        # Title
        dash_sheet.merge_range('B2:H3', 'NEXUS DATA INTELLIGENCE - OFFLINE DASHBOARD', title_format)
        
        # 2. Write Data to Sheet (starting from B5)
        dash_sheet.write('B5', cat_col, header_format)
        dash_sheet.write('C5', num_col, header_format)
        
        row = 5
        for index, record in df.iterrows():
            dash_sheet.write(row, 1, record[cat_col], cell_format)
            dash_sheet.write(row, 2, record[num_col], num_format)
            row += 1
            
        # 3. Create a Native Excel Chart
        chart = workbook.add_chart({'type': 'column'})
        
        # Configure the chart series using the data written above
        max_row = row
        chart.add_series({
            'name':       ['Dashboard', 4, 2],
            'categories': ['Dashboard', 5, 1, max_row - 1, 1],
            'values':     ['Dashboard', 5, 2, max_row - 1, 2],
            'fill':       {'color': '#3b82f6'},
            'border':     {'color': '#2563eb'}
        })
        
        # Chart layout
        chart.set_title({'name': f'{num_col} by {cat_col}'})
        chart.set_x_axis({'name': cat_col, 'major_gridlines': {'visible': False}})
        chart.set_y_axis({'name': num_col, 'major_gridlines': {'visible': True, 'line': {'color': '#e2e8f0'}}})
        chart.set_legend({'position': 'none'})
        chart.set_style(10)
        chart.set_size({'width': 700, 'height': 400})
        
        # Insert the chart into the worksheet
        dash_sheet.insert_chart('E5', chart)

    output.seek(0)
    return output.read()
