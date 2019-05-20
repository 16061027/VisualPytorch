
'''

Copyright @ 2019 buaa_huluwa. All rights reserved.

View more, visit our team's home page: https://home.cnblogs.com/u/1606-huluwa/


exception defined as follows:
	A:
	B:
	C:
	D:
	E:
	F:start
	G:

'''


import numpy as np
import sys
from .model import Node, Vector, GLOB
from .exception import *
import queue

#global parameters
# GL.layer_used_time = {'view_layer': 0, 'linear_layer': 0, 'conv1d_layer': 0, 'conv2d_layer': 0, 'element_wise_add_layer':0, 'concatenate_layer':0}
# GL.nn_linear = 'torch.nn.Linear'
# GL.nn_conv1d = 'torch.nn.Conv1d'
# GL.nn_conv2d = 'torch.nn.Conv2d'
# GL.nn_view = '.view'
# GL.nn_sequential = 'torch.nn.Sequential'

# #array of layers
# GL.start_layer = ['start']
# GL.norm_layer = ['conv1d_layer', 'conv2d_layer', 'view_layer', 'linaer_layer']
# GL.multi_layer = ['element_wise_add_layer', 'concatenate_layer']
# GL.layers_except_start = GL.norm_layer + GL.multi_layer

#parameters of convolutional layer
conv_layer_para = ['in_channels', 'out_channels', 'kernel_size', 'stride', 'padding']

#model
#GL.graph = Vector()


GL = GLOB()#global parameters

def error(str):

    return None

def init():
	for key in GL.layer_used_time:
		GL.layer_used_time[key] = 0
	GL.graph = {} #init
	GL.done = {}

def generate_n_tap(n):
    ans = ''
    n = n * 4
    for i in range(n):
        ans = ans + ' '
    return ans


def add_static_info(Main, glob):
    tmp = np.array(['from Model import *', 'from Ops import *', '', '', '#Hyper Parameters'])	

    Main = np.concatenate((Main, tmp))

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
        cnt = GL.layer_used_time[layer_name]
    except:
        raise ModelError('%s: No such layer' % layer_name)
        sys.exit(1)
    ans = layer_name
    if (cnt != 0):
        ans = ans + '_' + str(cnt)
    return ans + '_data'


def add_import_info():
    ans = np.array(['', '#standard library', "import os", '', '#third-party library', "import torch", "import numpy", "import torchvision", '', ''])

    return ans, ans, ans


def add_init_info():
    ans = np.array(['class NET(torch.nn.Module):', generate_n_tap(1) + 'def __init__(self):',
                    generate_n_tap(2) + 'super(NET, self).__init__()'])

    return ans

def update_GL_layer_used_time(layer):
    try:
        GL.layer_used_time[layer] = GL.layer_used_time[layer] + 1
    except:
        raise ModelError('%s: No such layer' % layer_name)
        sys.exit(1)


def generate_layer_name(layer_name):
    ans = 'self.' + layer_name
    cnt = 0
    try:
        cnt = GL.layer_used_time[layer_name]
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

    init_tmp = generate_n_tap(2) + self_layer + ' = ' + GL.nn_linear + '(' + in_c + ', ' + out_c + ')'
    init = np.append(init, init_tmp)

    return init, forward


def parse_shape(str_shape):
    try:
        shape = list(map(int, str_shape.split(',')))

    except:
        raise ModelError('Invalid view shape')
    if (len(shape) == 0):
        raise ModelError('Invalid view shape')
    return shape, str(shape)[1:-1]


def add_view_to_init_forward(init, forward, in_data, out_data, node):
    shape, shape_str = parse_shape(node['attribute']['shape'])

    #add shape checking of reshape layer  


    forward_tmp = generate_n_tap(2) + out_data + ' = ' + in_data + GL.nn_view + '(' + shape_str + ')'
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
    init_tmp = generate_n_tap(2) + self_layer + ' = ' + GL.nn_sequential + '('
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(3)
    if node['name'] == 'conv1d_layer':
        init_tmp = init_tmp + GL.nn_conv1d + '('
    elif node['name'] == 'conv2d_layer':
        init_tmp = init_tmp + GL.nn_conv2d + '('
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
        GL.graph[edge['target']['id']].in_channels = int(node['in_channels'])
    except:
        raise ModelError('invalid in_channels of convolution layer')

    try:
        GL.graph[edge['target']['id']].out_channels = int(node['out_channels'])
    except:
        raise ModelError('invalid out_channels of convolution layer')

    try:
        GL.graph[edge['target']['id']].kernel_size = int(node['kernel_size'])
    except:
        raise ModelError('invalid kernel_size of convolution layer')

    try:
        GL.graph[edge['target']['id']].stride = int(node['stride'])
    except:
        raise ModelError('invalid stride of convolution layer')

    try:
        GL.graph[edge['target']['id']].padding = int(node['padding'])
    except:
        raise ModelError('invalid padding of convolution layer')


    GL.graph[edge['target']['id']].activity = node['activity']
    GL.graph[edge['target']['id']].pool_way = node['pool_way']


