
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

def simulate_sensor_data(days=10, freq='H'):
    timestamps = pd.date_range(end=datetime.now(), periods=24*days, freq=freq)
    data = pd.DataFrame({
        'timestamp': timestamps,
        'temperature': np.random.normal(30, 5, size=len(timestamps)),
        'humidity': np.random.normal(60, 10, size=len(timestamps)),
        'pressure': np.random.normal(1010, 5, size=len(timestamps)),
        'rainfall': np.random.choice([0, 0.2, 0.5, 1.0, 2.0], size=len(timestamps), p=[0.6, 0.2, 0.1, 0.05, 0.05])
    })
    return data

def save_data(data, path="data/simulated_weather_data.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data.to_csv(path, index=False)

def load_data(path="data/simulated_weather_data.csv"):
    return pd.read_csv(path, parse_dates=['timestamp'])

def plot_trends(df):
    sns.set(style="darkgrid")
    plt.figure(figsize=(12, 8))
    sns.lineplot(x='timestamp', y='temperature', data=df, label='Temperature')
    sns.lineplot(x='timestamp', y='humidity', data=df, label='Humidity')
    sns.lineplot(x='timestamp', y='pressure', data=df, label='Pressure')
    plt.title('Weather Trends Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Sensor Values')
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs("images", exist_ok=True)
    plt.savefig("images/trend_plot.png")
    plt.show()

def trigger_alerts(df):
    alerts = []
    for _, row in df.iterrows():
        if row['temperature'] > 40:
            alerts.append(f"[ALERT] High temperature: {row['temperature']}°C at {row['timestamp']}")
        if row['humidity'] < 30:
            alerts.append(f"[ALERT] Low humidity: {row['humidity']}% at {row['timestamp']}")
        if row['rainfall'] > 1.0:
            alerts.append(f"[ALERT] Heavy rainfall: {row['rainfall']}mm at {row['timestamp']}")
    return alerts

def main():
    print("[INFO] Simulating weather sensor data...")
    data = simulate_sensor_data()
    save_data(data)

    print("[INFO] Loading data and visualizing trends...")
    df = load_data()
    plot_trends(df)

    print("[INFO] Checking for weather alerts...")
    alerts = trigger_alerts(df)
    if alerts:
        print("\n".join(alerts))
    else:
        print("No alerts triggered.")

if __name__ == "__main__":
    main()
