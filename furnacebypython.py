import tkinter as tk
from tkinter import messagebox

class Valve:
    def __init__(self, name):
        self.name = name
        self.is_open = False
    
    def toggle(self):
        self.is_open = not self.is_open

class FurnaceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Furnace Simulation")

        # Set the canvas size based on your image sizes
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(row=0, column=0, columnspan=2)

        # Load images
        self.air_image = tk.PhotoImage(file="airstream.png")
        self.fuel_image = tk.PhotoImage(file="fuel.png")
        self.furnace_image = tk.PhotoImage(file="furnace.png")
        self.closed_image = tk.PhotoImage(file="closed.png")
        self.open_image = tk.PhotoImage(file="open.png")
        self.flame1_image = tk.PhotoImage(file="flame1.png")
        self.flame2_image = tk.PhotoImage(file="flame2.png")

        # Calculate the center positions and spacing
        center_x = self.canvas_width // 2
        furnace_x = center_x
        furnace_y = self.canvas_height // 2

        spacing = 20  # Distance between each image
        valve_to_stream_distance = 50  # Distance between valve and stream images

        air_valve_x = furnace_x - 150 - valve_to_stream_distance
        fuel_valve_x = furnace_x - 150 - valve_to_stream_distance
        air_stream_x = furnace_x - 100 - spacing
        fuel_stream_x = furnace_x - 100 - spacing

        air_valve_y = furnace_y - 50 - spacing
        fuel_valve_y = furnace_y + 50 + spacing

        # Place the furnace image in the center
        self.canvas.create_image(furnace_x, furnace_y, image=self.furnace_image, tags="furnace")

        # Place the streams with valve images above them
        self.canvas.create_image(air_valve_x, air_valve_y, image=self.closed_image, tags="air_valve")
        self.canvas.create_image(air_stream_x, air_valve_y, image=self.air_image, tags="air_stream")
        self.canvas.create_image(fuel_valve_x, fuel_valve_y, image=self.closed_image, tags="fuel_valve")
        self.canvas.create_image(fuel_stream_x, fuel_valve_y, image=self.fuel_image, tags="fuel_stream")

        # Place the initial flame image under the furnace
        flame_y = furnace_y + 100
        self.flame = self.canvas.create_image(furnace_x, flame_y, image=self.flame1_image, tags="flame")

        # Create buttons to control valves
        self.air_valve_button = tk.Button(root, text="Toggle Air Valve", command=self.toggle_air_valve)
        self.fuel_valve_button = tk.Button(root, text="Toggle Fuel Valve", command=self.toggle_fuel_valve)

        self.air_valve_button.grid(row=1, column=0)
        self.fuel_valve_button.grid(row=1, column=1)

        # Temperature Label
        self.temperature_label = tk.Label(root, text="Temperature: 25°C", font=("Arial", 14))
        self.temperature_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Initialize valves and temperature
        self.air_valve = Valve("Air")
        self.fuel_valve = Valve("Fuel")
        self.temperature = 25.0
        self.update_temperature_flag = False

    def toggle_air_valve(self):
        self.air_valve.toggle()
        if self.air_valve.is_open:
            self.canvas.itemconfig("air_valve", image=self.open_image)
        else:
            self.canvas.itemconfig("air_valve", image=self.closed_image)
        self.check_all_valves()

    def toggle_fuel_valve(self):
        self.fuel_valve.toggle()
        if self.fuel_valve.is_open:
            self.canvas.itemconfig("fuel_valve", image=self.open_image)
        else:
            self.canvas.itemconfig("fuel_valve", image=self.closed_image)
        self.check_all_valves()

    def check_all_valves(self):
        if self.air_valve.is_open and self.fuel_valve.is_open:
            # Both valves are open, start temperature increase
            self.update_temperature_flag = True
            self.increase_temperature()
        else:
            # Any valve is closed, reset temperature and show error
            self.update_temperature_flag = False
            self.temperature = 25.0
            self.temperature_label.config(text=f"Temperature: {self.temperature:.2f}°C")
            messagebox.showerror("Error", f"{'Air' if not self.air_valve.is_open else 'Fuel'} valve is closed! Furnace shutting down.")

    def increase_temperature(self):
        if self.update_temperature_flag:
            self.temperature += 0.25
            self.temperature_label.config(text=f"Temperature: {self.temperature:.2f}°C")
            if self.temperature >= 50.0:
                # Replace flame1 with flame2 when temperature reaches 50°C
                self.canvas.itemconfig("flame", image=self.flame2_image)
            else:
                # Ensure flame1 is displayed if temperature is below 50°C
                self.canvas.itemconfig("flame", image=self.flame1_image)
            self.root.after(1000, self.increase_temperature)

# Main application
root = tk.Tk()
app = FurnaceGUI(root)
root.mainloop()
