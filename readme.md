# Airflow DAG: Generate and Anonymize CSV

This project demonstrates an Apache Airflow DAG that generates a CSV file with random data and anonymizes certain fields in the file. The workflow is containerized using Docker, and the setup involves using Docker Compose to run Airflow with Python scripts.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Usage](#setup-and-usage)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create the `requirements.txt`](#2-create-the-requirementstxt)
  - [3. Run Docker Compose](#3-run-docker-compose)
  - [4. Access Airflow Web UI](#4-access-airflow-web-ui)
  - [5. Trigger the DAG](#5-trigger-the-dag)
- [DAG Overview](#dag-overview)
- [License](#license)

## Project Overview
This Airflow DAG consists of two main tasks:
1. **Generate CSV**: Generates a CSV file containing random data using the `Faker` library.
2. **Anonymize CSV**: Anonymizes specific fields (e.g., `first_name`, `last_name`, `address`) in the generated CSV file.

The project is containerized using Docker to ensure easy deployment and repeatability.

## Project Structure
├── airflow/ # Airflow DAGs and configuration 
│ ├── dags/ # DAG folder 
│ │ ├── generate_and_anonymize_dag/ # Directory containing scripts and DAG 
│ │ │ ├── generate_csv.py # Script to generate CSV 
│ │ │ ├── anonymize_csv.py # Script to anonymize CSV 
│ │ │ └── generate_and_anonymize_dag.py # The DAG definition 
├── requirements.txt # Python dependencies (Faker) 
├── docker-compose.yaml # Docker Compose file for Airflow setup 
└── README.md # Project README file


## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Setup and Usage

### 1. Clone the Repository
git clone https://github.com/your-repo/airflow-csv-anonymize.git
cd airflow-csv-anonymize```

### 2. Create the requirements.txt
Ensure that the requirements.txt file contains the following Python dependency:
faker

### 3. Run Docker Compose
Run the following command to start the Airflow instance with Docker:
docker-compose up --build


### 4. Access Airflow Web UI
Once the services are up and running, you can access the Airflow web UI at:
http://localhost:8080
By default, the username is airflow and the password is airflow.

### 5. Trigger the DAG
-In the Airflow web UI, navigate to the DAGs page.
-Find the DAG with the ID generate_and_anonymize_dag.
-Toggle the DAG to "On" and trigger it by clicking the "Trigger DAG" button.
-This will run the DAG, which first generates a CSV file with random data, and then anonymizes specified     fields in the generated CSV file.

## DAG Overview
DAG ID: generate_and_anonymize_dag
This DAG performs the following steps:

#### Task 1: Generate CSV:
Generates a CSV file with 10,000 rows of random data using the Faker library.
The file is saved at /opt/airflow/dags/generate_and_anonymize_dag/fake_data.csv.
Task 2: Anonymize CSV:

#### Task 2: Anonymizes specific fields (first_name, last_name, address) in the CSV file.
The anonymized CSV is saved at /opt/airflow/dags/generate_and_anonymize_dag/anonymized_data.csv.
The DAG does not have a schedule (set to None), but you can modify the schedule interval if you want periodic execution.

## License
This project is licensed under the MIT License.
Copy and paste this block directly into your `README.md` file. Let me know if you need fur

