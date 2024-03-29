# LLM4ISR
LLM4ISR is a  simple yet effective
paradigm for intent-aware session recommendaton motivated by the advanced reasoning capability
of large language models (LLMs). Specifically, we first create an
initial prompt to instruct LLMs to predict the next items
by inferring varying user intents reflected in a session. Then, we propose
an effective optimization mechanism to automatically optimize prompts with an iterative self-reflection. Finally, we leverage the robust generalizability of LLMs across diverse domains to selects the optimal prompt. 

## Installtion
Install all dependencies via:
```
pip install -r requirements.txt
```

## Datasets
We adopt three real-world datasets from various domains: [MovieLens-1M](https://grouplens.org/datasets/movielens/1m/), [Games](https://cseweb.ucsd.edu/~jmcauley/datasets/amazon/links.html) and [Bundle](https://github.com/BundleRec/bundle_recommendation). You can find the datasets used in the experiment under the `Dataset` directory. Each dataset includes both its ID and text format. In addition to providing the randomly-sampled training data, we also provide full versions of the training data under the `Dataset` directory.
### ID-Formatted Dataset
* `train_sample_x.npy`: randomly select x sessions from the full version of the training dataset as the training set. x can be 50 or 150.
* `train.npy`: full version of the training data.
* `valid.npy`: the validation set containing all validation sessions.
* `valid_candidate.npy`: the candidate set corresponding to each session in the validation set.
* `test.npy`: test set containing all test sessions.
* `test_candidate_x.npy`: the candidate sets constructed by 5 different random seeds, corresponding to each session in the test set. x can be 0, 10, 42, 625 or 2023.
### Text-Formatted Dataset
* `train_x.json`: the training set in text format corresponding to the `train_sample_x.npy` file in ID format.
* `valid.json`: the validation set in text format containing both validation sessions and the candidates, which corresponds to the `valid.npy` and `valid_candidate.npy` file in ID format.
* `test_seed_x.json`: the test set in text format containing both test sessions and the candidates, which corresponds to the `test.npy` and `test_candidate_x.npy` file in ID format.


## LLM4ISR
### Tune
The `tune.py` corresponds to the process of prompt optimization. Before running the code, you need to fill in your OpenAI API token in the `./LLM4ISR/assets/openai.yaml` file and wandb token in the `./LLM4ISR/assets/overall.yaml` file. 
```
python tune.py --dataset='dataset name' --train_num='number of training data'
```
For example, optimize the prompt on bundle dataset of 50 data.
```
python tune.py --dataset='bundle' --train_num=50
```
### Test
The `test.py` file corresponds to the evaluation of the prompt.
```
python test.py --dataset='dataset name' --seed='value of the seed'
```
Note that all the optimal prompts are saved in the `LLM4ISR/prompts.py` file. If you want to test the results with these prompts, you can replace them in the `test.py`.

## LLM-Baseline-NIR
NIR Baseline is implemented in `./LLM-Baseline-NIR/`
```
python test.py --dataset='dataset name' --seed='value of the seed' --api_key='your OpenAI API token'
```

## Non-LLM-Baselines
### Parameter Tuning and Settings for Non-LLM-Baselines
We use the open-source framework [Optuna](https://optuna.org/) to automatically find out the optimal hyperparameters of all methods with 50 trails. The item embedding size is searched from {32, 64, 128}; learning rate is searched from {10−4, 10−3, 10−2}; batch size is searched from {64, 128, 256} and we use an early stop mechanism to halt the model training, with a maximum of 100 epochs. For SKNN, 𝐾 is searched from {50, 100, 150}. For NARM, the hidden size is searched in [50, 200] stepped by 50, and the number of layers is searched in {1, 2, 3}. For GCE-GNN, the number of hops is searched in {1, 2}; the dropout rate for global aggregators is searched in [0, 0.8] stepped by 0.2 and the dropout rate for local aggregators is searched in {0, 0.5}. For MCPRN, 𝜏 is searched in {0.01, 0.1, 1, 10} and the number of purpose channels is searched in {1, 2, 3, 4}. For HIDE, the number of factors is searched in {1, 3, 5, 7, 9}; the regularization and balance weights are searched in {10−5, 10−4, 10−3, 10−2}; the window size is searched in [1, 10] stepped by 1; and the sparsity coefficient is set as 0.4. For Atten-Mixer, the intent level 𝐿 is searched in [1, 10] stepped by 1 and the number of attention heads is searched in {1, 2, 4, 8}. The optimal parameter settings are shown in Table 1.

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Table 1: Optimal Parameter Settings for Non-LLM-Baselines.

|  | Bundle | ML-1M | Games |
| :------: | :------: | :------: | :------: |
| SKNN | ![equation](https://latex.codecogs.com/svg.image?K=50)| ![equation](https://latex.codecogs.com/svg.image?K=50) | ![equation](https://latex.codecogs.com/svg.image?K=50) |
| FPMC | ![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=128)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=64) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=128) |![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)|
|NARM|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32)<br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001)<br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br> ![equation](https://latex.codecogs.com/svg.image?hidden\\_size=100)<br> ![equation](https://latex.codecogs.com/svg.image?layers=2)| ![equation](https://latex.codecogs.com/svg.image?embedding\\_size=64)<br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.0001)<br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)<br> ![equation](https://latex.codecogs.com/svg.image?hidden\\_size=50)<br> ![equation](https://latex.codecogs.com/svg.image?layers=2)| ![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128)<br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01)<br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=128)<br> ![equation](https://latex.codecogs.com/svg.image?hidden\\_size=100)<br> ![equation](https://latex.codecogs.com/svg.image?layers=3)|
|STAMP|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.0001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)|
|GCE-GNN|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)<br> ![equation](https://latex.codecogs.com/svg.image?num\\_hop=2)<br>![equation](https://latex.codecogs.com/svg.image?dropout\\_gcn=0)<br>![equation](https://latex.codecogs.com/svg.image?dropout\\_local=0.5)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br> ![equation](https://latex.codecogs.com/svg.image?num\\_hop=1)<br>![equation](https://latex.codecogs.com/svg.image?dropout\\_gcn=0)<br>![equation](https://latex.codecogs.com/svg.image?dropout\\_local=0.5)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)<br> ![equation](https://latex.codecogs.com/svg.image?num\\_hop=2)<br>![equation](https://latex.codecogs.com/svg.image?dropout\\_gcn=0)<br>![equation](https://latex.codecogs.com/svg.image?dropout\\_local=0)|
|MCPRN|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=128)<br>![equation](https://latex.codecogs.com/svg.image?\tau=0.01)<br>![equation](https://latex.codecogs.com/svg.image?purposes=2)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)<br>![equation](https://latex.codecogs.com/svg.image?\tau=0.1)<br>![equation](https://latex.codecogs.com/svg.image?purposes=4)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.01) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br>![equation](https://latex.codecogs.com/svg.image?\tau=1)<br>![equation](https://latex.codecogs.com/svg.image?purposes=1)|
|HIDE|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=64) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.0001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br>![equation](https://latex.codecogs.com/svg.image?n\\_factor=1)<br>![equation](https://latex.codecogs.com/svg.image?regularization=1e-3)<br>![equation](https://latex.codecogs.com/svg.image?balance\\_weights=0.01)<br>![equation](https://latex.codecogs.com/svg.image?window\\_size=6)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br>![equation](https://latex.codecogs.com/svg.image?n\\_factor=1)<br>![equation](https://latex.codecogs.com/svg.image?regularization=1e-2)<br>![equation](https://latex.codecogs.com/svg.image?balance\\_weights=0.001)<br>![equation](https://latex.codecogs.com/svg.image?window\\_size=5)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br>![equation](https://latex.codecogs.com/svg.image?n\\_factor=1)<br>![equation](https://latex.codecogs.com/svg.image?regularization=1e-5)<br>![equation](https://latex.codecogs.com/svg.image?balance\\_weights=1e-5)<br>![equation](https://latex.codecogs.com/svg.image?window\\_size=3)|
|Atten-Mixer|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.0001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)<br> ![equation](https://latex.codecogs.com/svg.image?level\\_L=7) <br> ![equation](https://latex.codecogs.com/svg.image?number\\_of\\_attention\\_heads=1)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=32) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64)<br> ![equation](https://latex.codecogs.com/svg.image?level\\_L=10) <br> ![equation](https://latex.codecogs.com/svg.image?number\\_of\\_attention\\_heads=2)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=256)<br> ![equation](https://latex.codecogs.com/svg.image?level\\_L=3) <br> ![equation](https://latex.codecogs.com/svg.image?number\\_of\\_attention\\_heads=4)|
| UniSRec | ![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=128)|![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.0001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=64) |![equation](https://latex.codecogs.com/svg.image?embedding\\_size=128) <br> ![equation](https://latex.codecogs.com/svg.image?learning\\_rate=0.001) <br> ![equation](https://latex.codecogs.com/svg.image?batch\\_size=128)|

### Conventional, Single-Intent, and Multi-Intent Baselines
The Conventional, Single-Intent, and Multi-Intent Baselines are implemented in `./Non-LLM-Baselines/CSM/`.
#### Tune
You can run the following command to tune the model and find the optimal parameter combination.
```
python tune.py --dataset='dataset name' --train_num='number of training data' --model='model name'
```
#### Test
After completing the tuning process, we can find the optimal parameter settings in the `tune_log` directory. Additionally, we have placed the optimal parameters obtained during the experiment in the `config.py`. You can also use the following command to directly test the model.
```
python test.py --dataset='dataset name' --model='model name' --seed='value of the seed'
```

### Cross-Domain Baseline
We have selected [UniSRec](https://github.com/RUCAIBox/UniSRec) as our baseline for cross-domain recommendation. For setting up UniSRec, please refer to the [UniSRec](https://github.com/RUCAIBox/UniSRec) repo for detailed instructions on installing the necessary dependencies.

Additionally, please download the processed pre-trained, downstream datasets and the pre-trained model from [Google Drive](https://drive.google.com/drive/folders/1mNreuS5l0oa8tDmCtQfQKDv8u7cut4xV?usp=sharing). After unzipping, move `pretrain/` and `downstream/` to `dataset/`, and move `UniSRec-xx-xx-xx.pth` to `saved/`.


#### Pretrain
Pretrain the model and find the optimal parameter combination.
```
python tune.py -d 'dataset name'
```
The `'dataset name'` can be `mg`, `mb` or `gb`.

#### Finetune and Test
Once the model has been pretrained, proceed to finetune it on the target dataset. After finetuning, test the model on the target dataset to evaluate its performance.

For example, we finetune and test the model on the bundle dataset.
```
python test.py -d bundle -p ./saved/UniSRec-mg-xx-xx.pth -train_stage=inductive_ft -cand_seed xx
```
For each dataset, the corresponding parameters are located in the `config.py` and the results of the test are saved in `./res/`

## Acknowledgment
We refer to the following repositories to implement the baselines in our code:
* LLM-Baseline-NIR part with [LLM-Next-Item-Rec](https://github.com/AGI-Edgerunners/LLM-Next-Item-Rec).

* Non-LLM-Baselines part with [Understanding-Diversity-in-SBRSs](https://github.com/qyin863/Understanding-Diversity-in-SBRSs) and [UniSRec](https://github.com/RUCAIBox/UniSRec).
