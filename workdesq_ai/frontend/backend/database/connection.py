"""
Database connection manager
"""
import mysql.connector
from mysql.connector import Error
from config.settings import settings

class DatabaseConnection:
    """Manages MySQL database connections"""

    @staticmethod
    def get_connection():
        """
        Create and return a database connection

        Returns:
            mysql.connector.connection: Database connection object

        Raises:
            ConnectionError: If database connection fails
        """
        try:
            connection = mysql.connector.connect(
                host=settings.DB_HOST,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                port=settings.DB_PORT
            )
            return connection
        except Error as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    @staticmethod
    def test_connection():
        """
        Test if database connection is working

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            conn = DatabaseConnection.get_connection()
            conn.close()
            return True
        except:
            return False

# Convenience function for backward compatibility
def get_db():
    """Get database connection"""
    return DatabaseConnection.get_connection()
