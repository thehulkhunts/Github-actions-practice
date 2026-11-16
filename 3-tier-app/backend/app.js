const express = require('express');

// The DB pool is injected so tests can use a fake one.
function createApp(pool) {
  const app = express();
  app.use(express.json());

  app.get('/api/health', async (_req, res) => {
    try {
      await pool.query('SELECT 1');
      res.json({ status: 'ok' });
    } catch {
      res.status(503).json({ status: 'db_unavailable' });
    }
  });

  app.get('/api/todos', async (_req, res) => {
    try {
      const { rows } = await pool.query('SELECT * FROM todos ORDER BY id');
      res.json(rows);
    } catch (e) { res.status(500).json({ error: e.message }); }
  });

  app.post('/api/todos', async (req, res) => {
    const title = (req.body.title || '').trim();
    if (!title) return res.status(400).json({ error: 'title is required' });
    try {
      const { rows } = await pool.query(
        'INSERT INTO todos (title) VALUES ($1) RETURNING *', [title]);
      res.status(201).json(rows[0]);
    } catch (e) { res.status(500).json({ error: e.message }); }
  });

  app.put('/api/todos/:id', async (req, res) => {
    try {
      const { rows } = await pool.query(
        'UPDATE todos SET done = NOT done WHERE id = $1 RETURNING *', [req.params.id]);
      if (!rows.length) return res.status(404).json({ error: 'not found' });
      res.json(rows[0]);
    } catch (e) { res.status(500).json({ error: e.message }); }
  });

  app.delete('/api/todos/:id', async (req, res) => {
    try {
      await pool.query('DELETE FROM todos WHERE id = $1', [req.params.id]);
      res.status(204).end();
    } catch (e) { res.status(500).json({ error: e.message }); }
  });

  return app;
}

module.exports = createApp;
