# -*- coding: utf-8 -*-
"""Data_Modelling _&_Visualisation_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ezPGcJ-8R19RDItjN432yr-npmxj-uSg
"""

# Necessary imports for preprocessing and machine learning
# Necessary imports for preprocessing and machine learning
!pip install statsmodels
!pip install plotly
!pip install bioinfokit
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer # interpolation for missing values
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import RocCurveDisplay, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import balanced_accuracy_score
import plotly.express as px
from google.colab import drive
drive.mount('/content/drive')
from bioinfokit.analys import stat
from bioinfokit import visuz

#Import the data set:
!pip install ucimlrepo

from ucimlrepo import fetch_ucirepo

# fetch dataset
heart_disease = fetch_ucirepo(id=45)

# data (as pandas dataframes)
X = heart_disease.data.features
y = heart_disease.data.targets

# metadata
print(heart_disease.metadata)

# variable information
print(heart_disease.variables)

X = heart_disease.data.features
y = heart_disease.data.targets

# Combine features and targets into one DataFrame
heart_disease_df = pd.concat([X, y], axis=1)

# Export to CSV
heart_disease_df.to_csv('heart_disease_dataset.csv', index=False)

print("Dataset successfully saved as 'heart_disease_dataset.csv'.")

ls

df=pd.read_csv('heart_disease_dataset.csv')

df.head()

df.tail()

print(df.columns)

df.drop(columns=['cp', 'restecg', 'oldpeak','slope','thal'], inplace=True)

df.to_csv('finalized_data.csv', index=False)

ls

df1=pd.read_csv('finalized_data.csv')
#df1.to_csv('finalized_data.csv', index=False)
#file_path='Desktop/PythonClass/Assignments/finalized_data.csv'
#df1.to_csv(file_path, index=False)
df1.to_csv('/content/drive/MyDrive/finalized_data.csv', index=False)

# Is the dataset balanced?
ax = sns.countplot(data=df1, x='num')

for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline')

plt.show()

# Handle the missing data

columns_list=df1.columns.tolist()
columns_list

#List of categorical variables (dtype == object or category)

categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# List of numerical variables (dtype == int or float)
numerical_cols = df.select_dtypes(include=['number']).columns.tolist()

# Display the lists
print("Categorical columns:", categorical_cols)
print("Numerical columns:", numerical_cols)

## check null values in the numerical column

df1.isnull().sum()

# handle missing value in ca category
df1['ca'].fillna(df1['ca'].mean(), inplace=True)

# confirm whether the value are there or not

df1.isnull().sum()

# Find and remove outliers from the dataset

for cols in numerical_cols:
  plt.figure()
  sns.boxplot(data=df1, x=cols)
  plt.title(f'Boxplot of {cols}')
  plt.show()

# remove outlier from the data frame using IQR method
for col in numerical_cols:
    Q1 = df1[col].quantile(0.25)
    Q3 = df1[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df1 = df1[(df1[col] >= lower_bound) & (df1[col] <= upper_bound)]

# dataframe after removing outliers

for col in numerical_cols:
    Q1 = df1[col].quantile(0.25)
    Q3 = df1[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df1 = df1[(df1[col] >= lower_bound) & (df1[col] <= upper_bound)]

print(df1)

# check outlier using box plot again
for cols in numerical_cols:
  plt.figure()
  sns.boxplot(data=df1, x=cols)
  plt.title(f'Boxplot of {cols}')
  plt.show()

from sklearn.preprocessing import StandardScaler

# Create a StandardScaler object
scaler = StandardScaler()

# Fit the scaler to your data and transform it
df1_standardized = scaler.fit_transform(df1[numerical_cols])

# Create a new DataFrame with the standardized values
df1_standardized = pd.DataFrame(df1_standardized, columns=numerical_cols)

# define the feature

X=df1_standardized.drop(columns=['num'])
y=df1_standardized['num']

# resample using smote
y = y.astype(int)

smote = SMOTE()
X_res, y_res = smote.fit_resample(X,y)

# split into tranining and testing data

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.3, random_state=8)

# Naive Bayes model

nb_model=GaussianNB()
nb_model.fit(X_train, y_train)
y_pred_nb=nb_model.predict(X_test)

# Decison Tree

dt_model=DecisionTreeClassifier()
dt_model.fit(X_train, y_train)
y_pred_dt=dt_model.predict(X_test)

# Random Forest model

rf_model=RandomForestClassifier()
rf_model.fit(X_train, y_train)
y_pred_rf=rf_model.predict(X_test)

# KNN model

knn_moder=KNeighborsClassifier()
knn_moder.fit(X_train, y_train)
y_pred_kn=knn_moder.predict(X_test)

# Evaluation: Confusion Matrix and Metrics

def evaluate_model(y_test, y_pred, model_name):
  print(f"\nModel: {model_name}")
  print("Confusion Matrix:")
  print(confusion_matrix(y_test, y_pred))
  print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.2f}")
 # print(f"Precision: {precision_score(y_test, y_pred):.2f}")
  print(f"Precision: {precision_score(y_test, y_pred, average='weighted', zero_division=0):.2f}")
  print(f"PRecall: {recall_score(y_test, y_pred, average='weighted', zero_division=0):.2f}")
  #print(f"PRecall: {recall_score(y_test, y_pred):.2f}")
  print(f"F1 Score: {f1_score(y_test, y_pred, average='weighted'):.2f}\n")

