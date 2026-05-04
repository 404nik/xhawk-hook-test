import pytest
import json
import time
import shutil
from pathlib import Path
from workspace.uber import UserRegistry, LocationStore, FareCalculator, RideDispatcher


@pytest.fixture
def temp_data_dir(tmp_path):
    """Provide a temporary data directory for tests."""
    return str(tmp_path / "uber_data")


@pytest.fixture
def user_registry(temp_data_dir):
    """Provide a UserRegistry instance."""
    return UserRegistry(temp_data_dir)


@pytest.fixture
def location_store():
    """Provide a LocationStore instance."""
    return LocationStore()


@pytest.fixture
def fare_calculator():
    """Provide a FareCalculator instance."""
    return FareCalculator()


@pytest.fixture
def dispatcher(temp_data_dir):
    """Provide a RideDispatcher instance."""
    return RideDispatcher(temp_data_dir)


class TestUserRegistry:
    """Tests for UserRegistry."""
    
    def test_register_rider(self, user_registry):
        """Test registering a rider."""
        rider_id = user_registry.register_rider("Alice", "credit_card")
        assert rider_id is not None
        assert isinstance(rider_id, str)
        
        rider = user_registry.get_rider(rider_id)
        assert rider is not None
        assert rider["name"] == "Alice"
        assert rider["payment_method"] == "credit_card"
    
    def test_register_driver(self, user_registry):
        """Test registering a driver."""
        driver_id = user_registry.register_driver("Bob", "ABC123", "uber_x")
        assert driver_id is not None
        assert isinstance(driver_id, str)
        
        driver = user_registry.get_driver(driver_id)
        assert driver is not None
        assert driver["name"] == "Bob"
        assert driver["license_plate"] == "ABC123"
        assert driver["vehicle_type"] == "uber_x"
        assert driver["available"] is True
    
    def test_get_nonexistent_rider(self, user_registry):
        """Test getting a nonexistent rider."""
        assert user_registry.get_rider("nonexistent") is None
    
    def test_get_nonexistent_driver(self, user_registry):
        """Test getting a nonexistent driver."""
        assert user_registry.get_driver("nonexistent") is None
    
    def test_list_drivers_all(self, user_registry):
        """Test listing all drivers."""
        driver1 = user_registry.register_driver("Bob", "ABC123", "uber_x")
        driver2 = user_registry.register_driver("Charlie", "XYZ789", "uber_xl")
        
        drivers = user_registry.list_drivers()
        assert len(drivers) == 2
    
    def test_list_drivers_by_vehicle_type(self, user_registry):
        """Test listing drivers filtered by vehicle type."""
        user_registry.register_driver("Bob", "ABC123", "uber_x")
        user_registry.register_driver("Charlie", "XYZ789", "uber_xl")
        user_registry.register_driver("Dave", "DEF456", "uber_x")
        
        uber_x_drivers = user_registry.list_drivers(vehicle_type="uber_x")
        assert len(uber_x_drivers) == 2
        assert all(d["vehicle_type"] == "uber_x" for d in uber_x_drivers)
        
        uber_xl_drivers = user_registry.list_drivers(vehicle_type="uber_xl")
        assert len(uber_xl_drivers) == 1
        assert uber_xl_drivers[0]["vehicle_type"] == "uber_xl"
    
    def test_list_drivers_available_only(self, user_registry):
        """Test listing only available drivers."""
        driver1 = user_registry.register_driver("Bob", "ABC123", "uber_x")
        driver2 = user_registry.register_driver("Charlie", "XYZ789", "uber_x")
        
        # Mark one as unavailable
        user_registry.set_driver_available(driver1, False)
        
        available = user_registry.list_drivers(available_only=True)
        assert len(available) == 1
        assert available[0]["id"] == driver2
    
    def test_set_driver_available(self, user_registry):
        """Test setting driver availability."""
        driver_id = user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        driver = user_registry.get_driver(driver_id)
        assert driver["available"] is True
        
        user_registry.set_driver_available(driver_id, False)
        driver = user_registry.get_driver(driver_id)
        assert driver["available"] is False
        
        user_registry.set_driver_available(driver_id, True)
        driver = user_registry.get_driver(driver_id)
        assert driver["available"] is True
    
    def test_persistence_across_reload(self, temp_data_dir):
        """Test that data persists across UserRegistry reloads."""
        # Create and populate registry
        registry1 = UserRegistry(temp_data_dir)
        rider_id = registry1.register_rider("Alice", "credit_card")
        driver_id = registry1.register_driver("Bob", "ABC123", "uber_x")
        
        # Create new registry instance (simulating reload)
        registry2 = UserRegistry(temp_data_dir)
        
        # Verify data persisted
        assert registry2.get_rider(rider_id) is not None
        assert registry2.get_rider(rider_id)["name"] == "Alice"
        assert registry2.get_driver(driver_id) is not None
        assert registry2.get_driver(driver_id)["name"] == "Bob"


