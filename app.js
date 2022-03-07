import express  from 'express'
import bodyParser from 'body-parser'

import reminderRoutes from './routes/reminders.js'

const app = express()
const PORT = 3000;

app.use(bodyParser.json())

app.use('/reminders', reminderRoutes)

app.get('/', (_req, res) => {
    res.send('To-do website')
    
})

app.listen(PORT, () => {
    console.log(`Server is up on port ${PORT}.`)
})