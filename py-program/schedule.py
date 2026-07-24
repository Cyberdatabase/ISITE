import time
import schedule


# Define the tasks you want to run
def take_photo():
    print("[INFO] Taking camera snapshot...")
    # Add your Pi Camera code here


def read_sensors():
    print("[INFO] Reading temperature and humidity sensors...")
    # Add your DHT11/BMP280 sensor code here


def system_cleanup():
    print("[INFO] Running daily system cleanup logs...")


# --- Schedule the Tasks ---

# Task 1: Read sensors every 10 seconds
schedule.every(10).seconds.do(read_sensors)

# Task 2: Take a photo every hour
schedule.every(1).hours.do(take_photo)

# Task 3: Run system cleanup every day at midnight
schedule.every().day.at("00:00").do(system_cleanup)

print("Raspberry Pi Scheduler Started. Press Ctrl+C to exit.")

# --- The Main Loop ---
try:
    while True:
        # Checks if any scheduled task is ready to run
        schedule.run_pending()
        # Sleep for 1 second to prevent high CPU usage
        time.sleep(1)
except KeyboardInterrupt:
    print("\nScheduler stopped safely.")

