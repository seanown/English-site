# DESIGN.md — GaryVee 風格靜態個人品牌設計系統（Berkeley Blue & Gold 版）

> 參考對象：garyvaynerchuk.com（Gary Vaynerchuk 個人官網）
> 主色調：**Berkeley Blue `#003262` + California Gold `#FDB515`**（UC Berkeley 官方配色）
> 字體：**直接沿用 Gary 官網字體** — 顯示字 Bebas Neue、內文 Inter、輔助 Open Sans / Oswald
> 模式：**純靜態（Static-First）** — 無 JavaScript 動畫、無自動播放影片、無滾動動效、無動態載入。
> 頭像策略：**卡通插畫頭像（Cartoon Avatar）** 取代所有實拍人物照片。
> 本文件遵循 awesome-design-md 9 章節標準結構，供 AI 編程代理直接消費。

---

## 1. Visual Theme & Atmosphere（視覺主題與氛圍）

**設計哲學**：大膽、真實、能量爆發，但披上 Berkeley 的學院權威外衣。這是一個「自我品牌」網站，視覺語言要像一面揮舞的旗幟——高對比、不容忽視、說話很大聲。骨架極簡，但情緒極強。藍底金字（Berkeley 經典組合）帶來「可信又有衝勁」的雙重氣質。

**視覺基調**：High-Contrast Minimalism（高對比極簡）。Berkeley Blue 與 California Gold 構成絕對主體，白做平衡；金色只做強調與行動呼喚，藍色做結構與深色區塊。

**核心視覺特徵關鍵詞**：
1. `High-Contrast` 高對比 — 深藍底配亮金字，或白底配深藍字
2. `Bold-Type` 巨幅粗體 — Bebas Neue 全大寫窄體大標，佔滿視線
3. `Berkeley-Prestige` 學院權威 — 藍金配色自帶可信與經典感
4. `Flat-Skeleton` 扁平骨架 — 純扁平，輕陰影
5. `Gold-Accent` 金色點綴 — 金只用在 CTA 與關鍵詞

**光影與質感傾向**：純扁平（Flat）為主，允許極輕的微陰影（shadow-sm）做卡片層次；不使用毛玻璃、不使用漸變光暈。質感來自「對比」而非「裝飾」。

---

## 2. Color Palette & Roles（調色板與角色）

| 角色 | 名稱 | HEX | CSS 變數 | 使用場景 |
|------|------|-----|----------|----------|
| Primary | Berkeley Blue | `#003262` | `--color-primary` | 主結構色、深色區塊背景、主按鈕 |
| Primary Hover | 深藍 | `#001B3A` | `--color-primary-hover` | 主按鈕 hover/active |
| Accent | California Gold | `#FDB515` | `--color-accent` | CTA、關鍵強調詞、連結 hover、金色按鈕 |
| Accent Hover | 深金 | `#FC9313` | `--color-accent-hover` | 金色按鈕 hover |
| Blue Dark | 最深藍 | `#010133` | `--color-blue-dark` | overlay 遮罩、最深層 |
| Blue Medium | 中藍 | `#004AAE` | `--color-blue-medium` | 插畫/圖表輔色 |
| Gold Dark | 深金 | `#C4820E` | `--color-gold-dark` | 暗底上的金色文字、深金描邊 |
| Founders Rock | 淺藍 | `#3B7EA1` | `--color-founders` | 插畫輔色、分隔 |
| White | 純白 | `#FFFFFF` | `--color-white` | 主背景、深色區塊內文字 |
| Surface Alt | 淺灰底 | `#F4F4F4` | `--color-surface-alt` | 交替區塊背景、卡片底 |
| Gray Mid | 中灰 | `#9A9A9A` | `--color-gray-mid` | 次要文字、placeholder |
| Gray Deep | 深灰 | `#2B2B2B` | `--color-gray-deep` | 淺色區塊內的次要標題 |
| Border | 邊框灰 | `#E0E0E0` | `--color-border` | 卡片/輸入框邊界 |
| Success | 成功綠 | `#1F9D55` | `--color-success` | 表單成功狀態（功能色，例外） |
| Warning | 警告黃 | `#E0A800` | `--color-warning` | 提示標籤（功能色，例外） |
| Error | 錯誤紅 | `#D7263D` | `--color-error` | 表單錯誤（功能色，例外） |
| Info | 資訊藍 | `#1E6FE0` | `--color-info` | 資訊標籤（功能色，例外） |

