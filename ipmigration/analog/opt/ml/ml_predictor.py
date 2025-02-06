# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:11:12 2024

@author: shunqidai
modified setup_and_update_DNN_for_single_target:
    path_state_dict
    
24/09/2024
"""

import numpy as np
import os

import torch
import torch.nn.functional as F
import torch.utils.data as Data

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" #solve pytorch env error
torch.manual_seed(1)    # reproducible

def generate_target_bounds(targets, magnitude=2.0, mode='expensive'):
    if mode=='cheap':
        target_mins = [0.0]*len(targets['cheap'])
        target_maxs = list(np.array(targets['cheap'])*magnitude)
    elif mode=='expensive':
        target_mins = [0.0]*len(targets['expensive'])
        target_maxs = list(np.array(targets['expensive'])*magnitude)
    else:
        target_mins = [0.0]*len(targets['cheap']+targets['expensive'])
        target_maxs = list(np.array(targets['cheap']+targets['expensive'])*magnitude)
    target_bounds = list(zip(target_mins, target_maxs))
    return target_bounds
    
def normalize(data, bounds):
    # data: list
    #print("bounds:", bounds)
    for item in data:
        #print("item:", item)
        for i in range(len(item)):
            #print("len item:", len(item))
            maximum = bounds[i][1]
            minimum = bounds[i][0]
            middle = (maximum+minimum)/2.0
            dr = (maximum-minimum)*0.5
            if maximum > minimum:
                item[i] = (item[i]-middle)/dr
                if item[i]>1.0:
                    item[i]=1.0
                elif item[i]<-1.0:
                    item[i]=-1.0
            else:
                item[i] = 0.0
    return data

def denormalize(normalized_data, bounds):
    # normalized_data: list
    #print("bounds:", bounds)
    for num in range(len(normalized_data)):
        item = normalized_data[num]
        #print("item:", item)
        #print("item.shape[0]:", item.shape[0])
        if item.shape[0]>1:
            for i in range(item.shape[0]):
                maximum = bounds[i][1]
                minimum = bounds[i][0]
                middle = (maximum+minimum)*0.5
                dr = (maximum-minimum)*0.5
                item[i] = item[i]*dr+middle
        elif item.shape[0]==1:
            maximum = bounds[1]
            minimum = bounds[0]
            middle = (maximum+minimum)*0.5
            dr = (maximum-minimum)*0.5
            item = item*dr+middle
            #item = item*(maximum-minimum)+minimum
        normalized_data[num] = item
    return normalized_data


def generate_training_data(all_solutions, all_sim_results, bounds, targets, mode='all'):
    #mode: 'all', 'cheap', 'expensive'
    # generate normalized x_train data
    x = np.array(all_solutions).astype(np.float32)
    x_normalized = normalize(x, bounds)
    x_train = torch.from_numpy(x_normalized)
    # generate normalized y_train data
    target_bounds = generate_target_bounds(targets, mode=mode)
    y = np.array(all_sim_results).astype(np.float32)
    #print("y:", y)
    y_normalized = normalize(y, target_bounds)
    y_train=torch.from_numpy(y_normalized)
    return x_train, y_train, target_bounds

def setup_train_torch_dataset(x_train, y_train, BATCH_SIZE, shuffle_mode=True):
    # setup train_torch_dataset
    train_torch_dataset = Data.TensorDataset(x_train, y_train)
    train_loader = Data.DataLoader(
        dataset=train_torch_dataset,      # torch TensorDataset format
        batch_size=BATCH_SIZE,      # mini batch size
        shuffle=shuffle_mode,               # random shuffle for training
    )
    return train_loader


class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_hidden1, n_hidden2, n_output):
        super(Net, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden) # hidden layer1
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden1) # hidden layer2
        #self.hidden3 = torch.nn.Linear(n_hidden, n_hidden) # hidden layer2
        #self.hidden4 = torch.nn.Linear(n_hidden, n_hidden) # hidden layer2
        self.hidden5 = torch.nn.Linear(n_hidden1, n_hidden2) # hidden layer2
        self.predict = torch.nn.Linear(n_hidden2, n_output)   # output layer

    def forward(self, x):
        x = F.relu(self.hidden1(x))      # activation function for hidden layer
        x = F.relu(self.hidden2(x))     # activation function for hidden layer
        #x = F.relu(self.hidden3(x))     # activation function for hidden layer
        #x = F.relu(self.hidden4(x))     # activation function for hidden layer
        x = F.relu(self.hidden5(x))     # activation function for hidden layer
        x = self.predict(x)             # linear output
        return x

#初始化权重
def initialize_weights(model):
	for m in model.modules():
		# 判断是否属于Conv2d
		if isinstance(m, torch.nn.Conv2d):
			torch.nn.init.zeros_(m.weight.data)
			# 判断是否有偏置
			if m.bias is not None:
				torch.nn.init.constant_(m.bias.data,0.3)
		elif isinstance(m, torch.nn.Linear):
			torch.nn.init.normal_(m.weight.data, 0.01)
			if m.bias is not None:
				torch.nn.init.zeros_(m.bias.data)
		elif isinstance(m, torch.nn.BatchNorm2d):
			m.weight.data.fill_(1) 		 
			m.bias.data.zeros_()	
        

def setup_model(n_feature, n_output, n_hidden=None):
    if n_hidden is None:
        #n_hidden = round((n_feature+n_output)*2/3)   
        #n_hidden = n_feature+n_output
        n_hidden = 50
    else:
        n_hidden=n_hidden
    n_hidden1=50
    n_hidden2=30
    model = Net(n_feature=n_feature, n_hidden=n_hidden, n_hidden1=n_hidden1, n_hidden2=n_hidden2, n_output=n_output)     # define the network
    #print(model)  # net architecture
    #print(model.hidden1.weight.data)
    #print("-------初始化-------")
    #model.apply(initialize_weights)
    # 或者initialize_weights(model)
    #print(model.hidden1.weight.data)
    return model
    
def setup_optimizer(model, lr):
    # 网络调参使用Adam优化算法
    #optimizer = torch.optim.SGD(model.parameters(), lr=0.0002)
    #optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    optimizer=torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False)
    criterion = torch.nn.MSELoss()  # this is for regression mean squared loss
    return optimizer, criterion


# define a LossCounter class to record loss
class LossCounter:
    def __init__(self):
        self.count, self.sum, self.avg = 0, 0, 0
        return
    def update(self, value, num_updata=1):
        self.count += num_updata
        self.sum += value * num_updata
        self.avg = self.sum / self.count
        return
    def clear(self):
        self.count, self.sum, self.avg = 0, 0, 0
        return

def train_batch(EPOCH, train_loader, model, optimizer, criterion):
    # 用于存放loss
    # 在大循环外部先初始化这个类
    loss_recorder = LossCounter()
    optimizer = optimizer
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[10,20,30,40,], gamma=0.1)
    model.train()
    for epoch in range(EPOCH):   # train entire dataset 3 times
        for step, (batch_x, batch_y) in enumerate(train_loader):  # for each training step
            # train your data...
            output = model(batch_x)              # get output for every net
            loss = criterion(output, batch_y)    # compute loss for every net
            running_loss = loss.item()
            # 这里更新那个loss_recorder对象
            loss_recorder.update(running_loss)      # loss recorder 当这里的loss你要转化成 float 的
            optimizer.zero_grad()                # clear gradients for next train
            loss.backward()                      # backpropagation, compute gradients
            optimizer.step()                     # apply gradients
            
            #print('Epoch: ', epoch, '| Step: ', step, '| batch x: ',
            #      batch_x.numpy(), '| batch y: ', batch_y.numpy())
        scheduler.step()
        # 每个 epoch 打印一下这个loss
        #print('Epoch: ', epoch, "/ Loss:", loss_recorder.avg)
    print('Epoch: ', epoch, "/ Loss:", loss_recorder.avg)
    


def setup_and_update_DNN_for_single_target(all_target_solutions,\
                                 all_target_sim_results,\
                                 bounds, targets, target_index,\
                                 sim_mode='expensive',\
                                 BATCH_SIZE=1, EPOCH=10,\
                                 n_hidden=None, mode='setup',\
                                 path_state_dict=None):
    # bounds: list, targets: dict,
    BATCH_SIZE = BATCH_SIZE
    EPOCH = EPOCH
    sim_mode = sim_mode
    n_hidden=n_hidden
    [n_feature] = all_target_solutions[0].shape
    n_output = 1
    if not path_state_dict:
        path_state_dict = "./model_state_dict_{0}_target_{1}.pkl".format(sim_mode, target_index)
    else:
        path_state_dict=path_state_dict
    # data preprocess for all expensive targets
    x_train, y_train, target_bounds = generate_training_data(all_target_solutions,\
                                              all_target_sim_results,\
                                              bounds, targets,\
                                              mode=sim_mode)
    # choose expensive_target_index
    y_train=y_train[:, target_index]
    #print("y_tain:", y_train)
    train_loader=setup_train_torch_dataset(x_train, y_train,\
                                           BATCH_SIZE, shuffle_mode=True)
    # setup model 
    model = setup_model(n_feature, n_output, n_hidden)
    if mode=='update':
        #加载之前的model参数
        model.load_state_dict(torch.load(path_state_dict))
    else:
        pass
    # setup optimizer and criterion
    optimizer, criterion = setup_optimizer(model, lr=0.01)
    # train model
    train_batch(EPOCH, train_loader, model, optimizer, criterion)
    # 保存模型参数
    model_state_dict = model.state_dict()
    torch.save(model_state_dict, path_state_dict)
    # model cfg
    model_cfg=[path_state_dict, n_feature, n_output, n_hidden]
    target_bounds = target_bounds[target_index]
    return model_cfg, target_bounds

def run_DNN(model_cfg, target_bounds, bounds, x_test):
    #print("run_DNN")
    path_state_dict, n_feature, n_output, n_hidden = model_cfg
    model = setup_model(n_feature, n_output, n_hidden)
    x_test = np.array(x_test).astype(np.float32)
    x_test_normalized = normalize([x_test], bounds)
    #print("x_test_normalized:", x_test_normalized)
    x_test_normalized = torch.tensor(x_test_normalized)
    #加载的model参数
    model.load_state_dict(torch.load(path_state_dict))
    # 切换为评估模式
    model.eval()
    with torch.no_grad():
        # predict y_test
        y_test = model(x_test_normalized)
    y_test = y_test.detach()
    y_test = y_test
    #print("y_test:", y_test) # y_test: tensor([[0.9596]])
    denormalize_y_test = denormalize(y_test, target_bounds)
    # data format convert
    [[denormalize_y_test]]=list(denormalize_y_test.numpy())
    #print("denormalize_y_test:", denormalize_y_test)
    return denormalize_y_test

    
############################test function #########################
'''
# define range for input
l_min, l_max = 0.35, 1.4
w_min, w_max = 0.22, 50.0
c_min, c_max = 0.1, 3.0 #pF
r_min, r_max = 0.1, 100 #kohm   0.1kohm, 100kohm typical range of zero resistor
ib_min, ib_max = 5.0, 5.0 #uA

w_l_min = 1.0
w_l_max = 35.0

bounds = {'variables': [(c_min, c_max), (r_min, r_max), (ib_min, ib_max), \
                        (w_l_min, w_l_max), (w_l_min, w_l_max), (w_l_min, w_l_max), \
                        (w_l_min, w_l_max), (w_l_min, w_l_max)],
          'constants': [0.35, 1.4, 1.4, 1.4, 1.4], #length
              }

targets = {"cheap": [3163, 10, 60.0],\
           "expensive": [10, 10], }#60dB

bounds=bounds["variables"]
    
all_solutions = torch.tensor([[  2.4365,  56.1887,   5.0000,  10.9427,  32.7929,  20.0692,  28.3983,
          12.6157],
        [  2.2866,  89.8182,   5.0000,  31.2033,  13.1338,  19.1852,  29.5149,
          15.6831],
        [  0.1436,   5.6207,   5.0000,  17.9489,  25.2192,   1.2615,  21.2836,
          18.1558],
        [  0.2604,  65.4984,   5.0000,  34.8763,  11.9984,  20.2036,  11.8692,
          23.9651],
        [  1.0247,  38.1475,   5.0000,  33.2782,  14.4975,  16.1479,   7.2975,
          31.2254],
        [  1.4636,  71.3244,   5.0000,  27.7774,   9.0875,  14.0801,  14.9975,
          26.4273],
        [  1.8822,  23.2713,   5.0000,  21.6515,   5.7789,  24.1271,  32.2140,
          20.3712],
        [  0.5129,  42.8043,   5.0000,  11.2242,   5.3873,  19.5591,  31.0917,
          31.6104],
        [  1.7137,  45.6893,   5.0000,   9.2635,  16.2460,   4.6177,  28.1780,
           6.8706],
        [  1.9617,  95.2686,   5.0000,  16.3832,  16.5846,   5.0141,  22.5374,
          27.5646],
        [  2.8735,  79.3228,   5.0000,  14.4281,  25.8912,  11.0940,  15.6747,
           1.0368],
        [  2.2145,  80.8978,   5.0000,  14.9021,  32.0845,   6.5544,  31.3434,
          30.3525],
        [  0.9227,  16.4360,   5.0000,  10.2268,  29.0942,  34.3129,  15.2314,
          29.4340],
        [  2.5841,  67.6108,   5.0000,  14.4069,   9.8924,  16.3742,  23.5210,
          32.4158],
        [  2.8987,  11.4319,   5.0000,  26.7954,  29.5855,  33.9312,  25.4778,
          19.6572],
        [  2.0093,  54.2443,   5.0000,  17.8326,  27.4235,  30.3930,   4.4367,
          14.6468],
        [  2.2793,  24.5544,   5.0000,  27.9602,  14.8903,   8.5652,   8.4273,
          16.0912],
        [  2.7959,  80.3405,   5.0000,  13.9681,  16.8305,   1.1689,  11.2975,
          17.9065],
        [  2.8060,  87.7352,   5.0000,  21.7255,  25.3047,   2.5678,  13.7383,
          19.3280],
        [  1.2333,  96.5960,   5.0000,  15.1232,  16.3160,   2.6448,  15.5209,
           4.2222],
        [  2.1511,  28.7481,   5.0000,  31.8388,   5.7446,  30.2551,  25.1161,
          14.0228],
        [  1.5326,  32.1145,   5.0000,  33.9631,   4.4624,  10.9757,  15.1208,
           5.5785],
        [  0.7531,  36.0676,   5.0000,   8.8773,  31.2541,  13.0356,  14.3511,
          29.9126],
        [  2.3761,   2.7196,   5.0000,  11.4562,  11.4869,  13.7009,   6.4120,
          10.0243],
        [  1.7345,  73.3119,   5.0000,  25.5345,   7.8777,   5.7494,  19.8447,
          23.2492],
        [  1.8712,  99.0723,   5.0000,  15.6138,   5.1850,  24.7065,  27.3376,
           7.1759],
        [  1.0189,  69.3587,   5.0000,  31.1435,  25.1718,   5.8867,  27.2357,
          32.9993],
        [  1.4370,  44.7907,   5.0000,  25.7163,  30.5744,  15.3143,   1.3140,
           2.4829],
        [  1.2019,  15.8378,   5.0000,  15.7253,  16.9211,  26.7824,  13.4349,
          23.5799],
        [  2.5987,  51.1289,   5.0000,  24.4330,  12.2527,   2.2350,  33.7094,
          33.6082],
        [  2.4809,  25.3324,   5.0000,  32.8917,  33.2668,  32.1613,  12.8064,
          11.5788],
        [  2.2679,  68.9757,   5.0000,  14.1049,  22.0681,   9.8903,   5.8363,
          11.4971],
        [  2.9305,   0.4950,   5.0000,  12.9564,  14.0201,   9.2096,  13.5253,
          17.6540],
        [  0.8470,  97.9714,   5.0000,  34.2256,  31.2866,  15.5859,  33.6333,
          11.7102],
        [  2.6043,   5.9749,   5.0000,  22.2574,  22.5097,  28.8281,   9.9052,
           8.2130],
        [  1.3810,  82.1405,   5.0000,  23.0261,   5.4453,  26.9166,  19.0055,
          16.1811],
        [  0.8571,   1.9373,   5.0000,  27.8199,  22.2770,   5.1655,  15.2834,
          17.9484],
        [  2.0062,  29.3532,   5.0000,  34.4392,  20.8155,   1.3190,   6.4130,
           9.4672],
        [  1.5866,  46.6991,   5.0000,  14.8495,   5.3789,  31.4838,  20.0692,
          24.7331],
        [  2.2239,  73.9259,   5.0000,  22.3483,  27.1340,  26.5902,   2.8454,
          34.2977],
        [  2.7594, 100.0000,   5.0000,  22.2591,  17.7451,  24.9295,  13.9676,
          21.1745],
        [  2.2525, 100.0000,   5.0000,  18.3485,  13.9705,   9.4247,  35.0000,
          35.0000],
        [  1.8975,  73.3119,   5.0000,  25.5345,   7.8777,   5.7494,  19.8447,
          23.2492],
        [  2.7959,  80.3405,   5.0000,  13.9681,  16.8305,  22.2084,  11.2975,
          17.9065],
        [  2.5193, 100.0000,   5.0000,  16.9685,  11.2686,  35.0000,  10.6919,
          35.0000],
        [  2.5353,  73.2865,   5.0000,  12.0416,   8.2555,  11.9666,  28.1807,
           9.1059],
        [  1.9617,  95.2686,   5.0000,  16.3832,  16.5846,   5.0141,  22.5374,
          27.5646],
        [  2.2442,  52.1702,   5.0000,  34.2937,   2.6582,   1.0000,  21.2375,
          26.0802],
        [  3.0000, 100.0000,   5.0000,  27.5355,  16.7608,  27.3690,  12.7861,
          35.0000],
        [  1.7195,  97.9003,   5.0000,  11.8580,  14.8407,  13.1137,  35.0000,
           6.5441],
        [  1.2333,  96.5960,   5.0000,  15.1232,   1.4906,   2.6448,  15.5209,
           4.2222],
        [  3.0000, 100.0000,   5.0000,  21.5462,  23.1246,  34.4082,  34.9834,
          10.6375],
        [  1.5281,  68.2377,   5.0000,  35.0000,   1.0000,   1.0000,  34.1642,
          25.8946],
        [  1.8907, 100.0000,   5.0000,  34.3766,  21.9249,  25.1487,  27.8852,
          35.0000],
        [  1.2555,  71.6630,   5.0000,  16.5422,   1.0000,   1.0000,  35.0000,
          30.2832],
        [  3.0000, 100.0000,   5.0000,  18.7947,  19.6676,  19.8800,   9.2860,
          11.6584],
        [  1.2333,  96.5960,   5.0000,  15.1232,  16.3160,   2.6448,  15.5209,
           3.9648],
        [  3.0000, 100.0000,   5.0000,   1.0000,  11.8888,   1.4204,  24.9892,
           6.8371],
        [  0.9694,  99.3285,   5.0000,  14.2809,   1.0000,   1.1198,  25.3687,
           6.1774],
        [  3.0000,  91.6053,   5.0000,  14.6769,  35.0000,   6.9626,  29.1888,
          15.1567],
        [  3.0000,  59.0590,   5.0000,  32.5980,   9.1524,   9.5074,  10.7443,
          11.5903],
        [  2.5841,  67.6108,   5.0000,  14.4069,   9.8924,  16.3742,  23.5210,
          10.5055],
        [  2.2990, 100.0000,   5.0000,  35.0000,  27.1600,  28.6304,  18.2711,
          19.7358],
        [  1.6513, 100.0000,   5.0000,  10.3803,  15.0594,  12.0455,  19.0988,
          32.8206],
        [  3.0000, 100.0000,   5.0000,  24.4967,  15.0538,   1.0000,  21.6365,
           5.2148],
        [  1.0080,  86.3640,   5.0000,  20.2244,   7.2549,   1.0000,   8.5846,
           3.5819],
        [  3.0000, 100.0000,   5.0000,  13.1543,   2.9847,  19.3763,  24.5240,
          35.0000],
        [  0.7967, 100.0000,   5.0000,  16.6924,   1.5691,   1.0000,  18.1302,
          35.0000],
        [  2.2532,  88.6895,   5.0000,   6.9900,  23.4251,  35.0000,  16.5117,
          27.7065],
        [  2.3622,  69.8712,   5.0000,  18.9914,  11.9326,   8.1203,  23.9936,
          35.0000],
        [  1.5859, 100.0000,   5.0000,   1.0000,   1.0000,   1.0000,  25.6926,
          26.5306],
        [  3.0000, 100.0000,   5.0000,  13.6494,  25.4783,  31.2850,  35.0000,
          10.8034],
        [  1.3513, 100.0000,   5.0000,  17.8946,   1.0000,   1.0000,  11.6191,
          20.0623],
        [  3.0000,  74.0095,   5.0000,   3.7275,  23.3353,  13.9853,  24.0628,
          12.1034],
        [  2.2679,  68.9757,   5.0000,  14.1049,  22.0681,   9.8903,  29.4187,
          11.4971],
        [  2.4633,  91.3862,   5.0000,   1.0000,  17.9156,   1.0000,  35.0000,
           3.9419],
        [  1.7920,  89.4113,   5.0000,  10.7089,  17.0733,  33.9373,  15.1821,
          25.6724],
        [  3.0000,  48.9082,   5.0000,   4.6615,  11.2477,  35.0000,  26.3148,
          31.4125],
        [  2.8785,  44.0543,   5.0000,  14.5836,  13.3058,  12.7561,  35.0000,
          35.0000]])
all_sim_results = torch.tensor([[ 7.3400e+01,  2.2000e+00,  1.0190e+02,  5.5000e+00,  5.5000e+00],
        [ 9.3600e+01,  8.7000e+00,  5.8000e+01,  9.4000e+00,  9.4000e+00],
        [ 3.0000e+00,  1.1000e+00,  1.0490e+02,  1.2600e+01,  1.2600e+01],
        [ 1.9700e+01,  5.4000e+00,  6.7400e+01,  1.0100e+01,  1.0100e+01],
        [ 5.1000e+00,  6.0000e-01,  9.5000e+01,  4.1000e+00,  4.1000e+00],
        [ 2.1400e+01,  1.9000e+00,  1.2040e+02,  9.5000e+00,  9.5000e+00],
        [ 1.3200e+01,  7.0000e-01,  8.5500e+01,  2.9000e+00,  2.9000e+00],
        [ 3.7600e+01,  4.2000e+00,  7.7300e+01,  8.6000e+00,  8.6000e+00],
        [ 5.9600e+01,  2.6000e+00,  1.0710e+02,  6.3000e+00,  6.3000e+00],
        [ 7.1000e+00,  4.0000e-01,  1.1550e+02,  1.2900e+01,  1.2900e+01],
        [ 1.6300e+01,  6.0000e-01,  4.2900e+01,  5.0000e+00,  5.0000e+00],
        [ 6.3000e+00,  3.0000e-01,  1.0990e+02,  1.0600e+01,  1.0600e+01],
        [ 1.4000e+01,  1.4000e+00,  6.8600e+01,  3.5000e+00,  3.5000e+00],
        [ 3.8900e+01,  4.3000e+00,  1.3130e+02,  9.5000e+00,  9.5000e+00],
        [ 9.2200e+01,  1.7000e+00,  4.1300e+01,  1.3000e+00,  1.3000e+00],
        [ 6.8000e+00,  4.0000e-01,  6.7800e+01,  2.4000e+00,  2.4000e+00],
        [ 7.3000e+00,  4.0000e-01,  8.9000e+01,  2.0000e+00,  2.0000e+00],
        [ 2.1000e+00,  1.0000e-01,  1.2190e+02,  1.3300e+01,  1.3300e+01],
        [ 2.8000e+00,  1.0000e-01,  1.1560e+02,  1.1700e+01,  1.1700e+01],
        [ 2.5000e+01,  3.1000e+00,  1.1680e+02,  1.0500e+01,  1.0500e+01],
        [ 8.3000e+00,  4.0000e-01,  8.3600e+01,  2.6000e+00,  2.6000e+00],
        [ 1.2400e+01,  9.0000e-01,  7.3400e+01,  3.0000e+00,  3.0000e+00],
        [ 4.8000e+00,  6.0000e-01,  9.6000e+01,  5.5000e+00,  5.5000e+00],
        [ 1.8900e+01,  9.0000e-01,  5.0900e+01,  4.0000e-01,  4.0000e-01],
        [ 1.6100e+01,  1.2000e+00,  1.2310e+02,  1.1600e+01,  1.1600e+01],
        [ 3.9000e+00,  2.0000e-01,  1.0200e+02,  9.5000e+00,  9.5000e+00],
        [ 5.6000e+00,  6.0000e-01,  1.0580e+02,  1.0700e+01,  1.0700e+01],
        [ 6.3000e+00,  2.8000e+00, -6.0800e+01,  3.0000e-01,  3.0000e-01],
        [ 2.3300e+01,  1.8000e+00,  6.5000e+01,  2.9000e+00,  2.9000e+00],
        [ 6.4000e+00,  3.0000e-01,  1.0790e+02,  1.1300e+01,  1.1300e+01],
        [ 3.5400e+01,  1.3000e+00,  3.3600e+01,  1.6000e+00,  1.6000e+00],
        [ 5.6000e+00,  3.0000e-01,  9.3400e+01,  5.0000e+00,  5.0000e+00],
        [ 1.2700e+01,  5.0000e-01,  7.8800e+01,  6.0000e-01,  6.0000e-01],
        [ 8.7100e+01,  7.4000e+00,  5.1300e+01,  9.0000e+00,  9.0000e+00],
        [ 1.0740e+02,  2.8000e+00, -3.0200e+01,  4.0000e-01,  4.0000e-01],
        [ 1.5900e+01,  1.2000e+00,  1.0060e+02,  9.4000e+00,  9.4000e+00],
        [ 5.9000e+00,  8.0000e-01,  8.8700e+01,  4.1000e+00,  4.1000e+00],
        [ 2.0000e+00,  1.0000e-01,  1.1500e+02,  3.2000e+00,  3.2000e+00],
        [ 2.1800e+01,  1.2000e+00,  9.0500e+01,  6.1000e+00,  6.1000e+00],
        [ 1.6000e+00,  1.0000e-01,  1.2150e+02,  3.5000e+00,  3.5000e+00],
        [ 2.5200e+01,  2.3000e+00,  1.3240e+02,  9.4000e+00,  9.4000e+00],
        [ 1.8300e+01,  1.9000e+00,  1.3860e+02,  1.2500e+01,  1.2500e+01],
        [ 1.6100e+01,  1.1000e+00,  1.2390e+02,  1.1500e+01,  1.1500e+01],
        [ 2.1100e+01,  8.0000e-01,  1.1460e+02,  7.4000e+00,  7.4000e+00],
        [ 2.1700e+01,  1.6000e+00,  1.3580e+02,  1.0000e+01,  1.0000e+01],
        [ 2.4200e+01,  1.0000e+00,  1.1510e+02,  8.4000e+00,  8.4000e+00],
        [ 7.1000e+00,  4.0000e-01,  1.1550e+02,  1.2900e+01,  1.2900e+01],
        [ 8.5000e+00,  5.0000e-01,  1.1120e+02,  1.4100e+01,  1.4100e+01],
        [ 1.2500e+01,  5.0000e-01,  1.2320e+02,  1.0100e+01,  1.0100e+01],
        [ 2.2900e+01,  1.5000e+00,  1.1130e+02,  9.0000e+00,  9.0000e+00],
        [ 1.1000e+01,  1.0000e+00,  1.1100e+02,  1.2600e+01,  1.2600e+01],
        [ 2.1900e+01,  9.0000e-01,  1.1480e+02,  8.0000e+00,  8.0000e+00],
        [ 3.8200e+01,  1.0100e+01,  1.2020e+02,  1.6200e+01,  1.6200e+01],
        [ 2.5500e+01,  4.6000e+00,  1.1300e+02,  1.0500e+01,  1.0500e+01],
        [ 2.9000e+01,  4.5000e+00,  1.3380e+02,  1.7200e+01,  1.7200e+01],
        [ 2.1400e+01,  8.0000e-01,  1.1760e+02,  7.8000e+00,  7.8000e+00],
        [ 2.6700e+01,  3.5000e+00,  1.1440e+02,  1.0400e+01,  1.0400e+01],
        [ 2.2900e+01,  5.0000e-01,  1.2420e+02,  1.1500e+01,  1.1500e+01],
        [ 1.6100e+01,  2.0000e+00,  1.2090e+02,  1.5600e+01,  1.5600e+01],
        [ 1.2100e+01,  5.0000e-01,  1.1860e+02,  9.7000e+00,  9.7000e+00],
        [ 2.7600e+01,  1.0000e+00,  1.1550e+02,  6.2000e+00,  6.2000e+00],
        [ 3.5900e+01,  1.4000e+00,  1.1360e+02,  7.5000e+00,  7.5000e+00],
        [ 2.9400e+01,  3.0000e+00,  1.1650e+02,  8.8000e+00,  8.8000e+00],
        [ 1.0900e+01,  8.0000e-01,  1.1990e+02,  1.2000e+01,  1.2000e+01],
        [ 1.4700e+01,  8.0000e-01,  1.3530e+02,  1.3100e+01,  1.3100e+01],
        [ 1.4300e+01,  1.7000e+00,  1.1380e+02,  1.1200e+01,  1.1200e+01],
        [ 2.2300e+01,  2.5000e+00,  1.3770e+02,  1.3000e+01,  1.3000e+01],
        [ 7.0000e+00,  1.0000e+00,  1.1710e+02,  2.0700e+01,  2.0700e+01],
        [ 2.3600e+01,  1.1000e+00,  1.1900e+02,  8.4000e+00,  8.4000e+00],
        [ 1.1500e+01,  6.0000e-01,  1.1580e+02,  1.1000e+01,  1.1000e+01],
        [ 2.4700e+01,  9.0000e-01,  1.2800e+02,  1.7400e+01,  1.7400e+01],
        [ 3.2100e+01,  1.8000e+00,  1.1630e+02,  8.0000e+00,  8.0000e+00],
        [ 1.0400e+01,  1.1000e+00,  1.2950e+02,  1.9500e+01,  1.9500e+01],
        [ 5.1300e+01,  2.0000e+00,  1.2660e+02,  7.3000e+00,  7.3000e+00],
        [ 4.8400e+01,  4.0000e+00,  1.1500e+02,  7.9000e+00,  7.9000e+00],
        [ 3.4200e+01,  8.0000e-01,  1.2630e+02,  9.9000e+00,  9.9000e+00],
        [ 3.8300e+01,  3.7000e+00,  1.1250e+02,  8.9000e+00,  8.9000e+00],
        [ 1.3720e+02,  2.9000e+00,  1.1520e+02,  5.9000e+00,  5.9000e+00],
        [ 2.8700e+01,  1.0000e+00,  1.1570e+02,  7.3000e+00,  7.3000e+00]])


if __name__ == "__main__":
    print ('This is main function!')
    all_expensive_solutions = all_solutions
    all_expensive_sim_results = all_sim_results[:, :3]
    #print("all_expensive_sim_results:", all_expensive_sim_results)
    expensive_target_index=0
    model_cfg, target_bounds = setup_and_update_DNN_for_single_target(all_expensive_solutions,\
                                     all_expensive_sim_results,\
                                     bounds, targets, expensive_target_index,\
                                     sim_mode='cheap',\
                                     BATCH_SIZE=1, EPOCH=100,\
                                     n_hidden=None)
    #print("model_cfg:", model_cfg)
    #print("target_bounds:", target_bounds)
    x_test = np.array([ 2.4,  56,   5.0000,  11,  33,  21.2,  25.4, 13.1])
    print("x_test:", x_test)
    y_test=run_DNN(model_cfg, target_bounds, bounds, x_test)
    print("y_test:", y_test)
'''



    