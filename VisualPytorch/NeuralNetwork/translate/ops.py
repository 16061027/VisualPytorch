
'''
step:
	make_graph:
		fill the graph{} and done{}
		check model
		get codes
	return

exceptioin:
	A:
	B:
	C:
	D:
	E:
	F:多个start
	G:

'''

import numpy as np
import sys
from model import Node, Vector
from exception import *
import queue

#global parameters
layer_used_time = {'view_layer': 0, 'linear_layer': 0, 'conv1d_layer': 0, 'conv2d_layer': 0, 'element_wise_add_layer':0, 'concatenate_layer':0}
nn = 'torch.nn.'
nn_linear = 'torch.nn.Linear'
nn_conv1d = 'torch.nn.Conv1d'
nn_conv2d = 'torch.nn.Conv2d'
nn_view = '.view'
nn_sequential = 'torch.nn.Sequential'

#array of layers
start_layer = ['start']
norm_layer = ['conv1d_layer', 'conv2d_layer', 'view_layer', 'linaer_layer']
multi_layer = ['element_wise_add_layer', 'concatenate_layer']

#parameters of convolutional layer
conv_layer_para = ['in_channels', 'out_channels', 'kernel_size', 'stride', 'padding']

#model
#graph = Vector()
graph = {} #record the node information
done = {}

def error(str):

    return None

def init():
	for key in layer_used_time:
		layer_used_time[key] = 0
	graph = {} #init
	done = {}

def generate_n_tap(n):
    ans = ''
    n = n * 4
    for i in range(n):
        ans = ans + ' '
    return ans


def add_static_info(Main, glob):
    Main = np.append(Main, 'from Model import *')
    Main = np.append(Main, 'from Ops import *')	
    names = {'epoch': '1', 'optimizer': 'torch.optim.Adam', 'learning_rate': '0.5', \
             'batch_size': '1', 'data_dir': 'None', 'data_set': 'None', 'train': 'True'}

    for name in names:
        tmp = name + ' = '
        if name in glob:
            tmp = tmp + str(glob[name])
        elif name in names:
            tmp = tmp + str(names[name])
        else:
            raise ModelError('%s: No such global attribute' % name)
            sys.exit(1)
        Main = np.append(Main, tmp)

    return Main


def generate_variable_name(layer_name):
    cnt = 0
    try:
        cnt = layer_used_time[layer_name]
    except:
        raise ModelError('%s: No such layer' % layer_name)
        sys.exit(1)
    ans = layer_name
    if (cnt != 0):
        ans = ans + '_' + str(cnt)
    return ans + '_data'


def add_import_info():
    ans = np.array(["import torch", "import numpy", "import torchvision", "import os"])

    return ans, ans, ans


def add_init_info():
    ans = np.array(['class NET(torch.nn.Module):', generate_n_tap(1) + 'def __init__(self):',
                    generate_n_tap(2) + 'super(NET, self).__init__()'])

    return ans

def update_layer_used_time(layer):
    try:
        layer_used_time[layer] = layer_used_time[layer] + 1
    except:
        raise ModelError('%s: No such layer' % layer_name)
        sys.exit(1)


def generate_layer_name(layer_name):
    ans = 'self.' + layer_name
    cnt = 0
    try:
        cnt = layer_used_time[layer_name]
    except:
        raise ModelError('%s: No such layer' % layer_name)
        sys.exit(1)
    if cnt > 0:
        ans = ans + '_' + str(cnt)
    return ans


def add_linear_to_init_forward(init, forward, in_data, out_data, node):
    self_layer = generate_layer_name(node['name'])

    forward_tmp = generate_n_tap(2) + out_data + ' = ' + self_layer + '(' + in_data + ')'
    forward = np.append(forward, forward_tmp)

    in_c = str(node['attribute']['in_channels'])
    out_c = str(node['attribute']['out_channels'])

    init_tmp = generate_n_tap(2) + self_layer + ' = ' + nn_linear + '(' + in_c + ', ' + out_c + ')'
    init = np.append(init, init_tmp)

    return init, forward