class TestLocationStore:
    """Tests for LocationStore."""
    
    def test_update_and_get_location(self, location_store):
        """Test updating and retrieving driver location."""
        location_store.update_driver_location("driver1", 40.7128, -74.0060, time.time())
        
        loc = location_store.get_driver_location("driver1")
        assert loc is not None
        assert loc["lat"] == 40.7128
        assert loc["lng"] == -74.0060
    
    def test_get_nonexistent_location(self, location_store):
        """Test getting location for driver with no location."""
        assert location_store.get_driver_location("nonexistent") is None
    
    def test_haversine_distance(self):
        """Test haversine distance calculation."""
        # New York to Los Angeles (approximately 3944 km)
        distance = LocationStore.haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
        assert 3900 < distance < 4000
    
    def test_nearby_drivers_empty(self, location_store):
        """Test nearby_drivers with no drivers."""
        nearby = location_store.nearby_drivers(40.7128, -74.0060, 10.0, drivers_list=[])
        assert nearby == []
    
    def test_nearby_drivers_sorting_by_distance(self, location_store):
        """Test that nearby_drivers are sorted by distance."""
        # Create mock drivers
        drivers = [
            {"id": "driver1", "vehicle_type": "uber_x"},
            {"id": "driver2", "vehicle_type": "uber_x"},
            {"id": "driver3", "vehicle_type": "uber_x"}
        ]
        
        # Update locations (driver2 is closest, driver3 is farthest)
        location_store.update_driver_location("driver1", 40.7200, -74.0100, time.time())
        location_store.update_driver_location("driver2", 40.7130, -74.0061, time.time())
        location_store.update_driver_location("driver3", 40.7000, -74.0000, time.time())
        
        nearby = location_store.nearby_drivers(40.7128, -74.0060, 100.0, drivers_list=drivers)
        
        assert len(nearby) == 3
        # driver2 should be first (closest)
        assert nearby[0][0]["id"] == "driver2"
        # driver1 should be second
        assert nearby[1][0]["id"] == "driver1"
        # driver3 should be last (farthest)
        assert nearby[2][0]["id"] == "driver3"
    
    def test_nearby_drivers_respects_radius(self, location_store):
        """Test that nearby_drivers respects the radius parameter."""
        drivers = [
            {"id": "driver1", "vehicle_type": "uber_x"},
            {"id": "driver2", "vehicle_type": "uber_x"}
        ]
        
        # driver1 is close, driver2 is far
        location_store.update_driver_location("driver1", 40.7130, -74.0061, time.time())
        location_store.update_driver_location("driver2", 40.0000, -74.0000, time.time())
        
        # Search with small radius
        nearby = location_store.nearby_drivers(40.7128, -74.0060, 1.0, drivers_list=drivers)
        assert len(nearby) == 1
        assert nearby[0][0]["id"] == "driver1"
        
        # Search with large radius
        nearby = location_store.nearby_drivers(40.7128, -74.0060, 100.0, drivers_list=drivers)
        assert len(nearby) == 2
    
    def test_nearby_drivers_respects_vehicle_type_filter(self, location_store):
        """Test that nearby_drivers respects vehicle_type filter."""
        drivers = [
            {"id": "driver1", "vehicle_type": "uber_x"},
            {"id": "driver2", "vehicle_type": "uber_xl"},
            {"id": "driver3", "vehicle_type": "uber_x"}
        ]
        
        location_store.update_driver_location("driver1", 40.7130, -74.0061, time.time())
        location_store.update_driver_location("driver2", 40.7130, -74.0061, time.time())
        location_store.update_driver_location("driver3", 40.7130, -74.0061, time.time())
        
        # Filter by uber_x
        nearby = location_store.nearby_drivers(
            40.7128, -74.0060, 100.0,
            vehicle_type="uber_x",
            drivers_list=drivers
        )
        assert len(nearby) == 2
        assert all(d[0]["vehicle_type"] == "uber_x" for d in nearby)
        
        # Filter by uber_xl
        nearby = location_store.nearby_drivers(
            40.7128, -74.0060, 100.0,
            vehicle_type="uber_xl",
            drivers_list=drivers
        )
        assert len(nearby) == 1
        assert nearby[0][0]["vehicle_type"] == "uber_xl"
    
    def test_nearby_drivers_skips_missing_locations(self, location_store):
        """Test that nearby_drivers gracefully skips drivers without location."""
        drivers = [
            {"id": "driver1", "vehicle_type": "uber_x"},
            {"id": "driver2", "vehicle_type": "uber_x"},  # No location
            {"id": "driver3", "vehicle_type": "uber_x"}
        ]
        
        location_store.update_driver_location("driver1", 40.7130, -74.0061, time.time())
        # driver2 has no location
        location_store.update_driver_location("driver3", 40.7130, -74.0061, time.time())
        
        nearby = location_store.nearby_drivers(40.7128, -74.0060, 100.0, drivers_list=drivers)
        assert len(nearby) == 2
        assert all(d[0]["id"] != "driver2" for d in nearby)


