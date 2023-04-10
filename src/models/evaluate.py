import pandas as pd 
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve,classification_report)
import numpy as np

def custom_classification_report(X,y,model):
    """ 
    Erweitert Classification Report um AUC
    """
    y_pred = model.predict(X)
    y_score = model.predict_proba(X)[:,1]
    r = classification_report(y_pred=y_pred,y_true=y)
    print(r)
    print("AUC",np.round(roc_auc_score(y_true=y, y_score=y_score),3))


def custom_lazy_report(X,y,lazy_clf):
    """ 
    Erweitert Classification Report um AUC
    """

    precision = {}
    recall = {}
    auc = {}
    f_1 = {}
    accuracy = {}
    models = lazy_clf.models
    for name, model_fit in models.items():
        
        y_pred = model_fit.predict(X)
        try:
            print(name)
            y_proba =  model_fit.predict_proba(X)[:,1]
        except:
            
            y_proba = model_fit.predict(X)
        precision[name] = precision_score(y_pred=y_pred,y_true=y, average='micro')
        recall[name] = recall_score(y_pred=y_pred,y_true=y, average='micro')
        accuracy[name] = accuracy_score(y_pred=y_pred,y_true=y)
        
        try:
            auc[name] = roc_auc_score(y, y_proba)
            f_1[name]= f1_score(y_pred=y_pred,y_true=y)
        except:
            pass
    
    results = pd.DataFrame()
    results['recall'] = pd.Series(recall)
    results['precision'] = pd.Series(precision)
    results['auc'] = pd.Series(auc)
    results['f_1'] = pd.Series(f_1)
    results['accuracy'] = pd.Series(accuracy)
    return results.sort_values(['auc','f_1'],ascending=False)

@ DeprecationWarning
def evaluate_model(model, y_test, X_test, show=False,threshold=''):
    if threshold == '':
        y_pred = model.predict(X_test)
    else:
       y_pred = model.predict_proba(X_test)[:,1]>threshold

    modellguete = dict()
    modellguete["roc_auc_score"] = np.round(roc_auc_score(y_test, y_pred,), 3)
    modellguete["f1_score"] = np.round(f1_score(y_test, y_pred), 3)
    modellguete["accuracy_score"] = np.round(accuracy_score(y_test, y_pred), 3)
    modellguete["precision_score"] = np.round(
        precision_score(y_test, y_pred), 3)
    modellguete["recall_score"] = np.round(recall_score(y_test, y_pred), 3)

    print('AUC Score : ', modellguete["roc_auc_score"])
    print('F1 Score : ', modellguete["f1_score"])
    print('Accuracy Score : ', modellguete["accuracy_score"])
    print('Precision Score : ', modellguete["precision_score"])
    print('Recall Score : ', modellguete["recall_score"])

    # Model Accuracy, how often is the classifier correct?
    print('Confusion Matrix : /n' +
          str(np.round(confusion_matrix(y_test, y_pred), 3)))
    if True:
        try:
            print('-'*100)
            print('Feature Importance',)
            feature_imp = pd.Series(
                model.feature_importances_, index=X_test.columns).sort_values(ascending=False)[0:15]
            feature_imp.to_json()
            print('Important')
            print(feature_imp)
            feature_not_imp = pd.Series(
                model.feature_importances_, index=X_test.columns).sort_values(ascending=True)[0:15]
            print('Not Important')
            print(feature_not_imp)
        except:
            print('Fehler bei Feature Importance')
            pass

    if False:
        try:
            print('-'*100)
            print('Shap Values',)
            rf_shap_values = shap.TreeExplainer(model).shap_values(
                X_test.sample(100, random_state=42))
            shap_df = pd.DataFrame(rf_shap_values[0], columns=X_test.columns)
            print(np.abs(shap_df).mean().sort_values(ascending=False))
        except:
            pass

        try:
            X_test.corr().round(2)[X_test.corr().round(2) > 0.3].to_csv(
                'C:/Users/Robert/Documents/corr.csv', sep=';', decimal=',', index=True)
        except:
            pass

    print('-'*100)
    return modellguete