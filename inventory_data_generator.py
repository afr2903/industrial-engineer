import os
import random
import tensorflow as tf
from inventory_system import SimulationEnvironment

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
        'm2_max_production_rate': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_max_production_rate']])),
        'm2_status': tf.train.Feature(bytes_list=tf.train.BytesList(value=[data['m2_status'].encode()])),
        'm2_mttf': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_mttf']])),
        'm2_mttr': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_mttr']])),
        'm2_defect_rate': tf.train.Feature(float_list=tf.train.FloatList(value=[data['m2_defect_rate']])),
        'buffer_max_capacity': tf.train.Feature(float_list=tf.train.FloatList(value=[data['buffer_max_capacity']])),
        'produced_goods_max_capacity': tf.train.Feature(float_list=tf.train.FloatList(value=[data['produced_goods_max_capacity']])),
    }
    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()

def generate_data(steps, output_file):
    env = SimulationEnvironment()
    output_path = os.path.join(output_file)
    with tf.io.TFRecordWriter(output_path) as writer:
        for _ in range(steps):
            data = env.step()
            data.update({
                'lead_time': env.raw_material.lead_time,
                'reorder_point': env.raw_material.reorder_point,
                'reorder_quantity': env.raw_material.reorder_quantity,
                'inventory_max_capacity': env.raw_material.max_capacity,
                'inventory_position': env.raw_material.inventory_position,
                'inventory_on_hand': env.raw_material.inventory_on_hand,
                'm1_max_production_rate': env.machine1.max_production_rate,
                'm1_status': env.machine1.status,
                'm1_mttf': env.machine1.mttf,
                'm1_mttr': env.machine1.mttr,
                'm1_defect_rate': env.machine1.defect_rate,
                'm2_max_production_rate': env.machine2.max_production_rate,
                'm2_status': env.machine2.status,
                'm2_mttf': env.machine2.mttf,
                'm2_mttr': env.machine2.mttr,
                'm2_defect_rate': env.machine2.defect_rate,
                'buffer_max_capacity': env.buffer.max_capacity,
                'produced_goods_max_capacity': env.produced_goods.max_capacity,
            })
            example = serialize_example(data)
            writer.write(example)

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

if __name__ == "__main__":
    generate_data(1000, 'inventory_data.tfrecord')
