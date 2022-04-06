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
    est_dict, name_list = tester.test()
    for filename in est_dict:
        
    output = np.array(est_dict)
    names = np.array(name_list)
    with open("output.pkl", "wb") as f:
        pickle.dump(output, f)
    with open("name.pkl", "wb")as fr:
        pickle.dump(name_list, fr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base_dir', type=str, default='.', help='Root directory')
    parser.add_argument('-c', '--config', type=str, help='Path to option YAML file.')
    parser.add_argument('-d', '--dataset', type=str, help='Dataset')
    parser.add_argument('-m', '--mode', type=str, help='Train or Test')
    parser.add_argument('-r', '--resolution', type=int, help='Resolution, 224 or 320')
    args = parser.parse_args()

    if args.mode == 'Train':
        train(args)
    elif args.mode == 'Test':
        test(args)
    elif args.mode == 'Demo':
        demo(args)
