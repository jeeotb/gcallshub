// dc-lite — trình hiển thị tối giản cho các file mockup *.dc.html.
// Hỗ trợ: {{ path }}, <sc-if>, <sc-for>, <dc-import>, sự kiện onClick/onChange/...,
// state + setState, và link giữa các màn (<a href="X.dc.html">).
// Chỉ dùng để XEM mockup, không phải code production.
(function () {
  'use strict';

  var cache = {};       // name -> Promise<def>
  var helmetDone = {};  // name -> true
  var defs = {};
  var night = false;     // giao diện tối: thêm class night cho mọi .app

  function applyTheme(root) {
    root.querySelectorAll('.app').forEach(function (a) {
      a.classList.add('lt');
      a.classList.toggle('night', night);
    });
  }        // name -> def, filled once a file and its imports are loaded

  function DCLogic(props) {
    this.props = props || {};
    this.state = {};
  }
  DCLogic.prototype.setState = function (patch) {
    var p = typeof patch === 'function' ? patch(this.state, this.props) : patch;
    this.state = Object.assign({}, this.state, p);
    if (this.__rerender) this.__rerender();
  };
  DCLogic.prototype.forceUpdate = function () { if (this.__rerender) this.__rerender(); };

  function load(name) {
    if (!cache[name]) {
      var src = window.DC_SCREENS
        ? (window.DC_SCREENS[name] != null ? Promise.resolve(window.DC_SCREENS[name]) : Promise.reject(new Error('Không có màn ' + name)))
        : fetch('screens/' + name + '.dc.html').then(function (r) {
            if (!r.ok) throw new Error('Không tải được ' + name);
            return r.text();
          });
      cache[name] = src.then(function (txt) { return parse(name, txt); });
    }
    return cache[name];
  }

  function parse(name, txt) {
    var doc = new DOMParser().parseFromString(txt, 'text/html');
    var xdc = doc.querySelector('x-dc');
    var helmet = xdc.querySelector('helmet');
    var headLinks = Array.prototype.slice.call(doc.head.querySelectorAll('link[rel="stylesheet"]'));
    if (helmet) helmet.parentNode.removeChild(helmet);
    var script = doc.querySelector('script[data-dc-script]');
    var Klass = DCLogic;
    if (script) {
      Klass = new Function('DCLogic', script.textContent + '\n;return Component;')(DCLogic);
    }
    var title = doc.title;
    var def = { name: name, template: xdc, helmet: helmet, headLinks: headLinks, Klass: Klass, title: title, imports: [] };
    xdc.querySelectorAll('dc-import').forEach(function (n) { def.imports.push(n.getAttribute('name')); });
    return Promise.all(def.imports.map(load)).then(function () { defs[name] = def; return def; });
  }

  function installHead(def) {
    if (helmetDone[def.name]) return;
    helmetDone[def.name] = true;
    if (!window.DC_SCREENS) def.headLinks.forEach(function (l) {
      var href = l.getAttribute('href');
      if (!document.querySelector('link[href="' + href + '"]')) {
        var n = document.createElement('link'); n.rel = 'stylesheet'; n.href = href; document.head.appendChild(n);
      }
    });
    if (def.helmet) {
      Array.prototype.forEach.call(def.helmet.children, function (c) {
        if (c.tagName === 'LINK' && document.querySelector('link[href="' + c.getAttribute('href') + '"]')) return;
        document.head.appendChild(c.cloneNode(true));
      });
    }
  }

  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var WHOLE = /^\s*\{\{\s*([^}]+?)\s*\}\}\s*$/;

  function lookup(path, scope) {
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (path === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    if (/^'.*'$|^".*"$/.test(path)) return path.slice(1, -1);
    var parts = path.split('.');
    var v = scope;
    for (var i = 0; i < parts.length; i++) {
      if (v == null) return undefined;
      v = v[parts[i]];
    }
    return v;
  }
  function interp(str, scope) {
    return str.replace(HOLE, function (_, p) { var v = lookup(p, scope); return v == null ? '' : String(v); });
  }

  var EVENTS = { onclick: 'click', onchange: 'input', oninput: 'input', onmouseenter: 'mouseenter', onmouseleave: 'mouseleave', onfocus: 'focus', onblur: 'blur', onkeydown: 'keydown', onsubmit: 'submit' };

  // Render one component instance into a DocumentFragment.
  function Instance(def, props, onNavigate) {
    this.def = def;
    this.onNavigate = onNavigate;
    this.logic = new def.Klass(props || {});
    if (!this.logic.state) this.logic.state = {};
    this.children = {};
    this.root = document.createElement('div');
    this.root.className = 'dc-root';
    var self = this;
    var pending = false;
    this.logic.__rerender = function () {
      if (pending) return;
      pending = true;
      Promise.resolve().then(function () { pending = false; self.render(); });
    };
    installHead(def);
  }
  Instance.prototype.render = function () {
    var vals = (this.logic.renderVals && this.logic.renderVals()) || {};
    var focus = rememberFocus(this.root);
    var frag = document.createDocumentFragment();
    var self = this;
    var counter = { n: 0 };
    Array.prototype.forEach.call(this.def.template.childNodes, function (n) {
      self.walk(n, vals, frag, counter);
    });
    this.root.replaceChildren(frag);
    applyTheme(this.root);
    restoreFocus(this.root, focus);
    if (this.logic.componentDidMount && !this.mounted) { this.mounted = true; this.logic.componentDidMount(); }
    return this.root;
  };
  Instance.prototype.walk = function (node, scope, out, counter) {
    var self = this;
    if (node.nodeType === 3) {
      out.appendChild(document.createTextNode(interp(node.nodeValue, scope)));
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.tagName.toLowerCase();
    if (tag === 'sc-if') {
      var m = WHOLE.exec(node.getAttribute('value') || '');
      if (m && lookup(m[1], scope)) node.childNodes.forEach(function (c) { self.walk(c, scope, out, counter); });
      return;
    }
    if (tag === 'sc-for') {
      var lm = WHOLE.exec(node.getAttribute('list') || '');
      var list = (lm && lookup(lm[1], scope)) || [];
      var as = node.getAttribute('as') || 'item';
      list.forEach(function (item, i) {
        var s = Object.create(scope); s[as] = item; s.$index = i;
        node.childNodes.forEach(function (c) { self.walk(c, s, out, counter); });
      });
      return;
    }
    if (tag === 'dc-import') {
      var name = node.getAttribute('name');
      var key = name + '#' + (counter.n++);
      if (!this.children[key] && defs[name]) this.children[key] = new Instance(defs[name], {}, self.onNavigate);
      var ch = this.children[key];
      if (ch) out.appendChild(ch.render());
      return;
    }
    var el = node.namespaceURI === 'http://www.w3.org/2000/svg'
      ? document.createElementNS(node.namespaceURI, node.tagName)
      : document.createElement(tag);
    Array.prototype.forEach.call(node.attributes, function (a) {
      var nm = a.name, v = a.value;
      if (nm.indexOf('hint-') === 0) return;
      var lower = nm.toLowerCase();
      if (EVENTS[lower]) {
        var fm = WHOLE.exec(v);
        var fn = fm && lookup(fm[1], scope);
        if (typeof fn === 'function') el.addEventListener(EVENTS[lower], fn);
        return;
      }
      var wm = WHOLE.exec(v);
      var val = wm ? lookup(wm[1], scope) : (v.indexOf('{{') >= 0 ? interp(v, scope) : v);
      if (val === false || val == null) return;
      if (lower === 'value' && (tag === 'input' || tag === 'textarea')) { el.value = String(val); el.setAttribute('value', String(val)); return; }
      el.setAttribute(nm, val === true ? '' : String(val));
    });
    if (tag === 'a') {
      var href = node.getAttribute('href') || '';
      var dm = /^\/?([\w.-]+)\.dc\.html$/.exec(href);
      if (dm) {
        el.setAttribute('href', '?s=' + dm[1]);
        el.addEventListener('click', function (e) { e.preventDefault(); self.onNavigate(dm[1]); });
      }
    }
    var target = tag === 'template' ? el.content : el;
    node.childNodes.forEach(function (c) { self.walk(c, scope, target, counter); });
    if (tag === 'textarea' && el.hasAttribute('value')) el.value = el.getAttribute('value');
    out.appendChild(el);
  };

  function pathOf(root, el) {
    var p = [];
    while (el && el !== root) {
      var parent = el.parentNode; if (!parent) return null;
      p.unshift(Array.prototype.indexOf.call(parent.childNodes, el)); el = parent;
    }
    return el === root ? p : null;
  }
  function rememberFocus(root) {
    var a = document.activeElement;
    if (!a || !root.contains(a)) return null;
    return { path: pathOf(root, a), s: a.selectionStart, e: a.selectionEnd };
  }
  function restoreFocus(root, f) {
    if (!f || !f.path) return;
    var el = root;
    for (var i = 0; i < f.path.length && el; i++) el = el.childNodes[f.path[i]];
    if (el && el.focus) {
      el.focus();
      try { if (f.s != null) el.setSelectionRange(f.s, f.e); } catch (e) { /* not a text input */ }
    }
  }

  window.DcLite = {
    setNight: function (on) { night = !!on; applyTheme(document); },
    isNight: function () { return night; },
    mount: function (host, name, onNavigate, opts) {
      opts = opts || {};
      var anchor = opts.anchor || host;
      var leaving = opts.animate && host.firstChild
        ? new Promise(function (r) { anchor.classList.remove('dc-enter'); anchor.classList.add('dc-leave'); setTimeout(r, 230); })
        : Promise.resolve();
      return Promise.all([load(name), leaving]).then(function (res) {
        var def = res[0];
        var inst = new Instance(def, {}, onNavigate);
        var top = inst.render(); top.classList.add('dc-top');
        host.replaceChildren(top);
        if (opts.onRendered) opts.onRendered();
        anchor.classList.remove('dc-leave');
        void anchor.offsetWidth;
        anchor.classList.add('dc-enter');
        clearTimeout(anchor.__dcT);
        anchor.__dcT = setTimeout(function () { anchor.classList.remove('dc-enter'); }, 1100);
        document.title = def.title + ' · Gcalls ContactHub';
        return def;
      });
    }
  };
})();
