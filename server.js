const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello world');
});

app.listen(8080, () => {
  console.info('Server started at http://127.0.0.1:8080');
});