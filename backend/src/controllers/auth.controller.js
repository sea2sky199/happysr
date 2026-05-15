const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { validationResult } = require('express-validator');
const pool = require('../config/database');

const signToken = (user) =>
  jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET, { expiresIn: '7d' });

exports.register = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ success: false, error: errors.array()[0].msg });

  const { email, password, name } = req.body;
  try {
    const [existing] = await pool.query('SELECT id FROM sr_users WHERE email = ?', [email]);
    if (existing.length) return res.status(409).json({ success: false, error: 'Email already registered' });

    const hash = await bcrypt.hash(password, 12);
    const [result] = await pool.query(
      'INSERT INTO sr_users (email, password_hash, name) VALUES (?, ?, ?)',
      [email, hash, name || null]
    );
    const user = { id: result.insertId, role: 'user', email, name };
    res.status(201).json({ success: true, data: { token: signToken(user), user } });
  } catch (err) {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.login = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ success: false, error: errors.array()[0].msg });

  const { email, password } = req.body;
  try {
    const [rows] = await pool.query(
      'SELECT id, email, password_hash, role, name, gender, age, zipcode, language_pref FROM sr_users WHERE email = ?',
      [email]
    );
    if (!rows.length) return res.status(401).json({ success: false, error: 'Invalid credentials' });

    const user = rows[0];
    const match = await bcrypt.compare(password, user.password_hash);
    if (!match) return res.status(401).json({ success: false, error: 'Invalid credentials' });

    const { password_hash, ...safeUser } = user;
    res.json({ success: true, data: { token: signToken(safeUser), user: safeUser } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
