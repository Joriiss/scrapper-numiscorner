const express = require('express')
const bodyParser = require('body-parser')
const cron = require('node-cron')
const scrapePrices = require('./scraper')
const axios = require('axios')

const app = express()
app.use(bodyParser.json())

// app.post('/prices', (req, res) => {
//   const prices = req.body
//   console.log('Received prices:', prices)
//   res.status(200).send('Prices received')
// })

cron.schedule('* * * * *', async () => {
  const prices = await scrapePrices()
  console.log('prices', prices)
})

const PORT = 3000
app.listen(PORT, () => {
  scrapePrices()
  console.log(`Server is running on port ${PORT}`)
})
