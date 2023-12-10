const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const https = require('https');
const fs = require('fs');
const dotenv = require('dotenv');
dotenv.config();


const app = express();
const port = 8080;
const PORT = port || 8080;

app.use(cors());
app.use(express.json());

const privateKey = fs.readFileSync('/etc/letsencrypt/live/evlmei.dev/privkey.pem', 'utf8');
const certificate = fs.readFileSync('/etc/letsencrypt/live/evlmei.dev/fullchain.pem', 'utf8');
const httpsOptions = {
    key: privateKey,
    cert: certificate
};

https.createServer(httpsOptions, app).listen(8080, () => {
    console.log('Express server listening on port 8080');
});



console.log("string+", process.env.DB_PASSWORD);
const connection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
});

connection.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL database:', err);
    } else {
        console.log('Connected to MySQL database');
    }
});

app.post('/retrieveCart', async (req, res) => {
    console.log("Reached /retrieveCart");
    const { userId, numItems } = req.body;
    const query = `SELECT * FROM userCart.user${userId}Cart LIMIT ${numItems};`;

    try {
        const results = await executeQuery(query);
        console.log("First Query");
        console.log(results[0].item_id);

        const itemIds = results;
        const finalRes = [];

        console.log("Second Query");
        console.log(itemIds);

        for (let i = 0; i < itemIds.length; i++) {
            console.log(itemIds[i].item_id);
            const query2 = `SELECT * FROM wpdb.products WHERE productID = ${itemIds[i].item_id};`;
            const results2 = await executeQuery(query2);
            console.log(`Successfully retrieved ${i + 1} product(s) from products table.`);
            finalRes.push(results2);
        }

        res.json(finalRes);
    } catch (err) {
        console.error('Error:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Function to execute a query and return a promise
function executeQuery(query) {
    return new Promise((resolve, reject) => {
        connection.query(query, (err, results) => {
            if (err) {
                reject(err);
            } else {
                resolve(results);
            }
        });
    });
}

// Removes all data in cart
app.post('/deleteCart', (req, res) => {
    const { userId, itemId } = req.body;
    console.log("Reached /deleteCart");
    const query = `DELETE FROM userCart.${userId};`;
    connection.query(query, (err, results) => {
        if (err) {
            console.error('Error executing MySQL query:', err);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            console.log(`Deleted all products from ${userId}'s cart.`);
        }
    });
});

// Endpoint to add an item to the user's cart
app.post('/addCart', (req, res) => {
    console.log("Reached /addCart");
    const { userId, itemId } = req.body;
    const query = `INSERT INTO userCart.${userId} (item_id) VALUES (${itemId});`;
    connection.query(query, (err, results) => {
        if (err) {
            console.error('Error executing MySQL query:', err);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            console.log(`Successfully added product ${itemId} into ${userId}'s table.`);
        }
    });
});

// Route to retrieve entries from the 'products' table based on the number specified in the payload
app.post('/products', (req, res) => {

    const { numberOfProducts } = req.body;

    console.log(`Attempting to retrieve ${numberOfProducts} from products table.`);

    if (!numberOfProducts || isNaN(numberOfProducts)) {
        return res.status(400).json({ error: 'Invalid number in the payload' });
    }

    const query = `SELECT * FROM products LIMIT ${numberOfProducts}`;

    // Execute the query
    connection.query(query, (err, results) => {
        if (err) {
            console.error('Error executing MySQL query:', err);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            console.log(`Successfully retrieved ${numberOfProducts} from products table.`);
            res.json(results);
        }
    });
});


// Route for general-purpose testing
app.get('/', (req, res) => {
    res.json('Hello from the server!');
  });

// app.listen(port, () => {
//     console.log(`Server listening at http://localhost:${port}`);
// });