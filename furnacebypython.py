import time
from PIL import Image

# Define the valve class
class Valve:
    def __init__(self, name):
        self.name = name
        self.is_open = False

    def open(self):
        self.is_open = True
        print(f"{self.name} valve is open.")

    def close(self):
        self.is_open = False
        print(f"{self.name} valve is closed.")

    def check_valve(self):
        if not self.is_open:
            raise Exception(f"Error: {self.name} valve is closed! No flow is allowed.")
        else:
            print(f"{self.name} valve is operational.")
# Define the furnace class
class Furnace :
    def __init__(self):
            self.temperature = 25  # Initial temperature in degrees Celsius
            self.air_valve = Valve("Air")
            self.fuel_valve = Valve("Fuel")
    def update_temperature(self, time_seconds):
        self.temperature = 25 + 0.25 * time_seconds
        print(f"Temperature after {time_seconds} seconds: {self.temperature:.2f}°C")
        self.display_flame()
    def display_flame(self):
        if 25 <= self.temperature <= 100:
            print("Displaying flame 1 (low flame).")
            flame_image = Image.open("flame1.png")
        elif self.temperature > 300:
            print("Displaying flame 2 (high flame).")
            flame_image = Image.open("flame2.png")
        else:
            print("Displaying moderate flame.")
            flame_image = Image.open("flame1.png")  # Default 
    def run(self, duration_seconds):
        try:
            self.air_valve.check_valve()
            self.fuel_valve.check_valve()
            
            for t in range(0, duration_seconds + 1):
                self.update_temperature(t)
                time.sleep(1)
        except Exception as e:
            print(e)

    def show_fuel_valve_status(self):
        if self.fuel_valve.is_open:
            print("Fuel valve is open. Displaying open valve image.")
            valve_image = Image.open("valve_open.png")
        else:
            print("Fuel valve is closed.")
            valve_image = Image.open("valve_closed.png")
        valve_image.show()
# Main execution
if __name__ == "__main__":
    furnace = Furnace()

    # Open the valves
    furnace.air_valve.open()
    furnace.fuel_valve.open()

    # Show the fuel valve status
    furnace.show_fuel_valve_status()

    # Run the furnace for a certain duration (in seconds)
    run_time = 120  # Example: run for 120 seconds
    furnace.run(run_time)