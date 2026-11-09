import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, recall_score, f1_score

columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
    'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
    'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
    'attack', 'difficulty_level'
]

attack_group = {
    'back': 'DoS', 'land': 'DoS', 'neptune': 'DoS', 'pod': 'DoS', 'smurf': 'DoS', 'teardrop': 'DoS',
    'apache2': 'DoS', 'mailbomb': 'DoS', 'processtable': 'DoS', 'udpstorm': 'DoS',
    'ipsweep': 'Probe', 'nmap': 'Probe', 'portsweep': 'Probe', 'satan': 'Probe', 'mscan': 'Probe', 'saint': 'Probe',
    'ftp_write': 'R2L', 'guess_passwd': 'R2L', 'imap': 'R2L', 'multihop': 'R2L', 'phf': 'R2L', 'spy': 'R2L',
    'warezclient': 'R2L', 'warezmaster': 'R2L', 'sendmail': 'R2L', 'named': 'R2L', 'snmpgetattack': 'R2L',
    'snmpguess': 'R2L', 'xlock': 'R2L', 'xsnoop': 'R2L', 'worm': 'R2L',
    'buffer_overflow': 'U2R', 'loadmodule': 'U2R', 'perl': 'U2R', 'ps': 'U2R', 'sqlattack': 'U2R',
    'xterm': 'U2R', 'rootkit': 'U2R', 'httptunnel': 'U2R',
    'normal': 'Normal'
}

def clean_attack_name(name):
    name = str(name).strip().lower()
    if name.endswith('.'):
        name = name[:-1]
    return name

