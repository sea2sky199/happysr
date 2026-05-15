const db = require('../config/database');

exports.list = async (req, res) => {
  const activeOnly = req.query.active !== 'false';
  const [rows] = await db.query(
    `SELECT * FROM sr_orgs${activeOnly ? ' WHERE is_active = TRUE' : ''} ORDER BY name`,
  );
  res.json({ success: true, data: rows });
};

exports.getOne = async (req, res) => {
  const [[row]] = await db.query('SELECT * FROM sr_orgs WHERE id = ?', [req.params.id]);
  if (!row) return res.status(404).json({ success: false, error: 'Not found' });
  res.json({ success: true, data: row });
};

exports.create = async (req, res) => {
  const { name, category, description, website_url, phone, email, address, city, state, zipcode, is_active } = req.body;
  if (!name) return res.status(400).json({ success: false, error: 'name is required' });
  const [result] = await db.query(
    `INSERT INTO sr_orgs (name, category, description, website_url, phone, email, address, city, state, zipcode, is_active)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [name, category || null, description || null, website_url || null, phone || null,
     email || null, address || null, city || null, state || null, zipcode || null,
     is_active !== undefined ? is_active : true],
  );
  const [[created]] = await db.query('SELECT * FROM sr_orgs WHERE id = ?', [result.insertId]);
  res.status(201).json({ success: true, data: created });
};

exports.update = async (req, res) => {
  const { name, category, description, website_url, phone, email, address, city, state, zipcode, is_active } = req.body;
  const [[existing]] = await db.query('SELECT id FROM sr_orgs WHERE id = ?', [req.params.id]);
  if (!existing) return res.status(404).json({ success: false, error: 'Not found' });
  await db.query(
    `UPDATE sr_orgs SET name=?, category=?, description=?, website_url=?, phone=?, email=?,
     address=?, city=?, state=?, zipcode=?, is_active=? WHERE id=?`,
    [name, category || null, description || null, website_url || null, phone || null,
     email || null, address || null, city || null, state || null, zipcode || null,
     is_active !== undefined ? is_active : true, req.params.id],
  );
  const [[updated]] = await db.query('SELECT * FROM sr_orgs WHERE id = ?', [req.params.id]);
  res.json({ success: true, data: updated });
};

exports.remove = async (req, res) => {
  const [[existing]] = await db.query('SELECT id FROM sr_orgs WHERE id = ?', [req.params.id]);
  if (!existing) return res.status(404).json({ success: false, error: 'Not found' });
  await db.query('DELETE FROM sr_orgs WHERE id = ?', [req.params.id]);
  res.json({ success: true });
};
