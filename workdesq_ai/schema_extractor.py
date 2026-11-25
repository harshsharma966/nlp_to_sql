"""
Universal Database Schema Extractor
Dynamically inspects any connected SQL database (MySQL, PostgreSQL, SQLite, etc.)
and generates an accurate schema representation and sample data for the LLM.
"""
from typing import Dict, List, Any
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


class SchemaExtractor:
    """Extracts schema, columns, foreign keys, and sample data from any database."""

    @staticmethod
    def extract_schema_metadata(engine: Engine) -> Dict[str, Any]:
        """
        Inspects the database and returns structured metadata.
        """
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        metadata = {"tables": {}, "relationships": []}

        for table_name in tables:
            columns = []
            for col in inspector.get_columns(table_name):
                columns.append({
                    "name": col["name"],
                    "type": str(col["type"]),
                    "primary_key": col.get("primary_key", False),
                    "nullable": col.get("nullable", True),
                })

            # Foreign keys / relationships
            fks = inspector.get_foreign_keys(table_name)
            for fk in fks:
                referred_table = fk.get("referred_table")
                constrained_cols = fk.get("constrained_columns", [])
                referred_cols = fk.get("referred_columns", [])
                if referred_table and constrained_cols and referred_cols:
                    metadata["relationships"].append({
                        "from_table": table_name,
                        "from_columns": constrained_cols,
                        "to_table": referred_table,
                        "to_columns": referred_cols,
                    })

            # Fetch a sample of 2 rows to give LLM context on categorical values/formats
            sample_data = []
            try:
                with engine.connect() as conn:
                    # Escape table name safely using engine dialect
                    sample_query = f"SELECT * FROM `{table_name}` LIMIT 2" if "mysql" in engine.dialect.name else f'SELECT * FROM "{table_name}" LIMIT 2' if "postgres" in engine.dialect.name else f"SELECT * FROM {table_name} LIMIT 2"
                    result = conn.execute(text(sample_query))
                    rows = result.mappings().fetchall()
                    sample_data = [dict(row) for row in rows]
            except Exception:
                sample_data = []

            metadata["tables"][table_name] = {
                "columns": columns,
                "sample_data": sample_data
            }

        return metadata

    @staticmethod
    def format_schema_for_prompt(engine: Engine) -> str:
        """
        Converts the database metadata into an optimized prompt format for the LLM.
        """
        metadata = SchemaExtractor.extract_schema_metadata(engine)
        lines = [f"DATABASE DIALECT: {engine.dialect.name.upper()}", "SCHEMA STRUCTURE:"]

        if not metadata["tables"]:
            return "No tables found in the connected database."

        for table_name, details in metadata["tables"].items():
            lines.append(f"\nTable: {table_name}")
            lines.append("Columns:")
            for col in details["columns"]:
                pk_marker = " [PRIMARY KEY]" if col["primary_key"] else ""
                lines.append(f"  - {col['name']} ({col['type']}){pk_marker}")

            if details["sample_data"]:
                lines.append("Sample Data (first 2 rows):")
                for row in details["sample_data"]:
                    # Sanitize row display (limit length of strings)
                    clean_row = {
                        k: (str(v)[:50] + "..." if isinstance(v, str) and len(str(v)) > 50 else v)
                        for k, v in row.items()
                    }
                    lines.append(f"  {clean_row}")

        if metadata["relationships"]:
            lines.append("\nRELATIONSHIPS & FOREIGN KEYS:")
            for rel in metadata["relationships"]:
                lines.append(
                    f"  - {rel['from_table']}.{', '.join(rel['from_columns'])} "
                    f"-> {rel['to_table']}.{', '.join(rel['to_columns'])}"
                )

        return "\n".join(lines)
