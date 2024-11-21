"""Time-series simulation of a simple production system with two machines, a
buffer, and a raw material inventory."""
import random
import numpy as np

class RawMaterialInventory:
    """Buffer for the raw material inventory."""
    def __init__(self, lead_time, reorder_point, reorder_quantity, max_capacity):
        self.max_capacity = max_capacity
        self.lead_time = lead_time
        self.time_since_last_order = 0
        self.reorder_point = reorder_point
        self.reorder_quantity = reorder_quantity
        self.inventory_position = reorder_quantity
        self.inventory_on_hand = reorder_quantity

    def update(self, demand):
        """Update the inventory level based on the demand requested."""
        self.time_since_last_order += 1
        if self.time_since_last_order == self.lead_time:
            self.inventory_on_hand = self.inventory_position
        self.inventory_on_hand -= demand
        self.inventory_position -= demand
        if self.inventory_position <= self.reorder_point:
            self.order()

    def order(self):
        """Place an order for the raw material."""
        self.inventory_position += self.reorder_quantity
        self.inventory_position = min(self.inventory_position, self.max_capacity)
        self.time_since_last_order = 0

    def set_order_point_and_quantity(self, reorder_point, reorder_quantity):
        """Set the reorder point and reorder quantity."""
        self.reorder_point = reorder_point
        self.reorder_quantity = reorder_quantity

class Machine:
    """Machine in the production system."""
    def __init__(self, max_production_rate, mttf, mttr, defect_rate):
        self.max_production_rate = max_production_rate
        self.mttf = mttf
        self.mttr = mttr
        self.defect_rate = defect_rate
        self.production_rate = max_production_rate
        self.status = "operational"
        self.downtime = 0

    def operate(self):
        """Operate the machine for one time step."""
        if self.status == "operational":
            if random.random() < 1 / self.mttf:
                self.status = "failed"
                self.downtime = 1
                return 0
            return self.production_rate * (1 - self.defect_rate)
        else:
            self.downtime += 1
            if random.random() < 1 / self.mttr:
                self.status = "operational"
            return 0

class Buffer:
    """Buffer for the goods produced by the machines."""
    def __init__(self, holding_cost, max_capacity):
        self.holding_cost = holding_cost
        self.max_capacity = max_capacity
        self.capacity = 0

    def add(self, amount):
        """Add goods to the buffer."""
        self.capacity = min(self.capacity + amount, self.max_capacity)

    def remove(self, amount):
        """Remove goods from the buffer."""
        removed = min(amount, self.capacity)
        self.capacity -= removed
        return removed

class ProducedGoods:
    """Inventory for the produced goods."""
    def __init__(self, holding_cost, max_capacity, selling_cost):
        self.holding_cost = holding_cost
        self.max_capacity = max_capacity
        self.selling_cost = selling_cost
        self.capacity = 0

    def add(self, amount):
        """Add goods to the inventory."""
        self.capacity = min(self.capacity + amount, self.max_capacity)

    def remove(self, amount):
        """Remove goods from the inventory."""
        removed = min(amount, self.capacity)
        self.capacity -= removed
        return removed

class SimulationEnvironment:
    """Simulation environment for the production system."""
    def __init__(self):
        self.raw_material = RawMaterialInventory(lead_time=8,
                                                 reorder_point=10,
                                                 reorder_quantity=30,
                                                 max_capacity=100)
        self.machine1 = Machine(max_production_rate=10,
                                mttf=80, mttr=20, defect_rate=0.05)
        self.machine2 = Machine(max_production_rate=8,
                                mttf=75, mttr=10, defect_rate=0.03)
        self.buffer = Buffer(holding_cost=1, max_capacity=50)
        self.produced_goods = ProducedGoods(holding_cost=3,
                                            max_capacity=100, selling_cost=10)
        self.demand_mean = 7
        self.demand_std = 2
        self.accumulated_demand = 0
        self.accumulated_fulfilled_demand = 0

    def step(self):
        """Advance the simulation by one time step."""
        demand = max(0, int(np.random.normal(self.demand_mean, self.demand_std)))
        # Raw material consumption
        raw_material_consumed = min(self.raw_material.inventory_on_hand,
                                    self.machine1.production_rate)
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
            "production_m1": float(production_m1),
            "production_m2": float(production_m2),
            "buffer_level": float(self.buffer.capacity),
            "produced_goods_level": float(self.produced_goods.capacity),
            "demand": float(demand),
            "fulfilled_demand": float(fulfilled_demand),
            "m1_status": self.machine1.status,
            "m2_status": self.machine2.status
        }
