const express = require('express');
const bodyParser = require('body-parser');
const cron = require('node-cron');
const scrapePrices = require('./scraper');
const { exec } = require('child_process'); // Import child_process to execute Python scripts
const path = require('path');


const app = express();
app.use(bodyParser.json());

let scrapedData = []; // This will hold the scraped data

// Cron job to scrape prices and update the scraped data with python
cron.schedule('* * * * *', async () => {
  console.log('Running cron job...');
  scrapedData = await scrapePrices(); // Update the scraped data
  // console.log('Scraped Data:', scrapedData);

  // Run the Python script
  exec('py panda.py', (error, stdout, stderr) => {
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
});

// Define a route to serve the scraped data
app.get('/data', (req, res) => {
  res.json(scrapedData); // Respond with the current scraped data
});

// Serve the dashboard on the root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
// Serve static assets (CSS, JS, etc.)
app.use(express.static(path.join(__dirname, 'public')));


const PORT = 3000;
app.listen(PORT, async () => {
  scrapedData = await scrapePrices(); // Initial scrape on server start
  // console.log('Scraped Data:', scrapedData);
  console.log(`Server is running on port ${PORT}`);
});
