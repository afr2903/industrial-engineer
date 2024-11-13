import os
import random
import csv
from inventory_system import SimulationEnvironment

"""
def serialize_example(data):
    feature = {
        'm1_production': tf.train.Feature(float_list=tf.train.FloatList(value=[data['production_m1']])),
        'm2_production': tf.train.Feature(float_list=tf.train.FloatList(value=[data['production_m2']])),
        'buffer_level': tf.train.Feature(float_list=tf.train.FloatList(value=[data['buffer_level']])),
        'produced_goods_level': tf.train.Feature(float_list=tf.train.FloatList(value=[data['produced_goods_level']])),
        'demand': tf.train.Feature(float_list=tf.train.FloatList(value=[data['demand']])),
        'fulfilled_demand': tf.train.Feature(float_list=tf.train.FloatList(value=[data['fulfilled_demand']])),
        'lead_time': tf.train.Feature(float_list=tf.train.FloatList(value=[data['lead_time']])),
        'reorder_point': tf.train.Feature(float_list=tf.train.FloatList(value=[data['reorder_point']])),
        'reorder_quantity': tf.train.Feature(float_list=tf.train.FloatList(value=[data['reorder_quantity']])),
        'inventory_max_capacity': tf.train.Feature(float_list=tf.train.FloatList(value=[data['inventory_max_capacity']])),
        'inventory_position': tf.train.Feature(float_list=tf.train.FloatList(value=[data['inventory_position']])),
        'inventory_on_hand': tf.train.Feature(float_list=tf.train.FloatList(value=[data['inventory_on_hand']])),
        'm1_max_production_rate': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m1_max_production_rate']])),
        'm1_status': tf.train.Feature(bytes_list=tf.train.BytesList(value=[data['m1_status'].encode()])),
        'm1_mttf': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m1_mttf']])),
        'm1_mttr': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m1_mttr']])),
        'm1_defect_rate': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m1_defect_rate']])),
        'm1_downtime': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m1_downtime']])),
        'm2_max_production_rate': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_max_production_rate']])),
        'm2_status': tf.train.Feature(bytes_list=tf.train.BytesList(value=[data['m2_status'].encode()])),
        'm2_mttf': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_mttf']])),
        'm2_mttr': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_mttr']])),
        'm2_defect_rate': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_defect_rate']])),
        'm2_downtime': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_downtime']])),
        'buffer_max_capacity': tf.train.Feature(float_list=tf.train.FloatList(value=[data['buffer_max_capacity']])),
        'produced_goods_max_capacity': tf.train.Feature(float_list=tf.train.FloatList(value=[data['produced_goods_max_capacity']])),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()
"""

def generate_data(steps, output_file):
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
            for _ in range(int(steps/100)):
                data = env.step()
                data.update({
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
                    'produced_goods_max_capacity': float(env.produced_goods.max_capacity),
                })
                #example = serialize_example(data)
                writer.writerow(data.values())


if __name__ == "__main__":
    generate_data(1000, 'inventory_data.csv')
