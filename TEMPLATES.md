# TEMPLATES.md — 英文站（ownsean.com）新活動／新頁面標準片段

> 用途：每次要新增一個「活動報導頁」或「專欄頁」時，直接複製下面片段，換字換圖即可。
> 所有片段都遵守英文站鐵規：**純靜態、藍金（Berkeley Blue #003262 / California Gold #FDB515）Gary 風、前台 0 中文、照片下方不加 caption、列表一律 grid 直接排。**

---

## 0. 鐵規速查（動手前先讀）

| 項目 | 規則 |
|------|------|
| 語言 | 前台**全英文**；品牌名保留拼音（Feng Shen Music Festival / Materia Medica China），不寫中文。 |
| 日期 | **模糊處理**：新聞卡用 `Aug 2026`（`%Y-%m`），內文用 `In August 2026`，**不寫精確日**；精確日由用戶最終拍板。 |
| 圖說 | **一律不加 `<figcaption>`**；照片本體照貼，照片內 banner 文字保留不動。 |
| 列表 | 人員／照片牆**直接 grid 排出**，不做 carousel / scroll-snap / 任何 JS 控制元件。 |
| 媒體連結 | sources 區塊**只放用戶提供的真實 URL**；沒有就空著，不編造媒體報導。 |
| 圖片 | 全部 WebP；`alt` 全英文、含地點＋事件＋日期（例：`...Macao, 2 June 2026`）。 |
| 動效 | 無影片自動播放、無滾動特效；hover 只換色。互動效果可用 vanilla JS（IIFE / defer / `data-*`），但先評估是否值得。 |

---

## 1. 頁面 HEAD（標準 boilerplate）

新增頁面請用 `scripts/enhance_heads.py` 自動補齊 preconnect / components.css / hreflang / og / Plausible / JSON-LD（冪等、可重跑）。手寫時照這份：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EVENT TITLE — Sean Own</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700;800&family=Open+Sans:wght@400;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/components.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="description" content="One-line English summary.">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sean Own">
<meta property="og:title" content="EVENT TITLE — Sean Own">
<meta property="og:description" content="One-line English summary.">
<meta property="og:image" content="https://ownsean.com/img/og/SLUG.jpg">
<meta property="og:url" content="https://ownsean.com/SLUG.html">
<link rel="canonical" href="https://ownsean.com/SLUG.html">
<link rel="alternate" hreflang="en" href="https://ownsean.com/SLUG.html">
<link rel="alternate" hreflang="zh-Hant" href="https://seanown.org/">
<link rel="alternate" hreflang="x-default" href="https://ownsean.com/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="EVENT TITLE — Sean Own">
<meta name="twitter:description" content="One-line English summary.">
<meta name="twitter:image" content="https://ownsean.com/img/og/SLUG.jpg">
<script defer data-domain="ownsean.com" src="https://plausible.io/js/script.js"></script>
</head>
```

OG 圖：`python scripts/generate_og.py`（會讀 `PAGES` dict 生成 `img/og/SLUG.jpg`，1200×630）。

---

## 2. NAV（每頁都要有；2026-09-02 起 Insights 不再列入）

```html
<nav class="nav">
  <div class="container nav-inner">
    <a href="index.html" class="logo" style="text-decoration:none;">SEAN<span>OWN</span></a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
    <label for="nav-toggle" class="nav-burger" aria-label="Toggle menu"><span></span><span></span><span></span></label>
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="news.html">News</a>
      <a href="portfolio.html">Work</a>
      <a href="speaking.html">Speaking</a>
      <a href="contact.html">Contact</a>
      <a href="index.html#subscribe" class="btn btn-accent">Subscribe</a>
    </div>
  </div>
</nav>
```

> ⚠️ Insights 入口已撤離頂部 NAV 與全站 footer（2026-09-02 拍板）。頁面 `insights.html` 仍存在（會長專欄原文），但僅由 `news.html` 的 insight 卡片作為唯一入口。

---

## 3. HERO

```html
<header class="hero">
  <div class="container">
    <div class="eyebrow">EVENT KICKER</div>
    <h1 class="display">Event Headline In Title Case</h1>
    <p class="gold-line">One punchy English line — Gary style, no fluff.</p>
  </div>
</header>
```

---

## 4. STAT GRID（數字要給，強化可信度）

```html
<div class="stat-grid">
  <div class="stat-card"><div class="stat-num">5</div><div class="stat-label">Strategic partnerships signed</div></div>
  <div class="stat-card"><div class="stat-num">2</div><div class="stat-label">Flagship IP rights locked</div></div>
