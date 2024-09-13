from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import subprocess
import json
import logging
import re  # Added to sanitize task IDs

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load dynamic config from an external source (e.g., JSON file, database)
def load_config():
    config_file_path = '/opt/airflow/dags/generate_and_anonymize_dag/config.json'
    
    logger.info(f"Loading config from {config_file_path}")
    
    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        logger.info("Config loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise
    return config
    print(config)

# Sanitize task ID to remove invalid characters
def sanitize_task_id(file_name):
    # Replace any characters that are not alphanumeric, dash, dot, or underscore with underscore
    return re.sub(r'[^a-zA-Z0-9._-]', '_', file_name)

# Step 1: Generate CSV
def generate_csv_task(file_name, num_rows):
    logger.info(f"Starting CSV generation: file_name={file_name}, num_rows={num_rows}")
    
    command = [
        'python3', '/opt/airflow/dags/generate_and_anonymize_dag/generate_csv.py',
        '--file', file_name,
        '--rows', str(num_rows)
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"CSV generation failed with error: {result.stderr}")
            raise Exception(f"CSV generation failed: {result.stderr}")
        logger.info(f"CSV generation output: {result.stdout}")
    except Exception as e:
        logger.error(f"Error during CSV generation: {e}")
        raise

# Step 2: Anonymize CSV
def anonymize_csv_task(input_file, output_file, fields_to_anonymize, chunk_size=1000):
    logger.info(f"Starting CSV anonymization: input_file={input_file}, output_file={output_file}, fields={fields_to_anonymize}, chunk_size={chunk_size}")
    
    command = [
        'python3', '/opt/airflow/dags/generate_and_anonymize_dag/anonymize_csv.py',
        '--input',  input_file,
        '--output', output_file,
        '--fields'
    ] + fields_to_anonymize + ['--chunk_size', str(chunk_size)]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"CSV anonymization failed with error: {result.stderr}")
            raise Exception(f"CSV anonymization failed: {result.stderr}")
        logger.info(f"CSV anonymization output: {result.stdout}")
    except Exception as e:
        logger.error(f"Error during CSV anonymization: {e}")
        raise

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 12),
    'retries': 1
}

# Function to dynamically create the DAG
def create_dynamic_dag(dag_id, config):
    logger.info(f"Creating dynamic DAG with ID: {dag_id}")
    
    with DAG(
        dag_id=dag_id,
        default_args=default_args,
        schedule_interval=None,
        catchup=False
    ) as dag:
        task_dependencies = []
        
        for csv_config in config['csv_files']:
            sanitized_file_name = sanitize_task_id(csv_config['file_name'])
            
            logger.info(f"Creating tasks for file: {csv_config['file_name']}")
            
            # Task-1 to generate CSV
            generate_csv = PythonOperator(
                task_id=f'generate_csv_{sanitized_file_name}',
                python_callable=generate_csv_task,
                op_kwargs={
                    'file_name': csv_config['file_name'],
                    'num_rows': csv_config['num_rows']
                }
            )
            
            # Task-2 to anonymize CSV
            anonymize_csv = PythonOperator(
                task_id=f'anonymize_csv_{sanitized_file_name}',
                python_callable=anonymize_csv_task,
                op_kwargs={
                    'input_file': csv_config['file_name'],
                    'output_file': csv_config['anonymized_file_name'],
                    'fields_to_anonymize': csv_config['fields_to_anonymize'],
                    'chunk_size': csv_config['chunk_size']
                }
            )
            
            # Define task dependencies
            generate_csv >> anonymize_csv
            task_dependencies.append(anonymize_csv)
    
    logger.info(f"DAG {dag_id} created successfully")
    return dag

# Load dynamic config
config = load_config()

# Create the dynamic DAG
dag_id = 'generate_and_anonymize_dynamic_dag'
globals()[dag_id] = create_dynamic_dag(dag_id, config)
