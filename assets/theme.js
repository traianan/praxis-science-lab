(() => {
  const key = 'praxis-color-theme';
  const choices = ['light', 'black', 'system'];
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = value => choices.includes(value) ? value : 'system';
  let preference = 'system';
  try { preference = valid(localStorage.getItem(key)); } catch { /* Storage may be unavailable. */ }

  function apply() {
    const theme = preference === 'system' ? (system.matches ? 'black' : 'light') : preference;
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = theme === 'black' ? '#000000' : '#ffffff';
  }

  apply();
  system.addEventListener('change', () => {
    if (preference === 'system') apply();
  });

  document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('theme-select');
    select.value = preference;
    select.closest('.theme-control').hidden = false;
    select.addEventListener('change', () => {
      preference = valid(select.value);
      apply();
      try { localStorage.setItem(key, preference); } catch { /* Keep the choice for this page. */ }
    });
    window.addEventListener('storage', event => {
      if (event.key === key || event.key === null) {
        preference = valid(event.newValue);
        select.value = preference;
        apply();
      }
    });
  });
})();
