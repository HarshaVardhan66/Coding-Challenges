from flask import Flask, render_template, request, redirect
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import mean_squared_error


app = Flask('__main__')
real_price = None
predict_price = None
company_name = None

@app.route('/')
def home():
    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def predict():
	comp_name = request.form['company']
	global predict_price, company_name, real_price
	if comp_name == 'Google':
		dataset_train=pd.read_csv("Google_Stock_Price_Train.csv")

		train_set=dataset_train.iloc[:,1:2].values

		# # DATA PREPROCESSING 


		sc= MinMaxScaler()
		#fit=sc.fit(train_set)
		scaled_training=sc.fit_transform(train_set)


		x_train=[]
		y_train=[]

		for i in range(60,1258):
			x_train.append(scaled_training[i-60:i,0])
			y_train.append(scaled_training[i,0])


		x_train,y_train=np.array(x_train),np.array(y_train)

		x_train= np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))


		# # DEFINING LSTM RECURRENT MODEL  


		model= Sequential()


		model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
		model.add(Dropout(0.2))


		model.add(LSTM(units=50, return_sequences=True))
		model.add(Dropout(0.2))


		model.add(LSTM(units=50, return_sequences=True))
		model.add(Dropout(0.2))


		model.add(LSTM(units=50))
		model.add(Dropout(0.2))


		# ## COMPILING AND FITTING THE MODEL

		model.add(Dense(units = 1))
		model.compile(optimizer = 'adam', loss = 'mean_squared_error')


		gui=model.fit(x_train, y_train, epochs = 100, batch_size = 32)


		# ## FETCHING THE TEST DATA AND PREPROCESSING

		dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
		real_stock_price = dataset_test.iloc[:, 1:2].values


		dataset_total = pd.concat(( dataset_train['Open'], dataset_test['Open']), axis = 0)
		inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
		inputs = inputs.reshape(-1,1)
		inputs = sc.transform(inputs)


		X_test = []


		for i in range(60, 80):
			X_test.append(inputs[i-60:i, 0])
		X_test = np.array(X_test)
		X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


		predicted_stock_price = model.predict(X_test)


		predicted_stock_price = sc.inverse_transform(predicted_stock_price)

		real_price = real_stock_price
		predict_price = predicted_stock_price
		company_name = "Google"

		

		rmse = math.sqrt(mean_squared_error(real_stock_price, predicted_stock_price))
		print(rmse)


	else:
		dataset_train=pd.read_csv("NSE-TATAGLOBAL.csv")

		train_set=dataset_train.iloc[:,1:2].values


		# # DATA PREPROCESSING 

		sc= MinMaxScaler()
		fit=sc.fit(train_set)
		scaled_training=sc.fit_transform(train_set)


		print(len(train_set))


		x_train=[]
		y_train=[]

		for i in range(60,2035):
		    x_train.append(scaled_training[i-60:i,0])
		    y_train.append(scaled_training[i,0])


		x_train,y_train=np.array(x_train),np.array(y_train)

		x_train= np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))


		# # DEFINING LSTM RECURRENT MODEL  

		model= Sequential()


		model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
		model.add(Dropout(0.2))


		model.add(LSTM(units=50, return_sequences=True))
		model.add(Dropout(0.2))


		model.add(LSTM(units=50, return_sequences=True))
		model.add(Dropout(0.2))


		model.add(LSTM(units=50))
		model.add(Dropout(0.2))


		# ## COMPILING AND FITTING THE MODEL

		model.add(Dense(units = 1))
		model.compile(optimizer = 'adam', loss = 'mean_squared_error')


		model.fit(x_train, y_train, epochs = 100, batch_size = 32)


		# ## FETCHING THE TEST DATA AND PREPROCESSING


		dataset_test=pd.read_csv("tatatest.csv")
		real_stock_price = dataset_test.iloc[:, 1:2].values


		dataset_total = pd.concat(( dataset_train['Open'], dataset_test['Open']), axis = 0)
		inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
		inputs = inputs.reshape(-1,1)
		inputs = sc.transform(inputs)


		X_test = []


		for i in range(60,76):
		    X_test.append(inputs[i-60:i, 0])
		X_test = np.array(X_test)
		X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


		# ## MAKING PREDICTIONS ON TEST DATA

		predicted_stock_price = model.predict(X_test)


		predicted_stock_price = sc.inverse_transform(predicted_stock_price)


		# ## VISUALIZING THE PREDICTION

		real_price = real_stock_price
		predict_price = predicted_stock_price
		company_name = "tata"

		rmse = math.sqrt(mean_squared_error(real_stock_price, predicted_stock_price))

	return render_template('predict_result.html', rmse=rmse)


@app.route('/show')
def show():
	if company_name == "Google":
		plt.plot(real_price, color = 'red', label = 'Real Google Stock Price')
		plt.plot(predict_price, color = 'blue', label = 'Predicted Google Stock Price')
		plt.title('Google Stock Price Prediction')
		plt.xlabel('Time')
		plt.ylabel('Google Stock Price')
		plt.legend()
		plt.show()
		
	else:
		plt.plot(real_price, color = 'red', label = 'Taata Stock Price')
		plt.plot(predict_price, color = 'blue', label = 'Predicted TAT Stock Price')
		plt.title('Tata Price Prediction')
		plt.xlabel('Time')
		plt.ylabel('Tata Stock Price')
		plt.legend()
		plt.show()

    
	return redirect('http://127.0.0.1:5000/')


if __name__ == '__main__':
    app.run(debug=True)
