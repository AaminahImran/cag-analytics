import os
from bigquery_runner import init_client, run_query

def main():
    """
    Example script demonstrating how to use the bigquery_runner module
    to execute queries and process results.
    """
    # Initialize the BigQuery client
    client = init_client()
    
    # Example query - replace with your actual query
    query = """
    SELECT 
        name, 
        COUNT(*) as count
    FROM 
        `bigquery-public-data.usa_names.usa_1910_current`
    WHERE
        year >= 2000
    GROUP BY 
        name
    ORDER BY 
        count DESC
    LIMIT 10
    """
    
    # Run the query and get results as a DataFrame
    results = run_query(client, query)
    
    # Display the results
    print("Top 10 names since 2000:")
    print(results)
    
    # Example of how to work with the DataFrame
    print("\nTotal occurrences of these names:", results['count'].sum())

if __name__ == "__main__":
    main()
