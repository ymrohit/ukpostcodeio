import requests
from requests.adapters import HTTPAdapter, Retry
from typing import List, Optional, Dict, Any
from .exceptions import (
    PostcodesIOError,
    PostcodesIOTimeoutError,
    PostcodesIOHTTPError,
    PostcodesIOValidationError,
    PostcodesIONetworkError
)


class UKPostCodeIO:
    BASE_URL = "https://api.postcodes.io"
    DEFAULT_TIMEOUT = 5  # seconds

    def __init__(self, timeout: int = DEFAULT_TIMEOUT, max_retries: int = 3):
        self.session = requests.Session()
        self.timeout = timeout

        # Configure retries for transient errors
        retries = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, path: str, params: Dict[str, Any] = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.Timeout:
            raise PostcodesIOTimeoutError(self.timeout)
        except requests.ConnectionError as e:
            raise PostcodesIONetworkError(f"Connection error: {e}")
        except requests.RequestException as e:
            raise PostcodesIOError(f"An error occurred: {e}")

    def _post(self, path: str, data: Dict[str, Any], params: Dict[str, Any] = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        headers = {'Content-Type': 'application/json'}
        try:
            response = self.session.post(url, json=data, headers=headers, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except requests.Timeout:
            raise PostcodesIOTimeoutError(self.timeout)
        except requests.ConnectionError as e:
            raise PostcodesIONetworkError(f"Connection error: {e}")
        except requests.RequestException as e:
            raise PostcodesIOError(f"An error occurred: {e}")

    def _handle_response(self, response: requests.Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            raise PostcodesIOError("Invalid JSON response")

        if 200 <= response.status_code < 300:
            return data.get('result')
        else:
            error_message = data.get('error', 'An error occurred')
            raise PostcodesIOHTTPError(response.status_code, error_message)

    def lookup_postcode(self, postcode: str) -> Dict[str, Any]:
        """Lookup a single postcode."""
        return self._get(f"/postcodes/{postcode}")

    def bulk_lookup_postcodes(
        self, postcodes: List[str], filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Bulk lookup multiple postcodes."""
        data = {"postcodes": postcodes}
        params = {'filter': filter} if filter else None
        return self._post("/postcodes", data, params)

    def reverse_geocode(
        self, longitude: float, latitude: float, limit: int = 10, radius: int = 100
    ) -> List[Dict[str, Any]]:
        """Reverse geocode a coordinate to find nearest postcodes."""
        params = {
            'lon': longitude,
            'lat': latitude,
            'limit': limit,
            'radius': radius
        }
        return self._get("/postcodes", params)

    def bulk_reverse_geocode(
        self, geolocations: List[Dict[str, Any]], filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Bulk reverse geocode multiple coordinates."""
        data = {"geolocations": geolocations}
        params = {'filter': filter} if filter else None
        return self._post("/postcodes", data, params)

    def query_postcode(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Query postcodes by partial text."""
        params = {
            'q': query,
            'limit': limit
        }
        return self._get("/postcodes", params)

    def validate_postcode(self, postcode: str) -> bool:
        """Validate a postcode."""
        result = self._get(f"/postcodes/{postcode}/validate")
        return bool(result)

    def nearest_postcodes(
        self, postcode: str, limit: int = 10, radius: int = 100
    ) -> List[Dict[str, Any]]:
        """Find nearest postcodes to a given postcode."""
        params = {
            'limit': limit,
            'radius': radius
        }
        return self._get(f"/postcodes/{postcode}/nearest", params)

    def autocomplete_postcode(self, postcode: str, limit: int = 10) -> List[str]:
        """Autocomplete a postcode."""
        params = {
            'limit': limit
        }
        return self._get(f"/postcodes/{postcode}/autocomplete", params)

    def random_postcode(self, outcode: Optional[str] = None) -> Dict[str, Any]:
        """Get a random postcode."""
        params = {'outcode': outcode} if outcode else None
        return self._get("/random/postcodes", params)

    def lookup_outcode(self, outcode: str) -> Dict[str, Any]:
        """Lookup an outcode."""
        return self._get(f"/outcodes/{outcode}")

    def reverse_geocode_outcode(
        self, longitude: float, latitude: float, limit: int = 10, radius: int = 5000
    ) -> Dict[str, Any]:
        """Reverse geocode to find nearest outcodes."""
        params = {
            'lon': longitude,
            'lat': latitude,
            'limit': limit,
            'radius': radius
        }
        return self._get("/outcodes", params)

    def nearest_outcodes(
        self, outcode: str, limit: int = 10, radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Find nearest outcodes to a given outcode."""
        params = {
            'limit': limit,
            'radius': radius
        }
        return self._get(f"/outcodes/{outcode}/nearest", params)

    def scottish_postcode_lookup(self, postcode: str) -> Dict[str, Any]:
        """Lookup a Scottish postcode."""
        return self._get(f"/scotland/postcodes/{postcode}")

    def terminated_postcode_lookup(self, postcode: str) -> Dict[str, Any]:
        """Lookup a terminated postcode."""
        return self._get(f"/terminated_postcodes/{postcode}")

    def lookup_place(self, code: str) -> Dict[str, Any]:
        """Lookup a place by code."""
        return self._get(f"/places/{code}")

    def query_place(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Query places by name."""
        params = {
            'q': query,
            'limit': limit
        }
        return self._get("/places", params)

    def random_place(self) -> Dict[str, Any]:
        """Get a random place."""
        return self._get("/random/places")

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
