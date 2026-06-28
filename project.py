import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv('iris.csv')
# print(df)
le = LabelEncoder()
df['Species'] = le.fit_transform(df['Species'])
# print(df)
x = df.drop('Species', axis= 1)
y = df['Species']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=42)
lr = LogisticRegression(max_iter=1000)
lr.fit(x_train, y_train)
models = {'logistic_regression': lr}
for name, model in models.items():
    y_pred = model.predict(x)
    print('accuracy: ', accuracy_score(y, y_pred))
    y_pred = model.predict(x_test)
    print("Test Accuracy:", accuracy_score(y_test, y_pred))