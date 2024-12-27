import pandas as pd
import requests
import json
from pathlib import Path
import logging
import os

# Fetch data from the API
url = 'http://localhost:3000/api/raw'

try:
    # Request data from the API
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    data = response.json()      # Parse the JSON response

    # Ensure the directory for raw data exists
    os.makedirs('./data/raw', exist_ok=True)

    # Save the raw data to a JSON file
    json_file = './data/raw/raw_data.json'
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)  # Write JSON data with indentation for readability

    print(f"Data has been saved to {json_file}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# Configure logging to track the process
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, input_file: str, output_dir: str):
        """
        Initialize the data processor.
        Args:
            input_file: Path to the raw data JSON file.
            output_dir: Directory to save the processed results.
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.df = None

    def load_data(self):
        """Loads raw JSON data into a DataFrame."""
        logger.info(f"Loading data from {self.input_file}")
        try:
            # Read the JSON file
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert JSON data to a pandas DataFrame
            self.df = pd.DataFrame(data)
            logger.info(f"Data loaded: {len(self.df)} entries")

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def clean_data(self):
        """Cleans and processes the raw data."""
        logger.info("Cleaning the data...")

        # Remove duplicate entries
        initial_len = len(self.df)
        self.df = self.df.drop_duplicates()
        logger.info(f"Duplicates removed: {initial_len - len(self.df)} entries")

        # Normalize whitespace in the 'title' column
        if 'title' in self.df.columns:
            self.df['title'] = self.df['title'].str.replace(r'\s+', ' ', regex=True)

        # Clean and standardize the 'price' column
        if 'price' in self.df.columns:
            self.df['price'] = (
                self.df['price']
                .str.replace('$', '')
                .str.replace('€', '')
                .str.replace('.', '')
                .str.replace(',', '.')
            )
            self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')

        # Update image URLs to original size
        if 'image' in self.df.columns:
            self.df['image'] = self.df['image'].str.replace('_50x50', '')

        # Remove rows with missing prices and sort by price
        if 'price' in self.df.columns:
            self.df = self.df.dropna(subset=['price'])
            self.df = self.df.sort_values(by='price', ascending=False)

        logger.info(f"Remaining data after cleaning: {len(self.df)} entries")

    def analyze_data(self):
        """Analyzes the data and computes statistical metrics."""
        logger.info("Analyzing the data...")

        # Calculate overall price statistics
        stats = {}
        if 'price' in self.df.columns:
            stats = {
                'title': 'Total',
                'average_price': round(self.df['price'].mean(), 2),
                'median_price': self.df['price'].median(),
                'min_price': self.df['price'].min(),
                'max_price': self.df['price'].max(),
                'total_count': len(self.df)
            }

        # Calculate statistics for each unique metal
        stat_meta = []
        if 'metal' in self.df.columns:
            unique_metals = self.df['metal'].unique()
            for metal in unique_metals:
                metal_stats = {
                    'title': metal,
                    'average_price': round(self.df[self.df['metal'] == metal]['price'].mean(), 2),
                    'median_price': self.df[self.df['metal'] == metal]['price'].median(),
                    'min_price': self.df[self.df['metal'] == metal]['price'].min(),
                    'max_price': self.df[self.df['metal'] == metal]['price'].max(),
                    'total_count': len(self.df[self.df['metal'] == metal])
                }
                stat_meta.append(metal_stats)

        logger.info(f"Statistics calculated: {stats}")
        return stats, stat_meta

    def save_results(self, stats, stat_meta):
        """Saves the processed data and statistics to files."""
        logger.info(f"Saving results to {self.output_dir}")

        # Ensure the output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save the cleaned data to a CSV file
        self.df.to_csv(self.output_dir / 'processed_data.csv', index=False)

        # Save overall statistics to a CSV file
        stats_df = pd.DataFrame([stats])
        stats_df_meta = pd.DataFrame(stat_meta)
        stats_df.to_csv(self.output_dir / 'statistics.csv', index=False)
        stats_df_meta.to_csv(self.output_dir / 'statistics.csv', mode='a', header=False, index=False)

        logger.info("Results saved successfully!")

def main():
    """
    Main function to run the data processing pipeline:
    1. Load raw data.
    2. Clean and process the data.
    3. Analyze the data for statistical insights.
    4. Save the processed data and statistics.
    """
    processor = DataProcessor(
        input_file='./data/raw/raw_data.json',
        output_dir='./data/processed'
    )

    try:
        # Execute the pipeline steps
        processor.load_data()
        processor.clean_data()
        stats, stat_meta = processor.analyze_data()
        processor.save_results(stats, stat_meta)

        logger.info("Processing completed successfully!")

    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()