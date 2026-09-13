(() => {
  const tools = document.querySelector('.collection-tools');
  const search = document.querySelector('.app-search input');
  const count = document.querySelector('.collection-count');
  const cards = [...document.querySelectorAll('.portfolio-card')];
  if (!tools || !search || !count) return;
  let category = 'All';
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let shown = 0;
    cards.forEach(card => {
      const match = (category === 'All' || card.dataset.category === category) && card.textContent.toLocaleLowerCase().includes(query);
      card.hidden = !match;
      if (match) shown++;
    });
    count.textContent = shown ? `${shown} of ${cards.length} apps` : 'No apps found. Try another search or category.';
  }
  tools.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    tools.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    update();
  }));
  search.addEventListener('input', update);
  tools.hidden = false;
  count.hidden = false;
  update();
})();