def parse_shape(str_shape):
    try:
        shape = list(map(int, str_shape.split(',')))

    except:
        raise ModelError('Invalid view shape')
    if (len(shape) == 0):
        raise ModelError('Invalid view shape')
    return str(shape)[1:-1]


def add_view_to_init_forward(init, forward, in_data, out_data, node):
    shape = parse_shape(node['attribute']['shape'])
    forward_tmp = generate_n_tap(2) + out_data + ' = ' + in_data + nn_view + '(' + shape + ')'
    forward = np.append(forward, forward_tmp)

    return init, forward

def generate_one_conv_layer_para(para_name, para_val):
	ans = generate_n_tap(4) + para_name + ' = ' + para_val + ','

	return ans


def add_conv_layer_para(init, node):

	for para in conv_layer_para:
		init = np.append(init, generate_one_conv_layer_para(para, node['attribute'][para]))

	return init
def add_activity_pooling(init, node):
	activity_pooling = ['activity', 'pool_way']
	for attr in activity_pooling:
			if node['attribute'][attr] != 'None':
				init_tmp = generate_n_tap(3) + node['attribute'][attr] + '(),'
				init = np.append(init, init_tmp)
	return init

def add_convlayer_to_init_forward(init, forward, in_data, out_data, node):
    self_layer = generate_layer_name(node['name'])
    # add forward
    forward_tmp = generate_n_tap(2) + out_data + ' = ' + self_layer + '(' + in_data + ')'
    forward = np.append(forward, forward_tmp)
    # add init
    init_tmp = generate_n_tap(2) + self_layer + ' = ' + nn_sequential + '('
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(3)
    if node['name'] == 'conv1d_layer':
        init_tmp = init_tmp + nn_conv1d + '('
    elif node['name'] == 'conv2d_layer':
        init_tmp = init_tmp + nn_conv2d + '('
    else:
        raise ModelError('%s: No such convolution layer' % node['name'])
        sys.exit(1)
    init = np.append(init, init_tmp)

    #change here
    init = add_conv_layer_para(init, node)

    init_tmp = generate_n_tap(3) + '),'
    init = np.append(init, init_tmp)

    init = add_activity_pooling(init, node)

    init_tmp = generate_n_tap(2) + ')'
    init = np.append(init, init_tmp)

    return init, forward


def add_layer_except_add_and_concate(init_func, forward_func, in_data, out_data, node):
    init = np.array([])
    forward = np.array([])

    node_name = node['name']
    if node_name == 'linear_layer':
        init, forward = add_linear_to_init_forward(init, forward, in_data, out_data, node)
    elif node_name == 'view_layer':
        init, forward = add_view_to_init_forward(init, forward, in_data, out_data, node)
    elif node_name == 'conv1d_layer' or node_name == 'conv2d_layer':
        init, forward = add_convlayer_to_init_forward(init, forward, in_data, out_data, node)
    else:
        raise ModelError('%s: No such layer' % node_name)

    return np.concatenate((init_func, init)), np.concatenate((forward_func, forward))

def find_start_id(nets):
    one_start = True
    start_id = None

    for key in nets:
    	if nets[key]['name'] == 'start':
    		if start_id is not None:
    			one_start = False
    		start_id = key
        
    return start_id, one_start    

def add_node_information_about_conv_layer(edge, node):
    try:
        graph[edge['target']['id']].in_channels = int(node['in_channels'])
    except:
        raise ModelError('invalid in_channels of convolution layer')

    try:
        graph[edge['target']['id']].out_channels = int(node['out_channels'])
    except:
        raise ModelError('invalid out_channels of convolution layer')

    try:
        graph[edge['target']['id']].kernel_size = int(node['kernel_size'])
    except:
        raise ModelError('invalid kernel_size of convolution layer')

    try:
        graph[edge['target']['id']].stride = int(node['stride'])
    except:
        raise ModelError('invalid stride of convolution layer')

    try:
        graph[edge['target']['id']].padding = int(node['padding'])
    except:
        raise ModelError('invalid padding of convolution layer')


    graph[edge['target']['id']].activity = node['activity']
    graph[edge['target']['id']].pool_way = node['pool_way']


