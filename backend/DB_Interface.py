import mysql.connector
from fastapi import HTTPException

class InventoryDB:

    def __init__(self, host, port, username, password, DB_name):
        self.config = {
            "host" : host,
            "port" : port,
            "username" : username,
            "password" : password,
            "database" : DB_name
        }
    
    def get_db_connection(self):
        try:
            # Establish Connection
            connection = mysql.connector.connect(**self.config)
            return connection
        
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error: {err}")
        
    def borrow_device(self, data: dict):
        connection = None
        try:
            connection = self.get_db_connection()
            cursor = connection.cursor()

            # Extract student and borrowing details
            name = data["name"]
            roll_number = data["roll_number"]
            department = data["department"]
            email = data["email"]
            device_id = data["device_id"]
            due_date = data["due_date"]  # should be in 'YYYY-MM-DDTHH:MM:SS' format

            # Step 1: Check if student already exists
            cursor.execute("SELECT student_id FROM Students WHERE roll_number = %s", (roll_number,))
            student = cursor.fetchone()

            if student:
                student_id = student[0]
            else:
                # Insert new student
                cursor.execute(
                    "INSERT INTO Students (name, roll_number, department, email) VALUES (%s, %s, %s, %s)",
                    (name, roll_number, department, email)
                )
                student_id = cursor.lastrowid

            # Step 2: Insert into Borrowed_Devices
            query = """
            INSERT INTO Borrowed_Devices (student_id, device_id, borrowed_date, due_date, status)
            VALUES (%s, %s, NOW(), %s, 'Borrowed')
            """
            cursor.execute(query, (student_id, device_id, due_date))
            connection.commit()

            return {
                "message": "Device borrowed successfully.",
                "borrow_id": cursor.lastrowid,
                "student_id": student_id
            }

        except mysql.connector.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        finally:
            if connection:
                connection.close()
