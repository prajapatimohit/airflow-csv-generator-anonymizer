from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
import subprocess

# Define the command to run the Python script
def run_parsing_script(spec_file, input_file, output_file):
    command = [
        'python3', '/opt/airflow/dags/parsing_dag/fixed_width_parser.py',  # Adjust the path to your script location
        '--spec', spec_file,
        '--input_file', input_file,
        '--output_file', output_file
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    
    print(f"Script output: {result.stdout}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='parse_fixed_width_to_csv',
    default_args=default_args,
    start_date=datetime(2023, 9, 11),
    schedule_interval=None,  # Set to a cron expression for periodic execution
    catchup=False,
) as dag:

    # Task to run the Python script
    parse_fixed_width_task = PythonOperator(
        task_id='parse_fixed_width',
        python_callable=run_parsing_script,
        op_kwargs={
            'spec_file': '/opt/airflow/dags/parsing_dag/spec.json',  # Update with the path to your spec.json
            'input_file': '/opt/airflow/dags/parsing_dag/input_file.txt',  # Update with the path to your input fixed-width file
            'output_file': '/opt/airflow/dags/parsing_dag/output_file.csv'  # Update with the desired output CSV path
        }
    )

    parse_fixed_width_task
