# English-site — Sean Own 英文個人站（Gary 風格）

純靜態 HTML/CSS 個人品牌站。排版、字體、配色、組件完全參考
[garyvaynerchuk.com](https://garyvaynerchuk.com) 的設定；名字（Sean Own / SEANOWN）
與圖像（卡通 SVG 頭像）替換為 Sean Own 本人，個人敘事口吻直接 copy Gary 的。

## 上線資訊
- **目標域名**：`ownsean.com`（已在 name.com 購買，AUTO-RENEWS 已開）
- **部署平台**：Netlify（Import from Git，連此 repo，push 即自動部署）
- **設計系統**：見 `DESIGN.md`（Berkeley Blue `#003262` + California Gold `#FDB515`）

## 頁面結構
| 檔案 | 頁面 |
|------|------|
| `index.html` | 首頁 |
| `about.html` | 關於 |
| `article.html` | 文章詳情 |
| `news.html` | News 列表 |
| `portfolio.html` | 作品集 |
| `speaking.html` | 演講邀約 |
| `contact.html` | 聯絡表單 |

## 兩站分離（鐵規）
本 repo 與中文站 **完全獨立**：
- 中文站：`seanown-website` repo ／ 域名 `seanown.org` ／ Netlify Site A
- 英文站：本 `English-site` repo ／ 域名 `ownsean.com` ／ Netlify Site B

兩者獨立 repo、獨立 Netlify site、獨立 DNS、獨立 domain，互不影響。

## 上線前待補（軒哥）
- [ ] 社交連結實際網址（contact / speaking 頁目前為 `#` 佔位）
- [ ] 聯絡信箱確認（目前用 `hello@seanown.org`）
- [ ] 表單接後端（三個表單皆 `onsubmit="return false;"` 假表單）
- [ ] 是否需多語言（目前英文站）

## 技術約束
純靜態、無 JS 動效、無影片自動播放、無滾動特效。
