const router = require('express').Router();
const ctrl = require('../controllers/orgs.controller');
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');

router.get('/',     ctrl.list);
router.get('/:id',  ctrl.getOne);
router.post('/',    auth, admin, ctrl.create);
router.put('/:id',  auth, admin, ctrl.update);
router.delete('/:id', auth, admin, ctrl.remove);

module.exports = router;
