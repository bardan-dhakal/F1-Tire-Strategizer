"""
Client to access tire images from Raspberry Pi backend API
"""
import requests
from typing import List, Dict, Optional

class PiTireAPIClient:
    """
    Client for accessing tire images from your friend's Raspberry Pi API
    """
    
    def __init__(self, base_url: str = "https://sweet-rice-0766.zaineel-s-mithani.workers.dev"):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the Raspberry Pi API
        """
        self.base_url = base_url.rstrip('/')
        print(f"✓ API Client initialized: {self.base_url}")
    
    def list_all_tires(self) -> Optional[Dict]:
        """
        Get list of all tire images across all laps
        
        Returns:
            {
                "totalTires": 8,
                "laps": ["1", "2"],
                "tiresByLap": {
                    "1": [{"key": "...", "position": "..."}, ...],
                    "2": [...]
                }
            }
        """
        try:
            url = f"{self.base_url}/api/tires/list"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error listing all tires: {e}")
            return None
    
    def list_tires_by_lap(self, lap_number: int) -> Optional[Dict]:
        """
        Get tire images for a specific lap
        
        Args:
            lap_number: Lap number (1, 2, 3, ...)
            
        Returns:
            {
                "totalTires": 4,
                "laps": ["1"],
                "tiresByLap": {
                    "1": [
                        {"key": "lap_1/tire_front_left.jpg", "position": "front_left", ...},
                        {"key": "lap_1/tire_front_right.jpg", "position": "front_right", ...},
                        ...
                    ]
                }
            }
        """
        try:
            url = f"{self.base_url}/api/tires/list?lap={lap_number}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error listing tires for lap {lap_number}: {e}")
            return None
    
    def get_tire_image(self, tire_key: str) -> Optional[bytes]:
        """
        Download tire image by key
        
        Args:
            tire_key: Image key (e.g., "lap_1/tire_front_left.jpg")
            
        Returns:
            Image bytes or None
        """
        try:
            # URL encode the key
            import urllib.parse
            encoded_key = urllib.parse.quote(tire_key, safe='')
            
            url = f"{self.base_url}/api/tires/get/{encoded_key}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            image_bytes = response.content
            print(f"✓ Downloaded {tire_key} ({len(image_bytes)} bytes)")
            return image_bytes
            
        except Exception as e:
            print(f"Error downloading {tire_key}: {e}")
            return None
    
    def get_tire_url(self, tire_key: str) -> str:
        """
        Get direct URL to tire image (for displaying in frontend)
        
        Args:
            tire_key: Image key
            
        Returns:
            Full URL to image
        """
        import urllib.parse
        encoded_key = urllib.parse.quote(tire_key, safe='')
        return f"{self.base_url}/api/tires/get/{encoded_key}"
    
    def get_stats(self) -> Optional[Dict]:
        """
        Get storage statistics
        
        Returns:
            {
                "stats": {
                    "totalTires": 8,
                    "totalSize": 567890,
                    "byLap": {"1": 4, "2": 4},
                    "byPosition": {...}
                },
                "formattedSize": "554.58 KB",
                "laps": ["1", "2"]
            }
        """
        try:
            url = f"{self.base_url}/api/stats"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting stats: {e}")
            return None
    
    def get_latest_lap(self) -> Optional[int]:
        """
        Get the most recent lap number with images
        
        Returns:
            Latest lap number or None
        """
        try:
            data = self.list_all_tires()
            if data and 'laps' in data and data['laps']:
                # Laps are strings, convert to int and get max
                laps = [int(lap) for lap in data['laps']]
                return max(laps)
            return None
        except Exception as e:
            print(f"Error getting latest lap: {e}")
            return None
    
    def get_tire_by_position(self, lap_number: int, position: str) -> Optional[Dict]:
        """
        Get specific tire image by lap and position
        
        Args:
            lap_number: Lap number
            position: "front_left", "front_right", "rear_left", "rear_right"
            
        Returns:
            Tire metadata dict or None
        """
        try:
            data = self.list_tires_by_lap(lap_number)
            if not data or 'tiresByLap' not in data:
                return None
            
            lap_key = str(lap_number)
            if lap_key not in data['tiresByLap']:
                return None
            
            tires = data['tiresByLap'][lap_key]
            for tire in tires:
                if tire.get('position') == position:
                    return tire
            
            return None
            
        except Exception as e:
            print(f"Error getting tire at lap {lap_number}, position {position}: {e}")
            return None


# ============================================
# EXAMPLE USAGE & TESTING
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("RASPBERRY PI TIRE API - TEST")
    print("="*60)
    print()
    
    # Initialize client
    client = PiTireAPIClient()
    print()
    
    # Test 1: Get stats
    print("1. Getting storage stats...")
    stats = client.get_stats()
    if stats:
        print(f"✓ Total tires: {stats['stats']['totalTires']}")
        print(f"  Total size: {stats['formattedSize']}")
        print(f"  Laps available: {stats['laps']}")
        print(f"  By lap: {stats['stats']['byLap']}")
    print()
    
    # Test 2: List all tires
    print("2. Listing all tires...")
    all_tires = client.list_all_tires()
    if all_tires:
        print(f"✓ Found {all_tires['totalTires']} tire images")
        print(f"  Laps: {all_tires['laps']}")
        
        for lap, tires in all_tires['tiresByLap'].items():
            print(f"\n  Lap {lap}:")
            for tire in tires:
                print(f"    - {tire['position']}: {tire['key']}")
    print()
    
    # Test 3: Get latest lap
    print("3. Getting latest lap...")
    latest_lap = client.get_latest_lap()
    if latest_lap:
        print(f"✓ Latest lap: {latest_lap}")
    print()
    
    # Test 4: Get tires for specific lap
    if latest_lap:
        print(f"4. Getting tires for lap {latest_lap}...")
        lap_data = client.list_tires_by_lap(latest_lap)
        if lap_data:
            print(f"✓ Found {lap_data['totalTires']} tires for lap {latest_lap}")
            
            # Get first tire
            tires = lap_data['tiresByLap'][str(latest_lap)]
            if tires:
                first_tire = tires[0]
                print(f"\n  Downloading first tire: {first_tire['key']}")
                
                # Download image
                image_bytes = client.get_tire_image(first_tire['key'])
                
                if image_bytes:
                    # Save to temp
                    import os
                    os.makedirs('tire_images', exist_ok=True)
                    output_path = f"tire_images/{first_tire['key'].replace('/', '_')}"
                    
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    
                    print(f"  ✓ Saved to: {output_path}")
                    
                    # Verify it's a valid image
                    try:
                        from PIL import Image
                        import io
                        img = Image.open(io.BytesIO(image_bytes))
                        print(f"  ✓ Valid image: {img.size[0]}x{img.size[1]} pixels")
                    except:
                        print("  ⚠ Could not verify image format")
    
    print()
    print("="*60)
    print("TEST COMPLETE")
    print("="*60)
    print()
    print("API client is working!")
    print()
    print("Next steps:")
    print("  1. Integrate with Gemini: python analyze_from_pi.py")
    print("  2. Build monitoring script: python monitor_new_laps.py")