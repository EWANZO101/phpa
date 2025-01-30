const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const authMiddleware = require('../middleware/auth');

router.get('/dashboard', authMiddleware, adminController.getAdminDashboard);
router.get('/users', authMiddleware, adminController.getUsers);

module.exports = router;
