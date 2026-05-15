const pool = require('../config/database');

exports.getMe = async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT id, email, role, name, gender, age, zipcode, language_pref FROM users WHERE id = ?',
      [req.user.id]
    );
    if (!rows.length) return res.status(404).json({ success: false, error: 'User not found' });
    res.json({ success: true, data: rows[0] });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.updateMe = async (req, res) => {
  const { name, gender, age, zipcode, language_pref } = req.body;
  try {
    await pool.query(
      'UPDATE users SET name=?, gender=?, age=?, zipcode=?, language_pref=? WHERE id=?',
      [name, gender, age, zipcode, language_pref, req.user.id]
    );
    const [rows] = await pool.query(
      'SELECT id, email, role, name, gender, age, zipcode, language_pref FROM users WHERE id=?',
      [req.user.id]
    );
    res.json({ success: true, data: rows[0] });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.getAllUsers = async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT id, email, role, name, age, zipcode, created_at FROM users ORDER BY created_at DESC'
    );
    res.json({ success: true, data: rows });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.updateUserRole = async (req, res) => {
  const { role } = req.body;
  if (!['user', 'admin'].includes(role)) {
    return res.status(400).json({ success: false, error: 'Invalid role' });
  }
  try {
    await pool.query('UPDATE users SET role=? WHERE id=?', [role, req.params.id]);
    res.json({ success: true, data: { id: req.params.id, role } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
