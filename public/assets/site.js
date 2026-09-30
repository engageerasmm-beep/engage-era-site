/* Engage Era — shared behaviour */
(function () {
  var LIVE = /(^|\.)eesmm\.com$|(^|\.)engageera\.(com|co)$|netlify\.app$/.test(location.hostname);

  // Today's date in the masthead
  var d = document.getElementById('today');
  if (d) { try { d.textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' }); } catch (e) {} }

  // Category filter chips
  var chips = document.querySelectorAll('.chip'), cards = document.querySelectorAll('[data-c]');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      cards.forEach(function (k) { k.hidden = !(c.dataset.f === 'all' || k.dataset.c.split(' ').indexOf(c.dataset.f) > -1); });
    });
  });

  // Forms: validate, then let Netlify Forms handle submission on the live site.
  document.querySelectorAll('form[data-netlify]').forEach(function (form) {
    var msg = form.querySelector('.formmsg');
    form.addEventListener('submit', function (e) {
      var missing = [].filter.call(form.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
      var email = form.querySelector('input[type=email]');
      if (missing.length) { e.preventDefault(); if (msg) { msg.className = 'formmsg'; msg.textContent = 'Please fill in the required fields.'; } missing[0].focus(); return; }
      if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)) { e.preventDefault(); if (msg) { msg.className = 'formmsg'; msg.textContent = 'Enter a valid email address.'; } email.focus(); return; }
      if (!LIVE) { e.preventDefault(); if (msg) { msg.className = 'formmsg ok'; msg.textContent = 'Preview: this form goes live when the site is deployed.'; } }
    });
  });

  // Placeholder artwork until real photography is in place
  var BLUE = [20, 102, 255], RED = [228, 38, 44], W = [244, 245, 250], SKY = [90, 174, 230];
  function c(a, o) { return 'rgba(' + a[0] + ',' + a[1] + ',' + a[2] + ',' + o + ')'; }
  function glow(g, x, y, r, col, o) { var gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, c(col, o)); gr.addColorStop(1, c(col, 0)); g.fillStyle = gr; g.fillRect(0, 0, g.canvas.width, g.canvas.height); }
  function base(g, w, h) { var gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#0d1236'); gr.addColorStop(1, '#05071a'); g.fillStyle = gr; g.fillRect(0, 0, w, h); }
  function shade(g, w, h) { var gr = g.createLinearGradient(0, h * 0.45, 0, h); gr.addColorStop(0, 'rgba(6,8,25,0)'); gr.addColorStop(1, 'rgba(6,8,25,.92)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); }
  function seeded(s) { return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }
  var arts = {
    ai: function (g, w, h, r) {
      base(g, w, h); glow(g, w * 0.5, h * 0.35, w * 0.8, BLUE, 0.7);
      g.strokeStyle = c(W, 0.45); g.lineWidth = 2;
      var pts = []; for (var i = 0; i < 18; i++) pts.push([w * (0.15 + r() * 0.7), h * (0.1 + r() * 0.5)]);
      pts.forEach(function (p, i) { var q = pts[(i * 7 + 3) % pts.length]; g.beginPath(); g.moveTo(p[0], p[1]); g.lineTo(q[0], q[1]); g.stroke(); });
      pts.forEach(function (p, i) { g.fillStyle = i === 4 ? c(RED, 1) : c(W, 0.9); g.beginPath(); g.arc(p[0], p[1], i === 4 ? 9 : 4, 0, Math.PI * 2); g.fill(); });
      shade(g, w, h);
    },
    founder: function (g, w, h) {
      var gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#2a2f55'); gr.addColorStop(1, '#070918'); g.fillStyle = gr; g.fillRect(0, 0, w, h);
      glow(g, w * 0.15, h * 0.2, w * 0.9, W, 0.22);
      g.fillStyle = '#05060f'; g.beginPath(); g.ellipse(w * 0.52, h * 0.36, w * 0.15, h * 0.13, 0, 0, Math.PI * 2); g.fill();
      g.beginPath(); g.ellipse(w * 0.52, h * 0.26, w * 0.17, h * 0.05, 0, Math.PI, 0); g.fill(); g.fillRect(w * 0.35, h * 0.25, w * 0.36, h * 0.025);
      g.beginPath(); g.moveTo(w * 0.05, h); g.quadraticCurveTo(w * 0.08, h * 0.54, w * 0.52, h * 0.52); g.quadraticCurveTo(w * 0.96, h * 0.54, w * 0.99, h); g.fill();
    },
    stage: function (g, w, h, r) {
      base(g, w, h);
      g.save(); g.globalCompositeOperation = 'lighter';
      for (var i = 0; i < 5; i++) { var x = w * (0.1 + i * 0.2); var gr = g.createLinearGradient(x, 0, w * 0.5, h * 0.8); var col = i % 2 ? BLUE : RED; gr.addColorStop(0, c(col, 0.6)); gr.addColorStop(1, c(col, 0)); g.fillStyle = gr; g.beginPath(); g.moveTo(x - 3, 0); g.lineTo(x + 3, 0); g.lineTo(w * 0.7, h * 0.85); g.lineTo(w * 0.3, h * 0.85); g.closePath(); g.fill(); }
      g.restore();
      g.fillStyle = '#03040d'; for (var j = 0; j < 30; j++) { g.beginPath(); g.arc(r() * w, h * (0.72 + r() * 0.1), w * 0.035, 0, Math.PI * 2); g.fill(); }
      g.fillRect(0, h * 0.78, w, h);
      shade(g, w, h);
    },
    grid: function (g, w, h) {
      base(g, w, h); glow(g, w * 0.5, h * 0.35, w * 0.9, BLUE, 0.6);
      var s = w * 0.2, ox = w * 0.18, oy = h * 0.1;
      for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) { g.fillStyle = c(W, 0.08 + ((i + j) % 3) * 0.06); g.fillRect(ox + i * (s + 8), oy + j * (s * 1.25 + 8), s, s * 1.25); }
      g.fillStyle = c(RED, 0.95); g.fillRect(ox + (s + 8), oy + (s * 1.25 + 8), s, s * 1.25);
      shade(g, w, h);
    },
    meta: function (g, w, h) {
      base(g, w, h); glow(g, w * 0.55, h * 0.45, Math.max(w, h) * 0.6, BLUE, 0.85);
      g.strokeStyle = c(W, 0.25); g.lineWidth = Math.min(w, h) * 0.03; g.beginPath(); g.arc(w * 0.55, h * 0.45, Math.min(w, h) * 0.36, 0, Math.PI * 2); g.stroke();
      g.fillStyle = c(W, 0.9); g.font = Math.round(Math.min(w, h) * 0.55) + 'px Anton, Impact, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$', w * 0.55, h * 0.47);
      shade(g, w, h);
    },
    studio: function (g, w, h) {
      base(g, w, h); glow(g, w * 0.2, h * 0.2, w, RED, 0.35); glow(g, w * 0.8, h * 0.3, w * 0.7, SKY, 0.45);
      g.fillStyle = '#04050f'; g.beginPath(); g.ellipse(w * 0.5, h * 0.36, w * 0.14, h * 0.13, 0, 0, Math.PI * 2); g.fill();
      g.beginPath(); g.moveTo(w * 0.1, h); g.quadraticCurveTo(w * 0.12, h * 0.52, w * 0.5, h * 0.5); g.quadraticCurveTo(w * 0.88, h * 0.52, w * 0.9, h); g.fill();
      shade(g, w, h);
    }
  };
  function draw() {
    var seed = 11;
    document.querySelectorAll('canvas[data-art]').forEach(function (cv) {
      var f = arts[cv.dataset.art];
      if (f) try { f(cv.getContext('2d'), cv.width, cv.height, seeded(seed += 97)); } catch (e) {}
    });
  }
  draw();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
})();
