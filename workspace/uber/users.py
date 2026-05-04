import json
import os
import uuid
from pathlib import Path
from typing import Optional, Dict, List


class UserRegistry:
    """Manages riders and drivers with persistent JSON storage."""
    
    def __init__(self, data_dir: str = "/tmp/uber_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.riders_file = self.data_dir / "riders.json"
        self.drivers_file = self.data_dir / "drivers.json"
        
        # Load existing data or initialize empty
        self.riders = self._load_json(self.riders_file)
        self.drivers = self._load_json(self.drivers_file)
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON from file, return empty dict if file doesn't exist."""
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_json(self, filepath: Path, data: Dict) -> None:
        """Atomically save JSON to file."""
        # Write to temp file first, then rename (atomic on most filesystems)
        temp_file = filepath.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2)
        temp_file.replace(filepath)
    
    def register_rider(self, name: str, payment_method: str) -> str:
        """Register a new rider. Returns rider_id."""
        rider_id = str(uuid.uuid4())
        self.riders[rider_id] = {
            "id": rider_id,
            "name": name,
            "payment_method": payment_method
        }
        self._save_json(self.riders_file, self.riders)
        return rider_id
    
    def register_driver(self, name: str, license_plate: str, vehicle_type: str) -> str:
        """Register a new driver. Returns driver_id."""
        driver_id = str(uuid.uuid4())
        self.drivers[driver_id] = {
            "id": driver_id,
            "name": name,
            "license_plate": license_plate,
            "vehicle_type": vehicle_type,
            "available": True
        }
        self._save_json(self.drivers_file, self.drivers)
        return driver_id
    
    def get_rider(self, rider_id: str) -> Optional[Dict]:
        """Get rider by ID."""
        return self.riders.get(rider_id)
    
    def get_driver(self, driver_id: str) -> Optional[Dict]:
        """Get driver by ID."""
        return self.drivers.get(driver_id)
    
    def list_drivers(self, vehicle_type: Optional[str] = None, available_only: bool = False) -> List[Dict]:
        """List drivers, optionally filtered by vehicle_type and availability."""
        result = []
        for driver in self.drivers.values():
            if vehicle_type and driver["vehicle_type"] != vehicle_type:
                continue
            if available_only and not driver["available"]:
                continue
            result.append(driver)
        return result
    
    def set_driver_available(self, driver_id: str, available: bool) -> None:
        """Set driver availability status."""
        if driver_id in self.drivers:
            self.drivers[driver_id]["available"] = available
            self._save_json(self.drivers_file, self.drivers)
