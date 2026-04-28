# 📊 Nexus Data Intelligence: Auto-Create Report & Dashboard

**Nexus Data Intelligence** is an elite, autonomous data processing tool designed to instantly transform raw tabular data (Excel, CSV, Google Sheets) into interactive dashboards, pivot tables, and AI-driven analytical reports. 

Built with a decoupled architecture featuring a high-performance **FastAPI/Pandas** backend and a premium **Vanilla JS/CSS Glassmorphism** frontend.

![Dashboard UI Preview](https://via.placeholder.com/1200x600.png?text=Nexus+Data+Intelligence+Dashboard) *(Note: Replace this image with a real screenshot of your dashboard)*

## ✨ Key Features

*   **⚡ Instant Data Ingestion:** Drag-and-drop support for `.csv`, `.xls`, `.xlsx` (up to 500MB) or direct extraction from public Google Sheets URLs.
*   **📈 Interactive Web Dashboards:** Real-time data visualization using `Chart.js` with built-in UI Slicers for dynamic filtering.
*   **🤖 AI-Powered Executive Reports:** Integrated with OpenAI/Gemini to automatically generate professional markdown reports summarizing your data schema and trends based on your custom notes.
*   **💽 Premium Offline Export:** 
    *   Download your currently filtered dashboard as a high-res PNG.
    *   Generate a deeply formatted, native `.xlsx` offline dashboard containing your raw data and **Native Excel Charts** using `xlsxwriter`.
*   **💎 Elite UI/UX:** Dark mode, glassmorphism panels, and smooth micro-animations built strictly with Vanilla CSS (No heavy frameworks).

## 🏗️ Architecture Stack

*   **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript, Chart.js.
*   **Backend:** Python, FastAPI, Pandas (Data processing), XlsxWriter (Premium Excel generation), OpenAI API.

## 🚀 Getting Started

### Prerequisites
*   [Python 3.8+](https://www.python.org/downloads/)
*   (Optional) OpenAI API Key for AI Narrative Reports.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wahyunuriman999/Auto-Create-Report.git
   cd Auto-Create-Report/backend
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your AI API Key (Optional):**
   *   If you don't set this, the app will gracefully fall back to generating simulated (mock) AI reports.
   *   **Windows:** `set OPENAI_API_KEY=your-api-key-here`
   *   **Mac/Linux:** `export OPENAI_API_KEY=your-api-key-here`

### Running the Application

1. **Start the Backend Server:**
   ```bash
   uvicorn main:app --reload
   ```
   *The API will start on `http://localhost:8000`*

2. **Open the Frontend:**
   *   Since the frontend is built with pure HTML/JS, no Node.js installation is required!
   *   Simply navigate to the `frontend/` folder in your File Explorer and **double-click `index.html`** to open it in your browser.

## 🛠️ Usage Workflow
1. Upload your data file or paste a Google Sheets link.
2. Select the outputs you want (Dashboard, Pivot, AI Report).
3. (Optional) Add specific instructions for the AI in the Notes section.
4. Click **Generate Intelligence**.
5. Use the **Interactive Web Slicers** to filter your data.
6. Click **Download Dashboard (Excel)** to get a native Excel file with charts!

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
*Built with professional engineering standards focusing on Truth Over Impression, Root-Cause Thinking, and Robust Architecture.*
