# Final Task IDX Partners Data Scientist : Credit Risk Prediction

## 📋 Deskripsi Proyek

Proyek ini mengembangkan model machine learning untuk memprediksi risiko kredit peminjam. Model ini dapat membantu lembaga keuangan dalam mengidentifikasi apakah seorang calon peminjam berpotensi gagal bayar atau tidak, sehingga dapat meminimalkan risiko kerugian dan meningkatkan margin keuntungan.

## 🎯 Tujuan

- Membangun model prediksi yang dapat mengklasifikasikan peminjam ke dalam kategori "Good" atau "Bad" credit risk
- Membantu pengambilan keputusan investasi yang lebih akurat
- Meminimalkan potensi kerugian dari kredit macet
- Meningkatkan profitabilitas melalui manajemen risiko yang lebih baik

## 📊 Dataset

**Sumber Data**: Loan Dataset 2007-2014  
**URL**: `https://rakamin-lms.s3.ap-southeast-1.amazonaws.com/vix-assets/idx-partners/loan_data_2007_2014.csv`

### Target Variable
Dataset menggunakan `loan_status` yang dikategorikan menjadi:
- **Good Credit Risk**: Current, Fully Paid, In Grace Period, Does not meet the credit policy. Status:Fully Paid
- **Bad Credit Risk**: Charged Off, Late (31-120 days), Late (16-30 days), Default, Does not meet the credit policy. Status:Charged Off

## 🔧 Teknologi yang Digunakan

### Libraries
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Machine Learning**: scikit-learn
- **Imbalanced Data**: imbalanced-learn (SMOTE, RandomUnderSampler)
- **Model Persistence**: joblib

### Algoritma Machine Learning
1. **Logistic Regression** ⭐ (Model Terpilih)
2. **K-Nearest Neighbors (KNN)**
3. **Naive Bayes**

## 🚀 Metodologi

### 1. Data Understanding & EDA
- Analisis struktur dataset
- Eksplorasi distribusi target variable
- Pengelompokan fitur berdasarkan kategori:
  - Loan Characteristics
  - Borrower Profile & Capacity
  - Credit Score & History
  - Credit Utilization & Behavior
  - Loan Performance & Recovery

### 2. Data Preparation
- **Data Cleaning**: 
  - Menghapus kolom tidak relevan
  - Handling missing values (>10% dihapus, sisanya diisi dengan median/string)
  - Deteksi dan penanganan outliers menggunakan IQR method
- **Feature Engineering**:
  - Label encoding untuk data kategorikal
  - Standardisasi data numerik
  - Feature selection berdasarkan korelasi
- **Data Balancing**:
  - RandomUnderSampler untuk kelas mayoritas
  - SMOTE untuk kelas minoritas

### 3. Model Development
- Grid Search untuk hyperparameter tuning
- Cross-validation 5-fold
- Evaluasi menggunakan ROC-AUC score

### 4. Model Evaluation
- Confusion Matrix
- Classification Report
- ROC-AUC Score
- Analisis overfitting/underfitting

## 📈 Hasil Evaluasi

| Model | ROC AUC Score | Keterangan |
|-------|---------------|------------|
| **KNN** | **0.998** | Performa tertinggi, namun tidak efisien untuk dataset besar |
| **Logistic Regression** | **0.869** | ⭐ **Model Terpilih** - Balance antara performa dan efisiensi |
| **Naive Bayes** | **0.865** | Cepat namun asumsi independensi membatasi akurasi |

## 🎯 Model Terpilih: Logistic Regression

### Alasan Pemilihan:
✅ **Performa ROC AUC yang baik** (0.869)  
✅ **Efisien untuk dataset besar** - cepat dalam training dan prediksi  
✅ **Mudah diinterpretasikan** dan dijelaskan ke stakeholder  
✅ **Stabil dan reliable** - banyak digunakan dalam industri keuangan  
✅ **Model ringan** dengan ukuran file kecil  
✅ **Tahan terhadap noise** dan data imbalance  

### Hyperparameter Terbaik:
```python
{
    'C': [optimal_value],
    'penalty': ['l1'/'l2'],
    'solver': 'saga'
}
```

## 🔮 Penggunaan Model

### Load Model
```python
import joblib

# Load model terpilih
model = joblib.load('logistic_model_credit_risk.pkl')

# Prediksi
prediction = model.predict(X_new)
probability = model.predict_proba(X_new)
```

### Input Features
Model menggunakan 11 fitur terpilih:
- `total_rec_prncp`
- `loan_status`
- `total_pymnt_inv`
- `total_pymnt`
- `out_prncp`
- `out_prncp_inv`
- `last_pymnt_amnt`
- `last_pymnt_d`
- `grade`
- `int_rate`
- `sub_grade`

## 💡 Business Impact

### Keuntungan Implementasi:
1. **Pengurangan Risiko**: Identifikasi dini peminjam berisiko tinggi
2. **Optimasi Portfolio**: Alokasi kredit yang lebih efektif
3. **Peningkatan Profitabilitas**: Mengurangi kredit macet
4. **Efisiensi Operasional**: Otomasi proses screening awal
5. **Compliance**: Mendukung penerapan manajemen risiko yang terstruktur

### ROI Potensial:
- Pengurangan tingkat gagal bayar
- Peningkatan margin keuntungan bersih
- Efisiensi waktu proses approval

## 👨‍💻 Author

**Muhammad Farkhan Adhitama**  
Data Scientist | ID/X Partners Final Task

*Proyek ini merupakan bagian dari Final Task ID/X Partners untuk posisi Data Scientist*
