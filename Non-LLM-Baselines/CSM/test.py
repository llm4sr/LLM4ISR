import torch
import argparse
import time
import importlib
import os
import numpy as np

from sess.utils.utils import get_logger, ACC_KPI
from sess.utils.model_selection import handle_adj, build_graph
from sess.utils.metrics import accuracy_calculator

from sess.model.gcegnn import CombineGraph
from sess.model.hide import HIDE
from sess.model.attenMixer import AreaAttnModel
from sess.model.mostpop import MostPop
from sess.model.sknn import SessionKNN

from config import Model_setting, Dataset_setting, Best_setting

def init_seed(seed=None):
    if seed is None:
        seed = int(time.time() * 1000 // 1000)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default='ml-1m', help='bundle/games/ml-1m')
parser.add_argument('--model', default='MostPop', help='MCPRN/STAMP/NARM/GCE-GNN/FPMC/HIDE/MostPop/SKNN')
parser.add_argument('--seed', type=int, default=0, help='0, 10, 42, 625, 2023')
parser.add_argument('--train_num', type=int, default=50, help='50, 150')
parser.add_argument('--gpu', type=str, default='0')
opt = parser.parse_args()
init_seed(opt.seed)

def test():
    base_path = '../../Dataset/'
    train_data = np.load(f'{base_path}{opt.dataset}/ID/train_sample_{opt.train_num}.npy', allow_pickle=True).tolist()
    test_data = np.load(f'{base_path}{opt.dataset}/ID/test.npy', allow_pickle=True).tolist()
    candidate_data = np.load(f'{base_path}{opt.dataset}/ID/test_candidate_{opt.seed}.npy', allow_pickle=True).tolist()

    model_config = Model_setting[opt.model]
    data_config = Dataset_setting[opt.dataset]
    best_settings = Best_setting[opt.model][opt.dataset]
    model_config = {**model_config, **best_settings}
    model_config['gpu'] = opt.gpu
    logger = get_logger(f'test_{model_config["description"]}_{opt.dataset}')
    if opt.model not in ['MostPop', 'SKNN']:
        dataloader = getattr(importlib.import_module('sess.utils.dataset'), model_config['dataloader'], None)
        train_dataset = dataloader(train_data, model_config)
        test_dataset = dataloader(test_data, model_config, candidate_set=candidate_data, isTrain=False)
    else:
        train_dataset = train_data
        test_dataset = test_data

    if opt.model == 'MostPop':
        model = MostPop(pop_n=model_config['pop_n'], logger=None)
    elif opt.model == 'SKNN':
        model = SessionKNN(train_data, test_data, {'n': model_config['neibor']}, None)
    elif opt.model in ['NARM','FPMC','STAMP','MCPRN']:
        train_dataset = train_dataset.get_loader(model_config, shuffle=True)
        test_dataset = test_dataset.get_loader(model_config, shuffle=False)
        model = getattr(importlib.import_module('sess.model.{}'.format(model_config['model_dir'])), opt.model, None)
        model = model(data_config['num_node'], model_config, logger)
    elif opt.model in ['GCE-GNN']:
        adj, num = build_graph(train_data, data_config, model_config)
        num_node = data_config['num_node'] + 1
        adj, num = handle_adj(adj, num_node, model_config['n_sample_all'], num)
        model = CombineGraph(model_config, num_node, adj, num, logger)
    elif opt.model in ['HIDE']:
        num_node = data_config['num_node'] + 1
        model = HIDE(model_config, num_node, logger=logger)
    elif opt.model in ['AttenMixer']:
        train_dataset = train_dataset.get_loader(model_config, shuffle=True)
        test_dataset = test_dataset.get_loader(model_config, shuffle=False)
        num_node = data_config['num_node'] + 1
        model = AreaAttnModel(model_config, num_node, logger)

    model.fit(train_dataset)

    res_dir = f'res/train_{opt.train_num}/{opt.dataset}/'
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    f = open(res_dir + f'result_{opt.dataset}_{opt.model}_{opt.seed}.txt', 'a')
    for k in [1,5,10]:
        line = f'HR@{k}\tNDCG@{k}\tMAP@{k}\n'
        f.write(line)
        if opt.model == 'SKNN':
            preds, truth = model.predict(test_data, k=k, candidate=candidate_data)
            preds = torch.tensor(preds)
            truth = torch.tensor(truth)
        else:
            preds, truth = model.predict(test_dataset, k=k)   
        metrics = accuracy_calculator(preds, truth, ACC_KPI)
        res_line = f'{metrics[2]:.4f}\t{metrics[0]:.4f}\t{metrics[1]:.4f}\n'
        f.write(res_line)
        f.flush()
    f.close()

if __name__ == '__main__':
    test()