**Shadow Colors（陰影色，含 rgba）**：
```css
--shadow-color-sm: rgba(1, 27, 58, 0.08);
--shadow-color-md: rgba(1, 27, 58, 0.12);
--shadow-color-lg: rgba(1, 27, 58, 0.18);
```

**使用守則**：金色不得用於大面積背景（除非整屏 CTA 區）；金色只出現在「可點擊」或「想被看見」的元素（按鈕、連結 hover、關鍵詞）。深藍區塊（Berkeley Blue 底）與白/淺灰區塊必須交替出現，形成節奏。藍底金字是最高對比組合，優先用於英雄區與整屏 CTA。

---

## 3. Typography Rules（排版規則）

**字體來源（Gary 官網實際載入字體，Google Fonts 直接引用）**：
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700;800&family=Open+Sans:wght@400;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
```

**Font Family**：
```css
--font-display: "Bebas Neue", "Arial Narrow", Impact, sans-serif; /* 大標：Gary 招牌窄體全大寫 */
--font-body: "Inter", "Helvetica Neue", Arial, sans-serif;        /* 內文 */
--font-alt: "Open Sans", "Helvetica Neue", Arial, sans-serif;     /* 輔助 */
--font-condensed: "Oswald", "Arial Narrow", sans-serif;           /* 次標題窄體 */
```
> 這四款即 Gary 官網 CSS 中實際宣告的字體（Bebas Neue / Inter / Open Sans / Oswald）。顯示字一律 Bebas Neue，其字形天生全大寫、窄體、高挑，正是 Gary 網站「很酷」的視覺來源。若無法載入，回退 `Arial Narrow` / `Impact`。

**Type Scale（完整層級）**：

| 層級 | 用途 | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Display Hero | 英雄大標 | `clamp(56px, 10vw, 140px)` | 400* | 0.9 | `0.01em`（全大寫） |
| H1 | 主區塊標題 | `clamp(40px, 7vw, 80px)` | 400* | 0.95 | `0.01em`（全大寫） |
| H2 | 子區塊標題 | `clamp(30px, 5vw, 52px)` | 400* | 1.0 | `0.01em`（全大寫） |
| H3 | 卡片標題 | `24px` | 700 (Inter) | 1.2 | `0` |
| Body | 內文 | `17px` | 400 (Inter) | 1.6 | `0` |
| Small | 輔助文字 | `14px` | 500 (Inter) | 1.5 | `0.01em` |
| Nano | 標籤/版權 | `12px` | 600 (Inter) | 1.4 | `0.1em`（大寫） |

> \*Bebas Neue 為單字重（400）顯示字體，其「粗」來自字型本身的窄體筆畫，故 Display/H1/H2 統一用 Bebas Neue。所有 Bebas Neue 文字**強制 `text-transform: uppercase`**。

**設計哲學**：字重是情緒的開關。大標用 Bebas Neue 全大寫製造「招牌感」；內文維持 Inter 400 與 1.6 行高確保可讀。所有標籤類小字使用 `letter-spacing: 0.1em` + 大寫，帶出「徽章感」。

---

## 4. Component Stylings（組件樣式）

### Buttons（按鈕）
```css
/* Primary — Berkeley Blue 底白字，主結構行動色 */
.btn-primary {
  background: var(--color-primary); color: var(--color-white);
  border: 2px solid var(--color-primary); border-radius: 0; /* 直角，硬派 */
  padding: 16px 32px; font-family: var(--font-body); font-weight: 800; font-size: 16px;
  text-transform: uppercase; letter-spacing: 0.04em; cursor: pointer;
}
.btn-primary:hover { background: var(--color-primary-hover); border-color: var(--color-primary-hover); }

