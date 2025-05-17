"""
Model for file-related database operations.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union

from flask import current_app, g


class FileModel:
    """File model for database operations."""

    @staticmethod
    def get_db():
        """Get database connection."""
        if "db" not in g:
            g.db = current_app.db_connector()
        return g.db

    @staticmethod
    def get_file_by_id(file_id: int) -> Optional[Dict]:
        """Get file details by ID."""
        conn = FileModel.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Files WHERE id = ?", (file_id,))

        columns = [desc[0] for desc in cursor.description]
        file_data = cursor.fetchone()

        if file_data:
            return dict(zip(columns, file_data))
        return None

    @staticmethod
    def get_file_by_name(file_name: str) -> Optional[Dict]:
        """Get file details by name."""
        conn = FileModel.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Files WHERE file_name = ?", (file_name,))

        columns = [desc[0] for desc in cursor.description]
        file_data = cursor.fetchone()

        if file_data:
            return dict(zip(columns, file_data))
        return None

    @staticmethod
    def add_file(file_data: bytes, file_name: str) -> int:
        """Add a new file to the database."""
        conn = FileModel.get_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Files (file, file_name, upload_date) VALUES (?, ?, ?)", (file_data, file_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

        return cursor.lastrowid

    @staticmethod
    def update_file(file_id: int, file_data: bytes = None, file_name: str = None) -> bool:
        """Update an existing file."""
        conn = FileModel.get_db()
        cursor = conn.cursor()

        if file_data and file_name:
            cursor.execute("UPDATE Files SET file = ?, file_name = ?, upload_date = ? WHERE id = ?", (file_data, file_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_id))
        elif file_data:
            cursor.execute("UPDATE Files SET file = ?, upload_date = ? WHERE id = ?", (file_data, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_id))
        elif file_name:
            cursor.execute("UPDATE Files SET file_name = ?, upload_date = ? WHERE id = ?", (file_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_id))
        else:
            return False

        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def delete_file(file_id: int) -> bool:
        """Delete a file from the database."""
        conn = FileModel.get_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Files WHERE id = ?", (file_id,))
        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def link_file_to_subject(file_id: int, subject_id: int) -> bool:
        """Link a file to a subject."""
        conn = FileModel.get_db()
        cursor = conn.cursor()

        # Check if the connection already exists
        cursor.execute("SELECT COUNT(*) FROM SubjectFile WHERE subject_id = ? AND file_id = ?", (subject_id, file_id))
        if cursor.fetchone()[0] > 0:
            return False  # Connection already exists

        # Create the connection
        cursor.execute("INSERT INTO SubjectFile (subject_id, file_id) VALUES (?, ?)", (subject_id, file_id))
        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def unlink_file_from_subject(file_id: int, subject_id: int) -> bool:
        """Unlink a file from a subject."""
        conn = FileModel.get_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM SubjectFile WHERE subject_id = ? AND file_id = ?", (subject_id, file_id))
        conn.commit()

        return cursor.rowcount > 0

    @staticmethod
    def get_files_by_subject(subject_id: int) -> List[Dict]:
        """Get all files linked to a specific subject."""
        conn = FileModel.get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT f.* 
            FROM Files f
            JOIN SubjectFile sf ON f.id = sf.file_id
            WHERE sf.subject_id = ?
            """,
            (subject_id,),
        )

        columns = [desc[0] for desc in cursor.description]
        files = cursor.fetchall()

        return [dict(zip(columns, file)) for file in files]
