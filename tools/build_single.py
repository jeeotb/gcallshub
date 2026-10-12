#!/usr/bin/env python3
"""Đóng gói prototype thành 1 file index.html tự chứa (ở gốc repo).

Nhúng: CSS (ảnh trong CSS -> data URI), dc-lite.js, 25 màn hình, canvas.json,
và mọi ảnh/icon trong prototype/assets (data URI, mỗi file nhúng một lần).
Mở trực tiếp bằng trình duyệt, không cần server. Chạy lại script sau mỗi lần sửa prototype/.

    python3 tools/build_single.py
"""
import base64, json, mimetypes, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'prototype')
MIME = {'.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())


def read(rel):
    with open(os.path.join(P, rel), encoding='utf-8') as f:
        return f.read()


def js_json(obj):
    # an toàn khi đặt trong <script>: không để lọt chuỗi "</script"
    return json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


# 1) CSS: thay url(theme/..), url(deco/..) bằng data URI
css = read('assets/contacthub.css')
css = re.sub(r'url\((["\']?)((?:theme|deco|icons|people)/[^)"\']+)\1\)',
             lambda m: 'url("%s")' % data_uri(os.path.join(P, 'assets', m.group(2))), css)

# 2) Màn hình + danh sách màn
canvas = json.loads(read('canvas.json'))
screens = {f[:-len('.dc.html')]: read('screens/' + f) for f in canvas['order']}

# 3) Ảnh dùng trong màn hình: map "assets/..." -> data URI (mỗi file một lần)
used = set()
for src in screens.values():
    used.update(re.findall(r'assets/(?:icons|people|deco|theme)/[\w.\-]+|assets/[\w.\-]+\.(?:jpg|png|svg|webp)', src))
assets = {u: data_uri(os.path.join(P, u)) for u in sorted(used)}

# 4) dc-lite: thay đường dẫn ảnh khi đọc màn hình
lite = read('dc-lite.js')
lite = lite.replace("cache[name] = src.then(function (txt) { return parse(name, txt); });",
                    "cache[name] = src.then(function (txt) {\n        if (window.DC_ASSETS) txt = txt.replace(/assets\\/[\\w.\\/-]+/g, function (m) { return window.DC_ASSETS[m] || m; });\n        return parse(name, txt);\n      });")
assert 'DC_ASSETS' in lite

# 5) Khung iPhone (prototype/index.html): nhúng tất cả vào
shell = read('index.html')
shell = shell.replace('    <a href="gallery.html">Xem tất cả màn hình</a>\n', '')
data = ('<script>\nwindow.DC_SCREENS = %s;\nwindow.DC_CANVAS = %s;\nwindow.DC_ASSETS = %s;\n</script>\n'
        % (js_json(screens), js_json(canvas), js_json(assets)))
shell = shell.replace('<script src="dc-lite.js"></script>',
                      '<style>\n' + css + '\n</style>\n' + data + '<script>\n' + lite + '\n</script>')
assert 'src="dc-lite.js"' not in shell
out = os.path.join(ROOT, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(shell)
print('Đã tạo %s (%.0f KB, %d màn, %d ảnh)' % (out, os.path.getsize(out) / 1024, len(screens), len(assets)))