class TestFareCalculator:
    """Tests for FareCalculator."""
    
    def test_estimate_uber_x(self, fare_calculator):
        """Test fare estimation for uber_x."""
        fare = fare_calculator.estimate(10.0, 20.0, "uber_x")
        
        assert fare["base"] == 2.50
        assert fare["per_km"] == 12.50  # 10 * 1.25
        assert fare["per_min"] == 5.00  # 20 * 0.25
        assert fare["surge"] == 0.0  # No surge
        assert fare["total"] == 20.00
    
    def test_estimate_uber_xl(self, fare_calculator):
        """Test fare estimation for uber_xl."""
        fare = fare_calculator.estimate(10.0, 20.0, "uber_xl")
        
        assert fare["base"] == 3.50
        assert fare["per_km"] == 17.50  # 10 * 1.75
        assert fare["per_min"] == 7.00  # 20 * 0.35
        assert fare["surge"] == 0.0
        assert fare["total"] == 28.00
    
    def test_estimate_uber_black(self, fare_calculator):
        """Test fare estimation for uber_black."""
        fare = fare_calculator.estimate(10.0, 20.0, "uber_black")
        
        assert fare["base"] == 5.00
        assert fare["per_km"] == 25.00  # 10 * 2.50
        assert fare["per_min"] == 10.00  # 20 * 0.50
        assert fare["surge"] == 0.0
        assert fare["total"] == 40.00
    
    def test_estimate_with_surge(self, fare_calculator):
        """Test fare estimation with surge multiplier."""
        fare = fare_calculator.estimate(10.0, 20.0, "uber_x", surge_multiplier=2.0)
        
        # Base calculation: 2.50 + 12.50 + 5.00 = 20.00
        # Surge: 20.00 * (2.0 - 1.0) = 20.00
        # Total: 20.00 + 20.00 = 40.00
        assert fare["total"] == 40.00
        assert fare["surge"] == 20.00
    
    def test_estimate_surge_clamping(self, fare_calculator):
        """Test that surge multiplier is clamped to [1.0, 5.0]."""
        # Too low
        with pytest.raises(ValueError):
            fare_calculator.estimate(10.0, 20.0, "uber_x", surge_multiplier=0.5)
        
        # Too high
        with pytest.raises(ValueError):
            fare_calculator.estimate(10.0, 20.0, "uber_x", surge_multiplier=5.5)
        
        # Valid boundaries
        fare = fare_calculator.estimate(10.0, 20.0, "uber_x", surge_multiplier=1.0)
        assert fare["surge"] == 0.0
        
        fare = fare_calculator.estimate(10.0, 20.0, "uber_x", surge_multiplier=5.0)
        assert fare["surge"] > 0.0
    
    def test_estimate_negative_distance(self, fare_calculator):
        """Test that negative distance raises error."""
        with pytest.raises(ValueError):
            fare_calculator.estimate(-5.0, 20.0, "uber_x")
    
    def test_estimate_negative_duration(self, fare_calculator):
        """Test that negative duration raises error."""
        with pytest.raises(ValueError):
            fare_calculator.estimate(10.0, -5.0, "uber_x")
    
    def test_estimate_invalid_vehicle_type(self, fare_calculator):
        """Test that invalid vehicle type raises error."""
        with pytest.raises(ValueError):
            fare_calculator.estimate(10.0, 20.0, "invalid_type")
    
    def test_estimate_zero_distance_and_duration(self, fare_calculator):
        """Test fare with zero distance and duration."""
        fare = fare_calculator.estimate(0.0, 0.0, "uber_x")
        assert fare["base"] == 2.50
        assert fare["per_km"] == 0.0
        assert fare["per_min"] == 0.0
        assert fare["total"] == 2.50


