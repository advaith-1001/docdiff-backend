# DocDiff: AI-Powered Document Comparison Tool

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

DocDiff is a modern web application that allows users to upload two documents (PDF, DOCX, or images), intelligently compare their textual and formatting differences, and receive a summary of the changes powered by a Large Language Model.

---

**[Live Demo](https://doc-diff-ten.vercel.app/)** | **[Frontend Repository](https://github.com/advaith-1001/DocDiff)**

---

## Key Features

* **Multi-Format Upload:** Accepts `.pdf`, `.docx`, and image files (`.png`, `.jpg`).
* **Textual Difference Highlighting:** Generates new PDF files with additions and deletions clearly highlighted.
* **Formatting Comparison:** Detects changes in document formatting like font size, style, and alignment (for DOCX and PDF).
* **AI-Powered Summary:** Uses the Gemini API to provide a concise, human-readable summary of all the key changes between the two documents.
* **Side-by-Side Viewer:** A clean, intuitive UI to view the highlighted documents and the list of changes simultaneously.

## Architecture Overview

The application follows a simple client-server architecture. The frontend, built with React, handles file uploads and renders the results. The backend, built with Python (FastAPI), performs all the heavy lifting.

```
+----------------+      +--------------------------------+      +----------------------+
|   React (UI)   |----->|      FastAPI Backend           |----->|   Google Gemini API  |
+----------------+      | (File Conversion, Diff, OCR)   |      +----------------------+
                        +--------------------------------+
```

1.  **Upload:** The user uploads two files to the React frontend.
2.  **Process:** The frontend sends the files to the `/api/compare` endpoint on the backend.
3.  **Analyze:** The backend:
    * Converts all files to a standard format.
    * Extracts text and formatting data.
    * Compares both text and formatting using `difflib` and custom parsers.
    * Generates highlighted versions of the PDFs.
    * Sends the textual differences to the Gemini API for summarization.
4.  **Display:** The backend returns a single JSON payload containing the AI summary, a list of differences, and the base64-encoded highlighted PDFs. The frontend then renders this information.

## Tech Stack

| Area      | Technology                                                                                             |
| :-------- | :----------------------------------------------------------------------------------------------------- |
| **Frontend** | `React.js`, `React Router`, `react-pdf`                                                                |
| **Backend** | `Python 3`, `FastAPI`, `Uvicorn`                                                                       |
| **AI / ML** | `Google Gemini API`                                                                                    |
| **File Proc.**| `python-docx`, `pdf2docx`, `PyMuPDF (fitz)`, `Pillow`                                                    |
| **OCR** | `pytesseract`                                                                                          |
| **Diffing** | `difflib`                                                                                              |                                                                                |

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Node.js and npm (for frontend)
* Python 3.9+ and pip (for backend)
* Tesseract OCR Engine
    * **macOS:** `brew install tesseract`
    * **Ubuntu:** `sudo apt-get install tesseract-ocr`
* A Google Gemini API Key

### Installation

1.  **Clone the backend repository (this one):**
    ```sh
    git clone [https://github.com/your-username/docdiff-backend.git](https://github.com/your-username/docdiff-backend.git)
    cd docdiff-backend
    ```

2.  **Set up the Python environment:**
    ```sh
    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** in the root of the backend directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

4.  **Clone and set up the frontend:**
    ```sh
    # In a new terminal window
    git clone [https://github.com/your-username/docdiff-frontend.git](https://github.com/your-username/docdiff-frontend.git)
    cd docdiff-frontend
    npm install
    ```

## Usage

1.  **Run the backend server:**
    ```sh
    # From the backend directory
    uvicorn main:app --reload
    ```
    The backend will be running on `http://127.0.0.1:8000`.

2.  **Run the frontend development server:**
    ```sh
    # From the frontend directory
    npm start
    ```
    The application will open in your browser at `http://localhost:3000`. You can now upload files and test the comparison.

## API Endpoints

### `POST /api/compare`

This is the primary endpoint for the application.

* **Request:** `multipart/form-data`
    * `file1`: The first document to compare.
    * `file2`: The second document to compare.
* **Response:** `application/json`
    ```json
    {
      "diff": [...],
      "highlighted_pdf1": "base64_string",
      "highlighted_pdf2": "base64_string",
      "formatting_diffs": [...],
      "ai_summary": "A text summary of changes."
    }
    ```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
