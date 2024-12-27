const express = require('express');
const bodyParser = require('body-parser');
const { Client } = require('cassandra-driver');
const cron = require('node-cron');
const scrapePrices = require('./extract/scraper');
const { exec } = require('child_process'); // Import child_process to execute Python scripts
const path = require('path');

const app = express();
app.use(bodyParser.json()); // Middleware to parse JSON request bodies

// Cassandra connection configuration
const cassandraClient = new Client({
  contactPoints: ['127.0.0.1'], // Replace with your Cassandra host
  localDataCenter: 'datacenter1', // Replace with your datacenter name
});

// Function to initialize and set up the Cassandra database
async function setupDatabase() {
  try {
    // Create the keyspace if it doesn't exist
    await cassandraClient.execute(`
      CREATE KEYSPACE IF NOT EXISTS etl_data
      WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    `);

    // Connect to the keyspace
    await cassandraClient.execute('USE etl_data');

    // Drop the 'products' table if it exists
    await cassandraClient.execute('DROP TABLE IF EXISTS products');

    // Create the 'products' table
    await cassandraClient.execute(`
      CREATE TABLE IF NOT EXISTS products (
        date date,
        product_id uuid,
        image text,
        link text,
        metal text,
        price decimal,
        title text,
        PRIMARY KEY (date, product_id)
      )
    `);
    console.log('Database table "products" successfully initialized');

    // Drop the 'stats' table if it exists
    await cassandraClient.execute('DROP TABLE IF EXISTS stats');

    // Create the 'stats' table
    await cassandraClient.execute(`
      CREATE TABLE IF NOT EXISTS stats (
        date date,
        stat_id uuid PRIMARY KEY,
        average_price decimal,
        max_price decimal,
        median_price decimal,
        min_price decimal,
        title text,
        total int
      )
    `);
    console.log('Database table "stats" successfully initialized');
  } catch (error) {
    console.error("Error during database initialization:", error);
    throw error;
  }
}

// Function to perform data transformation using a Python script
async function transformData() {
  exec('py transform/panda.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Python script stderr: ${stderr}`);
      return;
    }
    console.log(`Python script output:\n${stdout}`);
  });
}

// Function to load data into the database using a Python script
async function loadData() {
  exec('py load/loader.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Python script stderr: ${stderr}`);
      return;
    }
    console.log(`Python script output:\n${stdout}`);
  });
}

// Function to run the complete ETL pipeline
async function runETLPipeline() {
  try {
    console.log('ETL pipeline started...');

    // Extraction phase
    console.log('1. Extraction...');
    scrapedData = await scrapePrices(); // Scrape data and update the variable

    // Transformation phase
    console.log('2. Transformation...');
    transformData();

    // Loading phase
    console.log('3. Loading...');
    loadData();

    console.log('ETL pipeline successfully completed!');
  } catch (error) {
    console.error('Error in ETL pipeline:', error);
  }
}

// Main initialization function
async function init() {
  try {
    // Connect to the Cassandra database
    await cassandraClient.connect();
    console.log('Connected to Cassandra');

    // Set up the database
    await setupDatabase();

    // Run the ETL pipeline for the first time
    await runETLPipeline();

    // Schedule the ETL pipeline to run every minute using CRON
    cron.schedule('* * * * *', () => {
      console.log('Scheduled execution of ETL pipeline');
      runETLPipeline();
    });

    // Define a route to serve the raw scraped data
    app.get('/api/raw', (req, res) => {
      res.json(scrapedData); // Respond with the current scraped data
    });

    // Start the Express server
    const PORT = 3000;
    app.listen(PORT, async () => {
      scrapedData = await scrapePrices(); // Initial scrape on server start
      console.log(`Server is running on port ${PORT}`);
    });
  } catch (error) {
    console.error("Initialization error:", error);
    process.exit(1);
  }

  // API endpoint to fetch all product data
  app.get('/api/data', async (req, res) => {
    try {
      const query = 'SELECT * FROM products';
      const result = await cassandraClient.execute(query);
      res.json(result.rows); // Send the product data to the client
    } catch (err) {
      console.error('Error fetching data:', err);
      res.status(500).json({ error: 'Failed to fetch data' });
    }
  });

  // API endpoint to fetch all statistics
  app.get('/api/stats', async (req, res) => {
    try {
      const query = 'SELECT * FROM stats';
      const result = await cassandraClient.execute(query);
      res.json(result.rows); // Send the statistics data to the client
    } catch (err) {
      console.error('Error fetching data:', err);
      res.status(500).json({ error: 'Failed to fetch data' });
    }
  });

  // Serve the dashboard on the root route
  app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/public', 'index.html'));
  });

  // Serve static assets such as CSS, JS, and images
  app.use(express.static(path.join(__dirname, 'public')));
}

init();