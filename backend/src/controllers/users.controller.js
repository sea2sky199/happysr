const pool = require('../config/database');

exports.getMe = async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT id, email, role, name, gender, age, zipcode, language_pref FROM sr_users WHERE id = ?',
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
      'UPDATE sr_users SET name=?, gender=?, age=?, zipcode=?, language_pref=? WHERE id=?',
      [name, gender, age, zipcode, language_pref, req.user.id]
    );
    const [rows] = await pool.query(
      'SELECT id, email, role, name, gender, age, zipcode, language_pref FROM sr_users WHERE id=?',
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
      'SELECT id, email, role, name, age, zipcode, created_at FROM sr_users ORDER BY created_at DESC'
    );
    res.json({ success: true, data: rows });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.changePassword = async (req, res) => {
  const { currentPassword, newPassword } = req.body;
  if (!currentPassword || !newPassword) {
    return res.status(400).json({ success: false, error: 'Current and new password are required' });
  }
  if (newPassword.length < 6) {
    return res.status(400).json({ success: false, error: 'New password must be at least 6 characters' });
  }
  try {
    const bcrypt = require('bcryptjs');
    const [rows] = await pool.query('SELECT password_hash FROM sr_users WHERE id=?', [req.user.id]);
    if (!rows.length) return res.status(404).json({ success: false, error: 'User not found' });
    const match = await bcrypt.compare(currentPassword, rows[0].password_hash);
    if (!match) return res.status(401).json({ success: false, error: 'Current password is incorrect' });
    const hash = await bcrypt.hash(newPassword, 12);
    await pool.query('UPDATE sr_users SET password_hash=? WHERE id=?', [hash, req.user.id]);
    res.json({ success: true });
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
    await pool.query('UPDATE sr_users SET role=? WHERE id=?', [role, req.params.id]);
    res.json({ success: true, data: { id: req.params.id, role } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
