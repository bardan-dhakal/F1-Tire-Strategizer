"""
Real-time tire image monitor for Raspberry Pi API
Continuously polls for new tire images and downloads them automatically
"""
import requests
import time
import os
import json
from datetime import datetime
from typing import Set, Dict, List
from pi_api_client import PiTireAPIClient
from main import cron_job

class TireImageMonitor:
    def __init__(self, poll_interval: int = 15, base_dir: str = "tire_images"):
        """
        Initialize tire image monitor
        
        Args:
            poll_interval: Seconds between API checks (default: 15)
            base_dir: Directory to save images (default: "tire_images")
        """
        self.client = PiTireAPIClient()
        self.poll_interval = poll_interval
        self.base_dir = base_dir
        self.downloaded_images: Set[str] = set()
        self.last_stats = None
        
        # Create directories
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(f"{self.base_dir}/logs", exist_ok=True)
        
        # Load previous downloads if exists
        self.load_download_history()
        
        print(f"✓ Monitor initialized - checking every {poll_interval}s")
        print(f"✓ Images will be saved to: {self.base_dir}/")
        print(f"✓ Previously downloaded: {len(self.downloaded_images)} images")
    
    def load_download_history(self):
        """Load previously downloaded image keys"""
        history_file = f"{self.base_dir}/logs/download_history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.downloaded_images = set(data.get('downloaded', []))
                    print(f"✓ Loaded download history: {len(self.downloaded_images)} images")
            except Exception as e:
                print(f"⚠ Could not load history: {e}")
                self.downloaded_images = set()
    
    def save_download_history(self):
        """Save downloaded image keys"""
        history_file = f"{self.base_dir}/logs/download_history.json"
        try:
            data = {
                'downloaded': list(self.downloaded_images),
                'last_updated': datetime.now().isoformat(),
                'total_count': len(self.downloaded_images)
            }
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠ Could not save history: {e}")
    
    def get_new_images(self) -> List[Dict]:
        """Get list of new images not yet downloaded"""
        try:
            all_tires = self.client.list_all_tires()
            if not all_tires:
                return []
            
            new_images = []
            for lap, tires in all_tires['tiresByLap'].items():
                for tire in tires:
                    tire_key = tire['key']
                    if tire_key not in self.downloaded_images:
                        new_images.append(tire)
            
            return new_images
            
        except Exception as e:
            print(f"⚠ Error checking for new images: {e}")
            return []
    
    def download_image(self, tire_data: Dict) -> bool:
        """Download a single tire image"""
        try:
            tire_key = tire_data['key']
            position = tire_data['position']
            lap = tire_key.split('/')[0].replace('lap_', '')
            
            # Create lap directory
            lap_dir = f"{self.base_dir}/lap_{lap}"
            os.makedirs(lap_dir, exist_ok=True)
            
            # Download image
            image_bytes = self.client.get_tire_image(tire_key)
            if not image_bytes:
                return False
            
            # Save image
            filename = f"tire_{position}.jpg"
            filepath = f"{lap_dir}/{filename}"
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            # Mark as downloaded
            self.downloaded_images.add(tire_key)
            
            # Log the download
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'key': tire_key,
                'lap': lap,
                'position': position,
                'size': len(image_bytes),
                'filepath': filepath
            }
            
            self.log_download(log_entry)
            print(f"✓ Downloaded: {tire_key} -> {filepath}")
            
            return True
            
        except Exception as e:
            print(f"⚠ Error downloading {tire_key}: {e}")
            return False
    
    def log_download(self, log_entry: Dict):
        """Log download activity"""
        log_file = f"{self.base_dir}/logs/downloads.log"
        try:
            with open(log_file, 'a') as f:
                f.write(f"{json.dumps(log_entry)}\n")
        except Exception as e:
            print(f"⚠ Could not log download: {e}")
    
    def print_status(self):
        """Print current monitoring status"""
        try:
            stats = self.client.get_stats()
            if stats:
                print(f"\n📊 API Status:")
                print(f"   Total tires on server: {stats['stats']['totalTires']}")
                print(f"   Total downloaded: {len(self.downloaded_images)}")
                print(f"   Available laps: {stats['laps']}")
                print(f"   Storage size: {stats['formattedSize']}")
        except Exception as e:
            print(f"⚠ Could not get API stats: {e}")
    
    def run_once(self):
        """Run one check cycle"""
        print(f"\n🔍 [{datetime.now().strftime('%H:%M:%S')}] Checking for new images...")
        
        new_images = self.get_new_images()
        
        if new_images:
            print(f"📥 Found {len(new_images)} new images!")
            for tire_data in new_images:
                self.download_image(tire_data)
            
            # Save updated history
            self.save_download_history()
            cron_job()
        else:
            print("✓ No new images found")
        
        self.print_status()
    
    def run_continuous(self):
        """Run continuous monitoring"""
        print(f"\n🚀 Starting continuous monitoring...")
        print(f"   Poll interval: {self.poll_interval} seconds")
        print(f"   Press Ctrl+C to stop")
        print("="*60)
        
        try:
            while True:
                self.run_once()
                
                print(f"\n⏳ Waiting {self.poll_interval}s until next check...")
                time.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Monitoring stopped by user")
            print(f"✓ Final count: {len(self.downloaded_images)} images downloaded")
            self.save_download_history()
            print("✓ Download history saved")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("F1 TIRE IMAGE MONITOR")
    print("="*60)
    
    # Initialize monitor with 15-second intervals
    monitor = TireImageMonitor(poll_interval=15)
    
    # Show initial status
    monitor.print_status()
    
    # Start continuous monitoring
    monitor.run_continuous()