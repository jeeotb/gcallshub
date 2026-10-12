#!/usr/bin/env python3
"""Sinh bộ brand guideline và gói bàn giao Figma vào thư mục design/.

    python3 tools/build_brand.py [--artifact OUT.html]

Tạo ra:
  design/brand-guidelines.html   trang guideline tự chứa (mở trực tiếp)
  design/gcalls-tokens.json      token W3C DTCG (Figma Variables / Tokens Studio)
  design/assets/                 logo (tím, trắng, icon app), icon nét SVG, icon kính 3D PNG
"""
import base64, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, 'tools')
A = os.path.join(ROOT, 'prototype', 'assets')
D = os.path.join(ROOT, 'design')

ICONS = {  # bộ icon nét: lưới 24, nét 1.7, bo tròn
    'phone': 'M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z',
    'call-outgoing': 'M16 2h6v6M22 2l-7 7M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3',
    'call-incoming': 'M16 2v6h6M22 2l-6 6M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3',
    'call-missed': 'M16 2l6 6M22 2l-6 6M22 16.9v3a2 2 0 0 1-2.2 2A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3',
    'message': 'M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z',
    'reminder': 'M12 21a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM12 9v4l2 2M5 3 2 6M22 6l-3-3',
    'pin': 'M12 17v5M9 3h6l-1 7 4 4H6l4-4z',
    'search': 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-3.5-3.5',
    'bell': 'M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9M10.3 21a1.94 1.94 0 0 0 3.4 0',
    'home': 'M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z',
    'contacts': 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75',
    'history': 'M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5M12 7v5l3 2',
    'tasks': 'M9 11l3 3 8-8M20 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11',
    'filter': 'M4 6h16M7 12h10M10 18h4',
    'calendar': 'M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM16 2v4M8 2v4M3 10h18',
    'mic': 'M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3zM19 10v2a7 7 0 0 1-14 0v-2M12 19v3',
    'speaker': 'M11 5 6 9H2v6h4l5 4zM15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14',
    'hold': 'M8 5v14M16 5v14',
    'transfer': 'M17 2l4 4-4 4M3 11V10a4 4 0 0 1 4-4h14M7 22l-4-4 4-4M21 13v1a4 4 0 0 1-4 4H3',
    'keypad': 'M5 4h.01M12 4h.01M19 4h.01M5 10h.01M12 10h.01M19 10h.01M5 16h.01M12 16h.01M19 16h.01M12 21h.01',
    'user': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0',
    'back': 'm15 6-6 6 6 6',
    'close': 'M18 6 6 18M6 6l12 12',
    'offline': 'M2 2l20 20M8.5 16.4a5 5 0 0 1 7 0M5 12.9a10 10 0 0 1 5.2-2.8M19 12.9a10 10 0 0 0-2-1.5M12 20h.01',
}
ICON_VI = {'phone': 'Gọi', 'call-outgoing': 'Gọi đi', 'call-incoming': 'Gọi đến', 'call-missed': 'Gọi nhỡ', 'message': 'Nhắn tin',
           'reminder': 'Nhắc hẹn', 'pin': 'Ghim', 'search': 'Tìm kiếm', 'bell': 'Thông báo', 'home': 'Tổng quan', 'contacts': 'Danh bạ',
           'history': 'Lịch sử', 'tasks': 'Công việc', 'filter': 'Bộ lọc', 'calendar': 'Lịch', 'mic': 'Micro', 'speaker': 'Loa ngoài',
           'hold': 'Giữ máy', 'transfer': 'Chuyển tiếp', 'keypad': 'Bàn phím', 'user': 'Tài khoản', 'back': 'Quay lại', 'close': 'Đóng',
           'offline': 'Mất kết nối'}
DECO = ['missed-pink', 'unassigned-violet', 'overdue-yellow', 'today-mint']


def b64(path, mime):
    with open(path, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())


