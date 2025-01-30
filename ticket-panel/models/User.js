const db = require('../config/db');
const bcrypt = require('bcryptjs');

module.exports = {
    findByEmail: async (email) => {
        const [rows] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
        return rows.length ? rows[0] : null;
    },
    create: async (username, email, password) => {
        const hashedPassword = bcrypt.hashSync(password, 10);
        await db.query('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', [username, email, hashedPassword]);
    }
};
