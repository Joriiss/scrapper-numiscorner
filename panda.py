import pandas as pd
import requests
import json
from pathlib import Path
import logging
import requests
import json
import os

# Fetch data from the API
url = 'http://localhost:3000/data'

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    data = response.json()      # Parse JSON response

    # Create the directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)

    # Save the data to a JSON file
    json_file = 'data/raw/raw_data.json'
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
        Initializes the data processor
        input_file: path to the raw data JSON file
        output_dir: directory to save the results
        """
        self.input_file = Path("data/raw/raw_data.json")
        self.output_dir = Path("data/processed")
        self.df = None

    def load_data(self):
        """Loads the JSON data into a DataFrame"""
        logger.info(f"Loading data from {self.input_file}")
        try:
            # Read the JSON file
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert to DataFrame
            self.df = pd.DataFrame(data)
            logger.info(f"Data loaded: {len(self.df)} entries")

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def clean_data(self):
        """Cleans and prepares the data"""
        logger.info("Cleaning the data...")

        # Remove duplicates
        initial_len = len(self.df)
        self.df = self.df.drop_duplicates()
        logger.info(f"Duplicates removed: {initial_len - len(self.df)} entries")

        # Clean prices (remove currency symbols and convert to float)
        self.df['price'] = self.df['price'].str.replace('$', '').str.replace('€', '').str.replace('.', '').str.replace(',', '.')
        self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')
        
        # Change the image URL to use the original size
        self.df['image'] = self.df['image'].str.replace('_50x50', '')

        # Remove rows without prices
        self.df = self.df.dropna(subset=['price'])
        logger.info(f"Remaining data after cleaning: {len(self.df)} entries")

    def analyze_data(self):
        """Analyzes the data and adds useful information"""
        logger.info("Analyzing the data...")

        # Calculate price statistics
        stats = {
            'average_price': self.df['price'].mean(),
            'median_price': self.df['price'].median(),
            'min_price': self.df['price'].min(),
            'max_price': self.df['price'].max()
        }

        # Categorize prices
        self.df['price_category'] = pd.qcut(
            self.df['price'],
            q=3,
            labels=['low', 'medium', 'high']
        )

        logger.info(f"Statistics calculated: {stats}")
        return stats

    def save_results(self, stats):
        """Saves the results"""
        logger.info(f"Saving results to {self.output_dir}")

        # Create the output directory if necessary
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save cleaned data
        self.df.to_csv(
            self.output_dir / 'processed_data.csv',
            index=False
        )

        # Save statistics
        with open(self.output_dir / 'statistics.json', 'w') as f:
            json.dump(stats, f, indent=2)

        logger.info("Statistics Saved")

def main():
    """Main function to orchestrate the processing"""
    processor = DataProcessor(
        input_file='data/raw/products.json',
        output_dir='data/processed'
    )

    try:
        # Run the processing pipeline
        processor.load_data()      # Loading
        processor.clean_data()     # Cleaning
        stats = processor.analyze_data()  # Analyzing
        processor.save_results(stats)     # Saving

        logger.info("Processing completed successfully!")

    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()