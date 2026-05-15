const pool = require('../config/database');

exports.expenseSummary = async (req, res) => {
  const { from, to } = req.query;
  try {
    let query = `
      SELECT category,
             SUM(amount) AS total,
             DATE_FORMAT(expense_date, '%Y-%m') AS month
      FROM expenses
      WHERE user_id = ?
    `;
    const params = [req.user.id];
    if (from) { query += ' AND expense_date >= ?'; params.push(from); }
    if (to)   { query += ' AND expense_date <= ?'; params.push(to); }
    query += ' GROUP BY category, month ORDER BY month DESC, total DESC';

    const [rows] = await pool.query(query, params);
    res.json({ success: true, data: rows });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
