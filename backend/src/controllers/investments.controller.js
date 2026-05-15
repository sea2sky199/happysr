const pool = require('../config/database');

exports.getAll = async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT * FROM investments WHERE user_id=? ORDER BY as_of_date DESC',
      [req.user.id]
    );
    res.json({ success: true, data: rows });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.create = async (req, res) => {
  const { type, institution, amount, notes, as_of_date } = req.body;
  try {
    const [result] = await pool.query(
      'INSERT INTO investments (user_id, type, institution, amount, notes, as_of_date) VALUES (?,?,?,?,?,?)',
      [req.user.id, type, institution, amount, notes, as_of_date]
    );
    res.status(201).json({ success: true, data: { id: result.insertId } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.remove = async (req, res) => {
  try {
    const [result] = await pool.query(
      'DELETE FROM investments WHERE id=? AND user_id=?',
      [req.params.id, req.user.id]
    );
    if (!result.affectedRows) return res.status(404).json({ success: false, error: 'Not found' });
    res.json({ success: true });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
