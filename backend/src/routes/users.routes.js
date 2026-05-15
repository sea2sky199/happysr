const router = require('express').Router();
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');
const ctrl = require('../controllers/users.controller');

router.get('/me', auth, ctrl.getMe);
router.put('/me', auth, ctrl.updateMe);
router.put('/me/password', auth, ctrl.changePassword);
router.get('/admin/users', auth, admin, ctrl.getAllUsers);
router.put('/admin/users/:id/role', auth, admin, ctrl.updateUserRole);

module.exports = router;
