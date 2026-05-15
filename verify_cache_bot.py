import subprocess
import re
import time

BASE_URL = "http://localhost:8000"

def get_header(url):
    # No cookies used here to simulate bot behavior
    cmd = ["curl", "-s", "-I", "-L", f"{BASE_URL}{url}"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        headers = result.stdout
        match = re.search(r"X-Wagtail-Cache:\s+(\w+)", headers, re.IGNORECASE)
        if match:
            return match.group(1).lower()
        return "none"
    except Exception as e:
        return f"error: {str(e)}"

def run_tests():
    try:
        with open("all_urls.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: all_urls.txt not found.")
        return
    
    # Add search queries
    urls.append("/search/?query=Dummy")
    urls.append("/search/?query=Innovation")
    urls.append("/search/?query=Generic")
    
    print(f"{'URL':<60} | {'Bot Req 1':<10} | {'Bot Req 2':<10} | {'Bot Req 3':<10}")
    print("-" * 95)
    
    for url in urls:
        # Bots do not send cookies back, so every request is a "first" request for that connection
        res1 = get_header(url)
        time.sleep(0.05)
        res2 = get_header(url)
        time.sleep(0.05)
        res3 = get_header(url)
        
        print(f"{url[:58]:<60} | {res1:<10} | {res2:<10} | {res3:<10}")

if __name__ == "__main__":
    run_tests()
