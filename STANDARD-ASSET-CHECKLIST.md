# STANDARD-ASSET-CHECKLIST.md — 每個活動／新頁面交付前必備素材清單

> 配合 `scripts/make_event.py` 使用。用戶（軒哥）提供下列素材後，AI 才能產出符合英文站鐵規的頁面。
> 缺項就先標 `⚠️ 待補`，不要自行編造或留空連結。

---

## A. 基本資訊（文字）

- [ ] **活動中文名 / 英文名**（英文名全站統一，例：Bay Youth AI Connects The World）
- [ ] **slug**（英文、短橫連接，例：`bay-youth-ai`）→ 決定檔名 `SLUG.html` 與 OG 圖 `img/og/SLUG.jpg`
- [ ] **模糊日期**（`Aug 2026` / `2026` / `20 August 2026` 暫定，最終由用戶拍板）
- [ ] **一句英文 summary**（用於 meta description / og:description / news 卡）
- [ ] **hero kicker**（例：`Event` / `Forum` / `Summit`）
- [ ] **3–6 組數字**（stat，含 num + label，英文）
- [ ] **場地名 + 地址**（用於場地卡與 alt）
- [ ] **真實媒體 URL**（sources 區塊，沒有不寫）

## B. 圖片素材（H 盤原檔 → 壓成 WebP）

- [ ] **cover 圖 1 張**（新聞卡用，建議人比讚合照等吸睛主視覺）
- [ ] **gallery 圖 N 張**（活動照牆，直接 grid；建議 8–13 張）
- [ ] 命名規範：`SLUG-cover.webp`、`SLUG-g01.webp`、`SLUG-g02.webp` ...
- [ ] 壓圖：`python scripts/convert_webp.py` 或手動 Pillow `quality=82, method=6`
- [ ] **EXIF 方向校正**：手機直拍先 `ImageOps.exif_transpose` 再存，儲前重讀校驗（天花板在上、人臉正立）

## C. 場地卡（靜態，無 JS）

- [ ] 跑 `python scripts/generate_map.py` 生成 `img/map/VENUE-SLUG.webp`（1200×600）
- [ ] 頁面 `<figure class="venue">` 引用，**不加 caption**

## D. OG 分享圖

- [ ] 在 `scripts/generate_og.py` 的 `PAGES` 加 `"SLUG": "Page Title"`
- [ ] 跑 `python scripts/generate_og.py` → 產出 `img/og/SLUG.jpg`

## E. 自動化產出（make_event.py 一鍵）

- [ ] `python scripts/make_event.py --spec event.json` → 生成 `SLUG.html` + 注入 news 卡
- [ ] 執行後再跑 `enhance_heads.py` 確保 head 標記一致

## F. 上線前最終檢查

- [ ] 前台 0 中文（品牌拼音例外）
- [ ] 無 `<figcaption>`
- [ ] 無 carousel / scroll-snap / JS 控制元件
- [ ] 所有 `alt` 全英文含地點＋日期
- [ ] `sitemap.xml` 已加該頁
- [ ] NAV 含 Insights（新頁照 TEMPLATES.md §2）
- [ ] `git add` 後交用戶 GitHub Desktop 推送
