import quandl,math
import pickle
import matplotlib.pyplot as plt
from sklearn import  preprocessing , svm
import datetime
from sklearn.model_selection import  train_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib import style
style.use('ggplot')
df = quandl.get('WIKI/GOOGL')
df = df[['Adj. Open' , 'Adj. High' , 'Adj. Low' , 'Adj. Volume' , 'Adj. Close']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close' , 'Adj. Volume' , 'HL_PCT' , 'PCT_change']]
df.fillna(-99999 , inplace=True)
forecast_col = 'Adj. Close'
forecast_out = int(math.ceil(0.01*len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)
X = np.array(df.drop(['label'] , 1))
X= preprocessing.scale(X)
X =  X[:-forecast_out]
X_lately = X[-forecast_out:]
df.dropna(inplace=True)
y = np.array(df['label'])
#once the pickle is saved you can just ignore the lines 27-32 and use our trained classifier
X_train , X_test , y_train , y_test = train_test_split(X,y , test_size = 0.2)
clf = LinearRegression(n_jobs= -1)
clf.fit(X_train , y_train)
with open('LinearRegression.pickle' , 'wb') as f:
    pickle.dump(clf, f)
pickle_in = open('LinearRegression.pickle' , 'rb')
clf = pickle.load(pickle_in)
accuracylinearregression = clf.score(X_test , y_test)
#print(accuracylinearregression)
#TRIED SVM BUT GOT AN ACCURACY OF ABOUT 70% IT has to do with the high variance of the dataset.
#clf = svm.SVR()
#clf.fit(X_train , y_train)
#accuracysvm = clf.score(X_test , y_test)
#print(accuracysvm)
forecast_set = clf.predict(X_lately)
print(forecast_set , accuracylinearregression , forecast_out)
df['Forecast'] = np.nan
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day
for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns) - 1 )] + [i] 
df['Adj. Close'].plot()
df['Forecast'].plot()
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
