import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

import pandas as pd
import numpy as np
import sys
import os
from os import listdir
import config as CONFIG
pd.set_option('display.max_columns', 500)
from src.data.provide_data import get_model_data


X_train, y_train = get_model_data(filename = "Train")
X_valid, y_valid = get_model_data(filename = "Valid")
X_test, y_test = get_model_data(filename = "Test")

cat = [X_train.columns.get_loc(i) for i in ["Team","Div","Opponent"]]

def add_bets(y,X,columns=['BW_Team','BW_Draw','BW_Opponent']):
    y_bets = pd.concat([y,X[columns]],axis=1)
    return y_bets

y_train_bets = np.array(add_bets(y=y_train,X=X_train,columns=['BW_Team','BW_Draw','BW_Opponent']))
y_test_bets = np.array(add_bets(y=y_test,X=X_test,columns=['BW_Team','BW_Draw','BW_Opponent']))
y_valid_bets = np.array(add_bets(y=y_valid,X=X_valid,columns=['BW_Team','BW_Draw','BW_Opponent']))

features = X_train.columns


# Scaling
from sklearn.preprocessing import StandardScaler

# Initialize scaler object
scaler = StandardScaler()

# Fit scaler on training data
scaler.fit(X_train)

# Scale training and test data
X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)
X_valid = scaler.transform(X_valid)

import torch
from pytorch_tabnet.tab_model import TabNetClassifier
n_d = 8
n_a = 8
n_steps = 3
gamma = 1
lambda_sparse = 0.001
lr = 2e-2
batch_size = 128
max_epochs = 1000
# Define a custom loss function

import torch
import torch.nn as nn

from functools import partial

import torch
from pytorch_tabnet.tab_model import TabNetClassifier
n_d = 8
n_a = 8
n_steps = 3
gamma = 1
lambda_sparse = 0.001
lr = 2e-2
batch_size = 128
max_epochs = 1000
# Define a custom loss function

import torch
import torch.nn as nn

from functools import partial

class BetLoss(nn.Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, output, target):
        if len(output.shape)>1:
            output =  output[:,1]
        output_pred = torch.clamp(torch.abs(output),min=0, max=1)            

        if len(target.shape)>1:
            target = target[:,0]
        target_pred = torch.clamp(torch.abs(target),min=0, max=1)

        #self.bets
        output_array = output_pred>0.5
        target_array = target_pred>0.5
        # loss = torch.sum(torch.abs(self.X_train_subset) * (torch.abs(target)-torch.abs(output)))/ torch.sum(torch.abs(self.X_train_subset))
        # precision = torch.sum((output_array == True) & (target_array == True))/target_array.size(0)
        loss = torch.sum(1/output_pred[output_array & (target_array==False)])/torch.sum(1/output_pred[output_array])
        
        return loss
    
class BetLoss(nn.Module):
    def __init__(self):
        super().__init__()
        
    def forward(self, output, target):
        if len(output.shape)>1:
            output =  output[:,1]
        output_pred = torch.clamp(torch.abs(output),min=0, max=1)            

        if len(target.shape)>1:
            target = target[:,0]
        target_pred = torch.clamp(torch.abs(target),min=0, max=1)

        #self.bets
        output_array = output_pred>0.5
        target_array = target_pred>0.5
        # loss = torch.sum(torch.abs(self.X_train_subset) * (torch.abs(target)-torch.abs(output)))/ torch.sum(torch.abs(self.X_train_subset))
        # precision = torch.sum((output_array == True) & (target_array == True))/target_array.size(0)
        loss = torch.sum(output_array)-torch.sum(1/output_pred[output_array])
        
        return loss
    
ind = [i for i, x in enumerate(features) if x in ["BW_Team"]]

model = TabNetClassifier(n_d=n_d, n_a=n_a, n_steps=n_steps, gamma=gamma, lambda_sparse=lambda_sparse, optimizer_fn=torch.optim.Adam, optimizer_params=dict(lr=lr), mask_type='entmax', device_name='cuda' if torch.cuda.is_available() else 'cpu')

# Define and train the model with the custom loss function
# Define and train the model with the custom loss function
model.fit(X_train=X_train, y_train=y_train,  eval_set=[(X_train, y_train), (X_valid, y_valid)],
    eval_name=['train', 'valid'], eval_metric=['balanced_accuracy','auc'],batch_size=batch_size, max_epochs=max_epochs, patience=50,loss_fn=BetLoss())


from matplotlib import pyplot as plt
clf = model
plt.plot(clf.history['loss'], label='Validation Loss')
plt.plot(clf.history['valid_auc'], label='AUC')
plt.plot(clf.history['valid_balanced_accuracy'], label='Accuracy')

plt.legend()
plt.show()

from sklearn.metrics import classification_report

y_pred = clf.predict(X_test)
r = classification_report(y_pred=y_pred,y_true=y_test)
print(r)

import numpy as np
f_i = np.round(pd.Series(clf.feature_importances_),3)
f_i.index = features
f_i.sort_values(ascending=False)
print(f_i)