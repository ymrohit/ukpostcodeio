# UKPostCodeIO Python Library

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Introduction

UKPostCodeIO is a Python client library for the [Postcodes.io](https://postcodes.io/) API, a free and open-source UK postcode lookup and geocoder. This library provides convenient access to the Postcodes.io API endpoints, allowing developers to integrate postcode data and geolocation services into their Python applications seamlessly.

## Features

- **Postcode Lookup**: Retrieve detailed information about a specific postcode.
- **Bulk Postcode Lookup**: Lookup multiple postcodes in a single request.
- **Reverse Geocoding**: Find nearest postcodes to given coordinates.
- **Bulk Reverse Geocoding**: Reverse geocode multiple coordinates.
- **Postcode Validation**: Validate the format and existence of a postcode.
- **Autocomplete**: Get postcode suggestions based on partial input.
- **Random Postcode**: Retrieve a random postcode.
- **Outcode Services**: Lookup and reverse geocode outcodes (the first part of a postcode).
- **Scottish Postcode Lookup**: Access data specific to Scottish postcodes.
- **Terminated Postcode Lookup**: Retrieve information on terminated postcodes.
- **Place Services**: Lookup and query places by code or name.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initializing the Client](#initializing-the-client)
  - [Lookup Postcode](#lookup-postcode)
  - [Bulk Lookup Postcodes](#bulk-lookup-postcodes)
  - [Reverse Geocode](#reverse-geocode)
  - [Bulk Reverse Geocode](#bulk-reverse-geocode)
  - [Postcode Validation](#postcode-validation)
  - [Nearest Postcodes](#nearest-postcodes)
  - [Autocomplete Postcode](#autocomplete-postcode)
  - [Random Postcode](#random-postcode)
  - [Outcode Services](#outcode-services)
  - [Scottish Postcode Lookup](#scottish-postcode-lookup)
  - [Terminated Postcode Lookup](#terminated-postcode-lookup)
  - [Place Services](#place-services)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

Install the library using pip:

```bash
pip install ukpostcodeio
```

*Note: Replace `ukpostcodeio` with the actual package name if it's different when published to PyPI.*

Alternatively, you can install it directly from the source:

```bash
git clone https://github.com/ymrohit/ukpostcodeio.git
cd ukpostcodeio
pip install .
```

## Usage

### Initializing the Client

```python
from ukpostcodeio.client import UKPostCodeIO

# Initialize the client with default settings
postcode_client = UKPostCodeIO()

# Initialize the client with custom timeout and retries
postcode_client = UKPostCodeIO(timeout=10, max_retries=5)
```

### Lookup Postcode

Retrieve information about a specific postcode.

```python
result = postcode_client.lookup_postcode("SW1A 1AA")
print(result)
```

### Bulk Lookup Postcodes

Lookup multiple postcodes in a single request.

```python
postcodes = ["SW1A 1AA", "EC1A 1BB", "W1A 0AX"]
results = postcode_client.bulk_lookup_postcodes(postcodes)
print(results)
```

### Reverse Geocode

Find the nearest postcodes to a given longitude and latitude.

```python
longitude = -0.1278  # Longitude for London
latitude = 51.5074   # Latitude for London

results = postcode_client.reverse_geocode(longitude, latitude)
print(results)
```

### Bulk Reverse Geocode

Reverse geocode multiple coordinates.

```python
geolocations = [
    {"longitude": -0.1278, "latitude": 51.5074},
    {"longitude": -0.1425, "latitude": 51.5010}
]

results = postcode_client.bulk_reverse_geocode(geolocations)
print(results)
```

### Postcode Validation

Check if a postcode is valid.

```python
is_valid = postcode_client.validate_postcode("SW1A 1AA")
print(is_valid)  # True

is_valid = postcode_client.validate_postcode("INVALID")
print(is_valid)  # False
```

### Nearest Postcodes

Find the nearest postcodes to a given postcode.

```python
results = postcode_client.nearest_postcodes("SW1A 1AA")
print(results)
```

### Autocomplete Postcode

Get postcode suggestions based on partial input.

```python
suggestions = postcode_client.autocomplete_postcode("SW1A")
print(suggestions)
```

### Random Postcode

Retrieve a random postcode.

```python
random_postcode = postcode_client.random_postcode()
print(random_postcode)

# Retrieve a random postcode within a specific outcode
random_postcode = postcode_client.random_postcode(outcode="SW1A")
print(random_postcode)
```

### Outcode Services

#### Lookup Outcode

Get information about an outcode.

```python
outcode_info = postcode_client.lookup_outcode("SW1A")
print(outcode_info)
```

#### Reverse Geocode Outcode

Find the nearest outcodes to given coordinates.

```python
results = postcode_client.reverse_geocode_outcode(-0.1278, 51.5074)
print(results)
```

#### Nearest Outcodes

Find the nearest outcodes to a given outcode.

```python
results = postcode_client.nearest_outcodes("SW1A")
print(results)
```

### Scottish Postcode Lookup

Retrieve data specific to a Scottish postcode.

```python
scottish_data = postcode_client.scottish_postcode_lookup("EH1 1YZ")
print(scottish_data)
```

### Terminated Postcode Lookup

Get information about a terminated postcode.

```python
terminated_postcode_info = postcode_client.terminated_postcode_lookup("EX16 5BL")
print(terminated_postcode_info)
```

### Place Services

#### Lookup Place

Find a place by its code.

```python
place_info = postcode_client.lookup_place("osgb4000000074564391")
print(place_info)
```

#### Query Place

Search for places by name.

```python
places = postcode_client.query_place("London")
print(places)
```

#### Random Place

Retrieve a random place.

```python
random_place = postcode_client.random_place()
print(random_place)
```

### Closing the Client

It's good practice to close the client session when done.

```python
postcode_client.close()
```

Or use it as a context manager:

```python
with UKPostCodeIO() as postcode_client:
    result = postcode_client.lookup_postcode("SW1A 1AA")
    print(result)
```

## Error Handling

The library defines custom exceptions to help handle different error scenarios:

- **PostcodesIOError**: Base exception class for all Postcodes.io errors.
- **PostcodesIOHTTPError**: Raised for HTTP errors (e.g., 404 Not Found, 500 Internal Server Error).
- **PostcodesIOTimeoutError**: Raised when a request times out.
- **PostcodesIOValidationError**: Raised for validation errors.
- **PostcodesIONetworkError**: Raised for network-related errors (e.g., connection errors).

### Handling Exceptions

```python
from ukpostcodeio.exceptions import (
    PostcodesIOError,
    PostcodesIOHTTPError,
    PostcodesIOTimeoutError,
    PostcodesIONetworkError
)

try:
    result = postcode_client.lookup_postcode("INVALID")
except PostcodesIOHTTPError as e:
    print(f"HTTP Error: {e.status_code} - {e.error_message}")
except PostcodesIOTimeoutError:
    print("The request timed out.")
except PostcodesIONetworkError:
    print("A network error occurred.")
except PostcodesIOError as e:
    print(f"An error occurred: {e}")
```

### Common Error Scenarios

- **Invalid Postcode**: Raises `PostcodesIOHTTPError` with a 404 status code.
- **Network Issues**: Raises `PostcodesIONetworkError` if there's a connection problem.
- **Timeouts**: Raises `PostcodesIOTimeoutError` if the request exceeds the specified timeout.
- **Invalid Parameters**: Raises `PostcodesIOValidationError` if parameters are invalid.

## Testing

The library includes a suite of unit tests to ensure functionality.

### Running Tests

1. Install the testing dependencies:

```bash
pip install -r requirements-dev.txt
```

2. Run the tests:

```bash
python -m unittest discover Tests
```

*Note: Ensure that you have network connectivity when running the tests, as they make real API calls.*

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

Please ensure your code passes all tests and adheres to the project's coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This library utilizes the [Postcodes.io](https://postcodes.io/) API, an open-source project that provides UK postcode data and geolocation services.
- Special thanks to the Postcodes.io team for their comprehensive API and open data initiatives.

## Additional Notes

- **Rate Limiting**: Postcodes.io does not enforce rate limiting, but it's good practice to implement it on your side if you're making a large number of requests.
- **Data Accuracy**: While the data is regularly updated, always cross-reference critical data with official sources.
- **API Changes**: The library is designed to handle the current API endpoints. Keep an eye on the [Postcodes.io documentation](https://postcodes.io/docs) for any changes.

---

For any issues or questions, please open an issue on the GitHub repository.