#Evaluate all models
evaluate_model(y_test, y_pred_nb, "Naive Bayes")
evaluate_model(y_test, y_pred_dt, "Decision Tree")
evaluate_model(y_test, y_pred_rf, "Random Forest")
evaluate_model(y_test, y_pred_kn, "KNN")

#plot confusion matrix using seaborn library
cm1=confusion_matrix(y_test, y_pred_nb)
cm2=confusion_matrix(y_test, y_pred_dt)
cm3=confusion_matrix(y_test, y_pred_rf)
cm4=confusion_matrix(y_test, y_pred_kn)

#confusion matrix for Naive Bayes
sns.heatmap(cm1,annot=True, fmt='d', cmap='YlGnBu')
plt.title('Confusiom Matric for the Naive Bias')
plt.xlabel('Predict')
plt.ylabel('Actual')
plt.show

# accuarcy in traning data for naive bias
print("Accuracy of Naive Bayes for training datatse is:", nb_model.score(X_train, y_train))

# Accuracy in testing data for naive bias
print("Accuracy of Naive Bayes for testing datatse is:", nb_model.score(X_test, y_test))

"""The accuracy of your Naive Bayes model on the training data (0.884) and testing data (0.898) are quite close. This generally suggests that there is no significant overfittin








"""

# confusion matrix for Decision Tree

