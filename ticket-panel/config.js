require('dotenv').config();
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'tickets',
    password: process.env.DB_PASSWORD || 'fpwkapak3747474',
    database: process.env.DB_NAME || 'ticket_system',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

module.exports = pool;
