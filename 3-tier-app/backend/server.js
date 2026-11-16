const { Pool } = require('pg');
const createApp = require('./app');

const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  database: process.env.DB_NAME || 'todos',
});

const port = process.env.PORT || 3000;
createApp(pool).listen(port, () => console.log(`Backend listening on ${port}`));
