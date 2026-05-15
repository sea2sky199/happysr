require('dotenv').config({ path: require('path').resolve(__dirname, '../.env') });
const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors({ origin: 'http://localhost:5173', credentials: true }));
app.use(express.json());

app.use('/api/v1/auth',        require('./routes/auth.routes'));
app.use('/api/v1/calendar',    require('./routes/calendar.routes'));
app.use('/api/v1/users',       require('./routes/users.routes'));
app.use('/api/v1/activities',  require('./routes/activities.routes'));
app.use('/api/v1/expenses',    require('./routes/expenses.routes'));
app.use('/api/v1/investments', require('./routes/investments.routes'));
app.use('/api/v1/reports',     require('./routes/reports.routes'));

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ success: false, error: 'Internal server error' });
});

module.exports = app;
