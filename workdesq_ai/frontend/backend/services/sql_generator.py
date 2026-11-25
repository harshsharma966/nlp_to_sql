"""
SQL Generator - Converts natural language to SQL
"""
import re
from database import SchemaExtractor
from .llm_service import llm_service
from .prompt_builder import PromptBuilder

class SQLGenerator:
    """Converts natural language questions to SQL queries"""

    @staticmethod
    def generate(question: str) -> str:
        """
        Generate SQL query from natural language question

        Args:
            question (str): User's natural language question

        Returns:
            str: Generated SQL query

        Process:
            1. Extract database schema
            2. Build optimized prompt
            3. Generate SQL using LLM
            4. Clean and validate output
        """
        # Step 1: Get database schema
        schema = SchemaExtractor.extract_schema()

        # Step 2: Build prompt
        prompt = PromptBuilder.build_sql_prompt(question, schema)

        # Step 3: Generate SQL using LLM
        raw_output = llm_service.generate(prompt, max_tokens=350, temperature=0.0)

        # Step 4: Clean and extract SQL
        sql = SQLGenerator._extract_sql(raw_output)

        return sql

    @staticmethod
    def _extract_sql(raw_output: str) -> str:
        """
        Extract clean SQL from LLM output

        Args:
            raw_output (str): Raw LLM output

        Returns:
            str: Cleaned SQL query
        """
        # Try to find SELECT....; pattern
        match = re.search(r"(SELECT[\s\S]+?;)", raw_output, re.IGNORECASE)
        if match:
            sql = match.group(1).strip()
        else:
            sql = raw_output.strip()

        # Remove markdown code blocks if present
        sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql
