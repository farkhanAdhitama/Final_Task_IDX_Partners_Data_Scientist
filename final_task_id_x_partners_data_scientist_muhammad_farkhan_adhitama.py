# -*- coding: utf-8 -*-
"""Final Task_ID/X Partners_Data Scientist_Muhammad Farkhan Adhitama.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RORXSTgiIuQv4do38TrX4Qs27prIqHsg

# Final Task ID/X Partners Data Scientist : Muhammad Farkhan Adhitama

**Prediksi credit risk** merupakan metode yang efektif untuk mengevaluasi apakah seorang calon peminjam akan mampu melunasi pinjamannya.

**Penjelasan solusi:**  
Sebagai seorang data scientist, kita akan membangun sebuah model machine learning yang dapat mengidentifikasi apakah suatu pinjaman tergolong berisiko atau berpotensi gagal bayar. Model ini nantinya dapat digunakan sebagai alat bantu dalam pengambilan keputusan investasi. Jika model yang kami kembangkan cukup andal, maka investasi pada pinjaman yang berisiko akan berkurang, potensi kerugian dapat diminimalkan, dan margin keuntungan bersih akan meningkat.

## Import Library
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import ConfusionMatrixDisplay , classification_report , accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import warnings
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import GridSearchCV

"""## Load Dataset

Data yang digunakan adalah data loan dataset dari tahun 2007 sampai 2014. Dataset tersebut dapat diakses pada link berikut :   
```
https://rakamin-lms.s3.ap-southeast-1.amazonaws.com/vix-assets/idx-partners/loan_data_2007_2014.csv
```
Dataset tersebut berisi data historis calon kreditur yang dapat digunakan untuk memprediksi apakah seseorang layak diberi kredit. Untuk memahami isi dataset tersebut, kita dapat melihat penjelasannya di link berikut:
```
https://docs.google.com/spreadsheets/d/1iT1JNOBwU4l616_rnJpo0iny7blZvNBs/edit?usp=sharing&ouid=106453318899954059421&rtpof=true&sd=true
```
"""

# Load dataset (load dataset) dari link yang disediakan
# URL CSV export dari Google Sheets
url = "https://rakamin-lms.s3.ap-southeast-1.amazonaws.com/vix-assets/idx-partners/loan_data_2007_2014.csv"
# Load ke DataFrame
df = pd.read_csv(url)
df.head()

"""## Data Understanding

### Struktur Dataset
"""

# Tampilkan struktur lengkap dataset loan
df.info()

"""### Statistik Dataset"""

# Tampilkan statistik dataset untuk kolom numerikal
df.describe()

"""### Mendefinisikan Fitur  Target

Sebelum melakukan Exploratory Data Analysis (EDA), kita akan memilih fitur target yang digunakan untuk memprediksi apakah peminjam layak diberi kredit pinjaman. Prediksi risiko kredit merupakan cara efektif untuk mengevaluasi apakah calon peminjam akan membayar kembali pinjamannya. Fitur target yang digunakan adalah loan_status (status kredit). Isi dari fitur tersebut yaitu:  
- Current
- Fully Paid
- Charged Off
- Late (31-120 days)
- In Grace Period
- Does not meet the credit policy. Status:Fully Paid
- Late (16-30 days)
- Default
- Does not meet the credit policy. Status:Charged Off  

Status tersebut akan dikelompokkan menjadi dua kelompok yaitu :   
- Good = ['Current', 'Fully Paid', 'In Grace Period', 'Does not meet the credit policy. Status:Fully Paid']
- Bad = ['Charged Off', 'Late (31-120 days)', 'Late (16-30 days)', 'Default', 'Does not meet the credit policy. Status:Charged Off']
"""

# Cek isi kolom loan_status
df["loan_status"].value_counts()

# Tambahkan kolom credit_risk berdasarkan kelompok yang dibuat
good_status = [
    'Current',
    'Fully Paid',
    'In Grace Period',
    'Does not meet the credit policy. Status:Fully Paid'
]

