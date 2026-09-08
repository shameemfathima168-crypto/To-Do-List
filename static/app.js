const form = document.querySelector('#todo-form');
const input = document.querySelector('#todo-input');
const list = document.querySelector('#todo-list');
const count = document.querySelector('#count');
const empty = document.querySelector('#empty-state');
const clearButton = document.querySelector('#clear-completed');

const request = async (url, options = {}) => {
  const response = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options });
  if (!response.ok) throw new Error('Something went wrong. Please try again.');
  return response.status === 204 ? null : response.json();
};

const escapeHtml = value => value.replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[char]);

function render(todos) {
  list.innerHTML = '';
  const active = todos.filter(todo => !todo.completed).length;
  count.textContent = `${active} task${active === 1 ? '' : 's'} left`;
  empty.hidden = todos.length > 0;
  clearButton.hidden = !todos.some(todo => todo.completed);
  todos.forEach(todo => {
    const item = document.createElement('li');
    item.className = todo.completed ? 'completed' : '';
    item.innerHTML = `<label><input type="checkbox" ${todo.completed ? 'checked' : ''}><span>${escapeHtml(todo.title)}</span></label><button class="delete" aria-label="Delete ${escapeHtml(todo.title)}">×</button>`;
    item.querySelector('input').addEventListener('change', () => update(todo.id, { completed: !todo.completed }));
    item.querySelector('.delete').addEventListener('click', () => remove(todo.id));
    list.appendChild(item);
  });
}

const load = async () => render(await request('/todos'));
const update = async (id, data) => { await request(`/todos/${id}`, { method: 'PATCH', body: JSON.stringify(data) }); load(); };
const remove = async id => { await request(`/todos/${id}`, { method: 'DELETE' }); load(); };

form.addEventListener('submit', async event => {
  event.preventDefault();
  const title = input.value.trim();
  if (!title) return;
  await request('/todos', { method: 'POST', body: JSON.stringify({ title }) });
  input.value = '';
  load();
});

clearButton.addEventListener('click', async () => {
  const todos = await request('/todos');
  await Promise.all(todos.filter(todo => todo.completed).map(todo => remove(todo.id)));
});

load().catch(() => { empty.hidden = false; empty.textContent = 'Unable to load tasks.'; });
