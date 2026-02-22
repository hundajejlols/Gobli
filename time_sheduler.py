import time
import data_collector
import json_to_db

def main():
    while True:
        try:
            data_collector.save()
            json_to_db.toDB()
        except Exception as e:
            print(f'Error {e}')
        print('Waiting 15 min')
        time.sleep(900)
if __name__ == "__main__":
    main()
    