bad_status = [
    'Charged Off',
    'Late (31-120 days)',
    'Late (16-30 days)',
    'Default',
    'Does not meet the credit policy. Status:Charged Off'
]

df['credit_risk'] = df['loan_status'].apply(
    lambda x: 'Good' if x in good_status else ('Bad' if x in bad_status else 'Unknown')
)

# Sample loan status dan credit risk
df[["loan_status", "credit_risk"]].head()

"""## EDA

### Status Kredit Peminjam
"""

# Perbandingan jumlah credit risk pada peminjam
df['credit_risk'].value_counts()

# Visualisasi perbandingan credit_risk antara good atau bad
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="credit_risk")
plt.title("Perbandingan Credit Risk")
plt.xlabel("Credit Risk")
plt.ylabel("Count")
plt.show()

"""Dilihat dari visualisasi di atas, mayoritas peminjam memiliki status kredit yang baik. Hanya sedikit peminjam yang memiliki status kredit yang buruk.

### Kelompokkan Fitur
"""

# Loan Characteristics
loan_cols = np.intersect1d(df.columns, [
'loan_amnt', 'funded_amnt', 'term', 'int_rate', 'installment',
'grade', 'sub_grade', 'purpose', 'loan_status', 'application_type'
])

# Borrower Profile & Capacity
borrower_cols = np.intersect1d(df.columns, [
'addr_state', 'home_ownership', 'emp_length', 'emp_title',
'annual_inc', 'dti', 'is_inc_v', 'zip_code'
])

# Credit Score & History
credit_history_cols = np.intersect1d(df.columns, [
'fico_range_low', 'fico_range_high', 'earliest_cr_line',
'open_acc', 'total_acc', 'pub_rec', 'mths_since_last_record'
])

# Credit Utilization & Behavior
credit_behavior_cols = np.intersect1d(df.columns, [
'revol_bal', 'revol_util', 'delinq_2yrs', 'mths_since_last_delinq',
'acc_now_delinq', 'inq_last_6mths', 'collections_12_mths_ex_med'
])

# Loan Performance & Recovery
performance_cols = np.intersect1d(df.columns, [
'out_prncp', 'out_prncp_inv', 'total_pymnt', 'total_pymnt_inv',
'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee',
'recoveries', 'collection_recovery_fee', 'last_pymnt_amnt'
])

# Target feature
target_col = ['credit_risk']

# Membuat dataframe untuk masing masing kelompok fitur
df_loan = df[loan_cols]
df_borrower = df[borrower_cols]
df_credit_history = df[credit_history_cols]
df_credit_behavior = df[credit_behavior_cols]
df_performance = df[performance_cols]

"""#### Loan Characteristics"""

# Gabungkan df_load dengan fitur target
df_loan = pd.concat([df_loan, df[target_col]], axis=1)
df_loan.head()

# Fitur numerik
num_cols = df_loan.select_dtypes(include=['int64', 'float64']).columns
n_cols = 3
n_rows = int(np.ceil(len(num_cols) / n_cols))

# Create subplots with 3 columns
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
if n_rows == 1:
    axes = axes.reshape(1, -1)
axes = axes.flatten()
# Create boxplots for each numerical column
for i, col in enumerate(num_cols):
    sns.boxplot(data=df_loan, x='credit_risk', y=col, ax=axes[i])
    axes[i].set_title(f'{col}', fontsize=12, fontweight='bold')
    axes[i].tick_params(axis='x', rotation=45)
# Hide empty subplots
for j in range(len(num_cols), len(axes)):
    axes[j].set_visible(False)
plt.tight_layout()
plt.show()

"""Dari visualisasi di atas, didapatkan insight bahwa int_rate pada credit risk yang buruk cenderung lebih tinggi dari pada yang baik."""

# Fitur Kategorikal
cat_cols = df_loan.select_dtypes(include=['object']).columns
cat_cols = [col for col in cat_cols if col != 'credit_risk']

# Calculate number of rows needed for 3 columns layout
n_cols = 3
n_rows = int(np.ceil(len(cat_cols) / n_cols))
# Create subplots with 3 columns
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
# Flatten axes array for easier indexing
if n_rows == 1:
    axes = axes.reshape(1, -1)
axes = axes.flatten()
# Create countplots for each categorical column
for i, col in enumerate(cat_cols):
    sns.countplot(data=df_loan, x=col, hue='credit_risk', ax=axes[i])
    axes[i].set_title(f'{col}', fontsize=12, fontweight='bold')
    axes[i].tick_params(axis='x', rotation=45)
    axes[i].legend(title='Credit Risk', loc='upper right')
# Hide empty subplots
for j in range(len(cat_cols), len(axes)):
    axes[j].set_visible(False)
plt.tight_layout()
plt.show()

"""Dari visualisasi tersebut, banyak insight yang didapatkan untuk memiliki fitur yang digunakan untuk prediksi credit risk dari peminjam

#### Borrower Profile & Capacity
"""

# Gabungkan df_borrower dengan fitur target
df_borrower = pd.concat([df_borrower, df[target_col]], axis=1)
df_borrower.head()

# Tampilkan rata-rata annual_inc dan dti berdasarkan credit risk
df_borrower.groupby('credit_risk')[['annual_inc', 'dti']].mean()

"""Annual income untuk peminjam dengan credit risk yang baik memiliki rata-rata yang lebih tinggi daripada yang buruk. Lalu tuntuk DTI hampir mirip"""

# Tampilkan jumlah home_ownership yang rent, kelompokan berdasarknan credit_risk
df_borrower.groupby('credit_risk')['home_ownership'].value_counts()

"""Dari tabel di atas, didapatkan hasil bahwa seseorang yang memiliki credit risk yang buruk cendreung melakukan kontrak dan mortgage dengan jumlah yang mirip. Pada credit risk yang baik hampir mirip namun mortgaes jauh lebih banyak daripada rent.

#### Credit History
"""

# Gabungkan df_credit_history dengan fitur target
df_credit_history = pd.concat([df_credit_history, df[target_col]], axis=1)
df_credit_history.head()

# Tampilkan rata-rata open acc, pub rec, dan total acc berdasarkan credit risk
df_credit_history.groupby('credit_risk')[['open_acc', 'pub_rec', 'total_acc']].mean()

"""#### Credit Behavior"""

# Gabungkan df_credit_behavior dengan fitur target
df_credit_behavior = pd.concat([df_credit_behavior, df[target_col]], axis=1)
df_credit_behavior.head()

# Fitur numerik
num_cols = df_credit_behavior.select_dtypes(include=['int64', 'float64']).columns
n_cols = 3
n_rows = int(np.ceil(len(num_cols) / n_cols))

# Create subplots with 3 columns
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
if n_rows == 1:
    axes = axes.reshape(1, -1)
axes = axes.flatten()
# Create boxplots for each numerical column
for i, col in enumerate(num_cols):
    sns.boxplot(data=df_credit_behavior, x='credit_risk', y=col, ax=axes[i])
    axes[i].set_title(f'{col}', fontsize=12, fontweight='bold')
    axes[i].tick_params(axis='x', rotation=45)
# Hide empty subplots
for j in range(len(num_cols), len(axes)):
    axes[j].set_visible(False)
plt.tight_layout()
plt.show()

"""#### Borrower Performance"""

# Gabungkan df_performance dengan fitur target
df_performance = pd.concat([df_performance, df[target_col]], axis=1)
df_performance.head()

# Fitur numerik
num_cols = df_performance.select_dtypes(include=['int64', 'float64']).columns
n_cols = 3
n_rows = int(np.ceil(len(num_cols) / n_cols))

# Create subplots with 3 columns
fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
if n_rows == 1:
    axes = axes.reshape(1, -1)
axes = axes.flatten()
# Create boxplots for each numerical column
for i, col in enumerate(num_cols):
    sns.boxplot(data=df_performance, x='credit_risk', y=col, ax=axes[i])
    axes[i].set_title(f'{col}', fontsize=12, fontweight='bold')
    axes[i].tick_params(axis='x', rotation=45)
