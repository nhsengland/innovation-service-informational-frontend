import subprocess
import re
import time

BASE_URL = "http://localhost:8000"

def get_header(url, cookies_file=None):
    cmd = ["curl", "-s", "-I", "-L"]
    if cookies_file:
        cmd.extend(["-b", cookies_file, "-c", cookies_file])
    cmd.append(f"{BASE_URL}{url}")
    
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
    with open("all_urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Add search queries
    urls.append("/search/?query=Dummy")
    urls.append("/search/?query=Innovation")
    urls.append("/search/?query=Generic")
    
    print(f"{'URL':<60} | {'Req 1':<8} | {'Req 2':<8} | {'Req 3':<8}")
    print("-" * 90)
    
    cookies_file = "test_cookies.txt"
    # Clear cookies for a fresh start
    open(cookies_file, "w").close()
    
    for url in urls:
        # Request 1: Prime (often skip/miss)
        res1 = get_header(url, cookies_file)
        time.sleep(0.1)
        
        # Request 2: Miss (if prime was skip) or Hit (if prime was miss)
        res2 = get_header(url, cookies_file)
        time.sleep(0.1)
        
        # Request 3: Hit (should be hit)
        res3 = get_header(url, cookies_file)
        
        print(f"{url[:58]:<60} | {res1:<8} | {res2:<8} | {res3:<8}")

if __name__ == "__main__":
    run_tests()
