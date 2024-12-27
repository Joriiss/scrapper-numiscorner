# NumisCorner Scraper Project

This project is designed to scrape product data from [NumisCorner](https://www.numiscorner.com/), process the data, and store it in a Cassandra database for further analysis.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
## Features

- **Data Extraction**: Utilizes Playwright to scrape product details from NumisCorner's Antique Greek collection.
- **Data Processing**: Cleans and analyzes the scraped data, calculating statistics such as average, median, minimum, and maximum prices.
- **Data Storage**: Stores both raw and processed data in a Cassandra database for persistent storage and further analysis.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 20.x or higher.
- **npm**: Comes with Node.js.
- **Python**: Version 3.6 or higher.
- **Cassandra**: A running instance of Cassandra database.

## Installation

1. **Clone the repository**:
   
   ```bash
   git clone https://github.com/Joriiss/scrapper-numiscorner.git
   cd scrapper-numiscorner

3. **Install Node.js dependencies**:
   
   ```bash
   npm install

5. **Set up Cassandra**:
   
   Ensure Cassandra is running and accessible. You can use the provided Docker Compose file to set up Cassandra:
   
   ```bash
   docker-compose -f docker-compose-cassandra.yml up -d
   ```
   This will start a Cassandra instance on localhost:9042.

## Usage

1. **Run the server**

   The scraper fetches product data from NumisCorner and saves it as a JSON file.

   ```
   node src/extract/scrape.js

## Project Structure

   The project is organized as follows:
   
   ```
   scrapper-numiscorner/
   ├── data/
   │   ├── raw/                      # Raw data files
   │   └── processed/                # Processed data and statistics
   ├── extract/                      # Data extracting scripts
   ├── transform/                    # Data processing scripts
   ├── load/                         # Data loading scripts
   ├── public/
   │   └── index.html/               # Dashboard to display the data
   ├── docker-compose-cassandra.yml  # Docker Compose file for Cassandra
   ├── package.json                  # Node.js dependencies
   └── README.md                     # Project documentation