def get_next_nodes_and_update_pre_nodes(nets, nets_conn, cur_id):
    next_nodes = np.array([], dtype = str)
    fa_nodes = np.array([], dtype = str)
    flag = True

    for edge in nets_conn:
        if edge['source']['id'] == cur_id:
            next_nodes = np.append(next_nodes, edge['target']['id'])

            if edge['target']['id'] not in done.keys():
                graph[edge['target']['id']] = Node(id = edge['target']['id'])
                graph[edge['target']['id']].name = nets[edge['target']['id']]['name']
                node = nets[edge['target']['id']]['attribute']

                if nets[edge['target']['id']]['name'] in ['conv2d_layer', 'conv1d_layer']:
                    add_node_information_about_conv_layer(edge, node)

                if nets[edge['target']['id']]['name'] == 'view_layer':
                        try:
                            shape = np.array(list(map(int, nets[edge['target']['id']]['attribute']['shape'].split(','))))
                        except:
                            raise ModelError('%s: invalid view_layer shape' % nets[edge['target']['id']]['attribute']['shape'])
                        graph[edge['target']['id']].data_shape = shape

                if nets[edge['target']['id']]['name'] == 'concatenate_layer':
                    try:
                        graph[edge['target']['id']].cat_dim = int(node['dim'])
                    except:
                        raise ModelError('%s: invalid concatenate dimension' % node['dim'])

                done[edge['target']['id']] = False	

        if edge['target']['id'] == cur_id:
            fa_nodes = np.append(fa_nodes, edge['source']['id'])
            if not done[edge['source']['id']]:
            	flag = False

    graph[cur_id].next = next_nodes
    graph[cur_id].fa = fa_nodes

    name = nets[cur_id]['name']
    if name in start_layer or name in norm_layer:
        if name == 'start' and len(graph[cur_id].fa) != 0:
            raise ModelError('start: can not have father nodes')
        elif name != 'start' and len(graph[cur_id].fa) != 1:
            raise ModelError('%s: should have one and only one father node' % name)
     
    if name in multi_layer and len(graph[cur_id].fa) == 0:
        raise ModelError('%s: should have one or more father nodes' % name)    

    
    return next_nodes, flag

def add_concatenate_layer(init_func, forward_func, cur_id, out_data):
    #check shape first
    dim = graph[cur_id].cat_dim
    array_of_inputs = graph[cur_id].fa[0]
    for indx in range(1, len(graph[cur_id].fa)):
        #check shape
        array_of_inputs = array_of_inputs + ', ' + graph[cur_id].fa[indx]      
    #check dim
    code = generate_n_tap(2) + out_data + ' = torch.cat((' + array_of_inputs + '), ' + graph[cur_id].cat_dim + ')'

    return init_func, np.append(forward_func, code)

def add_element_wise_add_layer(init_func, forward_func, cur_id, out_data):
    #error not ok
    if len(graph[cur_id].fa) == 0:
        raise ModelError('element wise layer has no inputs')
    
    array_of_nodes = '[' + graph[cur_id].fa[0]
    for indx in range(1, len(graph[cur_id].fa)):
        array_of_nodes = array_of_nodes + ', ' + graph[graph[cur_id].fa[indx]].data

    array_of_nodes = array_of_nodes + ']'
    code = generate_n_tap(2) + out_data + ' = element_wise_add(' + array_of_nodes + ')'
    forward_func = np.append(forward_func, code)

    return init_func, forward_func