sns.heatmap(cm2, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Confusion Matrix for Decision Tree')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# confusion matrix for Raqndom Forest
sns.heatmap(cm3, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Confusion Matrix for Random Forest')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# confusion matrix for KNN

sns.heatmap(cm4, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Confusion Matrix for KNN')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Random forest has the best performance. let's all the measures in a report

print(classification_report(y_test, y_pred_rf))

# plot ROC curve for Xtrain

disp =RocCurveDisplay.from_estimator(nb_model, X_train, y_train)
RocCurveDisplay.from_estimator(dt_model, X_train, y_train, ax=disp.ax_)
RocCurveDisplay.from_estimator(rf_model, X_train, y_train, ax=disp.ax_)
RocCurveDisplay.from_estimator(knn_moder, X_train, y_train, ax=disp.ax_)
plt.plot([0,1], [1,0], color='orange', linestyle='--');

# plot ROC curve for Xtest

disp =RocCurveDisplay.from_estimator(nb_model, X_test, y_test)
RocCurveDisplay.from_estimator(dt_model, X_test, y_test, ax=disp.ax_)
RocCurveDisplay.from_estimator(rf_model, X_test, y_test, ax=disp.ax_)
RocCurveDisplay.from_estimator(knn_moder, X_test, y_test, ax=disp.ax_)
plt.plot([0,1], [1,0], color='orange', linestyle='--');

#Make a new prediction for new patients (new observations)

# load new observations (new patients)
new_df = pd.read_csv('/content/drive/MyDrive/new.csv')
new_df=new_df.drop(columns=['num'])
new_df.head()

# use random forest for new data

y_new_rf=rf_model.predict(new_df)
print(y_new_rf)
print('# This shows that new aptinets have number of heart disease as 0')

# find the best value of K in KNN

# create list error[]
error =  []

for i in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    accuracy = balanced_accuracy_score(y_test, pred_i)
    error.append(1-accuracy)

error;

# plot the knn value

plt.figure(figsize=(12, 6))
plt.plot(range(1, 21), error, color='red', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Error')

##coding part for conditional probablity

# Separate features and target variable
X = df1.drop('num', axis=1)  # Assuming 'num' is the target variable (heart disease diagnosis)
y = df1['num']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute missing values with the mean (or you can use 'median', 'most_frequent', etc.)
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Standardize the features (scaling after imputation)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Apply SMOTE to the training data
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

# Check the new balance of the target variable
print("Original dataset shape:", y_train.value_counts())
print("Resampled dataset shape:", pd.Series(y_train_resampled).value_counts())

# Convert resampled data back to a DataFrame
X_train_resampled_df = pd.DataFrame(X_train_resampled, columns=X.columns)  # Use the original feature names
y_train_resampled_df = pd.DataFrame(y_train_resampled, columns=['num'])    # Create a DataFrame for the target

# Combine the resampled features and target into df2
df2 = pd.concat([X_train_resampled_df, y_train_resampled_df], axis=1)

# Assuming you used StandardScaler
X_train_original_scale = scaler.inverse_transform(X_train_resampled)

# Convert back to DataFrame with original column names
X_train_original_scale_df = pd.DataFrame(X_train_original_scale, columns=X.columns)

# Combine resampled features and target
df2 = pd.concat([X_train_original_scale_df, pd.DataFrame(y_train_resampled, columns=['num'])], axis=1)

# Check df2 with original scales
df2.head()

#convert any instances of 1,2,3,4 to 1 and leave instances of 0 to 0
# Convert 'num' column: 0 stays 0, and any value from 1-4 becomes 1
df2['num'] = df2['num'].apply(lambda x: 1 if x > 0 else 0)

# Check the updated column
print(df2['num'].value_counts())

import matplotlib.pyplot as plt

# Plot the value counts of the 'num' column
df2['num'].value_counts().plot(kind='bar', color=['skyblue', 'lightgreen'])

# Add labels and title
plt.title('Distribution of num Column')
plt.xlabel('Values')
plt.ylabel('Count')

# Show the plot
plt.show()

# Separate features (X) and the updated target variable (y)
X = df2.drop('num', axis=1)  # Features
y = df2['num']  # Target

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Convert resampled data back to a DataFrame
df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
df_resampled['num'] = y_resampled  # Add the resampled target back

# Check the new balance of the target variable
print(df_resampled['num'].value_counts())

import matplotlib.pyplot as plt

# Plot the value counts of the resampled 'num' column
df_resampled['num'].value_counts().plot(kind='bar', color=['lightcoral', 'lightskyblue'])

# Add labels and title
plt.title('Distribution of Resampled num Column (After SMOTE)')
plt.xlabel('Values')
plt.ylabel('Count')

# Show the plot
plt.show()

# Overwrite df2 with the resampled data
df2 = pd.DataFrame(X_resampled, columns=X.columns)
df2['num'] = y_resampled  # Add the resampled 'num' column back

# Check the updated df2
print(df2['num'].value_counts())



# Numerator: Count where num = 1 AND fbs = 1
numerator = ((df2['num'] == 1) & (df2['fbs'] == 1.0)).sum()
numerator

# Denominator: Count where fbs > 120 mg/dl
denominator = (df2['sex'] == 1.0).sum()
denominator

probability = numerator / denominator
print(f"P(heart disease = 1 | fast blood sugar = 1) = {probability}")

"""### **Calculate P(heart disease = 1 | fast blood sugar = 1.0)**"""

# Numerator: Count where num = 1 AND fbs = 1
numerator = ((df2['num'] == 1) & (df2['fbs'] == 1.0)).sum()
numerator

# Denominator: Count where fbs > 120 mg/dl
denominator = (df2['sex'] == 1.0).sum()
denominator

robability = numerator / denominator
print(f"P(heart disease = 1 | fast blood sugar = 1) = {probability}")



numerator = ((df2['num'] == 1) & (df2['sex'] == 1)).sum()
numerator

denominator = (df2['sex'] == 1).sum()
denominator

probability = numerator / denominator
probability_percentage = probability * 100

print(f"P(heart disease = 1 | sex = 1) = {probability_percentage}")

"""### **Calculate P(heart disease = 1 | sex = 1)**

In this instance, when sex is equal to 1, it indicates the sex is male

---


"""

numerator = ((df2['num'] == 1) & (df2['sex'] == 0)).sum()
numerator

denominator = (df2['sex'] == 0).sum()
denominator

probability = numerator / denominator
probability_percentage = probability * 100
print(f"P(heart disease = 1 | sex = 0) = {probability_percentage}")

"""### **Calculate P(heart disease = 1 | resting blood pressure > 130)**"""

numerator = ((df2['num'] == 1) & (df2['trestbps'] > 130)).sum()
numerator

denominator = (df2['trestbps'] > 130).sum()
denominator

probability_percentage = probability * 100
print(f"P(heart disease = 1 | resting blood pressure > 130) = {probability_percentage:.2f}%")

"""#**Feature importance using Naïve Bayes**

### Blood Pressure
"""

#Threshold for resting blood pressure
threshold = 130

# Calculate the numerator and denominator for P(heart disease = 1 | trestbps > 130)
numerator_above_threshold = ((df2['num'] == 1) & (df2['trestbps'] > threshold)).sum()
denominator_above_threshold = (df2['trestbps'] > threshold).sum()

# Calculate the conditional probability
if denominator_above_threshold != 0:
    probability_above = numerator_above_threshold / denominator_above_threshold
else:
    probability_above = 0

# Calculate the numerator and denominator for P(heart disease = 1 | trestbps <= 130)
numerator_below_threshold = ((df2['num'] == 1) & (df2['trestbps'] <= threshold)).sum()
denominator_below_threshold = (df2['trestbps'] <= threshold).sum()

if denominator_below_threshold != 0:
    probability_below = numerator_below_threshold / denominator_below_threshold
else:
    probability_below = 0

# Print results as percentages
print(f"P(heart disease = 1 | trestbps > {threshold}) = {probability_above * 100:.2f}%")
print(f"P(heart disease = 1 | trestbps <= {threshold}) = {probability_below * 100:.2f}%")

"""### Cholesterol"""

threshold_chol = 200
numerator_chol_high = ((df2['num'] == 1) & (df2['chol'] > threshold_chol)).sum()
denominator_chol_high = (df2['chol'] > threshold_chol).sum()

if denominator_chol_high != 0:
    probability_chol_high = numerator_chol_high / denominator_chol_high
else:
    probability_chol_high = 0

numerator_chol_low = ((df2['num'] == 1) & (df2['chol'] <= threshold_chol)).sum()
denominator_chol_low = (df2['chol'] <= threshold_chol).sum()

if denominator_chol_low != 0:
    probability_chol_low = numerator_chol_low / denominator_chol_low
else:
    probability_chol_low = 0

print(f"P(heart disease = 1 | chol > {threshold_chol}) = {probability_chol_high * 100:.2f}%")
print(f"P(heart disease = 1 | chol <= {threshold_chol}) = {probability_chol_low * 100:.2f}%")

"""#**Feature importance using Random Forest**"""

X = df2.drop('num', axis=1)  # Drop the target variable 'num'
y = df2['num']  # Target variable

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)
feature_importances = rf_model.feature_importances_

feature_importance_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importances
})

feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
palette = sns.color_palette("husl", len(feature_importance_df))  # "husl" gives a range of colors

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df, palette=palette)
plt.title('Feature Importance using Random Forest')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()

