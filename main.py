from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import uvicorn
from services.data_processor import process_file_data, process_url_data
from services.ai_analyzer import generate_report
from services.excel_generator import generate_premium_excel
from fastapi.responses import Response

app = FastAPI(title="Auto Data Dashboard API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/process")
async def process_data(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    options: str = Form(...), # JSON string of selected options {"dashboard":true,"pivot":true,"report":true}
    notes: Optional[str] = Form(None)
):
    try:
        opt_dict = json.loads(options)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid options format. Must be JSON.")

    if not file and not url:
        raise HTTPException(status_code=400, detail="Must provide either a file or a URL.")

    # 1. Process Data
    try:
        if file:
            # We process the uploaded file directly in memory for simplicity in this MVP.
            # For 500MB, we'd ideally save to disk and stream, but pandas can handle it if RAM is sufficient.
            contents = await file.read()
            data_result = process_file_data(contents, file.filename)
        elif url:
            data_result = process_url_data(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

    # 2. Extract configuration
    wants_dashboard = opt_dict.get("dashboard", False)
    wants_pivot = opt_dict.get("pivot", False)
    wants_report = opt_dict.get("report", False)

    response = {
        "status": "success",
        "data_summary": data_result["summary"],
    }

    # 3. Generate requested outputs
    if wants_pivot:
        response["pivot"] = data_result["pivot_data"]
    
    if wants_dashboard:
        response["dashboard"] = data_result["chart_data"]

    if wants_report:
        report_text = generate_report(data_result["summary"], notes)
        response["report"] = report_text

    return response

@app.post("/api/download_excel")
async def download_excel(pivot_data: str = Form(...)):
    try:
        data = json.loads(pivot_data)
        excel_bytes = generate_premium_excel(data)
        
        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=Dashboard_Offline.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Excel: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
