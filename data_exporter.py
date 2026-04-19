import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

class DataExporter:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_data(self, target_url):
        """Website se HTML data fetch karne ka professional method."""
        try:
            print(f"\n[INFO] Connecting to: {target_url}")
            response = requests.get(target_url, headers=self.headers, timeout=10)
            response.raise_for_status() # Agar link ghalat ho toh error handle karega
            return response.text
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return None

    def parse_and_save(self, html_content, filename):
        """Data ko extract karke CSV mein convert karne ki logic."""
        soup = BeautifulSoup(html_content, 'html.parser')
        extracted_data = []

        # Professional Logic: Hum saare headings (h1 to h3) aur unke links uthayenge
        tags = soup.find_all(['h1', 'h2', 'h3'])
        
        for tag in tags:
            text = tag.get_text().strip()
            link = tag.find('a')['href'] if tag.find('a') else "No Link Found"
            
            if text:
                extracted_data.append({"Content": text, "Source_URL": link})

        if extracted_data:
            df = pd.DataFrame(extracted_data)
            # File name ke saath date lagana professional touch hai
            final_name = f"{filename}_{datetime.now().strftime('%d%m%Y')}.csv"
            df.to_csv(final_name, index=False)
            print(f"[SUCCESS] Data exported successfully to: {final_name}")
        else:
            print("[WARNING] No relevant data found on this page.")

# --- Main Program ---
if __name__ == "__main__":
    exporter = DataExporter()
    
    print("=== SHAHZAD PROFESSIONAL DATA EXPORTER ===")
    user_url = input("Enter the Website URL to scrape: ").strip()
    user_filename = input("Enter output filename (without extension): ").strip()

    if user_url.startswith("http"):
        content = exporter.fetch_data(user_url)
        if content:
            exporter.parse_and_save(content, user_filename)
    else:
        print("[ERROR] Invalid URL. Please include http:// or https://")