import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='LLM4ISR')
    parser.add_argument('--model', 
                        type=str,
                        default='gpt-3.5-turbo',
                        help='which model as recommender, options: gpt-3.5-turbo')
    parser.add_argument('--seed', 
                        type=int,
                        default=42,
                        help='options: 42, 625, 2023, 0, 10')
    parser.add_argument('--candidate_size', 
                        type=int,
                        default=20,
                        help='options: 10, 20')
    parser.add_argument('--dataset', 
                        type=str,
                        default='bundle',
                        help='use which datset: bundle/games/ml-1m')
    parser.add_argument('--train_num', 
                        type=int,
                        default=50,
                        help='options: 50,150')
    parser.add_argument('--N_t', 
                        type=int,
                        default=32,
                        help='options: 16,32')

    args = parser.parse_args()
    
    return args