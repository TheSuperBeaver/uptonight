import unittest
from astropy.time import Time
from astropy.coordinates import EarthLocation
from astroplan import Observer, time_grid_from_range
import astropy.units as u
from pytz import timezone
import sys


from uptonight.magnitudeCalculator import MagnitudeCalculator

class TestPlanetMagnitudeCalculator(unittest.TestCase):
    
    def test_venus_magnitude_changes_over_time(self):
        """Test that the magnitude of Venus changes over time."""
        time_grid = time_grid_from_range(
            [
                Time("2024-01-01 00:00:00"),
                Time("2024-01-02 00:00:00"),
            ])
        time_grid2 = time_grid_from_range(
            [
                Time("2024-03-01 00:00:00"),
                Time("2024-03-02 00:00:00"),
            ])
        magnitude_1 = MagnitudeCalculator.calculate_magnitude(time_grid, get_mock_observer(), 299)
        magnitude_2 = MagnitudeCalculator.calculate_magnitude(time_grid2, get_mock_observer(), 299)
        
        # Assert that the magnitude is different at two different times
        self.assertNotEqual(magnitude_1, magnitude_2, "The magnitude of Venus should change over time.")
    
    def test_planetary_magnitudes_differ(self):
        """Test that the magnitudes of different planets are different."""
        time_grid = time_grid_from_range(
            [
                Time("2024-01-01 00:00:00"),
                Time("2024-01-02 00:00:00"),
            ])
        
        mars_magnitude = MagnitudeCalculator.calculate_magnitude(time_grid, get_mock_observer(), 499)
        jupiter_magnitude = MagnitudeCalculator.calculate_magnitude(time_grid, get_mock_observer(), 599)
        
        # Assert that the magnitude of Mars and Jupiter are different
        self.assertNotEqual(mars_magnitude, jupiter_magnitude, "The magnitudes of Mars and Jupiter should be different.")

    def test_venus_magnitude_accuracy(self):
        """Test the calculated magnitude of Venus against expected values for known dates."""
        # Known observation date for Venus
        time_grid = time_grid_from_range(
            [
                Time("2024-12-01 00:00:00"),
                Time("2024-12-02 00:00:00"),
            ])
        
        # Calculate magnitude
        calculated_magnitude = MagnitudeCalculator.calculate_magnitude(time_grid, get_mock_observer(), 299)
        
        # Example expected range for Venus's magnitude on the given date (this is an illustrative range)
        expected_min_magnitude = -4.9
        expected_max_magnitude = -2.8
        
        # Assert that the magnitude falls within the expected range
        self.assertTrue(expected_min_magnitude <= calculated_magnitude <= expected_max_magnitude,
                        f"The magnitude of Venus on {time_grid} should be within the range "
                        f"{expected_min_magnitude} to {expected_max_magnitude}. but was {calculated_magnitude}")

    def test_edge_case_for_venus_magnitude(self):
        """Test an edge case for Venus's magnitude, e.g., at greatest elongation."""
        time_grid = time_grid_from_range(
            [
                Time("2024-03-20 00:00:00"),
                Time("2024-03-21 00:00:00"),
            ])
        
        # Calculate magnitude
        calculated_magnitude = MagnitudeCalculator.calculate_magnitude(time_grid, get_mock_observer(), 299)
        
        # Example expected range for Venus's magnitude at greatest elongation
        expected_min_magnitude = -4.5
        expected_max_magnitude = -2.0
        
        # Assert that the magnitude falls within the expected range
        self.assertTrue(expected_min_magnitude <= calculated_magnitude <= expected_max_magnitude,
                        f"The magnitude of Venus on {time_grid} should be within the range "
                        f"{expected_min_magnitude} to {expected_max_magnitude}. but was {calculated_magnitude}")

def get_mock_observer():

    # Mock location values
    mock_location = {
        "longitude": 4.079247222222222,
        "latitude": 50.56960277777778,
        "elevation": 90.0,  # in meters
        "timezone": "Europe/Brussels"
    }

    # Mock environment values
    mock_environment = {
        "pressure": 1.013,  # Pressure in bar
        "relative_humidity": 0.6,  # Relative humidity (60%)
        "temperature": 20.0  # Temperature in degrees Celsius
    }

    # Create EarthLocation object from mock data
    observer_location = EarthLocation.from_geodetic(
        mock_location["longitude"],
        mock_location["latitude"],
        mock_location["elevation"] * u.m,
    )

    # Create Observer object with mock data
    observer = Observer(
        name="Backyard",
        location=observer_location,
        pressure=mock_environment["pressure"] * u.bar,
        relative_humidity=mock_environment["relative_humidity"],
        temperature=mock_environment["temperature"] * u.deg_C,
        timezone=timezone(mock_location["timezone"]),
        description="My beloved Backyard Telescope",
    )

    return observer

if __name__ == "__main__":
    if not sys.argv or sys.argv[0].endswith("json"):
        # Running in an interactive environment
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        # Normal command line execution
        unittest.main()