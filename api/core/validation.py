"""Validation utilities for the API."""

from typing import Dict, Any, List, Union
from datetime import datetime, date

def validate_request_data(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate that all required fields are present in the request data.
    
    Args:
        data: Request data dictionary
        required_fields: List of required field names
        
    Raises:
        ValueError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

def validate_date_format(date_str: str, format: str = '%Y-%m-%d') -> date:
    """Validate and parse a date string.
    
    Args:
        date_str: Date string to validate
        format: Expected date format (default: YYYY-MM-DD)
        
    Returns:
        date: Parsed date object
        
    Raises:
        ValueError: If date string is invalid or doesn't match format
    """
    try:
        return datetime.strptime(date_str, format).date()
    except ValueError:
        raise ValueError(f"Invalid date format. Expected format: {format}")

def validate_date_range(start_date: date, end_date: date) -> None:
    """Validate that end_date is after start_date.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Raises:
        ValueError: If end_date is before or equal to start_date
    """
    if end_date <= start_date:
        raise ValueError("End date must be after start date") 