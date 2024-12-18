import express from 'express';
import bodyParser from 'body-parser';
import cron from 'node-cron';
import scrapePrices from './scraper';
import axios from 'axios';

const app = express();
app.use(bodyParser.json());

app.post('/prices', (req, res) => {
  const prices = req.body;
  console.log('Received prices:', prices);
  res.status(200).send('Prices received');
});

cron.schedule('*/5 * * * *', async () => {
  console.log('Running scraper...');
  const prices = await scrapePrices();
  if (prices) {
    await axios.post('http://localhost:3000/prices', prices)
      .then(response => console.log(response.data))
      .catch(error => console.error('Error sending prices:', error));
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});