import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Load and prepare data
data = pd.read_csv('inventory_data.csv')

# Define features
input_features = [
    'buffer_level', 'produced_goods_level', 'demand', 'fulfilled_demand',
    'lead_time', 'inventory_max_capacity', 'inventory_position', 
    'inventory_on_hand', 'm1_max_production_rate', 'm1_mttf', 'm1_mttr',
    'm1_defect_rate', 'm2_max_production_rate', 'm2_mttf', 'm2_mttr',
    'm2_defect_rate', 'buffer_max_capacity', 'produced_goods_max_capacity'
]

output_features = [
    'm1_production', 'm2_production', 'reorder_point', 
    'reorder_quantity', 'm1_downtime', 'm2_downtime'
]

X = data[input_features]
Y = data[output_features]

# Split data with temporal consideration
train_size = int(len(data) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
Y_train, Y_test = Y[:train_size], Y[train_size:]

# Normalize data
x_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()

X_train_scaled = x_scaler.fit_transform(X_train)
X_test_scaled = x_scaler.transform(X_test)
Y_train_scaled = y_scaler.fit_transform(Y_train)
Y_test_scaled = y_scaler.transform(Y_test)

# Create sequence data
def create_sequences(X, y, time_steps=10):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps)])
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 10
X_train_seq, Y_train_seq = create_sequences(X_train_scaled, Y_train_scaled, time_steps)
X_test_seq, Y_test_seq = create_sequences(X_test_scaled, Y_test_scaled, time_steps)

# Define custom loss function correctly
def custom_loss(y_true, y_pred):
    mse = tf.reduce_mean(tf.square(y_true - y_pred))
    mae = tf.reduce_mean(tf.abs(y_true - y_pred))
    return 0.7 * mse + 0.3 * mae

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(128, return_sequences=True, 
                        input_shape=(time_steps, X_train.shape[1])),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(Y_train.shape[1])
])

# Compile model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=custom_loss,
    metrics=['mae', 'mse']
)

# Callbacks
callbacks = [
    EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=0.00001
    )
]

# Train model
history = model.fit(
    X_train_seq, Y_train_seq,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=callbacks,
    verbose=1
)

# Evaluate and predict
Y_pred_scaled = model.predict(X_test_seq)
Y_pred = y_scaler.inverse_transform(Y_pred_scaled)
Y_test_actual = y_scaler.inverse_transform(Y_test_seq)

# Calculate metrics
for i, feature in enumerate(output_features):
    mae = np.mean(np.abs(Y_pred[:, i] - Y_test_actual[:, i]))
    mse = np.mean((Y_pred[:, i] - Y_test_actual[:, i])**2)
    print(f'{feature} - MAE: {mae:.4f}, MSE: {mse:.4f}')

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss Over Time')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('training_results.png')
plt.close()

# Save model
model.save('inventory_lstm_model.keras')