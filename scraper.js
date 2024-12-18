const { chromium } = require('playwright')

async function scrapePrices() {
  console.log('Running scraper...')

  const browser = await chromium.launch({ headless: false })
  const page = await browser.newPage()
  await page.goto('https://www.dealabs.com')

  await page.getByRole('button', { name: 'Tout accepter' }).click()
  await page.getByRole('button', { name: 'Les + hot' }).click()
  await page.waitForTimeout(1000)

  const productOfTheDay = await page.evaluate(() => {
    const productElement = document.querySelector('article[id^="thread_"]')

    console.log('productElement', productElement)
    if (productElement) {
      return {
        title: productElement.querySelector('.thread-title').textContent.trim(),
        price: productElement.querySelector('.thread-price').textContent.trim(),
        link: productElement.querySelector('a').href,
      }
    }
    return null
  })

  await browser.close()
  console.log('productOfTheDay', productOfTheDay)
  return productOfTheDay
}
module.exports = scrapePrices
