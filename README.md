### CSV Processing API 

## Introduction  
This project provides an API for handling CSV files with authentication and data processing features. You can use this API to upload, process, and manage CSV files, as well as generate demo data for testing.  
## Getting Started  
## Clone the Repository  To get started, first clone the repository to your local machine:  

`git clone ____________`

### Install Dependencies

Install the required Python packages using requirements.txt:

`   bashCopy codepip install -r requirements.txt   `

### Run the Application

Start the FastAPI application using Uvicorn:

`   bashCopy code uvicorn app.main:app --reload   `

### Access the API

Open your browser and navigate to http://localhost:8000/docs to access the Swagger UI. Here you can interact with the API endpoints and test the functionality.

Authentication
--------------

The API includes two authentication endpoints:

*   **Signup**: Create a new user.
    
*   **Login**: Authenticate an existing user and receive a JWT token.
    

Use the "Authorize" button in Swagger UI to authenticate and use the provided JWT token. The token will expire in 30 minutes.

API Endpoints
-------------

### 1\. Download Demo CSV

Download a demo CSV file to use for testing:

*   **Endpoint**: GET /download-demo-csv
    

### 2\. Upload CSV

Upload your own CSV file:

*   **Endpoint**: POST /upload-csv
    
*   **Response**: The response will include two CSV file names: processed\_csv and summary\_csv.
    

### 3\. Create View of Processed CSV

Enter the name of the processed CSV to get the request URL. You can copy this URL and view the CSV in another tab.

*   **Endpoint**: GET /view-csv
    
*   **Parameters**: processed\_csv\_name (name of the processed CSV)
    

### 4\. Update Database

Push the data from the processed CSV into the database:

*   **Endpoint**: POST /update-db
    
*   **Parameters**: processed\_csv\_name (name of the processed CSV)
    

### 5\. Download Summary Report

Get the name of the summary report and download it:

*   **Endpoint**: GET /download-summary-report
    
*   **Parameters**: summary\_report\_name (name of the summary report)
    

Generate Demo Data
------------------

If you want to generate new CSV data for demo purposes, use the fake.py script:
`   bashCopy codepython3 fake.py   `

This will create new demo data that you can use to test the code.

Usage Notes
-----------

*   Ensure you have a valid JWT token for accessing secured endpoints.
    
*   Use the Swagger UI for easy interaction with the API and for obtaining tokens.
    
*   The upload-csv endpoint requires a valid CSV file and will provide two output files (processed\_csv and summary\_csv) for further use.