def get_next_nodes_and_update_pre_nodes(nets, nets_conn, cur_id):
    next_nodes = np.array([], dtype = str)
    fa_nodes = np.array([], dtype = str)
    flag = True

    for edge in nets_conn:
        if edge['source']['id'] == cur_id:
            next_nodes = np.append(next_nodes, edge['target']['id'])

            if edge['target']['id'] not in GL.done.keys():
                GL.graph[edge['target']['id']] = Node(id = edge['target']['id'])
                GL.graph[edge['target']['id']].name = nets[edge['target']['id']]['name']
                node = nets[edge['target']['id']]['attribute']

                if nets[edge['target']['id']]['name'] in ['conv2d_layer', 'conv1d_layer']:
                    add_node_information_about_conv_layer(edge, node)

                if nets[edge['target']['id']]['name'] == 'view_layer':
                        try:
                            shape = np.array(list(map(int, nets[edge['target']['id']]['attribute']['shape'].split(','))))
                        except:
                            raise ModelError('%s: invalid view_layer shape' % nets[edge['target']['id']]['attribute']['shape'])
                        GL.graph[edge['target']['id']].data_shape = shape

                if nets[edge['target']['id']]['name'] == 'concatenate_layer':
                    try:
                        GL.graph[edge['target']['id']].cat_dim = int(node['dim'])
                    except:
                        raise ModelError('%s: invalid concatenate dimension' % node['dim'])

                GL.done[edge['target']['id']] = False	

        if edge['target']['id'] == cur_id:
            fa_nodes = np.append(fa_nodes, edge['source']['id'])
            if not GL.done[edge['source']['id']]:
            	flag = False

    GL.graph[cur_id].next = next_nodes
    GL.graph[cur_id].fa = fa_nodes

    name = nets[cur_id]['name']
    if name in GL.start_layer or name in GL.norm_layer:
        if name == 'start' and len(GL.graph[cur_id].fa) != 0:
            raise ModelError('start: can not have father nodes')
        elif name != 'start' and len(GL.graph[cur_id].fa) != 1:
            raise ModelError('%s: should have one and only one father node' % name)
     
    if name in GL.multi_layer and len(GL.graph[cur_id].fa) == 0:
        raise ModelError('%s: should have one or more father nodes' % name)    

    
    return next_nodes, flag


def add_concatenate_layer(init_func, forward_func, cur_id, out_data):
    #check shape first
    dim = GL.graph[cur_id].cat_dim
    array_of_inputs = GL.graph[GL.graph[cur_id].fa[0]].data
    for indx in range(1, len(GL.graph[cur_id].fa)):
        #check shape
        array_of_inputs = array_of_inputs + ', ' + GL.graph[GL.graph[cur_id].fa[indx]].data      
    #check dim
    code = generate_n_tap(2) + out_data + ' = torch.cat((' + array_of_inputs + '), ' + str(GL.graph[cur_id].cat_dim) + ')'

    return init_func, np.append(forward_func, code)


def add_element_wise_add_layer(init_func, forward_func, cur_id, out_data):
    #error not ok
    if len(GL.graph[cur_id].fa) == 0:
        raise ModelError('element wise layer has no inputs')
    
    array_of_nodes = '[' + GL.graph[GL.graph[cur_id].fa[0]].data
    for indx in range(1, len(GL.graph[cur_id].fa)):
        array_of_nodes = array_of_nodes + ', ' + GL.graph[GL.graph[cur_id].fa[indx]].data

    array_of_nodes = array_of_nodes + ']'
    code = generate_n_tap(2) + out_data + ' = element_wise_add(' + array_of_nodes + ')'
    forward_func = np.append(forward_func, code)

    return init_func, forward_func


