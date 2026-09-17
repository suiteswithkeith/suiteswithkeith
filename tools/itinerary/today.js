(function () {
  // Collapse the confirmations by default; they stay open without JS and in print.
  var fold = document.querySelector('.jc-fold');
  if (fold) {
    if (location.hash !== '#confirmations') fold.open = false;
    window.addEventListener('beforeprint', function () { fold.dataset.was = fold.open ? '1' : ''; fold.open = true; });
    window.addEventListener('afterprint', function () { fold.open = !!fold.dataset.was; });
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href="#confirmations"]');
      if (a) fold.open = true;
    });
  }
  // Highlight today, on wine country time.
  var today;
  try { today = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Los_Angeles' }).format(new Date()); } catch (err) { return; }
  document.querySelectorAll('[data-date="' + today + '"]').forEach(function (el) {
    el.classList.add('today');
    var tag = el.querySelector('.jc-today'); if (tag) tag.hidden = false;
  });
})();
