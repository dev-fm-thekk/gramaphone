import express from 'express';

const app = express()
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res) => res.send("Welcome to Gramaphone"))

app.listen(3000)

export default app
