const router = require('express').Router();
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');
const ctrl = require('../controllers/calendar.controller');

router.get('/', ctrl.getEvents);
router.post('/', auth, admin, ctrl.createEvent);
router.delete('/:id', auth, admin, ctrl.removeEvent);

module.exports = router;
