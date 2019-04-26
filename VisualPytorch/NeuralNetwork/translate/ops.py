import numpy as np
import sys

# init
layer_used_time = {'view_layer': 0, 'linear_layer': 0, 'conv1d_layer': 0, 'conv2d_layer': 0}
nn = 'torch.nn.'
nn_linear = 'torch.nn.Linear'
nn_conv1d = 'torch.nn.Conv1d'
nn_conv2d = 'torch.nn.Conv2d'
nn_view = '.view'
nn_sequential = 'torch.nn.Sequential'


def init():
	layer_used_time['view_layer'] = 0
	layer_used_time['linear_layer'] = 0
	layer_used_time['conv1d_layer'] = 0
	layer_used_time['conv2d_layer'] = 0


def generate_n_tap(n):
    ans = ''
    n = n * 4
    for i in range(n):
        ans = ans + ' '
    return ans


def add_static_info(Main, glob):
    names = {'epoch': '1', 'optimizer': 'torch.optim.Adam', 'learning_rate': '0.5', \
             'batch_size': '1', 'data_dir': 'None', 'data_set': 'None', 'train': 'True'}
    for name in names:
        tmp = name + ' = '
        if name in glob:
            tmp = tmp + str(glob[name])
        elif name in names:
            tmp = tmp + str(names[name])
        else:
            print('[ERROR] %s: No such global attribute' % layer_name)
            sys.exit(1)
        Main = np.append(Main, tmp)
    return Main


def generate_variable_name(layer_name):
    cnt = 0
    try:
        cnt = layer_used_time[layer_name]
    except:
        print('[ERROR] %s: No such layer' % layer_name)
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


def find_next_edge(network, point_name):
    ans = None
    for edge in network:
        if edge['source']['id'] == point_name:
            ans = edge
            break
    return ans


def update_layer_used_time(layer):
    try:
        layer_used_time[layer] = layer_used_time[layer] + 1
    except:
        print('[ERROR] %s: No such layer' % layer_name)
        sys.exit(1)


def generate_layer_name(layer_name):
    ans = 'self.' + layer_name
    cnt = 0
    try:
        cnt = layer_used_time[layer_name]
    except:
        print('[ERROR] %s: No such layer' % layer_name)
        sys.exit(1)
    if cnt > 0:
        ans = ans + '_' + str(cnt)
    return ans


def add_linear_to_init_forward(init, forward, in_data, out_data, node):
    self_layer = generate_layer_name(node['name'])

    forward_tmp = generate_n_tap(2) + out_data + ' = ' + self_layer + '(' + in_data + ')'
    forward = np.append(forward, forward_tmp)

    in_c = str(node['attribute']['in_channel'])
    out_c = str(node['attribute']['out_channel'])
    init_tmp = generate_n_tap(2) + self_layer + ' = ' + nn_linear + '(' + in_c + ', ' + out_c + ')'
    init = np.append(init, init_tmp)

    return init, forward


def parse_shape(str_shape):
    try:
        shape = list(map(int, str_shape.split(',')))

    except:
        print('[ERROR] %s: Invalid view shape' % str)
        sys.exit(1)
    if (len(shape) == 0):
        print('[ERROR] %s: Invalid view shape' % str)
        sys.exit(1)
    return str(shape)[1:-1]


def add_view_to_init_forward(init, forward, in_data, out_data, node):
    shape = parse_shape(node['attribute']['shape'])
    forward_tmp = generate_n_tap(2) + out_data + ' = ' + in_data + nn_view + '(' + shape + ')'
    forward = np.append(forward, forward_tmp)

    return init, forward


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
        print('[ERROR] %s: No such convolution layer' % node['name'])
        sys.exit(1)
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(4) + 'in_channels = ' + node['attribute']['in_channel'] + ','
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(4) + 'out_channels = ' + node['attribute']['out_channel'] + ','
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(4) + 'kernel_size = ' + node['attribute']['kernel_size'] + ','
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(4) + 'stride = ' + node['attribute']['stride'] + ','
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(4) + 'padding = ' + node['attribute']['padding'] + ','
    init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(3) + '),'
    init = np.append(init, init_tmp)

    # activity
    if node['attribute']['activity'] != 'None':
        init_tmp = generate_n_tap(3) + node['attribute']['activity'] + '(),'
        init = np.append(init, init_tmp)

    # pooling
    if node['attribute']['pool_way'] != 'None':
        init_tmp = generate_n_tap(3) + node['attribute']['pool_way'] + '(),'
        init = np.append(init, init_tmp)

    init_tmp = generate_n_tap(2) + ')'
    init = np.append(init, init_tmp)

    return init, forward


def add_one_layer(init_func, forward_func, in_data, out_data, node):
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
        print('[ERROR] %s: No such layer' % node_name)
        sys.exit(1)
    return np.concatenate((init_func, init)), np.concatenate((forward_func, forward))


def find_start(network, start):
    for edge in network:
        if edge['source']['name'] == start:
            ans = edge['source']['id']
            break

    return ans


def add_net_info(network):
    # NET declaration and the head of init()
    init_func = add_init_info()
    # head of forword()
    forward_func = np.array([generate_n_tap(1) + 'def forward(self, x_data):'])

    in_data = ''
    out_data = 'x_data'

    # replace name with id
    edge_name = find_start(network, 'start')
    init_name = edge_name
    edge = find_next_edge(network, edge_name)
    while edge is not None:
        # if edge_name != init_name:
        # 	in_data = out_data
        # 	out_data = generate_variable_name(edge['source']['name'])
        # #
        # 	init_func, forward_func = add_one_layer(init_func, forward_func, in_data, out_data, edge['source'])
        # 	update_layer_used_time(edge['source']['name'])
        # #
        in_data = out_data
        out_data = generate_variable_name(edge['target']['name'])
        #
        init_func, forward_func = add_one_layer(init_func, forward_func, in_data, out_data, edge['target'])
        update_layer_used_time(edge['target']['name'])
        #

        edge_name = edge['target']['id']
        edge = find_next_edge(network, edge_name)

    forward_func = np.append(forward_func, generate_n_tap(2) + 'return ' + out_data)
    return np.concatenate((init_func, forward_func))


def main_func(edge_record):
    # add import information
    init()
    Main, Model, Ops = add_import_info()

    # Main
    glob = edge_record['static']
    Main = add_static_info(Main, glob)

    # Model
    Model = np.concatenate((Model, add_net_info(edge_record['network'])))
    # Ops

    return Main, Model, Ops
