"""Graphical User Interface for the Inventory System Simulation"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from inventory_system import SimulationEnvironment

class SimulationUI:
    """User Interface in Tkinter for the Inventory System Simulation"""
    def __init__(self, master):
        self.master = master
        self.master.title("Manufacturing Simulation")
        self.simulation = SimulationEnvironment()
        self.history = {
            'raw_material_level': [],
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
        """Create widgets for the UI"""
        # Raw Material Inventory
        ttk.Label(self.master, text="Raw Material Inventory").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Lead time (hours):").grid(row=1, column=0, padx=5, pady=2)
        self.raw_lead_time = ttk.Entry(self.master)
        self.raw_lead_time.insert(0, str(self.simulation.raw_material.lead_time))
        self.raw_lead_time.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Max capacity (units):").grid(row=2, column=0, padx=5, pady=2)
        self.raw_max_capacity= ttk.Entry(self.master)
        self.raw_max_capacity.insert(0, str(self.simulation.raw_material.max_capacity))
        self.raw_max_capacity.grid(row=2, column=1, padx=5, pady=2)
        
        #ttk.Label(self.master, text="Holding Cost:").grid(row=3, column=0, padx=5, pady=2)
        #self.raw_holding_cost = ttk.Entry(self.master)
        #self.raw_holding_cost.insert(0, str(self.simulation.raw_material.holding_cost))
        #self.raw_holding_cost.grid(row=3, column=1, padx=5, pady=2)
        
        #ttk.Label(self.master, text="Holding Cost:").grid(row=3, column=0, padx=5, pady=2)
        #self.raw_holding_cost = ttk.Entry(self.master)
        #self.raw_holding_cost.insert(0, str(self.simulation.raw_material.holding_cost))
        #self.raw_holding_cost.grid(row=3, column=1, padx=5, pady=2)
        
        # Machine 1
        ttk.Label(self.master, text="Machine 1").grid(row=0, column=2, columnspan=2, pady=5)
        ttk.Label(self.master, text="Max Production Rate (units/h):").grid(row=1, column=2, padx=5, pady=2)
        self.m1_max_rate = ttk.Entry(self.master)
        self.m1_max_rate.insert(0, str(self.simulation.machine1.max_production_rate))
        self.m1_max_rate.grid(row=1, column=3, padx=5, pady=2)
        
        # Mean Time To Failure (MTTF) and Mean Time To Repair (MTTR)
        ttk.Label(self.master, text="MTTF (hours):").grid(row=2, column=2, padx=5, pady=2)
        self.m1_mttf = ttk.Entry(self.master)
        self.m1_mttf.insert(0, str(self.simulation.machine1.mttf))
        self.m1_mttf.grid(row=2, column=3, padx=5, pady=2)

        ttk.Label(self.master, text="MTTR (hours):").grid(row=3, column=2, padx=5, pady=2)
        self.m1_mttr = ttk.Entry(self.master)
        self.m1_mttr.insert(0, str(self.simulation.machine1.mttr))
        self.m1_mttr.grid(row=3, column=3, padx=5, pady=2)

        ttk.Label(self.master, text="Defect Rate (%):").grid(row=4, column=2, padx=5, pady=2)
        self.m1_defect_rate = ttk.Entry(self.master)
        self.m1_defect_rate.insert(0, str(self.simulation.machine1.defect_rate))
        self.m1_defect_rate.grid(row=4, column=3, padx=5, pady=2)

        # Machine 2
        ttk.Label(self.master, text="Machine 2").grid(row=5, column=2, columnspan=2, pady=5)
        ttk.Label(self.master, text="Max Production Rate (units/h):").grid(row=6, column=2, padx=5, pady=2)
        self.m2_max_rate = ttk.Entry(self.master)
        self.m2_max_rate.insert(0, str(self.simulation.machine2.max_production_rate))
        self.m2_max_rate.grid(row=6, column=3, padx=5, pady=2)

        # Mean Time To Failure (MTTF) and Mean Time To Repair (MTTR)
        ttk.Label(self.master, text="MTTF (hours):").grid(row=7, column=2, padx=5, pady=2)
        self.m2_mttf = ttk.Entry(self.master)
        self.m2_mttf.insert(0, str(self.simulation.machine2.mttf))
        self.m2_mttf.grid(row=7, column=3, padx=5, pady=2)

        ttk.Label(self.master, text="MTTR (hours):").grid(row=8, column=2, padx=5, pady=2)
        self.m2_mttr = ttk.Entry(self.master)
        self.m2_mttr.insert(0, str(self.simulation.machine2.mttr))
        self.m2_mttr.grid(row=8, column=3, padx=5, pady=2)

        ttk.Label(self.master, text="Defect Rate (%):").grid(row=9, column=2, padx=5, pady=2)
        self.m2_defect_rate = ttk.Entry(self.master)
        self.m2_defect_rate.insert(0, str(self.simulation.machine2.defect_rate))
        self.m2_defect_rate.grid(row=9, column=3, padx=5, pady=2)
        
        # Buffer
        ttk.Label(self.master, text="Buffer").grid(row=3, column=0, columnspan=2, pady=5)
        #ttk.Label(self.master, text="Holding Cost ():").grid(row=4, column=0, padx=5, pady=2)
        #self.buffer_holding_cost = ttk.Entry(self.master)
        #self.buffer_holding_cost.insert(0, str(self.simulation.buffer.holding_cost))
        #self.buffer_holding_cost.grid(row=4, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Max Capacity (units):").grid(row=5, column=0, padx=5, pady=2)
        self.buffer_max_capacity = ttk.Entry(self.master)
        self.buffer_max_capacity.insert(0, str(self.simulation.buffer.max_capacity))
        self.buffer_max_capacity.grid(row=5, column=1, padx=5, pady=2)
        
        # Produced Goods
        ttk.Label(self.master, text="Produced Goods").grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Label(self.master, text="Max Capacity (units):").grid(row=7, column=0, padx=5, pady=2)
        self.pg_max_capacity = ttk.Entry(self.master)
        self.pg_max_capacity.insert(0, str(self.simulation.produced_goods.max_capacity))
        self.pg_max_capacity.grid(row=7, column=1, padx=5, pady=2)

        #ttk.Label(self.master, text="Selling Cost:").grid(row=8, column=0, padx=5, pady=2)
        #self.pg_selling_cost = ttk.Entry(self.master)
        #self.pg_selling_cost.insert(0, str(self.simulation.produced_goods.selling_cost))
        #self.pg_selling_cost.grid(row=8, column=1, padx=5, pady=2)

        # Simulation Parameters 
        ttk.Label(self.master, text="Mean Demand (units):").grid(row=9, column=0, padx=5, pady=2)
        self.demand_mean = ttk.Entry(self.master)
        self.demand_mean.insert(0, str(self.simulation.demand_mean))
        self.demand_mean.grid(row=9, column=1, padx=5, pady=2)
        
        ttk.Label(self.master, text="Demand StDeviation (units):").grid(row=10, column=0, padx=5, pady=2)
        self.demand_std = ttk.Entry(self.master)
        self.demand_std.insert(0, str(self.simulation.demand_std))
        self.demand_std.grid(row=10, column=1, padx=5, pady=2)
        
        ttk.Button(self.master, text="Update", command=self.update_simulation).grid(row=11, column=0, columnspan=2, pady=10)
        
        # Create canvas for machine and buffer visualization
        self.canvas = tk.Canvas(self.master, width=550, height=370)
        self.canvas.grid(row=12, column=0, rowspan=5, columnspan=4, padx=3, pady=0)
        
    def create_plot(self):
        # Demand fullfilled vs demand
        self.fig, self.ax = plt.subplots(3, sharex=True, figsize=(8, 8))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_plot_widget = self.canvas_plot.get_tk_widget()
        self.canvas_plot_widget.grid(row=0, column=5, rowspan=16, columnspan=2, padx=3, pady=3)

        
    def update_simulation(self):
        # Update simulation parameters
        self.simulation.raw_material.lead_time = float(self.raw_lead_time.get())
        self.simulation.raw_material.max_capacity = float(self.raw_max_capacity.get())
        #self.simulation.raw_material.holding_cost = float(self.raw_holding_cost.get())
        self.simulation.machine1.max_production_rate = float(self.m1_max_rate.get())
        self.simulation.machine1.mttf = float(self.m1_mttf.get())
        self.simulation.machine1.mttr = float(self.m1_mttr.get())
        self.simulation.machine1.defect_rate = float(self.m1_defect_rate.get())
        self.simulation.machine2.max_production_rate = float(self.m2_max_rate.get())
        self.simulation.machine2.mttf = float(self.m2_mttf.get())
        self.simulation.machine2.mttr = float(self.m2_mttr.get())
        self.simulation.machine2.defect_rate = float(self.m2_defect_rate.get())
        #self.simulation.buffer.holding_cost = float(self.buffer_holding_cost.get())
        self.simulation.buffer.max_capacity = int(self.buffer_max_capacity.get())
        self.simulation.produced_goods.max_capacity = float(self.pg_max_capacity.get())
        #self.simulation.produced_goods.selling_cost = float(self.pg_selling_cost.get())
        self.simulation.demand_mean = float(self.demand_mean.get())
        self.simulation.demand_std = float(self.demand_std.get())

        # Run simulation for 100 steps
        for _ in range(48):
            state = self.simulation.step()
            self.history['raw_material_level'].append(state['raw_material_level'])
            self.history['production_m1'].append(state['production_m1'])
            self.history['production_m2'].append(state['production_m2'])
            self.history['buffer_level'].append(state['buffer_level'])
            self.history['produced_goods_level'].append(state['produced_goods_level'])
            self.history['demand'].append(state['demand'])
            self.history['fulfilled_demand'].append(state['fulfilled_demand'])
        
        self.update_plot()
        self.update_visualization()
        
    def update_plot(self):
        self.ax[0].clear()
        self.ax[0].plot(self.history['demand'], label="Accumulated Demand")
        self.ax[0].plot(self.history['fulfilled_demand'], label="Accumulated Fulfilled Demand")
        self.ax[0].legend()
        #self.ax[0].set_title("Demand vs Fulfilled Demand")
        self.ax[0].set_ylabel("Demand")

        self.ax[1].clear()
        self.ax[1].plot(self.history['raw_material_level'], label="Raw Material")
        self.ax[1].plot(self.history['buffer_level'], label="Buffer")
        self.ax[1].plot(self.history['produced_goods_level'], label="Produced Goods")
        self.ax[1].legend()
        #self.ax[1].set_title("Inventory Levels")
        self.ax[1].set_ylabel("Inventory Level")

        self.ax[2].clear()
        self.ax[2].plot(self.history['production_m1'], label="Machine 1")
        self.ax[2].plot(self.history['production_m2'], label="Machine 2")
        self.ax[2].legend()
        #self.ax[2].set_title("Production Rate")
        self.ax[2].set_xlabel("Time")
        self.ax[2].set_ylabel("Production Rate")
        self.fig.canvas.draw()

        # Clear all history
        self.simulation.accumulated_demand = 0
        self.simulation.accumulated_fulfilled_demand = 0
        self.history = {
            'raw_material_level': [],
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
        self.canvas.create_rectangle(150, 50, 200, 100, fill="green" if self.simulation.machine1.status == "operational" else "red")
        self.canvas.create_text(175, 120, text="M1")
        self.canvas.create_rectangle(350, 50, 400, 100, fill="green" if self.simulation.machine2.status == "operational" else "red")
        self.canvas.create_text(375, 120, text="M2")
        
        # Draw buffer
        buffer_fill = self.simulation.buffer.capacity / self.simulation.buffer.max_capacity
        self.canvas.create_rectangle(250, 50, 300, 100, outline="black")
        self.canvas.create_rectangle(250, 100 - buffer_fill * 50, 300, 100, fill="blue")
        self.canvas.create_text(270, 120, text=f"Buffer: {self.simulation.buffer.capacity}/{self.simulation.buffer.max_capacity}")
        
        # Draw produced goods
        self.canvas.create_rectangle(450, 50, 500, 100, fill="yellow")
        self.canvas.create_text(475, 120, text="Produced Goods")
        
        # Draw inventory levels
        self.canvas.create_text(75, 180, text=f"Raw: {self.simulation.raw_material.inventory_on_hand}")
        self.canvas.create_text(325, 180, text=f"Produced: {self.simulation.produced_goods.capacity}")
        
    def run(self):
        self.update_simulation()
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationUI(root)
    app.run()