# Hide empty subplots
for j in range(len(num_cols), len(axes)):
    axes[j].set_visible(False)
plt.tight_layout()
plt.show()

"""## Data Preparation

### Drop Kolom yang Tidak Relevan

Kolom yang tidak relevan seperti Unnamed,0, id, url, dan lainnya. Kolom akan didrop karena tidak berpengaruh pada hasil prediksi.
"""

df_credit = df.copy()
df_credit.head()

df_credit.drop(columns=['Unnamed: 0', 'id', 'member_id', 'url', 'title', 'desc', 'zip_code' ,'emp_title'], inplace=True)
df_credit.head()

"""### Cek Missing Value"""

df_credit.isna().sum()

# Menghitung rasio missing value setiap kolom
# Hitung rasio missing value
missing_ratio = df_credit.isnull().mean()
missing_over_10 = missing_ratio[missing_ratio > 0.10]
missing_over_10_percent = (missing_over_10 * 100).round(2).astype(str) + '%'
print(missing_over_10_percent)

# Drop kolom yang memiliki mising value lebih dari 10 persen jumlah baris data
df_credit = df_credit.drop(columns=missing_over_10.index)

df_credit.isna().sum()

# Lihat isi dari masing masing kolom yang masih memiliki missinf values
missing_cols = df_credit.columns[df_credit.isna().any()]
df_credit[missing_cols].head()

# Hapus emp_length karena terlalu banyak data yang hilang
df_credit.drop(columns=['emp_length'], inplace=True)

# Isi earliest_cr_line, last_pymnt_d, last_credit_pull_d yang null dengan "unknown"
df_credit['earliest_cr_line'] = df_credit['earliest_cr_line'].fillna('unknown')
df_credit['last_pymnt_d'] = df_credit['last_pymnt_d'].fillna('unknown')
df_credit['last_credit_pull_d'] = df_credit['last_credit_pull_d'].fillna('unknown')
missing_cols = df_credit.columns[df_credit.isna().any()]
print(missing_cols)

# Mengisi missing value pada kolom numerik menggunakan median dari data tersebut
cols_to_impute = [
    'annual_inc', 'delinq_2yrs', 'inq_last_6mths', 'open_acc', 'pub_rec',
    'revol_util', 'total_acc',
    'collections_12_mths_ex_med', 'acc_now_delinq'
]
for col in cols_to_impute:
    if col in df_credit.columns:
        if df_credit[col].dtype in ['float64', 'int64']:
            median_val = int(df_credit[col].median())
            df_credit[col] = df_credit[col].fillna(median_val).astype(int)

# Cek kembali kolom yang memiliki missing values
df_credit.isna().sum()

"""Dari tabel di atas, dataset yang kita gunakan sudah bersih dari missing values dengan menerapkan beberapa cara yaitu menghapus kolom dan mengisi kolom dengan string dan median.

### Cek Data Duplikat
"""

# Cek data duplikat
df_credit.duplicated().sum()

"""Tidak ada data duplikat yang ditemukan, maka lanjutkan ke tahap berikutnya.

### Deteksi Outlier (IQR)
"""

# Ambil semua kolom numerik
df_iqr = df_credit.copy()
numeric_cols = df_iqr.select_dtypes(include=['int64', 'float64']).columns
# Simpan outlier dalam dictionary
print("Jumlah outlier sebelum penanganan:")
for col in numeric_cols:
    Q1 = df_iqr[col].quantile(0.25)
    Q3 = df_iqr[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_mask = (df_iqr[col] < lower_bound) | (df_iqr[col] > upper_bound)
    num_outliers = outlier_mask.sum()

    print(f"Kolom '{col}': {num_outliers} outlier")

# Atasi outliers dengan mengganti outlier dengan nilai median kolom
for col in numeric_cols:
    Q1 = df_iqr[col].quantile(0.25)
    Q3 = df_iqr[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_mask = (df_iqr[col] < lower_bound) | (df_iqr[col] > upper_bound)
    num_outliers = outlier_mask.sum()

    if num_outliers > 0:
        median_val = df_iqr[col].median()
        df_iqr.loc[outlier_mask, col] = median_val
        print(f"Kolom '{col}': {num_outliers} outlier telah diganti dengan median ({median_val})")
    else:
        print(f"Kolom '{col}': tidak memiliki outlier.")

"""### Encoding Data Kategorikal"""

df_encoded = df_iqr.copy()
df_encoded.head()

from sklearn.preprocessing import LabelEncoder
# Simpan kolom credit_risk
credit_risk_col = df_encoded['credit_risk']
# Pilih kolom kategorikal
categorical_cols = df_encoded.select_dtypes(include=['object'])
# Simpan label encoder untuk tiap kolom jika dibutuhkan nanti
label_encoders = {}
# Encode setiap kolom kategorikal
for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])
    label_encoders[col] = le

