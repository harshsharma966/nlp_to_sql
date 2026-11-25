# import mysql.connector
# import os

# def get_connection():
#     """
#     Get MySQL database connection with error handling.
#     Default database: edb15 (can be changed via environment variable)
#     """
#     try:
#         return mysql.connector.connect(
#             host=os.getenv("DB_HOST", "localhost"),
#             user=os.getenv("DB_USER", "root"),
#             password=os.getenv("DB_PASSWORD", ""),  # XAMPP default
#             database=os.getenv("DB_NAME", "worksdesq_ai"),
#             port=int(os.getenv("DB_PORT", "3306"))
#         )
#     except mysql.connector.Error as e:
#         raise ConnectionError(f"Failed to connect to database: {str(e)}")



import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # change if needed
        database="worksdesq_ai" # your DB name
    )


