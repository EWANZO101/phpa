const express = require('express');
const router = express.Router();
const ticketController = require('../controllers/ticketController');
const authMiddleware = require('../middleware/auth');

router.get('/dashboard', authMiddleware, ticketController.getDashboard);
router.post('/create', authMiddleware, ticketController.createTicket);

module.exports = router;

