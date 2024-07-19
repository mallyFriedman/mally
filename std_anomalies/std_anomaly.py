import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import os

# Load the CSV file
df = pd.read_csv(r"C:\Users\USER\Desktop\עבודה\בנימיני\אנומליות\stb_temp report.csv")

# Convert the 'date_created' column to datetime format
df['date_created'] = pd.to_datetime(df['date_created'], format='%Y-%m-%d')

# Define the date ranges
end_date = df['date_created'].max()
yesterday = end_date - timedelta(days=1)
start_date_4w = (end_date - timedelta(days=1)) - timedelta(weeks=4)
start_date_2w = (end_date - timedelta(days=1)) - timedelta(weeks=2)
start_date_1w = (end_date - timedelta(days=1)) - timedelta(weeks=1)
start_date_4d = [(yesterday - timedelta(days=7)) - timedelta(weeks=i) for i in range(4)]

dimensions = ['funding_source', 'payout_type', 'receive_currency', 'transaction_status', 'currency', 'transaction_type', 'transaction_origin', 'operator_alias', 'compliance_status', 'processing_agent_name', 'sender_city', 'sender_country', 'payment_status']  # Add your other dimensions here

# Function to detect anomalies
def detect_anomalies(data, dimension, check_date, start_date_4w, start_date_2w, start_date_1w, start_date_4d):
    daily_counts = data.groupby([dimension, 'date_created']).size().reset_index(name='count')
    daily_amounts = data.groupby([dimension, 'date_created'])['amount'].sum().reset_index(name='amount')

    def detect(data, value, metric):
        value_data = data[data[dimension] == value].copy()

        data_4w = value_data[(value_data['date_created'] >= start_date_4w) & (value_data['date_created'] < check_date)]
        data_2w = value_data[(value_data['date_created'] >= start_date_2w) & (value_data['date_created'] < check_date)]
        data_1w = value_data[(value_data['date_created'] >= start_date_1w) & (value_data['date_created'] < check_date)]
        data_4d = value_data[value_data['date_created'].isin(start_date_4d)]
        data_check_date = value_data[value_data['date_created'] == check_date]

        if data_check_date.empty or len(data_1w) < 2 or len(data_4w) < 2 or len(data_4d) < 2:
            return None  # Skip if there's no data for the check date or insufficient historical data

        def safe_std(series):
            std_dev = series.std()
            epsilon = 1e-10
            return std_dev if std_dev != 0 else epsilon

        def calculate_statistics(data, metric):
            size = data['date_created'].nunique()
            total_value = data[metric].sum()
            avg = total_value / size
            std_dev = safe_std(data[metric])
            return avg, std_dev

        avg_1w, std_dev_1w = calculate_statistics(data_1w, metric)
        avg_2w, std_dev_2w = calculate_statistics(data_2w, metric)
        avg_4w, std_dev_4w = calculate_statistics(data_4w, metric)
        avg_4d, std_dev_4d = calculate_statistics(data_4d, metric)

        check_date_value = data_check_date[metric].sum()
        std_ratio_1w = abs(check_date_value - avg_1w) / std_dev_1w
        std_ratio_2w = abs(check_date_value - avg_2w) / std_dev_2w
        std_ratio_4w = abs(check_date_value - avg_4w) / std_dev_4w
        std_ratio_4d = abs(check_date_value - avg_4d) / std_dev_4d

        results = {
            std_ratio_1w: (avg_1w, std_dev_1w),
            std_ratio_2w: (avg_2w, std_dev_2w),
            std_ratio_4w: (avg_4w, std_dev_4w),
            std_ratio_4d: (avg_4d, std_dev_4d)
        }

        max_std_ratio = max(results.keys())
        avg, std_deviation = results[max_std_ratio]

        upper_bound = avg + 2 * std_deviation
        lower_bound = avg - 2 * std_deviation

        if (std_ratio_1w > 2 and std_ratio_2w > 2 and std_ratio_4w > 2 and std_ratio_4d > 2):
            return {
                'dimension': dimension,
                'name': value,
                'date_of_anomaly': check_date,
                'check_date_value': check_date_value,
                #'avg_1w': avg_1w,
                #'avg_2w': avg_2w,
                #'avg_4w': avg_4w,
                #'avg_4d': avg_4d,
                #'std_1w': std_dev_1w,
                #'std_2w': std_dev_2w,
                #'std_4w': std_dev_4w,
                #'std_4d': std_dev_4d,
                'upper_bound': upper_bound,
                'lower_bound': lower_bound,
                'type': metric
            }
        return None

    anomalies = []
    for value in daily_counts[dimension].unique():
        count_anomaly = detect(daily_counts, value, 'count')
        amount_anomaly = detect(daily_amounts, value, 'amount')

        if count_anomaly:
            anomalies.append(count_anomaly)
        if amount_anomaly:
            anomalies.append(amount_anomaly)

    return anomalies

all_anomalies = []
for delta in range(1, 29):
    check_date = end_date - timedelta(days=delta)
    start_date_4w = check_date - timedelta(weeks=4)
    start_date_2w = check_date - timedelta(weeks=2)
    start_date_1w = check_date - timedelta(weeks=1)
    start_date_4d = [(check_date - timedelta(days=7)) - timedelta(weeks=i) for i in range(4)]

    for dimension in dimensions:
        anomalies = detect_anomalies(df, dimension, check_date, start_date_4w, start_date_2w, start_date_1w, start_date_4d)
        all_anomalies.extend(anomalies)

# Save anomalies to a CSV file
anomalies_df = pd.DataFrame(all_anomalies)
csv_file_path = "C:\\Users\\USER\\Desktop\\עבודה\\בנימיני\\אנומליות\\anomalies.csv"
anomalies_df.to_csv(csv_file_path, index=False)