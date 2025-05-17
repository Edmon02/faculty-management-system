"""
Service for handling file operations.
"""

import base64
import mimetypes
import os
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

from flask import current_app, make_response, url_for
from werkzeug.datastructures import FileStorage

from app.models.files import FileModel
from app.utils.validators import validate_file_extension, validate_file_size


class FileService:
    """Service for file operations."""

    @staticmethod
    def get_file_by_id(file_id: int) -> Optional[Dict]:
        """Get file by ID."""
        return FileModel.get_file_by_id(file_id)

    @staticmethod
    def get_file_by_name(file_name: str) -> Optional[Dict]:
        """Get file by name."""
        return FileModel.get_file_by_name(file_name)

    @staticmethod
    def save_file(file: FileStorage, allowed_extensions: set = None) -> Tuple[bool, Union[int, str]]:
        """
        Save a file to the database.

        Returns:
            Tuple containing success status and file ID or error message
        """
        if file is None or file.filename == "":
            return False, "No file selected"

        if not validate_file_extension(file.filename, allowed_extensions):
            return False, "File type not allowed"

        if not validate_file_size(file, max_size_mb=10):
            return False, "File size exceeds maximum limit (10MB)"

        file_data = file.read()
        file_name = file.filename

        file_id = FileModel.add_file(file_data, file_name)
        return True, file_id

    @staticmethod
    def update_file(file_id: int, file: Optional[FileStorage] = None, file_name: Optional[str] = None) -> Tuple[bool, str]:
        """Update an existing file."""
        if file is None and file_name is None:
            return False, "No updates provided"

        file_data = None
        if file and file.filename:
            if not validate_file_extension(file.filename):
                return False, "File type not allowed"

            if not validate_file_size(file):
                return False, "File size exceeds maximum limit"

            file_data = file.read()
            file_name = file.filename

        success = FileModel.update_file(file_id, file_data, file_name)
        if success:
            return True, "File updated successfully"
        return False, "Failed to update file"

    @staticmethod
    def delete_file(file_id: int) -> Tuple[bool, str]:
        """Delete a file."""
        success = FileModel.delete_file(file_id)
        if success:
            return True, "File deleted successfully"
        return False, "Failed to delete file"

    @staticmethod
    def link_file_to_subject(file_id: int, subject_id: int) -> Tuple[bool, str]:
        """Link a file to a subject."""
        success = FileModel.link_file_to_subject(file_id, subject_id)
        if success:
            return True, "File linked to subject successfully"
        return False, "Failed to link file to subject or link already exists"

    @staticmethod
    def unlink_file_from_subject(file_id: int, subject_id: int) -> Tuple[bool, str]:
        """Unlink a file from a subject."""
        success = FileModel.unlink_file_from_subject(file_id, subject_id)
        if success:
            return True, "File unlinked from subject successfully"
        return False, "Failed to unlink file from subject"

    @staticmethod
    def get_files_by_subject(subject_id: int) -> List[Dict]:
        """Get all files for a subject with formatted data."""
        files = FileModel.get_files_by_subject(subject_id)

        formatted_files = []
        for file in files:
            formatted_file = {
                "file_id": file["id"],
                "file_name": file["file_name"],
                "file_type": os.path.splitext(file["file_name"])[1],
                "upload_date": file.get("upload_date", ""),
            }
            formatted_files.append(formatted_file)

        return formatted_files

    @staticmethod
    def create_file_response(file_data: Dict) -> make_response:
        """Create a response for file download."""
        file_content = file_data["file"]
        file_name = file_data["file_name"]

        contents = BytesIO(file_content)

        # Set the Content-Type header based on file extension
        content_type, _ = mimetypes.guess_type(file_name)
        if not content_type:
            content_type = "application/octet-stream"

        response = make_response(contents.getvalue())
        response.headers.set("Content-Type", content_type)

        # Set the Content-Disposition header
        filename_header = f'filename="{file_name}"'
        if content_type != "application/pdf":
            response.headers.set("Content-Disposition", "attachment", filename=filename_header)
        else:
            response.headers.set("Content-Disposition", "inline", filename=filename_header)

        return response

    @staticmethod
    def encode_file_to_base64(file_data: bytes) -> str:
        """Convert file data to base64 encoded string."""
        if isinstance(file_data, bytes):
            return base64.b64encode(file_data).decode("utf-8")
        return ""