df_encoded.head()

"""### Data Standarization"""

# Standarization data dengan scaler
from sklearn.preprocessing import StandardScaler
df_scaled = df_encoded.copy()
# Scaling kolom numerik
scaler = StandardScaler()
scaled_array = scaler.fit_transform(df_scaled)  # hasilnya numpy array
df_scaled = pd.DataFrame(scaled_array, columns=df_scaled.columns, index=df_scaled.index)

df_scaled.head()

# Matriks korelasi antar fitur
corr_matrix = df_scaled.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix[['credit_risk']].sort_values(by='credit_risk', ascending=False), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Korelasi Fitur dengan Credit Risk')
plt.show()

"""### Feature Selection

Berdasarkan matriks korelasi sebelumnya, kita akan memilih beberapa fitur yang memiliki korelasi positif maupun negatif yang cukup besar dengan fitur target yaitu credit risk. Fitur tersebut yaitu 'total_rec_prncp',
    'loan_status',
    'total_pymnt_inv',
    'total_pymnt',
    'out_prncp',
    'out_prncp_inv',
    'last_pymnt_amnt',
    'last_pymnt_d',
    'grade',
    'int_rate', dan
    'sub_grade'.
"""

# Daftar fitur terpilih berdasarkan korelasi dengan credit_risk
selected_features = [
    'total_rec_prncp',
    'loan_status',
    'total_pymnt_inv',
    'total_pymnt',
    'out_prncp',
    'out_prncp_inv',
    'last_pymnt_amnt',
    'last_pymnt_d',
    'grade',
    'int_rate',
    'sub_grade',
]
# Buat dataframe baru hanya dengan fitur terpilih
df_selection = df_scaled[selected_features]
df_selection.head()

"""### Split Dataset"""

# X adalah fitur, Y adalah target
X = df_selection
# Ambil target fitur dari kolom credit risk yang sudah diencoding
y = df_encoded['credit_risk']

# Split data: 95% train, 5% test  karena data yang sangat banyak (tekankan pada training)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.05, random_state=42, stratify=y
)

# Cek bentuk hasil split
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)



"""### Resampling Dataset"""

# Perbandingan jumlah credit risk good dan bad
plt.figure(figsize=(6, 4))
sns.countplot(data=df_encoded, x="credit_risk")
plt.title("Perbandingan Credit Risk")
plt.xlabel("Credit Risk")
plt.ylabel("Count")
plt.show()

"""Dari gambar di atas, data yang dimiliki sangat tidak seimbang sehingga berpotensi menyebabkan bias dan menurunkan performa model. Oleh karena itu, resampling sangat dibutuhkan agar data seimbang. Kita akan melakukan undersampling terlebih dahulu pada kelas good atau 1 menjadi sekitar 250 ribu data. Lalu melakukan smote pada kelas bad atau 0 hingga menjadi 200 ribu data."""

# Undersampling kelas Good
target_counts = {
    1: 250000,  # Good → label 1
}

# Lakukan undersampling
rus = RandomUnderSampler(sampling_strategy=target_counts, random_state=42)
X_under, y_under = rus.fit_resample(X_train, y_train)

