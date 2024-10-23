import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('test_factory_data.csv')

# Define input and output features
X = data[['Vibration_Level', 'Temperature', 'Production_Rate', 'Inventory_Level', 'Energy_Consumption', 'Defect_Rate']]
Y = data[['Machine_Status', 'Production_Rate', 'Inventory_Level', 'Energy_Consumption', 'Defect_Rate', 'Downtime']]

# Split the dataset into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# Normalize the input features
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the neural network architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),  # Input layer
    tf.keras.layers.Dense(64, activation='relu'),  # First hidden layer
    tf.keras.layers.Dense(32, activation='relu'),  # Second hidden layer
    tf.keras.layers.Dense(Y_train.shape[1])  # Output layer
])

# Specify training options
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mse', metrics=["mae"])  # Mean squared error for regression

# Train the neural network
history = model.fit(
    X_train,
    Y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test, Y_test),
    validation_freq=10  # Validate every 10 epochs
)

# Make predictions on the test data
Y_pred = model.predict(X_test)

# Calculate the performance metrics (Mean Absolute Error)
mae_values = {}
for i, target in enumerate(Y.columns):
    mae = tf.keras.metrics.MeanAbsoluteError()(Y_test.iloc[:, i], Y_pred[:, i]).numpy()
    mae_values[target] = mae


# Display the results
for target, mae in mae_values.items():
    print(f'Mean Absolute Error for {target}: {mae}')

# Plotting the training and validation loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')

plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# plt.show()
# Save the plottable figure in an imaage file
plt.savefig('training_validation_loss.png')  # Save the plot as an image file
