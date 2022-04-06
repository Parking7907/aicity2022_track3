import sys
sys.path.append('./')
import argparse
import pdb
import argparse
import yaml 
from torch.utils.data import DataLoader
from trainer import ModelTrainer
from tester import ModelTester
from postprocess import Postprocess
from utils.setup import setup_solver
import os
import pickle
import numpy as np
from model_github import MYNET, MYNET_224

def train(args):
    with open(os.path.join(args.config,args.dataset + '.yml'), mode='r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
    if args.resolution == 224:
        model = MYNET_224(**config['MYNET'])
    elif args.resolution == 320:
        model = MYNET(**config['MYNET'])
    if args.dataset == 'AICity':
        from datasets.AICity import AICity
        train_dataset = AICity(config['datasets']['train'], 'train', config['MYNET']['sequence_size'], temporal_stride=config['datasets']['stride'])
        valid_dataset = AICity(config['datasets']['valid'], 'valid', config['MYNET']['sequence_size'])
        print("dataset_loaded")
    train_loader = DataLoader(train_dataset, **config['dataloader']['train'])
    valid_loader = DataLoader(valid_dataset, **config['dataloader']['valid'])

    optimizer, scheduler, criterion = setup_solver(model.parameters(), config)
    
    trainer = ModelTrainer(model, train_loader, valid_loader, criterion, optimizer, scheduler, config, config['criterion']['name'], dataset_name=config['datasets']['name'], **config['trainer'])
    trainer.train()


def test(args):
    with open(os.path.join(args.config,args.dataset + '.yml'), mode='r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)

    model = MYNET(**config['MYNET'])
    
    if args.dataset == 'AICity':
        from datasets.AICity import AICity
        test_dataset = AICity(config['datasets']['test'], config['MYNET']['sequence_size'])
    #pdb.set_trace()
    test_loader = DataLoader(test_dataset, **config['dataloader']['test'])
    tester = ModelTester(model, test_loader, **config['tester'])
    output, wrong_list = tester.test()
    output = np.array(output)
    wrong_list = np.array(wrong_list)
    #with open("output.pkl", "wb") as f:
        #pickle.dump(output, f)
    #with open("name.pkl", "wb")as fr:
        #pickle.dump(wrong_list, fr)
def demo(args): 
    with open(os.path.join(args.config,args.dataset + '.yml'), mode='r') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)

    model = MYNET_224(**config['MYNET'])
    
    if args.dataset == 'AICity':
        from datasets.AICity import AICity_Demo
        test_dataset = AICity_Demo(config['datasets']['test'], config['MYNET']['sequence_size'])
    #pdb.set_trace()
    print(len(test_dataset))
    test_loader = DataLoader(test_dataset, **config['dataloader']['test'])
    tester = Postprocess(model, test_loader, **config['tester'])
    est_dict, score_dict, name_list = tester.test()
    new_dict = {}
    new_dict_2 = {}
    final_output = {}
    for filename in est_dict:
        nn = filename.split('_')
        ss = int(nn[-1].split('.')[0])
        vv = ('_').join(nn[:-1])
        print(vv, ss)
        if vv not in new_dict:
            new_dict[vv] = {}
            new_dict[vv][ss] = est_dict[filename]
            new_dict_2[vv] = {}
            new_dict_2[vv][ss] = score_dict[filename]
        else:
            new_dict[vv][ss] = est_dict[filename]
            new_dict_2[vv][ss] = score_dict[filename]
    #pdb.set_trace()
    for filename in new_dict:
        print(filename)
        final_output[filename] = {'label':[], 'score':[]}
        print(len(new_dict[filename]))
        for k in range(len(new_dict[filename])):
            print(filename, k)
            final_output[filename]['label'].append(new_dict[filename][k])
            final_output[filename]['score'].append(new_dict_2[filename][k])
        print(len(final_output[filename]))
        with open('%s%s.pkl'%(args.save_dir,filename), 'wb') as f: 
            pickle.dump(final_output[filename], f)
    with open("%soutput.pkl"%args.save_dir, "wb") as f:
        pickle.dump(final_output, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', type=str, default='.', help='Root directory')
    parser.add_argument('-c', '--config', type=str, help='Path to option YAML file.')
    parser.add_argument('-d', '--dataset', type=str, help='Dataset')
    parser.add_argument('-m', '--mode', type=str, help='Train or Test')
    parser.add_argument('-r', '--resolution', type=int, help='Resolution, 224 or 320')
    parser.add_argument('-s', '--save_dir', type=str, default ='/home/data/aicity/output/', help='output path')
    args = parser.parse_args()

    if args.mode == 'Train':
        train(args)
    elif args.mode == 'Test':
        test(args)
    elif args.mode == 'Demo':
        demo(args)
