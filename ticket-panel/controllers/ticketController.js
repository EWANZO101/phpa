const db = require('../config/db');

module.exports = {
    getDashboard: async (req, res) => {
        const [tickets] = await db.query('SELECT * FROM tickets WHERE user_id = ?', [req.session.user.id]);
        res.render('tickets/dashboard', { user: req.session.user, tickets });
    },
    createTicket: async (req, res) => {
        const { title, description } = req.body;
        await db.query('INSERT INTO tickets (title, description, user_id) VALUES (?, ?, ?)', [title, description, req.session.user.id]);
        res.redirect('/tickets/dashboard');
    }
};
