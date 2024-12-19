const { chromium } = require('playwright')

async function scrapePrices() {
  console.log('Running scraper...')

  const browser = await chromium.launch({ headless: true }); 
  const page = await browser.newPage()
  await page.goto('https://www.numiscorner.com/collections/antique-greek')

  await page.getByRole('button', { name: 'Yes' }).click();
  await page.getByRole('button', { name: 'Accept' }).click();

  const productDetails = await page.$$eval(
    'div.product-item:not(#collectionProductPromo)',
    divs => divs.map(div => {
      const title = div.querySelector('h3')?.textContent.trim() || 'No title';
      const price = div.querySelector('span.money')?.textContent.trim() || 'No price';
      const metal = div.querySelector('div.legend-metal')?.textContent.trim() || 'No metal';
      const link = div.querySelector('a.icons-container')?.href || 'No link';
      const image = div.querySelector('div.solo-image img')?.src || 'No image';  // Get the first image's src
      return { title, price, metal, link, image };
    })
  );

  // console.log('Product Details:', productDetails);
  await browser.close()
  return productDetails; // Return the scraped data
}
module.exports = scrapePrices
