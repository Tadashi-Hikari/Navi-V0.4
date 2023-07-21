const express = require('express');
const app = express();

// Set the basic route for a (req)quest, send a basic (res)ponse
app.get('/', (req,res) => {
    res.send('Hello, World!');
});

const port = 7400

// Start the server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
})

