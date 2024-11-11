import random
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RawMaterialInventory:
    def __init__(self, lead_time, reorder_point, reorder_quantity, max_capacity):
        self.max_capacity = max_capacity
        self.lead_time = lead_time
        self.time_since_last_order = 0
        self.reorder_point = reorder_point
        self.reorder_quantity = reorder_quantity
        self.inventory_position = reorder_quantity
        self.inventory_on_hand = reorder_quantity

    def update(self, demand):
        self.time_since_last_order += 1
        if self.time_since_last_order == self.lead_time:
            self.inventory_on_hand = self.inventory_position
        self.inventory_on_hand -= demand
        self.inventory_position -= demand
        if self.inventory_position <= self.reorder_point:
            self.order()

    def order(self):
        self.inventory_position += self.reorder_quantity
        self.inventory_position = min(self.inventory_position, self.max_capacity)
        self.time_since_last_order = 0

    def set_order_point_and_quantity(self, reorder_point, reorder_quantity):
        self.reorder_point = reorder_point
        self.reorder_quantity = reorder_quantity

class Machine:
    def __init__(self, max_production_rate, mttf, mttr, defect_rate):
        self.max_production_rate = max_production_rate
        self.mttf = mttf
        self.mttr = mttr
        self.defect_rate = defect_rate
        self.production_rate = max_production_rate
        self.status = "operational"
        self.downtime = 0

    def operate(self):
        if self.status == "operational":
            if random.random() < self.mttf:
                self.status = "failed"
                self.downtime = 1
                return 0
            return self.production_rate * (1 - self.defect_rate)
        else:
            self.downtime += 1
            if random.random() < self.mttr:
                self.status = "operational"
            return 0

class Buffer:
    def __init__(self, holding_cost, max_capacity):
        self.holding_cost = holding_cost
        self.max_capacity = max_capacity
        self.capacity = 0

    def add(self, amount):
        self.capacity = min(self.capacity + amount, self.max_capacity)

    def remove(self, amount):
        removed = min(amount, self.capacity)
        self.capacity -= removed
        return removed

class ProducedGoods:
    def __init__(self, holding_cost, max_capacity, selling_cost):
        self.holding_cost = holding_cost
        self.max_capacity = max_capacity
        self.selling_cost = selling_cost
        self.capacity = 0

    def add(self, amount):
        self.capacity = min(self.capacity + amount, self.max_capacity)

    def remove(self, amount):
        removed = min(amount, self.capacity)
        self.capacity -= removed
        return removed

class SimulationEnvironment:
    def __init__(self):
        self.raw_material = RawMaterialInventory(lead_time=8,
                                                 reorder_point=10,
                                                 reorder_quantity=30,
                                                 max_capacity=100)
        self.machine1 = Machine(10, 0.05, 0.2, 0.05)  # Treated as failure and repair rates
        self.machine2 = Machine(8, 0.03, 0.3, 0.03)
        self.buffer = Buffer(1, 50)
        self.produced_goods = ProducedGoods(3, 100, 50)
        self.demand_mean = 7
        self.demand_std = 2
        self.accumulated_demand = 0
        self.accumulated_fulfilled_demand = 0

    def step(self):
        demand = max(0, int(np.random.normal(self.demand_mean, self.demand_std)))
        
        # Raw material consumption
        raw_material_consumed = min(self.raw_material.inventory_on_hand, self.machine1.production_rate)
        self.raw_material.update(raw_material_consumed)
        
        # Machine 1 production
        production_m1 = int(self.machine1.operate())
        self.buffer.add(production_m1)

        # Machine 2 production
        available_from_buffer = self.buffer.remove(self.machine2.production_rate)
        production_m2 = int(min(self.machine2.operate(), available_from_buffer))
        self.produced_goods.add(production_m2)

        # Fulfill demand
        fulfilled_demand = self.produced_goods.remove(demand)

        self.accumulated_demand += demand
        self.accumulated_fulfilled_demand += fulfilled_demand

        return {
            "raw_material_stock": self.raw_material.inventory_on_hand,
            "production_m1": production_m1,
            "production_m2": production_m2,
            "buffer_level": self.buffer.capacity,
            "produced_goods_level": self.produced_goods.capacity,
            "demand": self.accumulated_demand,
            "fulfilled_demand": self.accumulated_fulfilled_demand,
            "m1_status": self.machine1.status,
            "m2_status": self.machine2.status
        }

class SimulationUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manufacturing Simulation")
        
        self.env = SimulationEnvironment()
        
        self.history = {
            'raw_material_stock': [],
            'production_m1': [],
            'production_m2': [],
            'buffer_level': [],
            'produced_goods_level': [],
            'demand': [],
            'fulfilled_demand': []
        }
        
        self.create_widgets()
        self.create_plot()
        
    def create_widgets(self):
        # Raw Material Inventory
        ttk.Label(self.master, text="Raw Material Inventory").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Lead time:").grid(row=1, column=0, padx=5, pady=2)
        self.raw_lead_time = ttk.Entry(self.master)
        self.raw_lead_time.insert(0, str(self.env.raw_material.lead_time))
        self.raw_lead_time.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Max capacity:").grid(row=2, column=0, padx=5, pady=2)
        self.raw_max_capacity= ttk.Entry(self.master)
        self.raw_max_capacity.insert(0, str(self.env.raw_material.max_capacity))
        self.raw_max_capacity.grid(row=2, column=1, padx=5, pady=2)
        
        #ttk.Label(self.master, text="Holding Cost:").grid(row=3, column=0, padx=5, pady=2)
        #self.raw_holding_cost = ttk.Entry(self.master)
        #self.raw_holding_cost.insert(0, str(self.env.raw_material.holding_cost))
        #self.raw_holding_cost.grid(row=3, column=1, padx=5, pady=2)
        
        #ttk.Label(self.master, text="Holding Cost:").grid(row=3, column=0, padx=5, pady=2)
        #self.raw_holding_cost = ttk.Entry(self.master)
        #self.raw_holding_cost.insert(0, str(self.env.raw_material.holding_cost))
        #self.raw_holding_cost.grid(row=3, column=1, padx=5, pady=2)
        
        # Machine 1
        ttk.Label(self.master, text="Machine 1").grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Max Production Rate:").grid(row=5, column=0, padx=5, pady=2)
        self.m1_max_rate = ttk.Entry(self.master)
        self.m1_max_rate.insert(0, str(self.env.machine1.max_production_rate))
        self.m1_max_rate.grid(row=5, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="MTTF:").grid(row=6, column=0, padx=5, pady=2)
        self.m1_mttf = ttk.Entry(self.master)
        self.m1_mttf.insert(0, str(self.env.machine1.mttf))
        self.m1_mttf.grid(row=6, column=1, padx=5, pady=2)
        
        # Buffer
        ttk.Label(self.master, text="Buffer").grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Holding Cost:").grid(row=8, column=0, padx=5, pady=2)
        self.buffer_holding_cost = ttk.Entry(self.master)
        self.buffer_holding_cost.insert(0, str(self.env.buffer.holding_cost))
        self.buffer_holding_cost.grid(row=8, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Max Capacity:").grid(row=9, column=0, padx=5, pady=2)
        self.buffer_max_capacity = ttk.Entry(self.master)
        self.buffer_max_capacity.insert(0, str(self.env.buffer.max_capacity))
        self.buffer_max_capacity.grid(row=9, column=1, padx=5, pady=2)
        
        # Produced Goods
        ttk.Label(self.master, text="Produced Goods").grid(row=10, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Holding Cost:").grid(row=11, column=0, padx=5, pady=2)
        self.pg_holding_cost = ttk.Entry(self.master)
        self.pg_holding_cost.insert(0, str(self.env.produced_goods.holding_cost))
        self.pg_holding_cost.grid(row=11, column=1, padx=5, pady=2)

        ttk.Label(self.master, text="Selling Cost:").grid(row=12, column=0, padx=5, pady=2)
        self.pg_selling_cost = ttk.Entry(self.master)
        self.pg_selling_cost.insert(0, str(self.env.produced_goods.selling_cost))
        self.pg_selling_cost.grid(row=12, column=1, padx=5, pady=2)

        # Simulation Parameters
        
        ttk.Label(self.master, text="Mean Demand:").grid(row=13, column=0, padx=5, pady=2)
        self.demand_mean = ttk.Entry(self.master)
        self.demand_mean.insert(0, str(self.env.demand_mean))
        self.demand_mean.grid(row=13, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Demand Standard Deviation:").grid(row=14, column=0, padx=5, pady=2)
        self.demand_std = ttk.Entry(self.master)
        self.demand_std.insert(0, str(self.env.demand_std))
        self.demand_std.grid(row=14, column=1, padx=5, pady=2)
        
        ttk.Button(self.master, text="Update", command=self.update_simulation).grid(row=15, column=0, columnspan=2, pady=10)
        
        # Create canvas for machine and buffer visualization
        self.canvas = tk.Canvas(self.master, width=550, height=500)
        self.canvas.grid(row=0, column=3, rowspan=20, padx=10, pady=10)
        
    def create_plot(self):
        # Demand fullfilled vs demand
        self.demand_fig, self.demand_ax = plt.subplots(figsize=(4, 3))
        self.demand_canvas_plot = FigureCanvasTkAgg(self.demand_fig, master=self.master)
        self.demand_canvas_plot_widget = self.demand_canvas_plot.get_tk_widget()
        self.demand_canvas_plot_widget.grid(row=0, column=5, rowspan=6, padx=3, pady=3)

        # Inventory levels
        self.inventory_fig, self.inventory_ax = plt.subplots(figsize=(4, 3))
        self.inventory_canvas_plot = FigureCanvasTkAgg(self.inventory_fig, master=self.master)
        self.inventory_canvas_plot_widget = self.inventory_canvas_plot.get_tk_widget()
        self.inventory_canvas_plot_widget.grid(row=6, column=5, rowspan=6, padx=3, pady=3)

        # Machine status
        self.machine_fig, self.machine_ax = plt.subplots(figsize=(4, 3))
        self.machine_canvas_plot = FigureCanvasTkAgg(self.machine_fig, master=self.master)
        self.machine_canvas_plot_widget = self.machine_canvas_plot.get_tk_widget()
        self.machine_canvas_plot_widget.grid(row=12, column=5, rowspan=6, padx=5, pady=3)
        
    def update_simulation(self):
        # Update simulation parameters
        self.env.raw_material.lead_time = float(self.raw_lead_time.get())
        self.env.raw_material.max_capacity = float(self.raw_max_capacity.get())
        #self.env.raw_material.holding_cost = float(self.raw_holding_cost.get())
        self.env.machine1.max_production_rate = float(self.m1_max_rate.get())
        self.env.machine1.mttf = float(self.m1_mttf.get())
        self.env.buffer.holding_cost = float(self.buffer_holding_cost.get())
        self.env.buffer.max_capacity = int(self.buffer_max_capacity.get())
        self.env.produced_goods.holding_cost = float(self.pg_holding_cost.get())
        self.env.produced_goods.selling_cost = float(self.pg_selling_cost.get())
        self.env.demand_mean = float(self.demand_mean.get())
        self.env.demand_std = float(self.demand_std.get())
        
        # Run simulation for 100 steps
        for _ in range(100):
            state = self.env.step()
            self.history['raw_material_stock'].append(state['raw_material_stock'])
            self.history['production_m1'].append(state['production_m1'])
            self.history['production_m2'].append(state['production_m2'])
            self.history['buffer_level'].append(state['buffer_level'])
            self.history['produced_goods_level'].append(state['produced_goods_level'])
            self.history['demand'].append(state['demand'])
            self.history['fulfilled_demand'].append(state['fulfilled_demand'])
        
        self.update_plot()
        self.update_visualization()
        
    def update_plot(self):
        self.demand_ax.clear()
        self.demand_ax.plot(self.history['demand'], label="Demand")
        self.demand_ax.plot(self.history['fulfilled_demand'], label="Fulfilled Demand")
        self.demand_ax.legend()
        self.demand_ax.set_title("Demand vs Fulfilled Demand")
        self.demand_ax.set_xlabel("Time")
        self.demand_ax.set_ylabel("Demand")
        self.demand_fig.canvas.draw()

        self.inventory_ax.clear()
        self.inventory_ax.plot(self.history['raw_material_stock'], label="Raw Material")
        self.inventory_ax.plot(self.history['buffer_level'], label="Buffer")
        self.inventory_ax.plot(self.history['produced_goods_level'], label="Produced Goods")
        self.inventory_ax.legend()
        self.inventory_ax.set_title("Inventory Levels")
        self.inventory_ax.set_xlabel("Time")
        self.inventory_ax.set_ylabel("Inventory Level")
        self.inventory_fig.canvas.draw()

        self.machine_ax.clear()
        self.machine_ax.plot(self.history['production_m1'], label="Machine 1")
        self.machine_ax.plot(self.history['production_m2'], label="Machine 2")
        self.machine_ax.legend()
        self.machine_ax.set_title("Production Rate")
        self.machine_ax.set_xlabel("Time")
        self.machine_ax.set_ylabel("Production Rate")
        self.machine_fig.canvas.draw()

        # Clear all history
        self.env.accumulated_demand = 0
        self.env.accumulated_fulfilled_demand = 0
        self.history = {
            'raw_material_stock': [],
            'production_m1': [],
            'production_m2': [],
            'buffer_level': [],
            'produced_goods_level': [],
            'demand': [],
            'fulfilled_demand': []
        }
        
    def update_visualization(self):
        self.canvas.delete("all")
        
        # Draw raw material inventory
        self.canvas.create_rectangle(50, 50, 100, 100, fill="brown")
        self.canvas.create_text(75, 120, text="Raw Material")
        
        # Draw machines
        self.canvas.create_rectangle(150, 50, 200, 100, fill="green" if self.env.machine1.status == "operational" else "red")
        self.canvas.create_text(175, 120, text="M1")
        self.canvas.create_rectangle(350, 50, 400, 100, fill="green" if self.env.machine2.status == "operational" else "red")
        self.canvas.create_text(375, 120, text="M2")
        
        # Draw buffer
        buffer_fill = self.env.buffer.capacity / self.env.buffer.max_capacity
        self.canvas.create_rectangle(250, 50, 300, 100, outline="black")
        self.canvas.create_rectangle(250, 100 - buffer_fill * 50, 300, 100, fill="blue")
        self.canvas.create_text(270, 120, text=f"Buffer: {self.env.buffer.capacity}/{self.env.buffer.max_capacity}")
        
        # Draw produced goods
        self.canvas.create_rectangle(450, 50, 500, 100, fill="yellow")
        self.canvas.create_text(475, 120, text="Produced Goods")
        
        # Draw inventory levels
        self.canvas.create_text(75, 180, text=f"Raw: {self.env.raw_material.inventory_on_hand}")
        self.canvas.create_text(325, 180, text=f"Produced: {self.env.produced_goods.capacity}")
        
    def run(self):
        self.update_simulation()
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationUI(root)
    app.run()