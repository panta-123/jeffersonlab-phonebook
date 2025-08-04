import requests
from typing import Any
from jeffersonlab_phonebook.config.settings import settings

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
    headers = {
        "Client-Id": settings.ROR_CLIENT_ID
    }

    try:
        # In a real-world scenario, you would use this commented-out line.
        response = requests.get(f"{settings.ROR_API_BASE_URL}/{rorid}", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # --- Correct Data Extraction Logic ---
        full_name = None
        short_name = None

        # Find the full_name from the names list
        for name_obj in data.get("names", []):
            if "ror_display" in name_obj.get("types", []):
                full_name = name_obj.get("value")
                break
        
        # Fallback to 'label' if 'ror_display' is not found
        if full_name is None:
            for name_obj in data.get("names", []):
                if "label" in name_obj.get("types", []):
                    full_name = name_obj.get("value")
                    break
        
        # Find the short_name (acronym or alias)
        for name_obj in data.get("names", []):
            if "acronym" in name_obj.get("types", []):
                short_name = name_obj.get("value")
                break
        if short_name is None: # Fallback to alias if no acronym
            for name_obj in data.get("names", []):
                if "alias" in name_obj.get("types", []):
                    short_name = name_obj.get("value")
                    break

        first_location_details = data.get("locations", [{}])[0].get("geonames_details", {})

        latitude = first_location_details.get("lat")
        longitude = first_location_details.get("lng")
        city = first_location_details.get("name")
        address_line = first_location_details.get("name") # The provided data does not have an address line, so we can use city name as a proxy
        country = first_location_details.get("country_name")
        region = first_location_details.get("country_subdivision_name")

        ret =  {
            "full_name": full_name,
            "short_name": short_name,
            "country": country,
            "region": region,
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "address": address_line,
        }
        return ret
        
    except requests.exceptions.HTTPError as e:
        raise RorApiNetworkError(
            f"ROR API returned an HTTP error for ROR ID {rorid}: {e.response.status_code} - {e.response.text}",
            status_code=e.response.status_code,
            original_exception=e
        ) from e
    except requests.exceptions.ConnectionError as e:
        raise RorApiNetworkError(
            f"Failed to connect to ROR API for ROR ID {rorid}: {e}",
            original_exception=e
        ) from e
    except requests.exceptions.RequestException as e:
        raise RorApiNetworkError(
            f"An unknown network error occurred with ROR API for ROR ID {rorid}: {e}",
            original_exception=e
        ) from e
    except Exception as e:
        original_content = data if 'data' in locals() else None
        raise RorApiDataError(
            f"An unexpected error occurred processing ROR API response for {rorid}: {e}",
            original_exception=e,
            original_data=original_content
        ) from e