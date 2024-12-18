const { chromium } = require('playwright')

async function scrapePrices() {
  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()
  await page.goto('https://www.dealabs.com')

  await page.getByRole('button', { name: 'Tout accepter' }).click()
  await page.getByRole('button', { name: 'Les + hot' }).click()
  await page.pause()
  const productOfTheDay = await page.evaluate(() => {
    const productElement = document.querySelector('.top-deal');
    if (productElement) {
        return {
            title: productElement.querySelector('.thread-title').textContent.trim(),
            price: productElement.querySelector('.thread-price').textContent.trim(),
            link: productElement.querySelector('a').href
        };
    }
    return null;
  })

  await browser.close()
  return productOfTheDay
}
scrapePrices()
module.exports = scrapePrices
