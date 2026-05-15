const pool = require('../config/database');

exports.getAll = async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT * FROM expenses WHERE user_id=? ORDER BY expense_date DESC',
      [req.user.id]
    );
    res.json({ success: true, data: rows });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.create = async (req, res) => {
  const { amount, category, description, expense_date } = req.body;
  try {
    const [result] = await pool.query(
      'INSERT INTO expenses (user_id, amount, category, description, expense_date) VALUES (?,?,?,?,?)',
      [req.user.id, amount, category, description, expense_date]
    );
    res.status(201).json({ success: true, data: { id: result.insertId, amount, category, expense_date } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.remove = async (req, res) => {
  try {
    const [result] = await pool.query(
      'DELETE FROM expenses WHERE id=? AND user_id=?',
      [req.params.id, req.user.id]
    );
    if (!result.affectedRows) return res.status(404).json({ success: false, error: 'Not found' });
    res.json({ success: true });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
