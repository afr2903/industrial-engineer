import random
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RawMaterialInventory:
    def __init__(self, unit_cost, ordering_cost, holding_cost, lead_time, reorder_point, reorder_quantity):
        self.unit_cost = unit_cost
        self.ordering_cost = ordering_cost
        self.holding_cost = holding_cost
        self.lead_time = lead_time
        self.reorder_point = reorder_point
        self.reorder_quantity = reorder_quantity
        self.current_stock = reorder_quantity

    def update(self, demand):
        if self.current_stock <= demand:
            self.order()
        self.current_stock -= demand

    def order(self):
        self.current_stock += self.reorder_quantity

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
            if random.random() < 1 / self.mttf:
                self.status = "failed"
                self.downtime = random.expovariate(1 / self.mttr)
            return self.production_rate * (1 - self.defect_rate)
        else:
            self.downtime -= 1
            if self.downtime <= 0:
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
        self.raw_material = RawMaterialInventory(10, 100, 2, 5, 50, 200)
        self.machine1 = Machine(10, 100, 10, 0.05)
        self.machine2 = Machine(8, 120, 15, 0.03)
        self.buffer = Buffer(1, 50)
        self.produced_goods = ProducedGoods(3, 200, 50)
        self.demand_mean = 7
        self.demand_std = 2

    def step(self):
        demand = max(0, int(np.random.normal(self.demand_mean, self.demand_std)))
        
        # Raw material consumption
        raw_material_consumed = min(self.raw_material.current_stock, self.machine1.production_rate)
        self.raw_material.update(raw_material_consumed)
        
        # Machine 1 production
        production_m1 = self.machine1.operate()
        self.buffer.add(production_m1)

        # Machine 2 production
        available_from_buffer = self.buffer.remove(self.machine2.production_rate)
        production_m2 = min(self.machine2.operate(), available_from_buffer)
        self.produced_goods.add(production_m2)

        # Fulfill demand
        fulfilled_demand = self.produced_goods.remove(demand)

        return {
            "raw_material_stock": self.raw_material.current_stock,
            "production_m1": production_m1,
            "production_m2": production_m2,
            "buffer_level": self.buffer.capacity,
            "produced_goods_level": self.produced_goods.capacity,
            "demand": demand,
            "fulfilled_demand": fulfilled_demand,
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
            'buffer_level': [],
            'produced_goods_level': [],
            'demand': []
        }
        
        self.create_widgets()
        self.create_plot()
        
    def create_widgets(self):
        # Raw Material Inventory
        ttk.Label(self.master, text="Raw Material Inventory").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Unit Cost:").grid(row=1, column=0, padx=5, pady=2)
        self.raw_unit_cost = ttk.Entry(self.master)
        self.raw_unit_cost.insert(0, str(self.env.raw_material.unit_cost))
        self.raw_unit_cost.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Ordering Cost:").grid(row=2, column=0, padx=5, pady=2)
        self.raw_ordering_cost = ttk.Entry(self.master)
        self.raw_ordering_cost.insert(0, str(self.env.raw_material.ordering_cost))
        self.raw_ordering_cost.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Holding Cost:").grid(row=3, column=0, padx=5, pady=2)
        self.raw_holding_cost = ttk.Entry(self.master)
        self.raw_holding_cost.insert(0, str(self.env.raw_material.holding_cost))
        self.raw_holding_cost.grid(row=3, column=1, padx=5, pady=2)
        
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
        
        ttk.Button(self.master, text="Update", command=self.update_simulation).grid(row=13, column=0, columnspan=2, pady=10)
        
        # Create canvas for machine and buffer visualization
        self.canvas = tk.Canvas(self.master, width=400, height=200)
        self.canvas.grid(row=0, column=2, rowspan=14, padx=10, pady=10)
        
    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_plot_widget = self.canvas_plot.get_tk_widget()
        self.canvas_plot_widget.grid(row=0, column=5, rowspan=14, padx=15, pady=15)
        
    def update_simulation(self):
        # Update simulation parameters
        self.env.raw_material.unit_cost = float(self.raw_unit_cost.get())
        self.env.raw_material.ordering_cost = float(self.raw_ordering_cost.get())
        self.env.raw_material.holding_cost = float(self.raw_holding_cost.get())
        self.env.machine1.max_production_rate = float(self.m1_max_rate.get())
        self.env.machine1.mttf = float(self.m1_mttf.get())
        self.env.buffer.holding_cost = float(self.buffer_holding_cost.get())
        self.env.buffer.max_capacity = int(self.buffer_max_capacity.get())
        self.env.produced_goods.holding_cost = float(self.pg_holding_cost.get())
        self.env.produced_goods.selling_cost = float(self.pg_selling_cost.get())
        
        # Run simulation for 100 steps
        for _ in range(100):
            state = self.env.step()
            self.history['raw_material_stock'].append(state['raw_material_stock'])
            self.history['buffer_level'].append(state['buffer_level'])
            self.history['produced_goods_level'].append(state['produced_goods_level'])
            self.history['demand'].append(state['demand'])
        
        self.update_plot()
        self.update_visualization()
        
    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.history['raw_material_stock'][-100:], label='Raw Material')
        self.ax.plot(self.history['buffer_level'][-100:], label='Buffer')
        self.ax.plot(self.history['produced_goods_level'][-100:], label='Produced Goods')
        self.ax.plot(self.history['demand'][-100:], label='Demand')
        self.ax.legend()
        self.ax.set_title('Manufacturing Simulation')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Level')
        self.canvas_plot.draw()
        
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
        self.canvas.create_text(255, 120, text=f"Buffer: {self.env.buffer.capacity}/{self.env.buffer.max_capacity}")
        
        # Draw produced goods
        self.canvas.create_rectangle(500, 50, 550, 100, fill="yellow")
        self.canvas.create_text(525, 120, text="Produced Goods")
        
        # Draw inventory levels
        self.canvas.create_text(75, 180, text=f"Raw: {self.env.raw_material.current_stock}")
        self.canvas.create_text(325, 180, text=f"Produced: {self.env.produced_goods.capacity}")
        
    def run(self):
        self.update_simulation()
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationUI(root)
    app.run()