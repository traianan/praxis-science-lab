/* Fixed destination origin: preserve legacy paths, queries and fragments. */
(() => {
  const prefix = '/praxis-science-lab';
  let route = window.location.pathname;
  if (route === prefix) route = '/';
  else if (route.startsWith(prefix + '/')) route = route.slice(prefix.length);
  route = '/' + route.replace(/^\/+/, '');
  const target = 'https://praxissciencelab.app' + route + window.location.search + window.location.hash;
  window.location.replace(target);
})();
