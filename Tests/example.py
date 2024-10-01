
from ukpostcodeio.client import UKPostCodeIO
from ukpostcodeio.exceptions import (
    PostcodesIOError,
    PostcodesIOTimeoutError,
    PostcodesIOHTTPError,
    PostcodesIOValidationError,
    PostcodesIONetworkError
)

# Initialize the client
client = UKPostCodeIO(timeout=10)

try:
    # Lookup a postcode
    result = client.lookup_postcode('B170NL')
    print(result)
except PostcodesIOTimeoutError as e:
    print(f"Timeout Error: {e}")
except PostcodesIOHTTPError as e:
    print(f"HTTP Error {e.status_code}: {e.error_message}")
except PostcodesIONetworkError as e:
    print(f"Network Error: {e}")
except PostcodesIOValidationError as e:
    print(f"Validation Error: {e.message}")
except PostcodesIOError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
finally:
    client.close()
