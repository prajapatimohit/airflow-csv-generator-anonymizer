from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import subprocess

# Step 1: Generate CSV
def generate_csv_task(file_name, num_rows):
    command = [
        'python3', '/opt/airflow/dags/generate_and_anonymize_dag/generate_csv.py',  # Path to the CSV generation script
        '--file', file_name,
        '--rows', str(num_rows)
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"CSV generation failed with error: {result.stderr}")
    print(f"CSV generation output: {result.stdout}")

# Step 2: Anonymize CSV
def anonymize_csv_task(input_file, output_file, fields_to_anonymize, chunk_size=1000):
    command = [
        'python3', '/opt/airflow/dags/generate_and_anonymize_dag/anonymize_csv.py',  # Path to the anonymization script
        '--input',  input_file,
        '--output', output_file,
        '--fields'
    ] + fields_to_anonymize + ['--chunk_size', str(chunk_size)]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"CSV anonymization failed with error: {result.stderr}")
    print(f"CSV anonymization output: {result.stdout}")

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 12),
    'retries': 1
}

# Define the DAG
with DAG(
    dag_id='generate_and_anonymize_dag',
    default_args=default_args,
    schedule_interval=None,  # Set to a cron expression for periodic execution
    catchup=False
) as dag:

    # Task-1 to generate CSV
    generate_csv = PythonOperator(
        task_id='generate_csv',
        python_callable=generate_csv_task,
        op_kwargs={
            'file_name': '/opt/airflow/dags/generate_and_anonymize_dag/fake_data.csv',
            'num_rows': 10000
        }
    )

    # Task-2 to anonymize CSV
    anonymize_csv = PythonOperator(
        task_id='anonymize_csv',
        python_callable=anonymize_csv_task,
        op_kwargs={
            'input_file': '/opt/airflow/dags/generate_and_anonymize_dag/fake_data.csv',
            'output_file': '/opt/airflow/dags/generate_and_anonymize_dag/anonymized_data.csv',
            'fields_to_anonymize': ['first_name', 'last_name', 'address'],
            'chunk_size': 10000
        }
    )

    # Define task dependencies
    generate_csv >> anonymize_csv
