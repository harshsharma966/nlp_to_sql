"""
NLP to SQL Service - Main orchestrator for the entire flow
"""
from database import QueryExecutor
from .sql_generator import SQLGenerator

class NLPToSQLService:
    """
    Main service that orchestrates the complete NLP-to-SQL flow

    Flow:
        User Question → SQL Generation → SQL Execution → Results
    """

    @staticmethod
    def process_question(question: str):
        """
        Process a natural language question and return results

        Args:
            question (str): User's question in natural language

        Returns:
            dict: Contains SQL query and results
                {
                    'sql': str,
                    'rows': list,
                    'row_count': int
                }

        Flow:
            1. Generate SQL from question using LLM
            2. Execute SQL query on database
            3. Return results with metadata
        """
        # Step 1: Generate SQL
        sql = SQLGenerator.generate(question)

        # Step 2: Execute SQL
        rows = QueryExecutor.execute(sql)

        # Step 3: Return structured response
        return {
            'sql': sql,
            'rows': rows,
            'row_count': len(rows)
        }