# DATA Visuialization part starts here
df.columns

# Subsetting the DataFrame to include specific columns
# subset_df1 = heart_disease[['age', 'sex', 'trestbps', 'chol', 'fbs', 'thalach', 'exang', 'ca', 'num']]

# Plotting the Pie Chart for 'sex'
# plt.figure(figsize=(6, 6))
# sex_counts = subset_df1['sex'].value_counts()  # Get the value counts for the 'sex' column
# plt.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
# plt.title('Pie Chart of Sex')
# plt.show()

sums = df1['num'].sum()

# plt.figure(figsize=(8, 6))
# plt.pie(sums, labels=sums.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
# plt.title('Percentage Distribution of people having Disease')
# plt.show()

plt.figure(figsize=(8, 6))
plt.pie([sums,303-sums], labels=['Heart Disease','No Heart Disease'], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
plt.title('Distribution ')
plt.show()

# Set title

# Subsetting the DataFrame to include specific columns
# subset_df1 = heart_disease[['age', 'sex', 'trestbps', 'chol', 'fbs', 'thalach', 'exang', 'ca', 'num']]

# Plotting the bar graph for 'sex'
# plt.figure(figsize=(9, 5))
# sex_counts = subset_df1['sex'].value_counts()  # Get the value counts for the 'sex' column
# plt.bar graph(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
# plt.title('Bar graph of Sex')
# plt.show()
sums = df1.sum()

# Scaling down the values to a single-digit range (dividing by a large number like 1000)
scaled_sums = sums / 1000  # Adjust the divisor based on your needs

#Plotting the Bar Graph for the scaled sums
plt.figure(figsize=(9, 5))
plt.bar(scaled_sums.index, scaled_sums.values, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
plt.xlabel('Columns')
plt.ylabel('num ')  # Label indicates scaled values
plt.title('Bar Plot')
plt.xticks(rotation=35)  # Rotate x labels for better readability
plt.grid(axis='y')  # Add grid for better visual clarity
plt.show()

# Subsetting the DataFrame to include specific columns
# subset_df1 = heart_disease[['age', 'sex', 'trestbps', 'chol', 'fbs', 'thalach', 'exang', 'ca', 'num']]

# Plotting the matrix graph for 'sex'
# plt.figure(figsize=(6, 6))
# sex_counts = subset_df1['sex'].value_counts()  # Get the value counts for the 'sex' column
# plt.matrix graph(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
# plt.title('Matrix plot')
# plt.show()

# sums = df1['num'].sum()
plt.figure(figsize=(6, 6))
correlation_matrix = df1.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matrix plot')
plt.show()

# Subsetting the DataFrame to include specific columns
#subset_df1 = heart_disease[['age', 'sex', 'trestbps', 'chol', 'fbs', 'thalach', 'exang', 'ca', 'num']]

# Plotting the histogram for 'sex'
# plt.figure(figsize=(6, 6))
# sex_counts = subset_df1['sex'].value_counts()  # Get the value counts for the 'sex' column
# plt.matrix graph(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
# plt.title('Histrogram')
# plt.show()


# Plotting Histogram for each column in the subset
# sns.histplot(figsize=(12, 10), bins=15, color='#66b3ff', edgecolor='black')

# # Adjust the title for the overall plot
# plt.suptitle('Histogram', fontsize=16)

# # Show the plot
# plt.show()


df_int = df[df['num'] == df['num'].astype(int)]
df_int['num'].hist()
plt.xlabel('Health Disease')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.show()

"""## ***Regression Analysis***"""

def make_box(df, x_var):
    fig = px.box(df,
                 x=x_var
                )
    fig.show()

def make_scatter(df, x_var, y_var):
    fig = px.scatter(df,
                 x=x_var,
                 y=y_var,
                 trendline="ols"
                )
    fig.show()

def remove_outliers_iqr(df, column):
    """Removes outliers from a DataFrame column using the IQR method."""

    # Calculate quantiles and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out outliers
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    return df_filtered

def replace_nulls_median(df, column):
    """Replaces null values in a DataFrame column with the median value."""

    # Calculate median
    median = df[column].median()

    # Replace null values
    df[column] = df[column].fillna(median)

    return df

# fetch dataset
auto_mpg = fetch_ucirepo(id=9)

# data (as pandas dataframes)
X_temp = auto_mpg.data.features
y_temp = auto_mpg.data.targets

# metadata
print(auto_mpg.metadata)

# variable information
print(auto_mpg.variables)

df = pd.concat([X_temp, y_temp], axis=1)
df

"""### ***Data Processing***"""

print(df.isnull().sum())

# Replace null values with median value of column

df = df.copy()
for column in df.columns:
    df = replace_nulls_median(df, column)

print(df.isnull().sum())

# Using box plots to identify outliers in each feature of df

make_box(df, 'displacement')

make_box(df, 'cylinders')

make_box(df, 'horsepower')

make_box(df, 'weight')

make_box(df, 'acceleration')

make_box(df, 'model_year')

make_box(df, 'origin')

make_box(df, 'mpg')

# First pass of custom function to remove outliers of each feature

df_clean = df.copy()
for column in df_clean.columns:
    df_clean = remove_outliers_iqr(df_clean, column)

# Second pass of custom function to remove additional outliers

df_final = df_clean.copy()
for column in df_final.columns:
    df_final = remove_outliers_iqr(df_final, column)

make_box(df_final, 'displacement')

make_box(df_final, 'cylinders')

# Removing additional outliers from Horsepower causes more outliers to appear, so after two rounds of removing outliers it was decided to keep and proceed with the 3 outliers shown

make_box(df_final, 'horsepower')

make_box(df_final, 'weight')

make_box(df_final, 'acceleration')

make_box(df_final, 'model_year')

make_box(df_final, 'origin')

make_box(df_final, 'mpg')

"""# Data Analysis (Descriptive Statistics and Regression Analysis)"""

df_final.describe()

X = df_final.drop('mpg', axis=1)
y = df_final['mpg']

Xtrain, Xtest, ytrain, ytest = train_test_split (X, y, test_size=0.3, random_state=0)

# Initial regression results summary

import statsmodels.api as sm

X = sm.add_constant(X)

reg = sm.OLS(y, X).fit()
reg.summary()

# Final multivariate regression results
# Displacement, cylinders, and acceleration columns had P>0.05 so I dropped those column and reouput the regression training, testing, and summary

X_new = X.drop(['displacement','cylinders', 'acceleration'], axis=1, inplace=False)

Xtrain, Xtest, ytrain, ytest = train_test_split (X_new, y, test_size=0.3, random_state=0)

X_new = sm.add_constant(X_new)

reg = sm.OLS(y, X_new).fit()
reg.summary()

"""# Regression Equation of Final Multivariate Regression Model

y = -0.028(x1) - 0.006(x2) + -.73(x3) + 0.988(x4) - 14.423

# Interpretation of Model

Based on the R-squared value of 0.817 and the Adjusted R-squared value of 0.815, this model can performs well and consistently when predicting MPG. I would This level of permormance is realistic. The equation shows that horsepower and weight have a negative relationship with MPS, so as they increase, MPG will likewise decrease. Model Year and Origin on the other hand have a positive relationship with MPG, so as they increase, MPG also increases.

"""

X_new.describe()

df_remerged = pd.concat([X_new, y], axis=1)
df_remerged

make_scatter(df_remerged, 'horsepower', 'mpg')

make_scatter(df_remerged, 'weight', 'mpg')

make_scatter(df_remerged, 'model_year', 'mpg')

make_scatter(df_remerged, 'origin', 'mpg')

"""# Heatmaps That Show the Correlation Between Features"""

df_final.corr()

# Triangle heatmap that shows correlation between all features

plt.figure(figsize=(16, 6))
# define the mask to set the values in the upper triangle to True
mask = np.triu(np.ones_like(df_final.corr(), dtype=bool))
heatmap = sns.heatmap(df_final.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Triangle Correlation Heatmap', fontdict={'fontsize':18}, pad=16);

plt.figure(figsize=(8, 12))
heatmap = sns.heatmap(df_final.corr()[['mpg']].sort_values(by='mpg', ascending=False), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Features Correlating with MPG', fontdict={'fontsize':18}, pad=16);

X_hp = X_new['horsepower']
X_w = X_new['weight']
X_my = X_new['model_year']

X_w = sm.add_constant(X_w)

reg = sm.OLS(y, X_w).fit()
reg.summary()

"""# Regression Model Equation for Weight

y = -0.008(x) + 46.426

# Interpretation of Model

Based on the R-squared value of 0.674 and the Adjusted R-squared value of 0.673, this model does a reasonable but imperfect job of predicting MPG. It is the independent feature that best predicts MPG, but it still performs worse the multivariate model.
"""

res= stat()
res.reg_metric(y=np.array(y), yhat=np.array(reg.predict(X_w)), resid=np.array(reg.resid))
res.reg_metric_df

X_my = sm.add_constant(X_my)

reg = sm.OLS(y, X_my).fit()
reg.summary()

"""# Regression Model Equation for Model Year

y = 0.091(x) + 57.328

# Interpretation of Model

An R-squared value of 0.274 and an Adjusted R-squared value of 0.272 indicates that model year on its own is not a very good feature to use to predict MPG.
"""

res= stat()

res.reg_metric(y=np.array(y), yhat=np.array(reg.predict(sm.add_constant(X_my))), resid=np.array(reg.resid))
res.reg_metric_df

"""# Visualizing Feature Relationships with Line Charts"""

fig = px.line(df_remerged.groupby('model_year')['mpg'].mean().reset_index(),
             x='model_year',
             y='mpg',
             title = 'Average MPG by Model Year'
            )
fig.show()

fig = px.line(X_new.groupby('model_year')['horsepower'].mean().reset_index(),
             x='model_year',
             y='horsepower',
             title='Average Horsepower by Model Year'
             )
fig.show()

fig = px.line(df_remerged.groupby('model_year')['weight'].mean().reset_index(),
             x='model_year',
             y='weight',
             title = 'Average Weight by Model Year'
            )
fig.show()
