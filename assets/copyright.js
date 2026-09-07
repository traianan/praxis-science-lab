(() => {
  const startYear = 2026;
  const currentYear = new Date().getFullYear();
  const label = document.getElementById('copyright-years');
  if (label) {
    label.textContent = currentYear > startYear
      ? `${startYear}–${currentYear}`
      : String(startYear);
  }
})();
