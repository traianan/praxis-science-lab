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
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === 'black' ? '#000000' : '#ffffff';
    document.querySelectorAll('[data-theme-choice]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.themeChoice === preference));
    });
  }

  apply();
  system.addEventListener('change', () => {
    if (preference === 'system') apply();
  });

  function initialize() {
    const control = document.querySelector('.theme-control');
    if (!control) return;
    control.querySelectorAll('[data-theme-choice]').forEach(button => {
      button.addEventListener('click', () => {
        preference = valid(button.dataset.themeChoice);
        apply();
        try { localStorage.setItem(key, preference); } catch { /* Keep the choice for this page. */ }
      });
    });
    apply();
    control.hidden = false;
    window.addEventListener('storage', event => {
      if (event.key === key || event.key === null) {
        preference = valid(event.newValue);
        apply();
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
