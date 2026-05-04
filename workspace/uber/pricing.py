from typing import Dict


class FareCalculator:
    """Calculates ride fares based on distance, duration, vehicle type, and surge."""
    
    # Pricing rates per vehicle type
    RATES = {
        "uber_x": {
            "base": 2.50,      # Base fare in dollars
            "per_km": 1.25,    # Per kilometer in dollars
            "per_min": 0.25    # Per minute in dollars
        },
        "uber_xl": {
            "base": 3.50,
            "per_km": 1.75,
            "per_min": 0.35
        },
        "uber_black": {
            "base": 5.00,
            "per_km": 2.50,
            "per_min": 0.50
        }
    }
    
    @staticmethod
    def estimate(
        distance_km: float,
        duration_min: float,
        vehicle_type: str,
        surge_multiplier: float = 1.0
    ) -> Dict[str, float]:
        """
        Estimate fare for a ride.
        
        Args:
            distance_km: distance in kilometers (must be non-negative)
            duration_min: duration in minutes (must be non-negative)
            vehicle_type: one of "uber_x", "uber_xl", "uber_black"
            surge_multiplier: surge pricing multiplier (must be in [1.0, 5.0])
        
        Returns:
            Dict with keys: base, per_km, per_min, surge, total
        
        Raises:
            ValueError: if inputs are invalid
        """
        # Validate inputs
        if distance_km < 0:
            raise ValueError("distance_km must be non-negative")
        if duration_min < 0:
            raise ValueError("duration_min must be non-negative")
        if vehicle_type not in FareCalculator.RATES:
            raise ValueError(f"Invalid vehicle_type: {vehicle_type}")
        if not (1.0 <= surge_multiplier <= 5.0):
            raise ValueError("surge_multiplier must be in [1.0, 5.0]")
        
        rates = FareCalculator.RATES[vehicle_type]
        
        # Calculate components
        base_fare = rates["base"]
        distance_fare = rates["per_km"] * distance_km
        duration_fare = rates["per_min"] * duration_min
        
        # Subtotal before surge
        subtotal = base_fare + distance_fare + duration_fare
        
        # Apply surge
        surge_amount = subtotal * (surge_multiplier - 1.0)
        total = subtotal + surge_amount
        
        return {
            "base": round(base_fare, 2),
            "per_km": round(distance_fare, 2),
            "per_min": round(duration_fare, 2),
            "surge": round(surge_amount, 2),
            "total": round(total, 2)
        }
