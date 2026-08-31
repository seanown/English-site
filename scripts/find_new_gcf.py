"""列出 GCF 文件夹里 vs 已經上線的 gcf-*.jpg，找出還沒被用過的「新的」相片。"""
import os, glob
from PIL import Image

def phash(im, hash_size=8, hi_freq_factor=4):
    newsize = (hash_size * hi_freq_factor, hash_size * hi_freq_factor)
    im2 = im.convert("L").resize(newsize, Image.LANCZOS)
    px = list(im2.getdata())
    avg = sum(px) / len(px)
    return ''.join('1' if p > avg else '0' for p in px)

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

SRC = r"H:/桌面/2026全球華人網紅節/全球華人網紅節照片"
USED_DIR = r"C:/Users/user/WorkBuddy/2026-08-27-23-46-24/English-site/img"

# ① 加载在线 gcf-*.jpg
used = {}
for p in glob.glob(os.path.join(USED_DIR, "gcf-*.jpg")):
    name = os.path.basename(p)
    im = Image.open(p)
    used[name] = (phash(im), im.size, os.path.getsize(p) // 1024)

# ② 加载桌面文件夹
src = {}
for f in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, f)
    if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue
    im = Image.open(p)
    src[f] = (phash(im), im.size, os.path.getsize(p) // 1024, p)

# ③ 对每个源文件，找最像的 used
print("=== 桌面文件夹 18 张 vs 已上線 gcf-*.jpg phash 對照 ===\n")
print(f"{'source file':35s} {'src size':14s} {'src KB':>7s}  {'best match':18s} {'match size':12s} {'d':>3s}")
print("-" * 100)

results = []  # (d, src_name, best_used_name)
for sn, (sh, ssz, skb, sp) in src.items():
    best_d, best_used = 999, None
    for un, (uh, usz, ukb) in used.items():
        d = hamming(sh, uh)
        if d < best_d:
            best_d, best_used = d, un
    label = sn[:33]
    print(f"{label:35s} {str(ssz):14s} {skb:7d}  {best_used[:18]:18s} {str(used[best_used][1]):12s} {best_d:3d}")
    results.append((best_d, sn, best_used))

print("\n=== 按距離排序：距離 > 40 視為「新的」相片 ===\n")
NEW_THRESHOLD = 40
new_photos = sorted([(d, n, m) for (d, n, m) in results if d > NEW_THRESHOLD], key=lambda x: x[0])
for d, n, m in new_photos:
    p = src[n][3]
    sz = src[n][1]
    print(f"  d={d:3d}  {n}   ->  size={sz}  path={p}")

print(f"\n=== 新相片總數: {len(new_photos)} ===")

# ④ 為新相片生成建議檔名
print("\n=== 建議匯入為 gcf-g09, gcf-g10, ... ===")
for i, (d, n, m) in enumerate(new_photos, start=9):
    p = src[n][3]
    target = f"gcf-g{i:02d}.jpg"
    print(f"  {n:50s} -> {target}")
