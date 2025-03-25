from google.cloud import bigquery
import pandas as pd

def init_client(project_id: str = "datawarehouse-385707") -> bigquery.Client:
    """Initialize a BigQuery client."""
    return bigquery.Client(project=project_id)

def run_query(client: bigquery.Client, query: str) -> pd.DataFrame:
    """Run a SQL query in BigQuery and return the result as a DataFrame."""
    query_job = client.query(query)
    result = query_job.result()
    return result.to_dataframe()
