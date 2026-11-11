/* Apply the saved/system theme before CSS paints to avoid a light-theme flash. */
(() => {
  let saved;
  try { saved = localStorage.getItem('afterbyte-theme'); } catch { /* Storage is optional. */ }
  document.documentElement.dataset.theme = saved === 'dark' || (!saved && matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
})();
