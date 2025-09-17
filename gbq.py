# Google BigQuery Python Access Examples
# Install required packages: pip install google-cloud-bigquery pandas

from google.cloud import bigquery
import pandas as pd
import os
from google.oauth2 import service_account

# Method 1: Using Application Default Credentials (ADC)
# Set up authentication by running: gcloud auth application-default login
def connect_with_adc():
    """Connect using Application Default Credentials"""
    client = bigquery.Client()
    return client

# Method 2: Using Service Account Key File
def connect_with_service_account(key_path):
    """Connect using service account JSON key file"""
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client

# Method 3: Using Service Account Key from Environment Variable
def connect_with_env_credentials():
    """Connect using service account key stored in environment variable"""
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to path of your JSON key
    client = bigquery.Client()
    return client

# Basic query execution
def run_query(client, query):
    """Execute a SQL query and return results as DataFrame"""
    try:
        # Run the query
        query_job = client.query(query)
        
        # Convert results to pandas DataFrame
        df = query_job.to_dataframe()
        
        print(f"Query completed. Retrieved {len(df)} rows.")
        return df
    
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

# Example queries
def example_queries():
    """Example BigQuery SQL queries"""
    
    # Query public dataset
    public_query = """
    SELECT 
        name, 
        COUNT(*) as count
    FROM `bigquery-public-data.usa_names.usa_1910_2013` 
    WHERE state = 'CA' 
    GROUP BY name 
    ORDER BY count DESC 
    LIMIT 10
    """
    
    # Query your own dataset (replace with your project/dataset/table)
    custom_query = """
    SELECT 
        column1,
        column2,
        COUNT(*) as record_count
    FROM `your-project-id.your_dataset.your_table`
    WHERE date_column >= '2024-01-01'
    GROUP BY column1, column2
    ORDER BY record_count DESC
    LIMIT 100
    """
    
    return public_query, custom_query

# Advanced: Query with parameters
def parameterized_query(client, start_date, end_date, state):
    """Execute parameterized query for better security and reusability"""
    
    query = """
    SELECT 
        name,
        number,
        year
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = @state
        AND year BETWEEN @start_year AND @end_year
    ORDER BY number DESC
    LIMIT 20
    """
    
    # Configure query parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("state", "STRING", state),
            bigquery.ScalarQueryParameter("start_year", "INT64", start_date),
            bigquery.ScalarQueryParameter("end_year", "INT64", end_date),
        ]
    )
    
    query_job = client.query(query, job_config=job_config)
    return query_job.to_dataframe()

# Upload DataFrame to BigQuery
def upload_dataframe_to_bq(client, df, table_id):
    """Upload a pandas DataFrame to BigQuery table"""
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Overwrite table
        # write_disposition="WRITE_APPEND",  # Append to table
    )
    
    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for job to complete
        
        print(f"Loaded {len(df)} rows into {table_id}")
        
    except Exception as e:
        print(f"Error uploading data: {e}")

# List datasets and tables
def explore_bigquery_resources(client):
    """List available datasets and tables"""
    
    # List datasets
    datasets = list(client.list_datasets())
    print("Available datasets:")
    for dataset in datasets:
        print(f"  - {dataset.dataset_id}")
    
    # List tables in a specific dataset (replace with your dataset)
    if datasets:
        dataset_id = datasets[0].dataset_id
        tables = list(client.list_tables(dataset_id))
        print(f"\nTables in {dataset_id}:")
        for table in tables:
            print(f"  - {table.table_id}")

# Main execution example
def main():
    """Main function demonstrating BigQuery usage"""
    
    # Choose authentication method
    # Option 1: Use ADC (recommended for development)
    client = connect_with_adc()
    
    # Option 2: Use service account key file
    # client = connect_with_service_account('path/to/your/service-account-key.json')
    
    # Get example queries
    public_query, custom_query = example_queries()
    
    # Execute public dataset query
    print("Running public dataset query...")
    df_public = run_query(client, public_query)
    if df_public is not None:
        print(df_public.head())
    
    # Execute parameterized query
    print("\nRunning parameterized query...")
    df_param = parameterized_query(client, 2010, 2013, 'NY')
    print(df_param.head())
    
    # Explore available resources
    print("\nExploring BigQuery resources...")
    explore_bigquery_resources(client)
    
    # Example: Create and upload sample data
    sample_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'value': [10.5, 20.3, 15.7, 8.9, 12.1],
        'date': pd.date_range('2024-01-01', periods=5)
    })
    
    # Uncomment to upload (replace with your table ID)
    # table_id = "your-project-id.your_dataset.sample_table"
    # upload_dataframe_to_bq(client, sample_data, table_id)

if __name__ == "__main__":
    main()