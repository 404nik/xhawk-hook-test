import json
import time
import uuid
from pathlib import Path
from typing import Dict, Optional

from .users import UserRegistry
from .locations import LocationStore
from .pricing import FareCalculator


class RideDispatcher:
    """Orchestrates ride requests, matching riders with drivers."""
    
    SEARCH_RADIUS_KM = 10.0  # Maximum distance to search for drivers
    
    def __init__(self, data_dir: str = "/tmp/uber_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.rides_file = self.data_dir / "rides.json"
        
        # Initialize components
        self.user_registry = UserRegistry(data_dir)
        self.location_store = LocationStore()
        self.fare_calculator = FareCalculator()
        
        # Load existing rides
        self.rides = self._load_rides()
    
    def _load_rides(self) -> Dict:
        """Load rides from JSON file."""
        if self.rides_file.exists():
            try:
                with open(self.rides_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_rides(self) -> None:
        """Atomically save rides to JSON file."""
        temp_file = self.rides_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(self.rides, f, indent=2)
        temp_file.replace(self.rides_file)
    
    def request_ride(
        self,
        rider_id: str,
        pickup_lat: float,
        pickup_lng: float,
        dropoff_lat: float,
        dropoff_lng: float,
        vehicle_type: str
    ) -> Dict:
        """
        Request a ride. Matches with closest available driver within 10km.
        
        Returns:
            Dict with keys:
            - id: ride ID
            - status: "matched" or "no_drivers"
            - matched_driver_id: driver ID if matched, None otherwise
            - eta_min: estimated time to arrival in minutes (if matched)
            - fare_estimate: fare breakdown dict (if matched)
        """
        ride_id = str(uuid.uuid4())
        
        # Get available drivers of the right type
        available_drivers = self.user_registry.list_drivers(
            vehicle_type=vehicle_type,
            available_only=True
        )
        
        if not available_drivers:
            # No drivers available
            self.rides[ride_id] = {
                "id": ride_id,
                "rider_id": rider_id,
                "status": "no_drivers",
                "matched_driver_id": None,
                "pickup_lat": pickup_lat,
                "pickup_lng": pickup_lng,
                "dropoff_lat": dropoff_lat,
                "dropoff_lng": dropoff_lng,
                "vehicle_type": vehicle_type,
                "created_at": time.time()
            }
            self._save_rides()
            return {
                "id": ride_id,
                "status": "no_drivers",
                "matched_driver_id": None,
                "eta_min": None,
                "fare_estimate": None
            }
        
        # Find nearby drivers
        nearby = self.location_store.nearby_drivers(
            pickup_lat,
            pickup_lng,
            self.SEARCH_RADIUS_KM,
            vehicle_type=vehicle_type,
            drivers_list=available_drivers
        )
        
        if not nearby:
            # No drivers in range
            self.rides[ride_id] = {
                "id": ride_id,
                "rider_id": rider_id,
                "status": "no_drivers",
                "matched_driver_id": None,
                "pickup_lat": pickup_lat,
                "pickup_lng": pickup_lng,
                "dropoff_lat": dropoff_lat,
                "dropoff_lng": dropoff_lng,
                "vehicle_type": vehicle_type,
                "created_at": time.time()
            }
            self._save_rides()
            return {
                "id": ride_id,
                "status": "no_drivers",
                "matched_driver_id": None,
                "eta_min": None,
                "fare_estimate": None
            }
        
        # Match with closest driver
        matched_driver, distance_km = nearby[0]
        driver_id = matched_driver["id"]
        
        # Mark driver as unavailable
        self.user_registry.set_driver_available(driver_id, False)
        
        # Estimate fare (simple: assume 1 min per km for ETA)
        eta_min = max(1, int(distance_km))  # At least 1 minute
        
        # Calculate distance for fare (use haversine between pickup and dropoff)
        trip_distance = LocationStore.haversine_distance(
            pickup_lat, pickup_lng,
            dropoff_lat, dropoff_lng
        )
        trip_duration = max(1, int(trip_distance))  # Rough estimate: 1 min per km
        
        fare_estimate = self.fare_calculator.estimate(
            trip_distance,
            trip_duration,
            vehicle_type
        )
        
        # Create ride record
        self.rides[ride_id] = {
            "id": ride_id,
            "rider_id": rider_id,
            "status": "matched",
            "matched_driver_id": driver_id,
            "pickup_lat": pickup_lat,
            "pickup_lng": pickup_lng,
            "dropoff_lat": dropoff_lat,
            "dropoff_lng": dropoff_lng,
            "vehicle_type": vehicle_type,
            "created_at": time.time(),
            "distance_km": round(trip_distance, 2),
            "duration_min": trip_duration,
            "fare_estimate": fare_estimate
        }
        self._save_rides()
        
        return {
            "id": ride_id,
            "status": "matched",
            "matched_driver_id": driver_id,
            "eta_min": eta_min,
            "fare_estimate": fare_estimate
        }
    
    def complete_ride(self, ride_id: str) -> Optional[Dict]:
        """
        Complete a ride and free up the driver.
        
        Returns:
            Updated ride dict, or None if ride not found
        """
        if ride_id not in self.rides:
            return None
        
        ride = self.rides[ride_id]
        ride["status"] = "completed"
        
        # Free up driver if one was matched
        if ride.get("matched_driver_id"):
            self.user_registry.set_driver_available(ride["matched_driver_id"], True)
        
        self._save_rides()
        return ride
    
    def cancel_ride(self, ride_id: str) -> Optional[Dict]:
        """
        Cancel a ride and free up the driver.
        
        Returns:
            Updated ride dict, or None if ride not found
        """
        if ride_id not in self.rides:
            return None
        
        ride = self.rides[ride_id]
        ride["status"] = "cancelled"
        
        # Free up driver if one was matched
        if ride.get("matched_driver_id"):
            self.user_registry.set_driver_available(ride["matched_driver_id"], True)
        
        self._save_rides()
        return ride
    
    def get_ride(self, ride_id: str) -> Optional[Dict]:
        """Get ride by ID."""
        return self.rides.get(ride_id)
