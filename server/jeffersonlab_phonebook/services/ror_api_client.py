
import requests
from typing import  Any
from jeffersonlab_phonebook.config.settings import settings # Assuming settings is correctly configured

# --- Define Custom Exceptions (Recommended) ---
class RorApiClientError(Exception):
    """Base exception for ROR API client errors."""
    pass

class RorApiNetworkError(RorApiClientError):
    """Raised when there's a network issue or HTTP error with the ROR API."""
    def __init__(self, message, status_code=None, original_exception=None):
        super().__init__(message)
        self.status_code = status_code
        self.original_exception = original_exception

class RorApiDataError(RorApiClientError):
    """Raised when the ROR API returns unexpected or malformed data."""
    def __init__(self, message, original_data=None, original_exception=None):
        super().__init__(message)
        self.original_data = original_data
        self.original_exception = original_exception

# --- Modified Functional Approach with Error Propagation ---
def call_ror_api(rorid: str) -> dict[str, Any]:
    """
    Calls the ROR API and returns relevant data.
    Raises RorApiNetworkError or RorApiDataError on failure.
    """
    try:
        response = requests.get(f"{settings.ROR_API_BASE_URL}{rorid}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # You might add more robust data validation here
        # For example, if 'name' is absolutely required:
        if not data.get("name"):
            raise RorApiDataError(
                f"ROR API response for {rorid} missing 'name' field.",
                original_data=data
            )

        return {
            "full_name": data.get("name"),
            "short_name": data.get("acronyms", [None])[0],
            "country": data.get("country", {}).get("country_name"),
            "region": data.get("country", {}).get("country_code"),
            "latitude": data.get("addresses", [{}])[0].get("lat"),
            "longitude": data.get("addresses", [{}])[0].get("lng"),
            "city": data.get("addresses", [{}])[0].get("city"),
            "address": data.get("addresses", [{}])[0].get("line"),
        }
    except requests.exceptions.HTTPError as e:
        # Specific handling for HTTP errors (4xx, 5xx)
        raise RorApiNetworkError(
            f"ROR API returned an HTTP error for ROR ID {rorid}: {e.response.status_code} - {e.response.text}",
            status_code=e.response.status_code,
            original_exception=e
        ) from e # 'from e' chains the exceptions, preserving the original traceback
    except requests.exceptions.ConnectionError as e:
        # Specific handling for network connection issues
        raise RorApiNetworkError(
            f"Failed to connect to ROR API for ROR ID {rorid}: {e}",
            original_exception=e
        ) from e
    except requests.exceptions.RequestException as e:
        # Catch-all for other requests library errors
        raise RorApiNetworkError(
            f"An unknown network error occurred with ROR API for ROR ID {rorid}: {e}",
            original_exception=e
        ) from e
    except ValueError as e: # Raised by response.json() if content is not valid JSON
        raise RorApiDataError(
            f"ROR API response for {rorid} was not valid JSON: {e}",
            original_exception=e,
            original_data=response.text # Capture the raw text for debugging
        ) from e
    except Exception as e:
        # Catch-all for any other unexpected errors during data processing
        raise RorApiDataError(
            f"An unexpected error occurred processing ROR API response for {rorid}: {e}",
            original_exception=e,
            original_data=data # If data was parsed before the error
        ) from e
