"""驗證修正版 — 抓 GCF 卡片 article 完整區塊 + 5 條 URL"""
import re, os
root = r"C:/Users/user/WorkBuddy/2026-08-27-23-46-24/English-site"
n = open(root+"/news.html", encoding="utf-8").read()

# 找 GCF 卡 (用 src=gcf-group.jpg 為錨點)
m = re.search(
    r'(<article class="news-card">\s*<img[^>]+src="img/gcf-group\.jpg".*?</article>)',
    n, re.S)
print("[1] GCF card 抓到 :", bool(m))
block = m.group(1) if m else ""

# 5 條 URL 必須在 GCF card 內
urls_target = [
    "youtube.com/watch?v=cjnnhD7dAZc",
    "youtube.com/watch?v=gzLenQwUcdg",
    "macaodaily.com/html/2026-08/22/content_1928723",
    "hk.crntt.com/doc/1072/2/6/2/107226242",
    "jpchinapress.com/static/content/SS/2026-08-21/1540430688623401072",
]
print("[2] 5 條 URL 在 GCF 卡 card-media 中:")
all_ok = True
for u in urls_target:
    ok = u in block
    print(f"    [{'OK' if ok else '!!MISS'}] {u}")
    all_ok &= ok
print("    全部到位:", all_ok)

# card-media <li> 數量
li_count = block.count("<li>")
print("[3] GCF 卡 card-media <li> 數量 (應 5):", li_count)

# href list (確認 5 個都是 target=_blank rel=noopener + 5 條)
hrefs = re.findall(r'<a href="([^"]+)" target="_blank" rel="noopener">([^<]+)</a>', block)
print("[3.1] GCF 卡全部 a 標籤:")
for href, label in hrefs:
    print(f"    - {label.strip()} -> {href}")

# 中文 (應為 0: 歷史哥/館長 已換為 History Bro / Notorious Gym Master)
zh = re.findall(r'[一-鿿㐀-䶿＀-￯]', block)
print(f"[4] GCF 卡中文字 (應為 0): {len(zh)} -> {''.join(zh) if zh else '(none)'}")

# gcf-cover.jpg 全文件引用 (應 0)
print("[5] gcf-cover.jpg 殘留 (應 0):", len(re.findall(r'gcf-cover\.jpg', n)))

# gcf-group.jpg 應在 news.html 出現 1 次 (cover)
print("[6] gcf-group.jpg 在 news.html 出現次數 (應 1):", len(re.findall(r'gcf-group\.jpg', n)))

# 其他 3 張新聞卡的時間 / cover / card-media 完全不動
print("[7] 4 張新聞卡時間:")
for dt, label in re.findall(r'<time class="news-date" datetime="([^"]+)">([^<]+)</time>', n):
    print(f"    {dt} -> {label}")

# gcf-group.jpg 檔案存在
p = root+"/img/gcf-group.jpg"
print("[8] img/gcf-group.jpg on disk:", os.path.getsize(p)//1024, "KB" if os.path.exists(p) else "MISSING")