def icon_svg(d, color='#2A2838'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%s" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="%s"/></svg>' % (color, d))


def swatches(group, tokens):
    out = []
    for name, t in tokens['color'][group].items():
        if name.startswith('$'):
            continue
        hexv = t['$value']
        light = hexv.upper() in ('#FFFFFF', '#F3F3F6', '#FAF8FF', '#ECEAF4', '#F3F0FF', '#D9D1FF', '#FAD3EE', '#D9D3FF', '#FFE8A3', '#C8F2EA')
        fg = '#2A2838' if light else '#FFFFFF'
        desc = t.get('$description', '')
        out.append('<div class="swatch"><div class="chip" style="background:%s;color:%s">%s</div>'
                   '<div class="info"><b>%s</b><span class="code">%s</span><span>%s</span></div></div>'
                   % (hexv, fg, hexv.upper(), group + '/' + name, '--' + group + '-' + name, desc))
    return '\n    '.join(out)


TYPE_LABEL = {'page-title': ('Tiêu đề trang', 'Danh bạ'), 'display-number': ('Số lớn', '852'), 'sheet-title': ('Tiêu đề sheet', 'Trạng thái trực'),
              'section-title': ('Tiêu đề mục', 'Việc cần làm'), 'row-title': ('Tên dòng', 'Nguyễn Thiên – ĐH Quốc Tế'),
              'body': ('Chữ thân', 'Khách đã xác nhận, hẹn kỹ thuật đến lúc 15:00.'), 'button': ('Nút', 'Lưu kết quả'),
              'chip': ('Chip, phân đoạn', 'Gọi nhỡ 1'), 'caption': ('Chữ mô tả', '0901 234 567 · Gọi đi'), 'tag': ('Tag', 'Chưa nhận')}


def type_rows(tokens):
    rows = []
    for k, (label, sample) in TYPE_LABEL.items():
        v = tokens['typography'][k]['$value']
        style = 'font-size:%s;font-weight:%s;line-height:%s;letter-spacing:%s' % (v['fontSize'], v['fontWeight'], v['lineHeight'], v['letterSpacing'])
        rows.append('<div class="type-row"><div class="spec"><b>%s</b>%s / %s · %s</div><div style="%s">%s</div></div>'
                    % (label, v['fontSize'].replace('px', ''), v['fontWeight'], v['letterSpacing'], style, sample))
    return '\n    '.join(rows)


def main():
    tokens = json.load(open(os.path.join(T, 'brand_tokens.json'), encoding='utf-8'))
    html = open(os.path.join(T, 'brand_template.html'), encoding='utf-8').read()
    logo = b64(os.path.join(A, 'icons', 'logo-gcalls.svg'), 'image/svg+xml')
    html = html.replace('{{LOGO}}', logo)
    html = html.replace('{{AVATAR}}', b64(os.path.join(A, 'people', 'p2.jpg'), 'image/jpeg'))
    for n in DECO:
        html = html.replace('{{DECO:%s}}' % n, b64(os.path.join(A, 'deco', n + '.png'), 'image/png'))
    for g in ('brand', 'neutral', 'semantic', 'tile'):
        html = html.replace('{{SWATCHES:%s}}' % g, swatches(g, tokens))
    html = html.replace('{{TYPE_ROWS}}', type_rows(tokens))
    html = html.replace('{{ICONS}}', '\n    '.join(
        '<div><svg viewBox="0 0 24 24" aria-hidden="true"><path d="%s"/></svg>%s<span class="code">%s</span></div>' % (d, ICON_VI[k], k)
        for k, d in ICONS.items()))
    assert '{{' not in html, html[html.index('{{'):html.index('{{') + 40]

    # gói bàn giao
    os.makedirs(os.path.join(D, 'assets', 'icons'), exist_ok=True)
    os.makedirs(os.path.join(D, 'assets', 'logo'), exist_ok=True)
    os.makedirs(os.path.join(D, 'assets', '3d'), exist_ok=True)
    src_logo = open(os.path.join(A, 'icons', 'logo-gcalls.svg'), encoding='utf-8').read()
    open(os.path.join(D, 'assets', 'logo', 'gcalls-logo.svg'), 'w').write(src_logo)
    open(os.path.join(D, 'assets', 'logo', 'gcalls-logo-white.svg'), 'w').write(src_logo.replace('#673AB7', '#FFFFFF'))
    inner = src_logo[src_logo.index('>') + 1:src_logo.rindex('</svg>')].replace('#673AB7', '#FFFFFF')
    app_icon = ('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">'
                '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8D78FF"/><stop offset="1" stop-color="#673AB7"/></linearGradient></defs>'
                '<rect width="1024" height="1024" rx="229" fill="url(#g)"/>'
                '<g transform="translate(194.5 194.5) scale(1.0095)">%s</g></svg>' % inner)
    open(os.path.join(D, 'assets', 'logo', 'gcalls-app-icon.svg'), 'w').write(app_icon)
    for k, d in ICONS.items():
        open(os.path.join(D, 'assets', 'icons', k + '.svg'), 'w').write(icon_svg(d))
    for n in DECO:
        shutil.copy(os.path.join(A, 'deco', n + '.png'), os.path.join(D, 'assets', '3d', n + '.png'))
    shutil.copy(os.path.join(T, 'brand_tokens.json'), os.path.join(D, 'gcalls-tokens.json'))

    full = ('<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n%s\n</html>\n' % html.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1).rstrip() + '\n</body>')
    open(os.path.join(D, 'brand-guidelines.html'), 'w', encoding='utf-8').write(full)
    if '--artifact' in sys.argv:
        open(sys.argv[sys.argv.index('--artifact') + 1], 'w', encoding='utf-8').write(html)
    print('design/ OK:', len(ICONS), 'icon,', len(DECO), 'icon 3D, guideline %.0f KB' % (os.path.getsize(os.path.join(D, 'brand-guidelines.html')) / 1024))


if __name__ == '__main__':
    main()
