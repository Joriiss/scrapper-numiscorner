import scrapePrices from './scraper';
import axios from 'axios';

async function runScraper() {
  try {
    const productOfTheDay = await scrapePrices();
    if (productOfTheDay) {
      await axios.post('http://localhost:3000/prices', productOfTheDay);
      console.log('Product of the day sent:', productOfTheDay);
    } else {
      console.log('No product of the day found.');
    }
  } catch (error) {
    console.error('Error running scraper:', error);
  }
}

runScraper();