print("Distribusi setelah undersampling:", dict(zip(*np.unique(y_under, return_counts=True))))

# Visualisasi perbandingan y_under
plt.figure(figsize=(6, 4))
sns.countplot(data=pd.DataFrame({'credit_risk': y_under}), x="credit_risk")
plt.title("Perbandingan Credit Risk Setelah Undersampling")

# Lakukan SMOTE pada kelas Bad
# Tentukan target kelas minoritas
target_counts = {
    0: 175000
}

# Terapkan SMOTE untuk kelas Bad saja
smote = SMOTE(sampling_strategy=target_counts, random_state=42)
X_train_final, y_train_final = smote.fit_resample(X_under, y_under)

# Cek hasil distribusi
print("Distribusi setelah SMOTE:", dict(zip(*np.unique(y_train_final, return_counts=True))))

# Visualisasi perbandingan data training final
plt.figure(figsize=(6, 4))
sns.countplot(data=pd.DataFrame({'credit_risk': y_train_final}), x="credit_risk")
plt.title("Perbandingan Credit Risk Setelah SMOTE")

"""## Data Modelling

### Logistic Regression
"""

# Set Up logistic regreesion
log_reg = LogisticRegression(max_iter=1000)

# Grid Search
param_grid = {
    'C': [0.001, 0.01, 0.1, 10],
    'penalty': ['l1', 'l2'],
    'solver': ['saga']
}
grid_search = GridSearchCV(
    log_reg,
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_train_final, y_train_final)

# Simpan model terbaik
best_model_lr = grid_search.best_estimator_

# Evaluasi Model
y_pred_lr = best_model_lr.predict(X_test)
y_proba_lr = best_model_lr.predict_proba(X_test)[:, 1]

print("Best Params:", grid_search.best_params_)
print("\nLogistic Regression Classification Report:\n", classification_report(y_test, y_pred_lr))
print("ROC-AUC Score:", roc_auc_score(y_test, y_proba_lr))

# Confusion Matrix
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred_lr), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Cek Kemungkinan Overfitting
train_score = best_model_lr.score(X_train_final, y_train_final)
test_score = best_model_lr.score(X_test, y_test)

print(f"Train Accuracy: {train_score:.4f}")
print(f"Test Accuracy: {test_score:.4f}")

if abs(train_score - test_score) > 0.1:
    print("⚠️ Model kemungkinan overfitting atau underfitting.")
else:
    print("✅ Model seimbang antara train dan test.")

import joblib
# Simpan model ke file
joblib.dump(best_model_lr, 'logistic_model_credit_risk.pkl')

"""### K Nearest Neighbor (KNN)"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

# Set up KNN classifier
knn = KNeighborsClassifier()

# Grid Search parameter grid untuk KNN
param_grid = {
    'n_neighbors': [3, 5],         # jumlah tetangga terdekat
    'weights': ['uniform', 'distance'], # pembobotan tetangga
    'metric': ['euclidean', 'manhattan'] # metrik jarak
}

grid_search = GridSearchCV(
    knn,
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_final, y_train_final)

# Simpan model terbaik
best_model_knn = grid_search.best_estimator_

# Evaluasi Model KNN
y_pred_knn = best_model_knn.predict(X_test)
y_proba_knn = best_model_knn.predict_proba(X_test)[:, 1]

print("Best Params:", grid_search.best_params_)
print("\nKNN Classification Report:\n", classification_report(y_test, y_pred_knn))
print("ROC-AUC Score:", roc_auc_score(y_test, y_proba_knn))

# Confusion Matrix
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred_knn), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Cek Kemungkinan Overfitting pada random forest
train_score_knn = best_model_knn.score(X_train_final, y_train_final)
test_score_knn = best_model_knn.score(X_test, y_test)

print(f"Train Accuracy: {train_score_knn:.4f}")
print(f"Test Accuracy: {test_score_knn:.4f}")

if abs(train_score_knn - test_score_knn) > 0.1:
    print("⚠️ Model kemungkinan overfitting atau underfitting.")
else:
    print("✅ Model seimbang antara train dan test.")

# Simpan model ke file
joblib.dump(best_model_knn, 'knn_model_credit_risk.pkl')

"""### Naive Bayes"""

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

