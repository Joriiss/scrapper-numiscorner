const { chromium } = require('playwright');

// Function to scrape prices from the specified website
async function scrapePrices() {
  console.log('Running scraper...');

  // Launch a new browser instance in headless mode
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage(); // Open a new page in the browser
  
  // Navigate to the target URL
  await page.goto('https://www.numiscorner.com/collections/antique-greek');

  // Handle cookie consent pop-ups
  await page.getByRole('button', { name: 'Yes' }).click(); // Click "Yes" button if displayed
  await page.getByRole('button', { name: 'Accept' }).click(); // Click "Accept" button if displayed

  // Extract product details from the page
  const productDetails = await page.$$eval(
    'div.product-item:not(#collectionProductPromo)', // Exclude promotional products
    divs => divs.map(div => {
      // Extract title, price, metal, link, and image for each product
      const title = div.querySelector('h3')?.textContent.trim() || 'No title'; // Get product title or fallback
      const price = div.querySelector('span.money')?.textContent.trim() || 'No price'; // Get product price or fallback
      const metal = div.querySelector('div.legend-metal')?.textContent.trim() || 'No metal'; // Get product metal type or fallback
      const link = div.querySelector('a.icons-container')?.href || 'No link'; // Get product link or fallback
      const image = div.querySelector('div.solo-image img')?.src || 'No image'; // Get product image source or fallback

      return { title, price, metal, link, image }; // Return the extracted details as an object
    })
  );

  // Close the browser
  await browser.close();

  return productDetails; // Return the scraped product details
}

// Export the function for use in other parts of the application
module.exports = scrapePrices;