const router = require('express').Router();
const auth = require('../middleware/auth');
const ctrl = require('../controllers/reports.controller');

router.get('/expenses', auth, ctrl.expenseSummary);

module.exports = router;
