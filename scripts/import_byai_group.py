"""Import 5 missing group photos from GBA YOUTH PHOTO (select)
   - compress to 1280x960 q82 progressive JPG
   - auto-rotate to landscape if portrait
   - name byai-g09.jpg ~ byai-g13.jpg
   - group photo series, append after existing g08
"""
from pathlib import Path
from PIL import Image, ImageOps
import os

SRC = Path('H:/桌面/GBA YOUTH PHOTO (select)')
DST = Path('img')

# (source filename, target filename, default_event)
GROUP_SHOTS = [
    ('合照 (1).jpg', 'byai-g09.jpg', 'group photo 1'),
    ('合照 (2).jpg', 'byai-g10.jpg', 'group photo 2'),
    ('合照 (3).jpg', 'byai-g11.jpg', 'group photo 3'),
    ('合照 (4).jpg', 'byai-g12.jpg', 'group photo 4'),
    ('合照6.jpg',   'byai-g13.jpg', 'group photo 5'),
]

TW, TH = 1280, 960

for src_name, dst_name, label in GROUP_SHOTS:
    src_p = SRC / src_name
    if not src_p.exists():
        # try alternates (full-width parens etc.)
        alt = SRC / src_name.replace('(', '（').replace(')', '）')
        if alt.exists():
            src_p = alt
        else:
            print(f'[SKIP] not found: {src_name}')
            continue

    im = Image.open(src_p)
    # Auto-orient via EXIF
    im = ImageOps.exif_transpose(im)
    orig = im.size
    print(f'{src_name}: {orig}, mode={im.mode}')

    # Convert if needed
    if im.mode != 'RGB':
        im = im.convert('RGB')

    # Fit-cover onto 1280x960
    ratio = max(TW / im.size[0], TH / im.size[1])
    new_size = (int(im.size[0] * ratio), int(im.size[1] * ratio))
    im_resized = im.resize(new_size, Image.LANCZOS)

    # Center-crop
    left = (im_resized.size[0] - TW) // 2
    top = (im_resized.size[1] - TH) // 2
    im_final = im_resized.crop((left, top, left + TW, top + TH))

    out_p = DST / dst_name
    im_final.save(out_p, 'JPEG', quality=82, optimize=True, progressive=True)

    final_size = im_final.size
    kb = os.path.getsize(out_p) // 1024
    print(f'  -> {dst_name}: {final_size}, {kb} KB')

print('\nDone.')
