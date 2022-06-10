# Vee-ML-Deployment
Vee Machine Learning Deployment

## Folder Structure
### dataset
Dataset folder contain the dataset used for training. This folder also contains the code for generating the dataset.

### model
Model folder contain the model used machine learning with format .h5. The model generated from the dataset is stored in this folder.

### notebook
Notebook folder contain the notebook used for training and generating the model. You can import the notebook on Jupyter Notebook or Google Colab.

## Minimum Requirements
- Python 3.6
- pip3
- numpy
- pandas
- matplotlib
- tensorflow
- keras
- sklearn

## Installation instructions
Fork and clone the forked repository:
```shell
git clone git://github.com/<your_fork>/Vee-ML-Deployment
```
Install requirement libraries:
```shell
pip3 install -r requirements.txt
```
Run **main.py**:
```shell
python3 main.py
```

## Usage
Predicting the data:
```
curl -H 'Content-Type: application/json' -X POST -d '{"data": [83000, 70000, 80000, 120000, 300000]}' \
     http://<YOUR_IP>:8080/v2/predict
```
Example response:
```
    {
        "forecast":[90767,89717,90525,93743],
        "success":true
    }
```