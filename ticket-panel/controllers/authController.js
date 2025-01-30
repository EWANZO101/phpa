const User = require('../models/User');
const bcrypt = require('bcryptjs');

module.exports = {
    getLogin: (req, res) => {
        res.render('auth/login', { error: null });
    },
    postLogin: async (req, res) => {
        const { email, password } = req.body;
        const user = await User.findByEmail(email);
        if (user && bcrypt.compareSync(password, user.password)) {
            req.session.user = { id: user.id, username: user.username };
            return res.redirect('/tickets/dashboard');
        }
        res.render('auth/login', { error: 'Invalid credentials' });
    },
    getSignup: (req, res) => {
        res.render('auth/signup', { error: null });
    },
    postSignup: async (req, res) => {
        const { username, email, password } = req.body;
        const existingUser = await User.findByEmail(email);
        if (existingUser) {
            return res.render('auth/signup', { error: 'Email already exists' });
        }
        await User.create(username, email, password);
        res.redirect('/login');
    },
    logout: (req, res) => {
        req.session.destroy();
        res.redirect('/');
    }
};
