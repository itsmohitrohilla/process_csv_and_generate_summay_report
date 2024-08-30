from fastapi import APIRouter, UploadFile, File, HTTPException, Query, FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, RedirectResponse
from app.services.csv_service import process_csv, generate_summary_report
import os
import shutil
from app.database.db import SessionLocal
from app.services.csv_to_db_service import push_csv_to_db
import pandas as pd
from app.services import auth
from app.schemas import schemas


router = APIRouter()

# Folder to save the summary reports
SUMMARY_REPORT_FOLDER = "data/summary_report"
PROCESSED_CSV_FOLDER = "data/processed_csv"
DEMO_CSV_FOLDER = "data/demo_csv"



#***********************************************************************************************************************  

@router.get("/download-demo-csv/")
async def download_demo_csv(current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Endpoint to download the Demo CSV File.
    """
    # Define the path to the summary report file
    demo_csv_path = "data/demo_csv/demo.csv"
    
    return FileResponse(
        demo_csv_path,
        media_type='text/csv',
        filename=f"demo.csv"
    )

#***********************************************************************************************************************  

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...),current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Endpoint to upload a CSV file and process it.
    """
    # Validate the file type
    if not file.filename.endswith('.csv'):
        return JSONResponse(
            status_code=400,
            content={"detail": "Only CSV files are allowed."}
        )
    
    # Save the uploaded file temporarily
    temp_file_path = os.path.join("data", file.filename)
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error saving file: {str(e)}"}
        )
    
    try:
        # Process the CSV file
        process_id = process_csv(temp_file_path)
        
        # Generate the summary report
        summary_csv_path = generate_summary_report(process_id)
        
        # Return a response indicating successful processing
        return JSONResponse(content={
            "message": "CSV file processed successfully.",
            "cleaned_csv_file": f"{process_id}.csv",
            "summary_report_file": f"{process_id}_sr.csv"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing CSV file: {str(e)}"}
        )
    finally:
        # Clean up temporary file if it exists
        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)
#***********************************************************************************************************************  

@router.get("/view_processed_csv", response_class=HTMLResponse)
async def view_processed_csv(processed_csv_to_view: str = Query(..., min_length=1)):
    
    """
    1. Please Enter The Processed CSV name 
    2. Copy the request URL path and paste in anothe tab to view the csv.
    """
    
    processed_csv_path_to_view = os.path.join(PROCESSED_CSV_FOLDER, f"{processed_csv_to_view}")
    
    print(f"Attempting to access file at: {processed_csv_to_view}")
    
    if not os.path.isfile(processed_csv_path_to_view):
        return JSONResponse(
            status_code=404,
            content={"detail": "Processed CSV file not found."}
        )
    
    df = pd.read_csv(processed_csv_path_to_view)
    
    # Convert the DataFrame to an HTML table
    html_table = df.to_html(classes="table table-striped", index=False)
    
    # Basic HTML template with Bootstrap for styling
    html_content = f"""
    <html>
    <head>
        <title>Processd CSV Viewer</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h2 class="mt-5">CSV File Viewer : {processed_csv_to_view}</h2>
            <div class="table-responsive">
                {html_table}
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
#***********************************************************************************************************************  
            
@router.get("/push_to_database/")
async def push_to_database(processed_csv_name: str = Query(..., min_length=1),current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Endpoint to push the processed CSV data into the database.
    """
    # Define the path to the CSV file
    processed_csv_path = os.path.join(PROCESSED_CSV_FOLDER, f"{processed_csv_name}")
    
    # Debugging: Print out the file path and check if file exists
    print(f"Attempting to access file at: {processed_csv_path}")
    
    # Check if the file exists
    if not os.path.isfile(processed_csv_path):
        return JSONResponse(
            status_code=404,
            content={"detail": "Processed CSV file not found."}
        )
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Push the CSV data to the database
        success = push_csv_to_db(db, processed_csv_path)
        
        if success:
            return JSONResponse(
                content={"message": "CSV data pushed to database successfully.", "csv_file": f"{processed_csv_name}"}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"detail": "Failed to push CSV data to the database."}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error processing CSV data: {str(e)}"}
        )
    finally:
        db.close()
            
#***********************************************************************************************************************  

@router.get("/download-summary-report/")
async def download_summary_report(summary_report_name: str = Query(..., min_length=1), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Endpoint to download the summary report for a given process ID.
    """
    # Define the path to the summary report file
    summary_csv_path = os.path.join(SUMMARY_REPORT_FOLDER, f"{summary_report_name}")
    
    # Debugging: Print out the file path and check if file exists
    print(f"Attempting to access file at: {summary_csv_path}")
    
    try:
        # Check if the file exists
        if not os.path.isfile(summary_csv_path):
            return JSONResponse(
                status_code=404,
                content={"detail": "Summary report not found."}
            )
        
        # Return the file for download
        return FileResponse(
            summary_csv_path,
            media_type='text/csv',
            filename=f"{summary_report_name}"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error accessing file: {str(e)}"}
        )


