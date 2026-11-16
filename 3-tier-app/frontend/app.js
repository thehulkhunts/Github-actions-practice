const list = document.getElementById('list');
const status = document.getElementById('status');

async function api(path, options) {
  const res = await fetch('/api' + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error('Request failed: ' + res.status);
  return res.status === 204 ? null : res.json();
}

async function load() {
  try {
    const todos = await api('/todos');
    status.textContent = '';
    list.innerHTML = '';
    todos.forEach((t) => {
      const li = document.createElement('li');
      if (t.done) li.className = 'done';
      const span = document.createElement('span');
      span.textContent = t.title;
      span.onclick = async () => { await api('/todos/' + t.id, { method: 'PUT' }); load(); };
      const del = document.createElement('button');
      del.textContent = '✕';
      del.onclick = async () => { await api('/todos/' + t.id, { method: 'DELETE' }); load(); };
      li.append(span, del);
      list.appendChild(li);
    });
  } catch (e) { status.textContent = 'Error: ' + e.message; }
}

document.getElementById('form').onsubmit = async (e) => {
  e.preventDefault();
  const input = document.getElementById('title');
  await api('/todos', { method: 'POST', body: JSON.stringify({ title: input.value }) });
  input.value = '';
  load();
};

load();