def make_graph(nets, nets_conn, init_func, forward_func):
   #error not ok
    start_id, one_start = find_start_id(nets)

    Q = queue.Queue()
    #Q.put(start_id)
    graph[start_id] = Node(id = start_id, name = 'start', data = 'x_data')
    done[start_id] = True

    cur_id = start_id

    next_nodes, flag = get_next_nodes_and_update_pre_nodes(nets, nets_conn, cur_id)

    # #update Q
    for node_id in next_nodes:
        Q.put(node_id)

    while not Q.empty():
        cur_id = Q.get()
        if done[cur_id]:
            continue
        next_nodes, flag = get_next_nodes_and_update_pre_nodes(nets, nets_conn, cur_id)
        if cur_id != start_id and flag is False:
            Q.put(cur_id)
            continue

        #update Q
        for node_id in next_nodes:
            Q.put(node_id)
        #generate codes and update Node.fa[]
        out_data = generate_variable_name(nets[cur_id]['name'])
        graph[cur_id].data = out_data
        if nets[cur_id]['name'] == 'concatenate_layer':
            init_func, forward_func = add_concatenate_layer(init_func, forward_func, cur_id, out_data)
        elif nets[cur_id]['name'] == 'element_wise_add_layer':
            init_func, forward_func = add_element_wise_add_layer(init_func, forward_func, cur_id, out_data)
        else:
            in_data = graph[graph[cur_id].fa[0]].data
        	
            init_func, forward_func = add_layer_except_add_and_concate(init_func, forward_func, in_data, out_data, nets[cur_id])
        update_layer_used_time(nets[cur_id]['name'])

        done[cur_id] = True

    return init_func, forward_func


def add_net_info(nets, nets_conn):
    # NET declaration and the head of init()
    init_func = add_init_info()
    # head of forword()
    forward_func = np.array([generate_n_tap(1) + 'def forward(self, x_data):'])


    init_func, forward_func = make_graph(nets, nets_conn, init_func, forward_func)


    return np.concatenate((init_func, forward_func))

def add_element_add_to_Ops(Ops):
    tmp = ['def element_wise_add(inputs):', 
            generate_n_tap(1) + 'ans = inputs[0]', 
            generate_n_tap(1) + 'for indx in range(1, len(inputs)):', 
            generate_n_tap(2) + 'ans.add_(inputs[indx])', 
            generate_n_tap(1) + 'return ans']

    return np.concatenate((Ops, tmp))


def main_func(edge_record):
    # add import information
    init()
    Main, Model, Ops = add_import_info()

    # Main
    glob = edge_record['static']
    Main = add_static_info(Main, glob)

    # Model
    Model = np.concatenate((Model, add_net_info(edge_record['nets'], edge_record['nets_conn'])))
    # Ops
    Ops = add_element_add_to_Ops(Ops)
    return Main, Model, Ops


test = {
    "nets": {
        "canvas_1": {
            "name": "start",
            "attribute": {
                "start": "true"
            },
            "left": "350px",
            "top": "163px"
        },
        "canvas_2": {
            "name": "view_layer",
            "attribute": {
                "shape": "3"
            },
            "left": "325px",
            "top": "307px"
        },
        "canvas_3": {
            "name": "conv1d_layer",
            "attribute": {
                "in_channels": "2",
                "out_channels": "32",
                "kernel_size": "2",
                "stride": "3",
                "padding": "2",
                "activity": "torch.nn.functional.leaky_relu",
                "pool_way": "torch.nn.functional.max_pool1d"
            },
            "left": "590px",
            "top": "312px"
        },
        "canvas_4": {
            "name": "conv2d_layer",
            "attribute": {
                "in_channels": "2",
                "out_channels": "3",
                "kernel_size": "2",
                "stride": "1",
                "padding": "3",
                "activity": "torch.nn.functional.tanh",
                "pool_way": "torch.nn.AvgPool2d"
            },
            "left": "401px",
            "top": "461px"
        }
    },
    "nets_conn": [
        {
            "source": {
                "id": "canvas_1",
                "anchor_position": "Bottom"
            },
            "target": {
                "id": "canvas_2",
                "anchor_position": "Top"
            }
        },
        {
            "source": {
                "id": "canvas_2",
                "anchor_position": "Bottom"
            },
            "target": {
                "id": "canvas_4",
                "anchor_position": "Top"
            }
        },
        {
            "source": {
                "id": "canvas_4",
                "anchor_position": "Right"
            },
            "target": {
                "id": "canvas_3",
                "anchor_position": "Left"
            }
        }
    ],
    "static": {
        "epoch": "1",
        "learning_rate": "0.5",
        "batch_size": "1"
    }
}

Main, Model, Ops = main_func(test)
print('Model')
for val in Model:
	print(val)
print('Ops', Ops)
for ops in Ops:
	print(ops)






