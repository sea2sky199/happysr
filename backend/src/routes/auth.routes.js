const router = require('express').Router();
const { body } = require('express-validator');
const ctrl = require('../controllers/auth.controller');

const emailPass = [
  body('email').isEmail().withMessage('Valid email required'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
];

router.post('/register', emailPass, ctrl.register);
router.post('/login', emailPass, ctrl.login);

module.exports = router;
