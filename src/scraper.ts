import { chromium } from 'playwright';

async function scrapePrices(): Promise<{ title: string; price: string; link: string } | null> {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://www.dealabs.com');

  await page.getByRole('button', { name: 'Tout accepter' }).click();
  await page.getByRole('button', { name: 'Les + hot' }).click();
  await page.pause();
  const productOfTheDay = await page.evaluate(() => {
    const productElement = document.querySelector('.top-deal');
    if (productElement) {
      return {
        title: (productElement.querySelector('.thread-title') as HTMLElement).textContent?.trim() || '',
        price: (productElement.querySelector('.thread-price') as HTMLElement).textContent?.trim() || '',
        link: (productElement.querySelector('a') as HTMLAnchorElement).href
      };
    }
    return null;
  });

  await browser.close();
  return productOfTheDay;
}

scrapePrices();
export default scrapePrices;