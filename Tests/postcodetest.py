import unittest
from typing import List, Dict, Any
from unittest.mock import patch
from ukpostcodeio.exceptions import (
    PostcodesIOError,
    PostcodesIOTimeoutError,
    PostcodesIOHTTPError,
    PostcodesIOValidationError,
    PostcodesIONetworkError
)
from ukpostcodeio.client import UKPostCodeIO  # Adjust the import path as necessary
import requests

class TestUKPostCodeIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the UKPostCodeIO instance once for all tests."""
        cls.postcode_io = UKPostCodeIO()

    @classmethod
    def tearDownClass(cls):
        """Close the session after all tests."""
        cls.postcode_io.close()

    def test_lookup_postcode_valid(self):
        """Test lookup_postcode with a valid postcode."""
        postcode = "SW1A 1AA"  # Buckingham Palace
        result = self.postcode_io.lookup_postcode(postcode)
        self.assertIsInstance(result, Dict)
        self.assertEqual(result['postcode'], postcode.upper())

    def test_lookup_postcode_invalid(self):
        """Test lookup_postcode with an invalid postcode."""
        postcode = "INVALID"
        with self.assertRaises(PostcodesIOHTTPError):
            self.postcode_io.lookup_postcode(postcode)

    def test_bulk_lookup_postcodes(self):
        """Test bulk_lookup_postcodes with multiple valid postcodes."""
        postcodes = ["SW1A 1AA", "EC1A 1BB", "W1A 0AX"]
        results = self.postcode_io.bulk_lookup_postcodes(postcodes)
        self.assertIsInstance(results, List)
        self.assertEqual(len(results), len(postcodes))
        for res, pc in zip(results, postcodes):
            if res['result']:
                self.assertEqual(res['result']['postcode'], pc.upper())
            else:
                self.assertIsNone(res['result'])

    def test_reverse_geocode(self):
        """Test reverse_geocode with valid coordinates."""
        # Coordinates for Buckingham Palace
        longitude = -0.14189
        latitude = 51.501364
        results = self.postcode_io.reverse_geocode(longitude, latitude)
        self.assertIsInstance(results, List)
        self.assertGreater(len(results), 0)
        for res in results:
            self.assertIn('postcode', res)

    def test_bulk_reverse_geocode(self):
        """Test bulk_reverse_geocode with multiple geolocations."""
        geolocations = [
            {"longitude": -0.14189, "latitude": 51.501364},  # Buckingham Palace
            {"longitude": -0.1276, "latitude": 51.5074},     # London
        ]
        results = self.postcode_io.bulk_reverse_geocode(geolocations)
        self.assertIsInstance(results, List)
        self.assertEqual(len(results), len(geolocations))
        for res in results:
            self.assertIn('result', res)

    def test_query_postcode(self):
        """Test query_postcode with a partial query."""
        query = "SW1A"
        results = self.postcode_io.query_postcode(query)
        self.assertIsInstance(results, List)
        self.assertGreater(len(results), 0)
        for res in results:
            self.assertIn('postcode', res)
            self.assertTrue(res['postcode'].startswith(query.upper()))

    def test_validate_postcode_valid(self):
        """Test validate_postcode with a valid postcode."""
        postcode = "SW1A 1AA"
        is_valid = self.postcode_io.validate_postcode(postcode)
        self.assertTrue(is_valid)

    def test_validate_postcode_invalid(self):
        """Test validate_postcode with an invalid postcode."""
        postcode = "INVALID"
        is_valid = self.postcode_io.validate_postcode(postcode)
        self.assertFalse(is_valid)

    def test_nearest_postcodes(self):
        """Test nearest_postcodes with a valid postcode."""
        postcode = "SW1A 1AA"
        results = self.postcode_io.nearest_postcodes(postcode)
        self.assertIsInstance(results, List)
        self.assertGreater(len(results), 0)
        for res in results:
            self.assertIn('postcode', res)

    def test_autocomplete_postcode(self):
        """Test autocomplete_postcode with a partial postcode."""
        partial_postcode = "SW1A"
        suggestions = self.postcode_io.autocomplete_postcode(partial_postcode)
        self.assertIsInstance(suggestions, List)
        self.assertGreater(len(suggestions), 0)
        for suggestion in suggestions:
            self.assertTrue(suggestion.startswith(partial_postcode.upper()))

    def test_random_postcode(self):
        """Test random_postcode without specifying outcode."""
        result = self.postcode_io.random_postcode()
        self.assertIsInstance(result, Dict)
        self.assertIn('postcode', result)

    def test_random_postcode_with_outcode(self):
        """Test random_postcode with a specific outcode."""
        outcode = "SW1A"
        result = self.postcode_io.random_postcode(outcode=outcode)
        self.assertIsInstance(result, Dict)
        self.assertTrue(result['postcode'].startswith(outcode.upper()))

    def test_lookup_outcode_valid(self):
        """Test lookup_outcode with a valid outcode."""
        outcode = "SW1A"
        result = self.postcode_io.lookup_outcode(outcode)
        self.assertIsInstance(result, Dict)
        self.assertEqual(result['outcode'], outcode.upper())

    def test_reverse_geocode_outcode(self):
        """Test reverse_geocode_outcode with valid coordinates."""
        # Coordinates near Buckingham Palace
        longitude = -0.14189
        latitude = 51.501364
        results = self.postcode_io.reverse_geocode_outcode(longitude, latitude)
        self.assertIsInstance(results[0], Dict)
        self.assertIn('outcode', results[0])

    def test_nearest_outcodes(self):
        """Test nearest_outcodes with a valid outcode."""
        outcode = "SW1A"
        results = self.postcode_io.nearest_outcodes(outcode)
        self.assertIsInstance(results, List)
        self.assertGreater(len(results), 0)
        for res in results:
            self.assertIn('outcode', res)

    def test_scottish_postcode_lookup_valid(self):
        """Test scottish_postcode_lookup with a valid Scottish postcode."""
        postcode = "EH1 1YZ"  # Edinburgh Castle
        result = self.postcode_io.scottish_postcode_lookup(postcode)
        self.assertIsInstance(result, Dict)
        self.assertEqual(result['postcode'], postcode.upper())

    def test_scottish_postcode_lookup_invalid(self):
        """Test scottish_postcode_lookup with a non-Scottish postcode."""
        postcode = "SW1A 1AA"  # London
        with self.assertRaises(PostcodesIOHTTPError):
            self.postcode_io.scottish_postcode_lookup(postcode)

    def test_terminated_postcode_lookup_valid(self):
        """Test terminated_postcode_lookup with a terminated postcode."""
        # Example terminated postcode (Note: Replace with a real terminated postcode if available)
        postcode = "BN1 1AU"
        result = self.postcode_io.terminated_postcode_lookup(postcode)
        self.assertIsInstance(result, Dict)
        self.assertEqual(result['postcode'], postcode.upper())

    def test_terminated_postcode_lookup_invalid(self):
        """Test terminated_postcode_lookup with an active postcode."""
        postcode = "SW1A 1AA"
        with self.assertRaises(PostcodesIOHTTPError):
            self.postcode_io.terminated_postcode_lookup(postcode)

    def test_lookup_place_valid(self):
        """Test lookup_place with a valid place code."""
        # Example place code (Note: Replace with a real place code if available)
        place_code = "osgb4000000074564391"  # Example OSGB CODE
        result = self.postcode_io.lookup_place(place_code)
        self.assertIsInstance(result, Dict)
        self.assertEqual(result['code'], place_code)

    def test_lookup_place_invalid(self):
        """Test lookup_place with an invalid place code."""
        place_code = "INVALID"
        with self.assertRaises(PostcodesIOHTTPError):
            self.postcode_io.lookup_place(place_code)

    def test_query_place(self):
        """Test query_place with a partial place name."""
        query = "London"
        results = self.postcode_io.query_place(query)
        self.assertIsInstance(results, List)
        self.assertGreater(len(results), 0)
        for res in results:
            self.assertIn('name_1', res)
            self.assertIn(query.lower(), res['name_1'].lower())

    def test_random_place(self):
        """Test random_place."""
        result = self.postcode_io.random_place()
        self.assertIsInstance(result, Dict)
        self.assertIn('name_1', result)

    def test_session_close(self):
        """Test that the session can be closed and handles connection errors properly."""
        # Mock the session's get method to raise a ConnectionError
        with patch.object(self.postcode_io.session, 'get', side_effect=requests.ConnectionError):
            with self.assertRaises(PostcodesIONetworkError):
                self.postcode_io.lookup_postcode("SW1A 1AA")
        # No need to reinitialize here since the session is still open; we only patched the get method temporarily



if __name__ == '__main__':
    unittest.main()