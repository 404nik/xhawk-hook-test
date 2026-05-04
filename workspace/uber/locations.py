import math
from typing import Optional, Dict, List, Tuple


class LocationStore:
    """Tracks current location of drivers using haversine distance."""
    
    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0
    
    def __init__(self):
        # driver_id -> {"lat": float, "lng": float, "ts": float}
        self.locations: Dict[str, Dict] = {}
    
    @staticmethod
    def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate distance between two points using haversine formula.
        Returns distance in kilometers.
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return LocationStore.EARTH_RADIUS_KM * c
    
    def update_driver_location(self, driver_id: str, lat: float, lng: float, ts: float) -> None:
        """Update driver's current location and timestamp."""
        self.locations[driver_id] = {
            "lat": lat,
            "lng": lng,
            "ts": ts
        }
    
    def get_driver_location(self, driver_id: str) -> Optional[Dict]:
        """Get driver's current location, or None if not set."""
        return self.locations.get(driver_id)
    
    def nearby_drivers(
        self,
        lat: float,
        lng: float,
        radius_km: float,
        vehicle_type: Optional[str] = None,
        drivers_list: Optional[List[Dict]] = None
    ) -> List[Tuple[Dict, float]]:
        """
        Find drivers within radius_km, sorted by distance (closest first).
        
        Args:
            lat: pickup latitude
            lng: pickup longitude
            radius_km: search radius in kilometers
            vehicle_type: optional filter by vehicle type
            drivers_list: list of driver dicts to filter (from UserRegistry.list_drivers)
        
        Returns:
            List of (driver_dict, distance_km) tuples sorted by distance.
            Gracefully skips drivers without location data.
        """
        nearby = []
        
        # If drivers_list provided, use it; otherwise use all drivers with locations
        drivers_to_check = drivers_list if drivers_list is not None else []
        
        for driver in drivers_to_check:
            driver_id = driver["id"]
            
            # Skip if no location data
            if driver_id not in self.locations:
                continue
            
            # Skip if vehicle_type filter doesn't match
            if vehicle_type and driver.get("vehicle_type") != vehicle_type:
                continue
            
            loc = self.locations[driver_id]
            distance = self.haversine_distance(lat, lng, loc["lat"], loc["lng"])
            
            # Only include if within radius
            if distance <= radius_km:
                nearby.append((driver, distance))
        
        # Sort by distance (closest first)
        nearby.sort(key=lambda x: x[1])
        
        return nearby