def make_graph(nets, nets_conn, init_func, forward_func):
   #error not ok
    start_id, one_start = find_start_id(nets)

    Q = queue.Queue()
    #Q.put(start_id)
    GL.graph[start_id] = Node(id = start_id, name = 'start', data = 'x_data')
    GL.done[start_id] = True

    cur_id = start_id

    next_nodes, flag = get_next_nodes_and_update_pre_nodes(nets, nets_conn, cur_id)

    # #update Q
    for node_id in next_nodes:
        Q.put(node_id)

    while not Q.empty():
        cur_id = Q.get()
        if GL.done[cur_id]:
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
        GL.graph[cur_id].data = out_data
        if nets[cur_id]['name'] == 'concatenate_layer':
            init_func, forward_func = add_concatenate_layer(init_func, forward_func, cur_id, out_data)
        elif nets[cur_id]['name'] == 'element_wise_add_layer':
            init_func, forward_func = add_element_wise_add_layer(init_func, forward_func, cur_id, out_data)
        else:
            in_data = GL.graph[GL.graph[cur_id].fa[0]].data
        	
            init_func, forward_func = add_layer_except_add_and_concate(init_func, forward_func, in_data, out_data, nets[cur_id])
        update_GL_layer_used_time(nets[cur_id]['name'])

        GL.done[cur_id] = True

    return init_func, forward_func


def add_net_info(nets, nets_conn):
    # NET declaration and the head of init()
    init_func = add_init_info()
    # head of forword()
    forward_func = np.array([generate_n_tap(1) + 'def forward(self, x_data):'])


    init_func, forward_func = make_graph(nets, nets_conn, init_func, forward_func)

    #add check for return
    for node in nets:
        if node not in GL.graph or (nets[node]['name'] in GL.layers_except_start and len(GL.graph[node].fa) == 0):
            raise ModelError('invalid layer')
    
    #add return statement to forward_func
    ret_state = None
    for node_id in GL.graph:
        if len(GL.graph[node_id].next) == 0:
            if ret_state is None: 
                ret_state = GL.graph[node_id].data
            else:
                ret_state = ret_state + ', ' + GL.graph[node_id].data
    ret_state = generate_n_tap(2) + 'return ' + ret_state

    return np.concatenate((init_func, np.append(forward_func, ret_state)))

def add_element_add_to_Ops(Ops):
    tmp = ['def element_wise_add(inputs):', 
            generate_n_tap(1) + 'ans = inputs[0]', 
            generate_n_tap(1) + 'for indx in range(1, len(inputs)):', 
            generate_n_tap(2) + 'ans.add_(inputs[indx])', 
            generate_n_tap(1) + 'return ans']

    return np.concatenate((Ops, tmp))

def generate_copyright_information(flag):
    copy_right = 'Copyright @2019 buaa_huluwa. All rights reserved.'

    view_more = "View more, visit our team's home page: https://home.cnblogs.com/u/1606-huluwa/"

    declaration = 'This code is the corresponding pytorch code generated from the model built by the user.'

    Main_py = ' "main.py" mainly contains the code of the training and testing part, and you can modify it according to your own needs.'

    Model_py = '"model.py" contains the complete model code, and you can modify it according to your own needs'

    Ops_py = '"ops.py" contains functions you might use'

    none = ''

    tmp = np.array([])
    if flag == 'Main':
        tmp = np.array(["'''", none, copy_right, none, view_more, none, none, declaration, none, Main_py, none, "'''"])

    if flag == 'Model':
        tmp = np.array(["'''", none, declaration, none, Model_py, none, "'''"])

    if flag == 'Ops':
        tmp = np.array(["'''", none, declaration, none, Ops_py, none, "'''"])
    
    return tmp

def generate_train_codes():
    ans = np.array(['',
    	          '', 
    	          '#initialize a NET object', 
                  'net = NET()',
                  '#print net architecture', 
                  'print(net)', 
                  '',  
                  '', 
    	          '#load your own dataset and normalize', '', '',
                  '', 
                  '#you can add some functions for visualization here or you can ignore them', 
                  '', 
                  '', 
                  '', 
                  '#training and testing, you can modify these codes as you expect', 
                  'for epo in range(epoch):', 
                  '', 
                  ''
    	])


    return ans

def main_func(edge_record):
    # add import information
    init()

    Main, Model, Ops = add_import_info()

    # Main
    glob = edge_record['static']
    Main = add_static_info(Main, glob)
    Main = np.concatenate((generate_copyright_information('Main'), Main, generate_train_codes()))
    

    # Model
    Model = np.concatenate((Model, add_net_info(edge_record['nets'], edge_record['nets_conn'])))
    Model = np.concatenate((generate_copyright_information('Model'), Model))

    # Ops
    Ops = add_element_add_to_Ops(Ops)
    Ops = np.concatenate((generate_copyright_information('Ops'), Ops))

    return Main, Model, Ops


