import pandas as pd
from cassandra.cluster import Cluster
import uuid
from datetime import datetime

# Connect to Cassandra
def connect_to_cassandra():
    """
    Establish a connection to the Cassandra database.
    Sets the keyspace to 'etl_data'. Replace with your actual keyspace name.
    """
    cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra host
    session = cluster.connect()
    session.set_keyspace('etl_data')  # Replace with your keyspace name
    return session

# Truncate the table to delete all rows
def truncate_table(session, table_name):
    """
    Truncate the specified table to remove all rows.
    Args:
        session: Cassandra session object.
        table_name: Name of the table to truncate.
    """
    truncate_query = f"TRUNCATE {table_name}"
    session.execute(truncate_query)
    print(f"Table {table_name} has been truncated.")

# Insert raw product data
def insert_raw_data(session, data):
    """
    Insert raw product data into the 'products' table.
    Args:
        session: Cassandra session object.
        data: List of dictionaries containing product data.
    """
    # Define the insert query
    insert_query = """
    INSERT INTO products (date, product_id, image, link, metal, price, title)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    # Insert each product record into the table
    for product in data:
        session.execute(insert_query, (
            product['date'],
            product['product_id'],
            product['image'],
            product['link'],
            product['metal'],
            product['price'],
            product['title']
        ))

# Insert statistical data
def insert_stats(session, stats):
    """
    Insert statistical data into the 'stats' table.
    Args:
        session: Cassandra session object.
        stats: List of dictionaries containing statistical data.
    """
    # Define the insert query
    insert_query = """
    INSERT INTO stats (title, date, stat_id, average_price, median_price, max_price, min_price, total)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Insert each statistic record into the table
    for stat in stats:
        session.execute(insert_query, (
            stat['title'],
            stat['date'],
            stat['stat_id'],
            stat['average_price'],
            stat['median_price'],
            stat['max_price'],
            stat['min_price'],
            stat['total_count']
        ))

# Load and prepare products from CSV
def load_data_from_csv(file_path):
    """
    Load product data from a CSV file, add necessary fields, and prepare it for insertion.
    Args:
        file_path: Path to the CSV file containing product data.
    Returns:
        List of dictionaries representing the product data.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Add a unique UUID for each product
    df['product_id'] = [uuid.uuid4() for _ in range(len(df))]

    # Add the current date as the `date` field
    df['date'] = datetime.now().date()

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    return data

# Load and prepare statistics from CSV
def load_stats_from_csv(file_path):
    """
    Load statistical data from a CSV file, add necessary fields, and prepare it for insertion.
    Args:
        file_path: Path to the CSV file containing statistical data.
    Returns:
        List of dictionaries representing the statistical data.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Add a unique UUID for each statistic
    df['stat_id'] = [uuid.uuid4() for _ in range(len(df))]

    # Add the current date as the `date` field
    df['date'] = datetime.now().date()

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    return data

def main():
    """
    Main function to run the ETL pipeline:
    1. Load product and statistical data from CSV files.
    2. Connect to the Cassandra database.
    3. Truncate existing tables.
    4. Insert new data into the database.
    """
    # File path to the processed data CSV
    file_path = 'data/processed/processed_data.csv'  # Path to product data CSV
    stat_path = 'data/processed/statistics.csv'  # Path to statistical data CSV

    # Load data from the CSV files
    data = load_data_from_csv(file_path)
    stats = load_stats_from_csv(stat_path)

    # Connect to Cassandra
    session = connect_to_cassandra()

    # Truncate the tables before inserting new data
    truncate_table(session, 'products')
    truncate_table(session, 'stats')

    # Insert data into the Cassandra tables
    insert_raw_data(session, data)
    insert_stats(session, stats)

    print("Data inserted successfully!")

if __name__ == "__main__":
    main()