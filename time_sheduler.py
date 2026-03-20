import time
import subprocess
import sys
import data_collector
import json_to_db

def start_services():
    python_exec = sys.executable 
    
    print("Starting API server...")
    api_process = subprocess.Popen([
        python_exec, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"
    ])
    
    print("Starting Frontend...")
    # Naprawiony parametr subprocess dla srodowiska macOS
    frontend_process = subprocess.Popen(
        "npm run dev -- --host 0.0.0.0", 
        shell=True, 
        cwd="frontend"
    )
    
    return api_process, frontend_process

def main():
    api_proc, front_proc = start_services()
    
    try:
        while True:
            try:
                print("Fetching data from Blizzard API...")
                data_collector.save()
                json_to_db.toDB()
            except Exception as e:
                print(f"Error {e}")
                
            print("Waiting 15 min")
            time.sleep(900)
            
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        api_proc.terminate()
        front_proc.terminate()

if __name__ == "__main__":
    main()