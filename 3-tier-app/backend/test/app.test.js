const test = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const createApp = require('../app');

const fakePool = {
  query: async (sql, params) => {
    if (sql.startsWith('SELECT 1')) return { rows: [{ '?column?': 1 }] };
    if (sql.startsWith('SELECT * FROM todos')) return { rows: [{ id: 1, title: 'a', done: false }] };
    if (sql.startsWith('INSERT')) return { rows: [{ id: 2, title: params[0], done: false }] };
    return { rows: [] };
  },
};

function request(server, method, path, body) {
  return new Promise((resolve, reject) => {
    const { port } = server.address();
    const req = http.request({ port, method, path, headers: { 'Content-Type': 'application/json' } }, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => resolve({ status: res.statusCode, body: data ? JSON.parse(data) : null }));
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

test('API endpoints', async () => {
  const server = createApp(fakePool).listen(0);
  try {
    assert.strictEqual((await request(server, 'GET', '/api/health')).status, 200);
    assert.strictEqual((await request(server, 'GET', '/api/todos')).body.length, 1);
    const created = await request(server, 'POST', '/api/todos', { title: 'new' });
    assert.strictEqual(created.status, 201);
    assert.strictEqual((await request(server, 'POST', '/api/todos', { title: ' ' })).status, 400);
    assert.strictEqual((await request(server, 'PUT', '/api/todos/99')).status, 404);
  } finally { server.close(); }
});
