"""
File to generate training data from the inventory system simulation.
"""
import os
import random
import csv
from inventory_system import SimulationEnvironment

def generate_data(steps, output_file):
    """Generate training data for the inventory system simulation."""
    env = SimulationEnvironment()
    output_path = os.path.join(output_file)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Add header
        header = [
            'm1_production', 'm2_production', 'buffer_level', 'produced_goods_level', 'demand', 'fulfilled_demand',
            'm1_status', 'm2_status','lead_time', 'reorder_point', 'reorder_quantity', 'inventory_max_capacity', 'inventory_position',
            'inventory_on_hand', 'm1_max_production_rate', 'm1_mttf', 'm1_mttr', 'm1_defect_rate',
            'm1_downtime', 'm2_max_production_rate', 'm2_mttf', 'm2_mttr', 'm2_defect_rate', 'm2_downtime',
            'buffer_max_capacity', 'produced_goods_max_capacity']
        writer.writerow(header)
        for _ in range(100):
            # Randomize data for the next step
            env.raw_material.lead_time = random.randint(5, 10)
            env.raw_material.reorder_point = random.randint(5, 15)
            env.raw_material.reorder_quantity = random.randint(20, 40)
            env.raw_material.max_capacity = random.randint(80, 120)
            env.machine1.max_production_rate = random.randint(5, 30)
            env.machine1.mttf = random.randint(70, 120)
            env.machine1.mttr = random.randint(15, 30)
            env.machine1.defect_rate = random.uniform(0.01, 0.07)
            env.machine2.max_production_rate = random.randint(5, 30)
            env.machine2.mttf = random.randint(70, 120)
            env.machine2.mttr = random.randint(15, 30)
            env.machine2.defect_rate = random.uniform(0.01, 0.07)
            env.buffer.max_capacity = random.randint(20, 60)
            env.produced_goods.max_capacity = random.randint(80, 150)
            env.demand_mean = random.randint(3, 15)
            env.demand_std = random.uniform(0.5, 3.5)
            data = {
                'lead_time': float(env.raw_material.lead_time),
                'reorder_point': float(env.raw_material.reorder_point),
                'reorder_quantity': float(env.raw_material.reorder_quantity),
                'inventory_max_capacity': float(env.raw_material.max_capacity),
                'inventory_position': float(env.raw_material.inventory_position),
                'inventory_on_hand': float(env.raw_material.inventory_on_hand),
                'm1_max_production_rate': float(env.machine1.max_production_rate),
                'm1_mttf': float(env.machine1.mttf),
                'm1_mttr': float(env.machine1.mttr),
                'm1_defect_rate': float(env.machine1.defect_rate),
                'm1_downtime': float(env.machine1.downtime),
                'm2_max_production_rate': float(env.machine2.max_production_rate),
                'm2_mttf': float(env.machine2.mttf),
                'm2_mttr': float(env.machine2.mttr),
                'm2_defect_rate': float(env.machine2.defect_rate),
                'm2_downtime': float(env.machine2.downtime),
                'buffer_max_capacity': float(env.buffer.max_capacity),
                'produced_goods_max_capacity': float(env.produced_goods.max_capacity)
            }
            for _ in range(int(steps/100)):
                dynamic_data = env.step()
                # All values to float
                dynamic_data = {k: float(v) for k, v in dynamic_data.items()}
                data.update(dynamic_data)
                writer.writerow(data.values())


if __name__ == "__main__":
    generate_data(1000, 'inventory_data.csv')
