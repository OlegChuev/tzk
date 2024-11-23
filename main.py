import time
from time import localtime, strftime
import os
from dotenv import load_dotenv
import psutil
import thingspeak

# Load environment variables from a .env file
load_dotenv()

# Constants for Thingspeak configuration
CHANNEL_ID = os.getenv('CHANNEL_ID')
WRITE_API_KEY = os.getenv('WRITE_API_KEY')

def update_channel(channel):
    """
    Update the ThingSpeak channel with system metrics.

    Args:
        channel (thingspeak.Channel): The ThingSpeak channel object.
    """
    # Collect system metrics: CPU usage and memory usage percentage
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    try:
        # Send data to ThingSpeak
        response = channel.update({1: cpu_usage, 2: memory_usage})

        # Log data and response
        print(f"CPU Usage (%): {cpu_usage}")
        print(f"Memory Usage (%): {memory_usage}")
        print(f"Timestamp: {strftime('%a, %d %b %Y %H:%M:%S', localtime())}")
        print(f"ThingSpeak Response: {response}")
    except Exception as e:
        # Handle connection or API errors
        print(f"Connection failed: {e}")

def main():
    """
    Main loop to periodically send system metrics to ThingSpeak.
    """
    # Initialize the ThingSpeak channel
    channel = thingspeak.Channel(id=CHANNEL_ID, api_key=WRITE_API_KEY)

    if not CHANNEL_ID or not WRITE_API_KEY:
        raise ValueError("CHANNEL_ID and WRITE_API_KEY must be set in the environment variables.")

    # Infinite loop to update metrics every 16 seconds
    while True:
        update_channel(channel)
        time.sleep(16)  # Adhere to ThingSpeak's API rate limit (15 seconds minimum)

if __name__ == "__main__":
    # Run the main program
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")