def run_train():
    print("Loading data...")
    train_path = "Dataset/KDDTrain+.txt"
    test_path = "Dataset/KDDTest+.txt"
    
    df_train = pd.read_csv(train_path, header=None, names=columns)
    df_test = pd.read_csv(test_path, header=None, names=columns)
    
    df_train['attack_clean'] = df_train['attack'].apply(clean_attack_name)
    df_test['attack_clean'] = df_test['attack'].apply(clean_attack_name)
    
    df_train['attack_multiclass'] = df_train['attack_clean'].apply(lambda x: attack_group.get(x, 'Normal' if x == 'normal' else 'R2L'))
    df_test['attack_multiclass'] = df_test['attack_clean'].apply(lambda x: attack_group.get(x, 'Normal' if x == 'normal' else 'R2L'))
    
    df_train['attack_binary'] = df_train['attack_clean'].apply(lambda x: 0 if x == 'normal' else 1)
    df_test['attack_binary'] = df_test['attack_clean'].apply(lambda x: 0 if x == 'normal' else 1)
    
    categorical_cols = ['protocol_type', 'service', 'flag']
    numeric_cols = [c for c in columns if c not in categorical_cols + ['attack', 'difficulty_level']]
    
    scaler = joblib.load("DataMining/scaler.pkl")
    encoder = joblib.load("DataMining/encoder.pkl")
    
    X_train_num = scaler.transform(df_train[numeric_cols])
    X_train_cat = encoder.transform(df_train[categorical_cols])
    X_train = np.hstack((X_train_num, X_train_cat))
    
    X_test_num = scaler.transform(df_test[numeric_cols])
    X_test_cat = encoder.transform(df_test[categorical_cols])
    X_test = np.hstack((X_test_num, X_test_cat))
    
    np.random.seed(42)
    sample_idx = np.random.choice(len(X_train), 30000, replace=False)
    X_train_sample = X_train[sample_idx]
    
    y_train_binary_sample = df_train['attack_binary'].values[sample_idx]
    y_train_multi_sample = df_train['attack_multiclass'].values[sample_idx]
    
    # Define FRESH model instances for Binary (including SVM & Gradient Boosting)
    binary_models = {
        'Decision Tree': DecisionTreeClassifier(max_depth=15, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Naive Bayes': GaussianNB(),
        'SVM': LinearSVC(dual=False, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, random_state=42)
    }
    
    print("\n--- Training Binary Models ---")
    best_binary_model = None
    best_binary_f1 = -1
    best_binary_name = ""
    
    for name, model in binary_models.items():
        print(f"Training {name} for Binary...")
        model.fit(X_train_sample, y_train_binary_sample)
        preds = model.predict(X_test)
        acc = accuracy_score(df_test['attack_binary'], preds)
        rec = recall_score(df_test['attack_binary'], preds)
        f1 = f1_score(df_test['attack_binary'], preds)
        print(f"{name} -> Accuracy: {acc:.4f}, Recall: {rec:.4f}, F1-Score: {f1:.4f}")
        
        if f1 > best_binary_f1:
            best_binary_f1 = f1
            best_binary_model = model
            best_binary_name = name
            
    print(f"Saving Best Binary Model: {best_binary_name} (F1: {best_binary_f1:.4f})")
    joblib.dump(best_binary_model, "DataMining/model_binary.pkl")
    
    # Define FRESH model instances for Multiclass
    multiclass_models = {
        'Decision Tree': DecisionTreeClassifier(max_depth=15, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Naive Bayes': GaussianNB(),
        'SVM': LinearSVC(dual=False, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, random_state=42)
    }
    
    print("\n--- Training Multiclass Models ---")
    best_multi_model = None
    best_multi_f1 = -1
    best_multi_name = ""
    
    for name, model in multiclass_models.items():
        print(f"Training {name} for Multiclass...")
        model.fit(X_train_sample, y_train_multi_sample)
        preds = model.predict(X_test)
        acc = accuracy_score(df_test['attack_multiclass'], preds)
        f1 = f1_score(df_test['attack_multiclass'], preds, average='macro')
        print(f"{name} -> Accuracy: {acc:.4f}, Macro F1-Score: {f1:.4f}")
        
        if f1 > best_multi_f1:
            best_multi_f1 = f1
            best_multi_model = model
            best_multi_name = name
            
    print(f"Saving Best Multiclass Model: {best_multi_name} (F1: {best_multi_f1:.4f})")
    joblib.dump(best_multi_model, "DataMining/model_multiclass.pkl")
    print("SUCCESS: Retraining with all models complete!")

def update_notebook():
    file_path = "DataMining/DM_Classification.ipynb"
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
        
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            new_source = []
            modified = False
            for line in source:
                if "'Naive Bayes': GaussianNB()" in line:
                    new_source.append(line)
                    # Add SVM and Gradient Boosting to binary models dictionary definition
                    if "models =" in "".join(source):
                        new_source.append("    'SVM': LinearSVC(dual=False, random_state=42),\n")
                        new_source.append("    'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, random_state=42)\n")
                        modified = True
                    elif "models_multi =" in "".join(source):
                        new_source.append("    'SVM': LinearSVC(dual=False, random_state=42),\n")
                        new_source.append("    'Gradient Boosting': GradientBoostingClassifier(n_estimators=50, random_state=42)\n")
                        modified = True
                else:
                    new_source.append(line)
            if modified:
                # Remove duplicate keys if any or filter
                filtered = []
                for l in new_source:
                    if "LinearSVC" in l and l in filtered:
                        continue
                    if "GradientBoostingClassifier" in l and l in filtered:
                        continue
                    filtered.append(l)
                cell["source"] = filtered
                cell["outputs"] = []
                cell["execution_count"] = None
                print("Updated notebook imports & dictionary with SVM/GB!")
                
    # Also add imports of LinearSVC and GradientBoostingClassifier at cell 15
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            if "from sklearn.linear_model import LogisticRegression" in "".join(source):
                new_source = []
                for line in source:
                    if "from sklearn.linear_model import LogisticRegression" in line:
                        new_source.append(line)
                        new_source.append("from sklearn.svm import LinearSVC\n")
                        new_source.append("from sklearn.ensemble import GradientBoostingClassifier\n")
                    else:
                        new_source.append(line)
                cell["source"] = new_source
                cell["outputs"] = []
                cell["execution_count"] = None
                print("Added SVM and GB imports to training cell in notebook!")
                
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)

if __name__ == "__main__":
    run_train()
    update_notebook()
