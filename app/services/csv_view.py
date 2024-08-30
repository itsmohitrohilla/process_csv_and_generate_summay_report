import os
import pandas as pd
from fastapi.responses import HTMLResponse, JSONResponse

# Define the folder where the processed CSV files are located
PROCESSED_CSV_FOLDER = "data/processed_csv"  # Replace with your actual folder path

def generate_csv_html(processed_csv_to_view: str) -> HTMLResponse:
    """
    Reads a CSV file and converts it into an HTML table.
    Returns the HTML content.
    """
    # Construct the full path to the CSV file
    processed_csv_path_to_view = os.path.join(PROCESSED_CSV_FOLDER, processed_csv_to_view)
    
    # Check if the file exists
    if not os.path.isfile(processed_csv_path_to_view):
        return JSONResponse(
            status_code=404,
            content={"detail": "Processed CSV file not found."}
        )
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(processed_csv_path_to_view)
    
    # Convert the DataFrame to an HTML table
    html_table = df.to_html(classes="table table-striped", index=False)
    
    # Basic HTML template with Bootstrap for styling
    html_content = f"""
    <html>
    <head>
        <title>Processed CSV Viewer</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5">CSV File Viewer</h1>
            <div class="table-responsive">
                {html_table}
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

def get_csv_view_link(processed_csv_to_view: str) -> dict:
    """
    Generates a link to view the CSV in a tabular format.
    Returns a dictionary containing the link.
    """
    link = f"http://127.0.0.1:8000/view_processed_csv?processed_csv_to_view={processed_csv_to_view}&return_html=true"
    return {"link": link}
