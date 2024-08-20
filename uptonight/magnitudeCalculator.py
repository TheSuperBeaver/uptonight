from astropy.coordinates import EarthLocation
from astropy.time import Time
from astroquery.jplhorizons import Horizons

class MagnitudeCalculator:

    @staticmethod
    def calculate_magnitude(observation_time: Time, observer: EarthLocation, horizon_id: str) -> float:
        """
        Calculate the apparent magnitude of a solar system body.

        Parameters:
        - body_name (str): Name of the body (e.g., 'venus', 'mars', 'jupiter').
        - observation_time (Time): Observation time as an astropy Time object.

        Returns:
        - float: The calculated apparent magnitude of the body.
        """

        observerLocation = {'lon': observer.location.lon.value,
                            'lat': observer.location.lat.value,
                            'elevation': observer.location.height.value}
        
        horizonEpochs = {'start': observation_time.iso[0], 
                         'stop': observation_time.iso[observation_time.iso.size - 1], 
                         'step': '30m'}
        
        horizonBody = Horizons(id = horizon_id, location= observerLocation, epochs=horizonEpochs)
        ephemerides = horizonBody.ephemerides()
        magnitudes = ephemerides['V']
        return sum(magnitudes) / len(magnitudes)