class TestRideDispatcher:
    """Tests for RideDispatcher."""
    
    def test_request_ride_happy_path(self, dispatcher):
        """Test requesting a ride with available driver."""
        # Register rider and driver
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        # Set driver location
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        # Request ride
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,  # pickup
            40.7200, -74.0100,  # dropoff
            "uber_x"
        )
        
        assert ride["status"] == "matched"
        assert ride["matched_driver_id"] == driver_id
        assert ride["eta_min"] is not None
        assert ride["fare_estimate"] is not None
        assert ride["fare_estimate"]["total"] > 0
    
    def test_request_ride_no_drivers_available(self, dispatcher):
        """Test requesting a ride when no drivers are available."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        assert ride["status"] == "no_drivers"
        assert ride["matched_driver_id"] is None
        assert ride["eta_min"] is None
        assert ride["fare_estimate"] is None
    
    def test_request_ride_no_drivers_in_range(self, dispatcher):
        """Test requesting a ride when no drivers are within range."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        # Set driver location far away (Los Angeles)
        dispatcher.location_store.update_driver_location(driver_id, 34.0522, -118.2437, time.time())
        
        # Request ride in New York
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        assert ride["status"] == "no_drivers"
        assert ride["matched_driver_id"] is None
    
    def test_request_ride_wrong_vehicle_type(self, dispatcher):
        """Test requesting a ride when no drivers of correct type are available."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_xl")
        
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        # Request uber_x but only uber_xl available
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        assert ride["status"] == "no_drivers"
    
    def test_request_ride_marks_driver_unavailable(self, dispatcher):
        """Test that requesting a ride marks the driver as unavailable."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        # Verify driver is available
        driver = dispatcher.user_registry.get_driver(driver_id)
        assert driver["available"] is True
        
        # Request ride
        dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        # Verify driver is now unavailable
        driver = dispatcher.user_registry.get_driver(driver_id)
        assert driver["available"] is False
    
    def test_request_ride_matches_closest_driver(self, dispatcher):
        """Test that request_ride matches the closest available driver."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver1_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        driver2_id = dispatcher.user_registry.register_driver("Charlie", "XYZ789", "uber_x")
        
        # driver1 is far, driver2 is close
        dispatcher.location_store.update_driver_location(driver1_id, 40.6000, -74.0000, time.time())
        dispatcher.location_store.update_driver_location(driver2_id, 40.7130, -74.0061, time.time())
        
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        # Should match driver2 (closest)
        assert ride["matched_driver_id"] == driver2_id
    
    def test_complete_ride_frees_driver(self, dispatcher):
        """Test that completing a ride frees up the driver."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        # Request ride
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        # Verify driver is unavailable
        driver = dispatcher.user_registry.get_driver(driver_id)
        assert driver["available"] is False
        
        # Complete ride
        dispatcher.complete_ride(ride["id"])
        
        # Verify driver is available again
        driver = dispatcher.user_registry.get_driver(driver_id)
        assert driver["available"] is True
    
    def test_cancel_ride_frees_driver(self, dispatcher):
        """Test that cancelling a ride frees up the driver."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        # Request ride
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        # Verify driver is unavailable
        driver = dispatcher.user_registry.get_driver(driver_id)
        assert driver["available"] is False
        
        # Cancel ride
        dispatcher.cancel_ride(ride["id"])
        
        # Verify driver is available again
        driver = dispatcher.user_registry.get_driver(driver_id)
        assert driver["available"] is True
    
    def test_get_ride(self, dispatcher):
        """Test getting a ride by ID."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        
        retrieved = dispatcher.get_ride(ride["id"])
        assert retrieved is not None
        assert retrieved["id"] == ride["id"]
        assert retrieved["status"] == "matched"
    
    def test_rides_persistence_across_reload(self, temp_data_dir):
        """Test that rides persist across RideDispatcher reloads."""
        # Create dispatcher and request ride
        dispatcher1 = RideDispatcher(temp_data_dir)
        rider_id = dispatcher1.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher1.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        dispatcher1.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        ride = dispatcher1.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        ride_id = ride["id"]
        
        # Create new dispatcher instance (simulating reload)
        dispatcher2 = RideDispatcher(temp_data_dir)
        
        # Verify ride persisted
        retrieved = dispatcher2.get_ride(ride_id)
        assert retrieved is not None
        assert retrieved["id"] == ride_id
        assert retrieved["status"] == "matched"


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_negative_coordinates(self, dispatcher):
        """Test that negative coordinates are handled."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        driver_id = dispatcher.user_registry.register_driver("Bob", "ABC123", "uber_x")
        
        # Negative coordinates are valid (Southern/Western hemispheres)
        dispatcher.location_store.update_driver_location(driver_id, -33.8688, 151.2093, time.time())
        
        ride = dispatcher.request_ride(
            rider_id,
            -33.8688, 151.2093,
            -33.8700, 151.2100,
            "uber_x"
        )
        
        assert ride["status"] == "matched"
    
    def test_invalid_vehicle_type_in_request(self, dispatcher):
        """Test requesting a ride with invalid vehicle type."""
        rider_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        
        # Should return no_drivers for invalid vehicle type
        ride = dispatcher.request_ride(
            rider_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "invalid_type"
        )
        
        assert ride["status"] == "no_drivers"
    
    def test_multiple_rides_same_driver(self, dispatcher):
        """Test that a driver can't be matched to multiple rides simultaneously."""
        rider1_id = dispatcher.user_registry.register_rider("Alice", "credit_card")
        rider2_id = dispatcher.user_registry.register_rider("Bob", "debit_card")
        driver_id = dispatcher.user_registry.register_driver("Charlie", "ABC123", "uber_x")
        
        dispatcher.location_store.update_driver_location(driver_id, 40.7128, -74.0060, time.time())
        
        # First ride request
        ride1 = dispatcher.request_ride(
            rider1_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        assert ride1["status"] == "matched"
        assert ride1["matched_driver_id"] == driver_id
        
        # Second ride request should fail (driver unavailable)
        ride2 = dispatcher.request_ride(
            rider2_id,
            40.7128, -74.0060,
            40.7200, -74.0100,
            "uber_x"
        )
        assert ride2["status"] == "no_drivers"
