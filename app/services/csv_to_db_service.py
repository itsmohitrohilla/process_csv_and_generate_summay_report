import csv
from sqlalchemy.orm import Session
from app.models.models import ProcessedData

def push_csv_to_db(session: Session, file_path: str):
    try:
        # Open the CSV file
        with open(file_path, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Iterate through each row in the CSV
            for row in csv_reader:
                # Create a new ProcessedData object
                processed_data = ProcessedData(
                    product_id=row["product_id"],
                    product_name=row["product_name"],
                    category=row["category"],
                    price=float(row["price"]),
                    quantity_sold=int(row["quantity_sold"]),
                    rating=float(row["rating"]) if row["rating"] else None,
                    review_count=int(row["review_count"]) if row["review_count"] else None
                )
                # Add the object to the session
                session.add(processed_data)
            
            # Commit the transaction
            session.commit()
        
        return True
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return False
