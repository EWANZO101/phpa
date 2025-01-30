const mysql = require('mysql2/promise');

async function testConnection() {
    try {
        const conn = await mysql.createConnection({
            host: 'localhost',
            user: 'tickets',
            password: 'fpwkapak3747474',
            database: 'ticket_system'
        });
        console.log("✅ Database connection successful!");
        conn.end();
    } catch (err) {
        console.error("❌ Database connection failed:", err);
    }
}

testConnection();
