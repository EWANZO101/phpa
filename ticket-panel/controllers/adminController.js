const db = require('../config/db');

module.exports = {
    getAdminDashboard: async (req, res) => {
        const [tickets] = await db.query('SELECT * FROM tickets');
        res.render('admin/adminDashboard', { tickets });
    },
    getUsers: async (req, res) => {
        const [users] = await db.query('SELECT * FROM users');
        res.render('admin/users', { users });
    }
};