# Set up Naive Bayes classifier
nb = GaussianNB()

# Tidak banyak hyperparameter untuk GaussianNB,
# tapi kamu bisa pakai GridSearchCV kalau mau uji `var_smoothing`
param_grid = {
    'var_smoothing': [1e-9, 1e-8, 1e-7]
}

grid_search = GridSearchCV(
    nb,
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train_final, y_train_final)

# Simpan model terbaik
best_model_nb = grid_search.best_estimator_

# Evaluasi Model Naive Bayes
y_pred_nb = best_model_nb.predict(X_test)
y_proba_nb = best_model_nb.predict_proba(X_test)[:, 1]

print("Best Params:", grid_search.best_params_)
print("\nNaive Bayes Classification Report:\n", classification_report(y_test, y_pred_nb))
print("ROC-AUC Score:", roc_auc_score(y_test, y_proba_nb))

# Confusion Matrix
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred_nb), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Cek Kemungkinan Overfitting pada random forest
train_score_nb = best_model_nb.score(X_train_final, y_train_final)
test_score_nb = best_model_nb.score(X_test, y_test)

print(f"Train Accuracy: {train_score_nb:.4f}")
print(f"Test Accuracy: {test_score_nb:.4f}")

if abs(train_score_nb - test_score_nb) > 0.1:
    print("⚠️ Model kemungkinan overfitting atau underfitting.")
else:
    print("✅ Model seimbang antara train dan test.")

# Simpan model ke file
joblib.dump(best_model_nb, 'naive_bayes_model_credit_risk.pkl')

"""## Evaluasi

### Hasil Testing Tiap Model
"""

# Logistic Regression
# Hitung metrik evaluasi
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr, pos_label=1)
recall_lr = recall_score(y_test, y_pred_lr, pos_label=1)
f1_lr = f1_score(y_test, y_pred_lr, pos_label=1)
roc_auc_lr = roc_auc_score(y_test, y_proba_lr)

# Tampilkan hasil
print("Logistic Regression Metrics Test:")
print(f"Accuracy : {accuracy_lr:.4f}")
print(f"Precision: {precision_lr:.4f}")
print(f"Recall   : {recall_lr:.4f}")
print(f"F1 Score : {f1_lr:.4f}")
print(f"ROC AUC  : {roc_auc_lr:.4f}")

# KNN
# Hitung metrik evaluasi
accuracy_knn = accuracy_score(y_test, y_pred_knn)
precision_knn = precision_score(y_test, y_pred_knn, pos_label=1)
recall_knn = recall_score(y_test, y_pred_knn, pos_label=1)
f1_knn = f1_score(y_test, y_pred_knn, pos_label=1)
roc_auc_knn = roc_auc_score(y_test, y_proba_knn)

# Tampilkan hasil
print("Logistic Regression Metrics Test:")
print(f"Accuracy : {accuracy_knn:.4f}")
print(f"Precision: {precision_knn:.4f}")
print(f"Recall   : {recall_knn:.4f}")
print(f"F1 Score : {f1_knn:.4f}")
print(f"ROC AUC  : {roc_auc_knn:.4f}")

# Naive Bayes
# Hitung metrik evaluasi
accuracy_nb = accuracy_score(y_test, y_pred_nb)
precision_nb = precision_score(y_test, y_pred_nb, pos_label=1)
recall_nb = recall_score(y_test, y_pred_nb, pos_label=1)
f1_nb = f1_score(y_test, y_pred_nb, pos_label=1)
roc_auc_nb = roc_auc_score(y_test, y_proba_nb)

# Tampilkan hasil
print("Logistic Regression Metrics Test:")
print(f"Accuracy : {accuracy_nb:.4f}")
print(f"Precision: {precision_nb:.4f}")
print(f"Recall   : {recall_nb:.4f}")
print(f"F1 Score : {f1_nb:.4f}")
print(f"ROC AUC  : {roc_auc_nb:.4f}")