/* Accent — California Gold 底深藍字，最高對比 CTA */
.btn-accent {
  background: var(--color-accent); color: var(--color-primary);
  border: 2px solid var(--color-accent); border-radius: 0;
  padding: 16px 32px; font-weight: 800; font-size: 16px;
  text-transform: uppercase; letter-spacing: 0.04em; cursor: pointer;
}
.btn-accent:hover { background: var(--color-accent-hover); border-color: var(--color-accent-hover); color: var(--color-blue-dark); }

/* Secondary — 藍框白底 */
.btn-secondary {
  background: transparent; color: var(--color-primary);
  border: 2px solid var(--color-primary); border-radius: 0;
  padding: 16px 32px; font-weight: 800; text-transform: uppercase; cursor: pointer;
}
.btn-secondary:hover { background: var(--color-primary); color: var(--color-white); }

/* Ghost — 純文字連結按鈕 */
.btn-ghost { background: none; border: none; color: var(--color-primary); font-weight: 700; text-decoration: underline; }

/* Danger */
.btn-danger { background: var(--color-error); color: #fff; border: 2px solid var(--color-error); padding: 16px 32px; font-weight: 800; }
```
> 靜態規範：按鈕一律**直角（border-radius: 0）**，強化硬派街頭感；hover 只做顏色切換，不加 transform/位移動畫。

### Cards（卡片）
```css
.card {
  background: var(--color-white); border: 1px solid var(--color-border);
  border-radius: 0; padding: 24px;
  box-shadow: 0 1px 3px var(--shadow-color-sm);
}
.card:hover { box-shadow: 0 4px 12px var(--shadow-color-md); } /* 唯一允許的靜態 hover 反饋 */
```

### Inputs（輸入框）
```css
.input {
  width: 100%; padding: 14px 16px; font-size: 16px;
  border: 2px solid var(--color-border); border-radius: 0; background: #fff;
  color: var(--color-primary);
}
.input:focus { outline: none; border-color: var(--color-accent); }
.input::placeholder { color: var(--color-gray-mid); }
```

### Navigation（頂部導航）
```css
.nav {
  background: var(--color-primary); color: var(--color-white);
  height: 64px; display: flex; align-items: center; padding: 0 24px;
  position: sticky; top: 0; z-index: 100;
}
.nav a { color: var(--color-white); font-family: var(--font-body); font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; margin: 0 16px; }
.nav a:hover { color: var(--color-accent); } /* 活躍/hover 用金 */
```

### Badges / Tags（標籤）
```css
.badge {
  display: inline-block; padding: 4px 10px; font-size: 12px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.1em; border-radius: 0;
  background: var(--color-primary); color: var(--color-white);
}
.badge--gold { background: var(--color-accent); color: var(--color-primary); }
```

### Modals / Dialogs（對話框，純 CSS 靜態顯示）
```css
.modal-overlay { background: rgba(1,1,51,0.6); position: fixed; inset: 0; z-index: 200; display: flex; align-items: center; justify-content: center; }
.modal-content { background: #fff; padding: 32px; max-width: 480px; border-top: 6px solid var(--color-accent); }
```
> 靜態站點若無 JS，對話框預設以 `:target` 或純展示區塊呈現，不下拉動畫。

### 🎨 Cartoon Avatar（卡通插畫頭像 — 取代實拍照片）
**規範**：所有人物呈現一律使用卡通插畫，禁止置入 Gary 或其他人的實拍照片。
- **風格**：扁平（Flat）插畫，粗輪廓線（stroke `3–4px`，色 `#003262` 或 `#0A0A0A`），有限調色（僅用 Berkeley Blue `#003262` / California Gold `#FDB515` / 白 `#FFFFFF` ＋1 個膚色替換色如 `#F2C9A0`）。
- **表情**：能量、自信、略帶街頭痞氣；可誇張化（大笑容、挑眉）。
- **占位模板**：用 SVG `<circle>` + `<path>` 構成頭/身，背景圓用 **Berkeley Blue `#003262`** 或 **California Gold `#FDB515`**，外圈描金/描藍。
- **尺寸**：頭像區統一 `width: 96px; height: 96px; border-radius: 50%;`（圓形裁切），描邊 `border: 3px solid var(--color-accent)`。
- **取用**：AI 代理生成時，直接產出內聯 SVG 卡通頭像，或引用 `assets/avatar-*.svg`，不得引用任何 `.jpg/.png` 實拍照。

---

## 5. Layout Principles（佈局原則）

**Spacing System（8px 基數）**：
```css
--space-1: 8px;  --space-2: 16px; --space-3: 24px; --space-4: 32px;
--space-5: 48px; --space-6: 64px; --space-7: 96px; --space-8: 128px;
```

**Grid System**：12 欄，`gap: 24px`，容器最大寬度 `1200px`。
```css
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.grid-12 { display: grid; grid-template-columns: repeat(12, 1fr); gap: 24px; }
```

**Section Spacing（區塊間距）**：每個大區塊上下 padding `var(--space-7)`（96px）；Berkeley Blue 深色區塊與白/淺灰區塊嚴格交替。

**留白哲學**：內容區飽滿（Gary 式資訊密度高），但區塊之間用大留白切換節奏；Bebas Neue 大標周圍留白要大，讓大標「呼吸」。

---

## 6. Depth & Elevation（深度與層級）

**Shadow System**：
```css
--shadow-xs: 0 1px 2px var(--shadow-color-sm);
--shadow-sm: 0 1px 3px var(--shadow-color-sm);
--shadow-md: 0 4px 12px var(--shadow-color-md);
--shadow-lg: 0 12px 32px var(--shadow-color-lg);
--shadow-2xl: 0 24px 64px rgba(1,27,58,0.24);
```

**Surface Layers**：
```
background(白 #FFF) → surface-alt(淺灰 #F4F4F4) → elevated(白卡+shadow-md) → overlay(深藍遮罩 rgba(1,1,51,.6))
```

**Z-index Scale**：
```css
--z-nav: 100; --z-modal: 200; --z-toast: 300;
```

**Backdrop Effects**：靜態站點**不使用** `backdrop-filter` 毛玻璃；層次只靠實色背景與陰影。

---

## 7. Do's and Don'ts（設計規範與禁忌）

**Do's（推薦）**
1. 深藍為主、金為點綴；藍底金字（Berkeley 經典）用於英雄區與整屏 CTA。
2. 大標一律 Bebas Neue 全大寫（Gary 招牌字），內文用 Inter。
3. 深色（Berkeley Blue）區塊與淺色區塊交替，形成視覺節奏。
4. 人物一律用卡通插畫頭像（SVG），保持藍金三色一致。
5. hover 只做顏色/陰影切換，不加位移、縮放、旋轉。
6. 內容用 12 欄網格對齊，保持結構秩序。
7. 標籤類小字用大寫 + `0.1em` 字距，強化徽章感。
8. 按鈕與卡片一律直角（`border-radius: 0`），硬派街頭感。

**Don'ts（禁忌）**
1. ❌ 不放任何實拍人物照片（Gary 本人或其他人）。
2. ❌ 不加 JavaScript 動畫、滾動視差、自動播放影片。
3. ❌ 不用毛玻璃、漸變光暈、柔和陰影做裝飾。
4. ❌ 不用圓角按鈕（Gary 式是硬直角）。
5. ❌ 金色不得鋪滿大面積背景（除整屏 CTA 區外）；藍可鋪大面積。
6. ❌ 不出現低對比灰字（次要文字也需 `#2B2B2B` 以上對比）。
7. ❌ 不堆砌裝飾圖示，留白即設計。
8. ❌ 不使用非 Gary 字體（嚴格限定 Bebas Neue / Inter / Open Sans / Oswald）。

---

## 8. Responsive Behavior（響應式行為）

**Breakpoints**：
```css
--bp-mobile: 480px;   /* 手機 */
--bp-tablet: 768px;   /* 平板 */
--bp-desktop: 1024px; /* 桌面 */
--bp-wide: 1440px;    /* 寬屏 */
```

**觸控目標**：所有可點擊元素最小 `44px × 44px`。

**折疊策略**：
- 桌面：12 欄，英雄區雙欄（左 Bebas Neue 大標右卡通頭像），三大標語卡 3 欄並排，新聞網格 3 欄。
- 平板（≤768px）：標語卡降為 1–2 欄，新聞網格 2 欄，導航收為横滑或簡化。
- 手機（≤480px）：全部單欄堆疊；英雄大標 `clamp` 自動縮小；導航隱藏次要連結，僅留 Logo + 主 CTA。

**Font Scaling**：Bebas Neue 標題用 `clamp()` 流體縮放；內文在手機維持 `16–17px` 不低於 15px。

---

## 9. Agent Prompt Guide（AI 代理提示指南）

**Quick Reference（快速參考）**
- 配色：Berkeley Blue `#003262` / California Gold `#FDB515` / 白 `#FFFFFF`
- 字體：顯示 Bebas Neue（全大寫）/ 內文 Inter / 輔助 Open Sans / 窄體 Oswald
- 形狀：全直角 `border-radius: 0`
- 頭像：卡通 SVG 插畫，禁實拍照
- 模式：純靜態，無 JS 動畫

**Component Prompts（可直接複製的組件生成提示）**
1. 「生成一個 GaryVee 風格英雄區：Berkeley Blue 深藍底、白色 Bebas Neue 全大寫巨幅標題、一句 California Gold 金色強調副標、右下角一個卡通插畫頭像（SVG，粗藍輪廓＋金底圓），純 CSS 無動畫。」
2. 「做三張並排標語卡（BUILDS BUSINESSES / DAY TRADES ATTENTION / CREATES MEANINGFUL IP），白底深藍字、直角邊框、hover 僅加深陰影，每張配一個藍金卡通圖示 SVG。」
3. 「生成頂部導航：Berkeley Blue 底白字、sticky、連結大寫粗體、hover 變金，含一個 California Gold 直角 CTA 按鈕（藍字）。」
4. 「做一個新聞/文章卡片網格（3 欄），每張含卡通封面圖 SVG、金色分類 badge、Bebas Neue 標題、摘要、『READ THIS』金色連結。」
5. 「生成頁尾：Berkeley Blue 底、白字、三欄（ABOUT / SOCIAL / SUBSCRIBE）、訂閱輸入框＋金色直角按鈕（藍字），底部版權小字大寫。」
6. 「做一個整屏 CTA 區：California Gold 金底、Berkeley Blue 巨標『LEGACY IS GREATER THAN CURRENCY.』、深藍直角次按鈕，無動畫。」

**Iteration Guide（AI 生成 UI 時的迭代建議）**
1. 先定對比：確認每屏不是深藍就是白/淺灰，金只在關鍵處。
2. 大標不夠帥就換 Bebas Neue 全大寫，字級拉到 `clamp` 上限 140px。
3. 看到圓角就改 `border-radius: 0`。
4. 看到實拍圖立刻換成卡通 SVG 頭像（藍金三色）。
5. 任何 `transform`/`@keyframes`/`transition` 動畫一律移除，只留 `:hover` 顏色/陰影。
6. 檢查藍底金字對比是否足夠；金底則用深藍字確保可讀。
7. 用手機斷點（480px）測單欄堆疊是否仍清晰。
8. 確認字體載入 `<link>` 含 Bebas Neue / Inter / Open Sans / Oswald 且 `display=swap`。
9. 區塊間距用 `--space-7`(96px) 保持呼吸感。
10. 交付前跑一遍 Do's/Don'ts 清單自檢。
