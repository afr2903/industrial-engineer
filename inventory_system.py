import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class Machine:
    def __init__(self, name, production_rate, failure_rate, repair_rate):
        self.name = name
        self.production_rate = production_rate
        self.failure_rate = failure_rate
        self.repair_rate = repair_rate
        self.status = "operational"

    def operate(self):
        if self.status == "operational":
            if random.random() < self.failure_rate:
                self.status = "failed"
                return 0
            return self.production_rate
        else:
            if random.random() < self.repair_rate:
                self.status = "operational"
            return 0

class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.level = 0

    def add(self, amount):
        self.level = min(self.level + amount, self.capacity)

    def remove(self, amount):
        removed = min(amount, self.level)
        self.level -= removed
        return removed

class Inventory:
    def __init__(self, initial_level):
        self.level = initial_level

    def add(self, amount):
        self.level += amount

    def remove(self, amount):
        removed = min(amount, self.level)
        self.level -= removed
        return removed

class SimulationEnvironment:
    def __init__(self):
        self.machine1 = Machine("M1", 10, 0.05, 0.2)
        self.machine2 = Machine("M2", 8, 0.03, 0.3)
        self.buffer = Buffer(50)
        self.inventory = Inventory(100)
        self.demand_mean = 7
        self.demand_std = 2

    def step(self):
        production_m1 = self.machine1.operate()
        self.buffer.add(production_m1)

        available_from_buffer = self.buffer.remove(self.machine2.production_rate)
        production_m2 = min(self.machine2.operate(), available_from_buffer)
        self.inventory.add(production_m2)

        demand = max(0, int(np.random.normal(self.demand_mean, self.demand_std)))
        fulfilled_demand = self.inventory.remove(demand)

        return {
            "production_m1": production_m1,
            "production_m2": production_m2,
            "buffer_level": self.buffer.level,
            "inventory_level": self.inventory.level,
            "demand": demand,
            "fulfilled_demand": fulfilled_demand,
            "m1_status": self.machine1.status,
            "m2_status": self.machine2.status
        }

class SimulationUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management Simulation")
        
        self.env = SimulationEnvironment()
        #self.predictor = InventoryPredictor()
        #self.llm = SimpleLLM()
        
        self.history = {
            'inventory_level': [],
            'buffer_level': [],
            'demand': []
        }
        
        self.create_widgets()
        self.create_plot()
        
    def create_widgets(self):
        # Create input fields
        ttk.Label(self.master, text="M1 Production Rate:").grid(row=0, column=0, padx=5, pady=5)
        self.m1_rate = ttk.Entry(self.master)
        self.m1_rate.insert(0, str(self.env.machine1.production_rate))
        self.m1_rate.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.master, text="M2 Production Rate:").grid(row=1, column=0, padx=5, pady=5)
        self.m2_rate = ttk.Entry(self.master)
        self.m2_rate.insert(0, str(self.env.machine2.production_rate))
        self.m2_rate.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.master, text="Buffer Capacity:").grid(row=2, column=0, padx=5, pady=5)
        self.buffer_capacity = ttk.Entry(self.master)
        self.buffer_capacity.insert(0, str(self.env.buffer.capacity))
        self.buffer_capacity.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.master, text="Update", command=self.update_simulation).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Create canvas for machine and buffer visualization
        self.canvas = tk.Canvas(self.master, width=400, height=200)
        self.canvas.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_plot_widget = self.canvas_plot.get_tk_widget()
        self.canvas_plot_widget.grid(row=0, column=2, rowspan=5, padx=10, pady=10)
        
    def update_simulation(self):
        # Update simulation parameters
        self.env.machine1.production_rate = float(self.m1_rate.get())
        self.env.machine2.production_rate = float(self.m2_rate.get())
        self.env.buffer.capacity = int(self.buffer_capacity.get())
        
        # Run simulation for 100 steps
        for _ in range(100):
            state = self.env.step()
            self.history['inventory_level'].append(state['inventory_level'])
            self.history['buffer_level'].append(state['buffer_level'])
            self.history['demand'].append(state['demand'])
        
        self.update_plot()
        self.update_visualization()
        
    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.history['inventory_level'][-100:], label='Inventory')
        self.ax.plot(self.history['buffer_level'][-100:], label='Buffer')
        self.ax.plot(self.history['demand'][-100:], label='Demand')
        self.ax.legend()
        self.ax.set_title('Inventory Management Simulation')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Level')
        self.canvas_plot.draw()
        
    def update_visualization(self):
        self.canvas.delete("all")
        
        # Draw machines
        self.canvas.create_rectangle(50, 50, 100, 100, fill="green" if self.env.machine1.status == "operational" else "red")
        self.canvas.create_text(75, 120, text="M1")
        self.canvas.create_rectangle(300, 50, 350, 100, fill="green" if self.env.machine2.status == "operational" else "red")
        self.canvas.create_text(325, 120, text="M2")
        
        # Draw buffer
        buffer_fill = self.env.buffer.level / self.env.buffer.capacity
        self.canvas.create_rectangle(150, 50, 250, 100, outline="black")
        self.canvas.create_rectangle(150, 100 - buffer_fill * 50, 250, 100, fill="blue")
        self.canvas.create_text(200, 120, text=f"Buffer: {self.env.buffer.level}/{self.env.buffer.capacity}")
        
        # Draw inventory
        self.canvas.create_text(200, 150, text=f"Inventory: {self.env.inventory.level}")
        
    def run(self):
        self.update_simulation()
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationUI(root)
    app.run()