"""### Perbandingan Metriks Evaluasi

Pada kasus ini, kita akan menggunakan ROC AUC score untuk melihat dan memilih model terbaik. ROC AUC dipilih karena metrik ini memberikan gambaran menyeluruh tentang kemampuan model dalam membedakan antara kelas Bad dan Good, tanpa bergantung pada threshold tertentu. Selain itu, ROC AUC sangat cocok digunakan pada data yang tidak seimbang, seperti pada kasus credit risk prediction, karena tetap memberikan evaluasi yang adil terhadap performa model.

Meskipun dalam credit risk prediction umumnya recall penting untuk meminimalkan risiko pemberian kredit kepada peminjam yang berisiko tinggi, ROC AUC memberikan evaluasi yang lebih stabil dan komprehensif atas seluruh rentang threshold. Hal ini memungkinkan pihak pemberi pinjaman untuk menyesuaikan threshold pengambilan keputusan sesuai kebijakan risiko internal berdasarkan probabilitas risiko yang dihasilkan model.
"""

# Buat dictionary dari nama model dan skor ROC AUC-nya
roc_auc_scores = {
    "Logistic Regression": roc_auc_lr,
    "KNN": roc_auc_knn,
    "Naive Bayes": roc_auc_nb,
}

# Buat DataFrame untuk tampilkan tabel
df_roc_auc = pd.DataFrame(list(roc_auc_scores.items()), columns=["Model", "ROC AUC Score"])
df_roc_auc = df_roc_auc.sort_values(by="ROC AUC Score", ascending=False).reset_index(drop=True)
df_roc_auc

"""### Analisa Hasil Evaluasi

1. **KNN**
- ✅ ROC AUC Score sangat tinggi (0.998) menunjukkan performa klasifikasi yang sangat baik.
- ⚠️ **Kurang cocok untuk dataset besar**, karena KNN harus menghitung jarak ke seluruh data saat prediksi → proses prediksi lambat dan memakan banyak memori. Pada
- ⚠️ Sensitif terhadap skala fitur dan outlier.
- **Rekomendasi**: Tidak disarankan untuk digunakan dalam skenario produksi berskala besar, kecuali jika dilakukan optimasi khusus (misalnya KD-Tree atau Approximate Nearest Neighbors).

2. **Logistic Regression**
- ✅ Skor ROC AUC cukup baik (0.869).
- ✅ **Cocok untuk dataset besar** karena model ini ringan, cepat saat pelatihan dan prediksi, serta skalabel.
- ✅ Mudah diinterpretasikan dan dijelaskan ke stakeholder.
- ✅ Stabil dan sering digunakan dalam dunia nyata untuk credit scoring.
- **Rekomendasi**: **Sangat layak digunakan untuk dataset besar**, terutama jika dibutuhkan efisiensi dan interpretabilitas.

3. **Naive Bayes**
- ✅ Skor ROC AUC kompetitif (0.865), sangat cepat dilatih dan dieksekusi.
- ✅ Cocok untuk data besar, namun asumsi independensi antar fitur bisa membatasi akurasi.
- ⚠️ Kurang akurat jika korelasi antar fitur tinggi.
- **Rekomendasi**: Bisa digunakan sebagai baseline atau model alternatif jika kebutuhan utamanya adalah kecepatan inferensi.

### Kesimpulan

🔵 **Logistic Regression** adalah pilihan terbaik. Walaupun skor untuk ROC AUC lebih rendah dibandingkan dengan KNN, Pada dataset yang besar dalam kasus credit risk prediction ini, model ini dipilih karena:
- Memberikan performa ROC AUC yang baik,
- Sangat cepat dalam melakukan prediksi dibandingakan KNN yang sangat lambat
- Mudah dipahami dan diimplementasikan,
- Model yang dihasilkan memiliki ukuran yang kecil serta ringan
- Lebih tahan terhadap noise dan data imbalance dibanding KNN,
- Banyak digunakan secara luas dalam industri keuangan.
"""