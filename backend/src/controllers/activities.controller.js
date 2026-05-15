const pool = require('../config/database');

exports.getAll = async (req, res) => {
  try {
    const [rows] = await pool.query(
      'SELECT * FROM activities WHERE event_date >= NOW() ORDER BY event_date ASC'
    );
    res.json({ success: true, data: rows });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.create = async (req, res) => {
  const { title, description, location, event_date, category } = req.body;
  try {
    const [result] = await pool.query(
      'INSERT INTO activities (title, description, location, event_date, category, created_by) VALUES (?,?,?,?,?,?)',
      [title, description, location, event_date, category, req.user.id]
    );
    res.status(201).json({ success: true, data: { id: result.insertId, title, event_date } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.update = async (req, res) => {
  const { title, description, location, event_date, category } = req.body;
  try {
    await pool.query(
      'UPDATE activities SET title=?, description=?, location=?, event_date=?, category=? WHERE id=?',
      [title, description, location, event_date, category, req.params.id]
    );
    res.json({ success: true, data: { id: req.params.id } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.remove = async (req, res) => {
  try {
    await pool.query('DELETE FROM activities WHERE id=?', [req.params.id]);
    res.json({ success: true });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