</div>
```
`stat-grid` / `stat-card` / `stat-num` / `stat-label` 已定義在頁面 inline `<style>`（參考 about.html）。如用 components.css 類別，請改用 `.cards-3` + `.stat`。

---

## 5. GALLERY（零 JS、零 caption、grid 直排）

```html
<div class="gallery">
  <img loading="lazy" src="img/SLUG-g01.webp" alt="Sean Own on stage at VENUE, Macao, 2 June 2026">
  <img loading="lazy" src="img/SLUG-g02.webp" alt="Audience seated at VENUE, Macao, 2 June 2026">
</div>
```
規則：3 欄 grid（components.css 已定義，`<figure>` 包也可，但 `figcaption` 一律不寫）。

---

## 6. VENUE（互動 Google Maps，2026-09-03 起取代靜態 PNG）

```html
<h2>Venue</h2>
<figure class="venue">
  <iframe class="venue-map" src="https://maps.google.com/maps?q=VENUE+NAME&amp;z=15&amp;output=embed"
          title="Google Maps — VENUE NAME, ADDRESS, Macao" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  <a class="venue-link" href="https://www.google.com/maps/search/?api=1&amp;query=VENUE+NAME" target="_blank" rel="noopener">Open in Google Maps &#8599;</a>
</figure>
```
- 純 `<iframe>`（HTML 元素，**非 JS**），免 API key；Google 會自動重導向到 `google.com/maps/embed?pb=...` 渲染互動地圖。
- `VENUE NAME` 用 Google 可解析的地標名（如 `Macao+Science+Centre`）；要精準落針可改 `q=lat,lng`。
- 樣式在 `css/components.css` 的 `.venue` / `.venue-map` / `.venue-link`（藍金、直角、hover 換色）。
- 舊 `python scripts/generate_map.py` 靜態 PNG 流程已棄用（舊 `img/map/*.webp` 留作備援，未引用）。

---

## 7. SOURCES（只放真實 URL）

```html
<div class="source-link">
  Sources:
  <a href="https://REAL-URL" target="_blank" rel="noopener">Media Name →</a> &nbsp;
  <a href="https://REAL-URL-2" target="_blank" rel="noopener">Media Name (2) →</a>
</div>
```
⚠️ 沒有真實 URL 就**整段省略**，不要編造。

---

## 8. NEWS CARD（插入 news.html 的 `.news-grid`）

```html
<a class="news-card" href="SLUG.html">
  <div class="cover"><img loading="lazy" src="img/SLUG-cover.webp" alt="EVENT cover"></div>
  <div class="body">
    <div class="meta">Aug 2026 · Event</div>
    <h3>Event Headline</h3>
    <p>One-line English summary of the event.</p>
    <span class="read">Read →</span>
  </div>
</a>
```

---

## 9. CONTINUE EXPLORING（每頁 footer 前插入，強化內鏈）

```html
<section class="explore-block">
  <span class="kicker">Continue Exploring</span>
  <h2>More from Sean Own</h2>
  <div class="explore-grid">
    <a href="news.html" class="explore-card"><span class="ex-kicker">Latest</span><h3>News &amp; Press</h3><span class="ex-read">Read →</span></a>
    <a href="bay-youth-ai.html" class="explore-card"><span class="ex-kicker">Event</span><h3>Bay Youth AI Connects The World</h3><span class="ex-read">Read →</span></a>
    <a href="global-influencer-festival.html" class="explore-card"><span class="ex-kicker">Event</span><h3>Global Chinese Influencer Festival</h3><span class="ex-read">Read →</span></a>
    <a href="gba-leadership.html" class="explore-card"><span class="ex-kicker">Council</span><h3>GBA E-Commerce Leadership</h3><span class="ex-read">Read →</span></a>
  </div>
</section>
```

---

## 10. 自動化清單（新增一頁後照做）

1. 寫 `SLUG.html`（照上面片段）。
2. 把圖片壓成 WebP 放 `img/`，更新 `generate_og.py` 的 `PAGES` 加 `SLUG`。
3. 跑 `python scripts/enhance_heads.py`（補 preconnect/components/hreflang/og/plausible）。
4. 跑 `python scripts/generate_og.py`（生成 OG 圖）。
5. 在 `sitemap.xml` 加 `<url><loc>https://ownsean.com/SLUG.html</loc>...`。
6. 在 `news.html` 的 `.news-grid` 加新聞卡（照 §8）。
7. 新頁 NAV 請照 §2 手寫（**不要再帶 `<a href="insights.html">Insights</a>`**）。footer Go 區也照 §2 對齊。
8. `git add` 後交用戶 GitHub Desktop 推送（AI 不代推）。
