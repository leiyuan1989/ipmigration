import json, os
from datetime import datetime
import logging

logging.basicConfig(level=logging.ERROR)

def list_to_tuple(lst):
    if isinstance(lst, list):
        return tuple(list_to_tuple(item) for item in lst)
    return lst



def convert_tuples_to_lists(data):
    if isinstance(data, tuple):
        return list(data)
    elif isinstance(data, dict):
        return {key: convert_tuples_to_lists(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_tuples_to_lists(item) for item in data]
    return data

def load_routing_expertise(data, name, left_nodes, right_nodes, node_match=True, only_left=False):
    #TODO must also use columns number to search. some may not add left nodes or right nodes
    if not isinstance(name, str):
        logging.error("Parameter 'name' must be a string type.")
        return []

    left_nodes = convert_tuples_to_lists(left_nodes)
    # right_nodes = convert_tuples_to_lists(right_nodes)
    if name in data:
        results = []
        for item in data[name]:
            if node_match:
                item_left_nodes = item.get('left_nodes')
                item_right_nodes = item.get('right_nodes')
                #left are matched right name are same
                if only_left:
                    c1 = set(list(item_right_nodes.keys())) == set(list(right_nodes.keys()))
                else:
                    c1 = item_right_nodes == right_nodes 
                    # print('^^^',c1,item_right_nodes,right_nodes)
                if item_left_nodes == left_nodes and c1:
                    results.append(item)
            else:
                results.append(item)
        if not results:
            logging.warning(f"No data matching {name}, {left_nodes}, and {right_nodes} was found.")
        return results
    logging.warning(f"No data with the key {name} was found.")
    return []



def save_routing_expertise(file_path, data, name, new_item):
    new_item = convert_tuples_to_lists(new_item)
    try:
        if name not in data:
            data[name] = [new_item]
        else:
            found = False
            for index, item in enumerate(data[name]):
                if item.get('left_nodes') == new_item.get('left_nodes') and item.get('right_nodes') == new_item.get(
                        'right_nodes'): 
                    # if item.get('edges') is None or len(item.get('edges'))==0 :
                    #     print('add new')
                    data[name][index] = new_item
                    found = True
                    break
            if not found:
                data[name].append(new_item)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print("JSON file has been updated.")
    except Exception as e:
        logging.error(f"An error occurred while saving the file: {e}")

class RouteDB:
    def __init__(self, track_num):
        self.db_dir = 'ipmigration/cell/apr/cir/pattern_route'
        self.track_num = track_num
        self.db_path = os.path.join(self.db_dir,'pattern_route_%d.json'%(self.track_num))
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as file:
                route_data = json.load(file)
                copy_json_file(self.db_path) #for save
        except FileNotFoundError:
            route_data = {}

        self.data = route_data
    
    def save(self, path=None):
        if not(path):
            path = self.db_path
        # try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)
        print("JSON file has been updated.")
        # except Exception as e:
            # logging.error(f"An error occurred while saving the file: {e}")
    
    def find(self, name, l_nodes, r_nodes, m2_nodes):
        if name in self.data: #not inv pattern
            for index, item in enumerate(self.data[name]):
                if is_dict_equal(l_nodes,item.get('l_nodes')) and \
                   is_dict_equal(r_nodes,item.get('r_nodes')) and\
                   is_dict_equal(m2_nodes,item.get('m2_nodes')) :
                       result = True
                       data = list(item.get('data').values())[0]
                       # print(self.data[name])
                       routed_edges = {k:list_to_tuple(v) for k,v in data.get('routed_edges').items()}
                       io_pins = data.get('io_pins')
                       pw_pins = data.get('pw_pins')
                       graph_index = data.get('graph_index')
                       m2_edges = data.get('m2_edges')
                       v1_pins = data.get('v1_pins')
                       return result, graph_index, routed_edges, io_pins, pw_pins, m2_edges,v1_pins
        return False, None, None, None, None, None   ,None
        # else:
        #     pass
        
        
        
        # pass
    
    def update(self, name, l_nodes, r_nodes, m2_nodes, graph_index, 
               routed_edges, io_pins, pw_pins, m2_edges,v1_pins, save=True):
        
        new_data = {'graph_index':graph_index,
                    'routed_edges':routed_edges, 
                    'io_pins':io_pins, 
                    'pw_pins':pw_pins,
                    'm2_edges':m2_edges,
                    'v1_pins':v1_pins}
        
        new_item = {'l_nodes'    :l_nodes,
                    'r_nodes':r_nodes,
                    'm2_nodes'   :m2_nodes,
                    'data': {graph_index:new_data}}


        if name not in self.data:
            # if name != 'INV':
            self.data[name] = [new_item]
        else:
            found = False
            for index, item in enumerate(self.data[name]):
                if is_dict_equal(l_nodes,item.get('l_nodes')) and \
                   is_dict_equal(r_nodes,item.get('r_nodes')) and\
                   is_dict_equal(m2_nodes,item.get('m2_nodes')) :
                       self.data[name][index]['data'][graph_index] = new_data
                       found = True
                       break

            if not found:
                self.data[name].append(new_item)   
        if save:
            self.save()
        
        # new_item = convert_tuples_to_lists(new_item)

    
def is_dict_equal(dict_a, dict_b):
    if len(dict_a) != len(dict_b):
        return False
    for key, value in dict_a.items():
        if key not in dict_b:
            return False
        if dict_b[key] != value:
            return False
    return True    


def copy_json_file(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return
        now = datetime.now()
        month_day = now.strftime("%m%d")
        file_name, file_ext = os.path.splitext(file_path)
        new_file_name = f"{file_name}_{month_day}{file_ext}"
        with open(file_path, 'rb') as src, open(new_file_name, 'wb') as dst:
            dst.write(src.read())
        print(f"File successfully copied to {new_file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
if __name__ == "__main__":
    file_path = 'example.json'
    name = 'your_name'
    left_nodes = {'a': [1, 2], 'b': [3, 4]}
    right_nodes = {'c': [5, 6], 'd': [7, 8]}

    loaded_data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
    except FileNotFoundError:
        logging.error(f"Error: File {file_path} was not found.")
    except json.JSONDecodeError:
        logging.error("Error: Unable to parse the JSON file.")



    matches = load_routing_expertise(loaded_data, name, left_nodes, right_nodes)
    if matches:
        print("Matching data found:")
        for match in matches:
            print(match)
    else:
        print("No matching data found.")

    # Example new item
    new_item = {
        "left_nodes": {'a': (1, 3), 'b': (3, 4)},
        "right_nodes": {'c': (5, 6), 'd': (7, 8)},
        "edges": ["edge3", "edge4"]
    }
    name = '1234'
    save_routing_expertise(file_path, loaded_data, name, new_item)
    