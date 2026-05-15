const pool = require('../config/database');

exports.getEvents = async (req, res) => {
  try {
    const [activities] = await pool.query(`
      SELECT id, title, description, location,
             DATE(event_date) AS event_date, category,
             'activity' AS source
      FROM activities
      WHERE event_date >= CURDATE()
      ORDER BY event_date ASC
    `);

    const [calEvents] = await pool.query(`
      SELECT id, title, description, NULL AS location,
             event_date, NULL AS category,
             'event' AS source
      FROM calendar_events
      WHERE event_date >= CURDATE() AND is_public = TRUE
      ORDER BY event_date ASC
    `);

    const merged = [...activities, ...calEvents].sort(
      (a, b) => new Date(a.event_date) - new Date(b.event_date)
    );

    res.json({ success: true, data: merged });
  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.createEvent = async (req, res) => {
  const { title, description, event_date } = req.body;
  if (!title || !event_date) {
    return res.status(400).json({ success: false, error: 'Title and date are required' });
  }
  try {
    const [result] = await pool.query(
      'INSERT INTO calendar_events (title, description, event_date, is_public) VALUES (?, ?, ?, TRUE)',
      [title, description || null, event_date]
    );
    res.status(201).json({ success: true, data: { id: result.insertId, title, event_date } });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};

exports.removeEvent = async (req, res) => {
  try {
    const [result] = await pool.query('DELETE FROM calendar_events WHERE id = ?', [req.params.id]);
    if (!result.affectedRows) return res.status(404).json({ success: false, error: 'Not found' });
    res.json({ success: true });
  } catch {
    res.status(500).json({ success: false, error: 'Server error' });
  }
};
