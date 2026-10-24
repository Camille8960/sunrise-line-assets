# 昇揚展覽 每週社群貼文 作業手冊

排程每週六 09:00（台北）自動執行，目標是產出「下週二、三、四」三篇 IG + FB 草稿（共 6 則），放進 Metricool 草稿，由 Camille 週日審核。

## 目標
吸引**台灣 AI／資安廠商報名參展**，不是單純市場評論。每篇都要讓讀者看完想詢問展位。

## 固定資料
- Metricool 品牌：昇揚展覽 Sunrise Expo，`blogId` = `6989429`
- 發文時間：週二、三、四 08:30（Asia/Taipei），`draft: true`、`autoPublish: true`
- 三個展：
  - 週二 AI EXPO KOREA　https://sunriseexpo.com/event/aiexpokorea/
  - 週三 AI Asia　https://sunriseexpo.com/event/ai-asia/
  - 週四 Cybersec Asia　https://sunriseexpo.com/event/cybersec-asia/
  （網址以官網實際頁面為準，先 WebFetch 確認；如連結失效，改用 https://sunriseexpo.com/）
- 洽詢：LINE 搜尋 `@225imowp`／https://lin.ee/ldTgBgo／表單 https://sunriseexpo.com/contact/
- 圖庫（公開 repo，只能放圖和版型）：`Camille8960/sunrise-line-assets`，圖放 `social/<週二日期>/`
  公開網址：`https://raw.githubusercontent.com/Camille8960/sunrise-line-assets/main/social/<週二日期>/<檔名>.png`

## 每週步驟
1. **查證資料**：用 WebFetch／WebSearch 讀三個展的官網與主辦單位頁面、近期產業新聞。每個數字都要對到來源；對不到來源就不要用。
2. **選本週角度**（每個展不要連兩週同一角度，先看 `social/` 資料夾與 Metricool 近期貼文避免重複）：
   買家數據／展區亮點／台灣館／報名倒數（距離開展週數）／市場觀察（只在能連到「為什麼要參展」時用）
3. **寫 posts JSON**：格式見 `social/tools/example_posts_2026-10-27.json`。每篇 4 張：
   封面（大標＋副標）、4 個數字卡、3 個要點、CTA（日期地點＋洽詢＋資料來源）。
4. **產圖**：`python3 -I social/tools/render_slides.py <posts.json> <輸出資料夾>`
   （需 Python Playwright 與 Noto Sans CJK TC；環境已預裝。版面溢出就縮減文字，不要改版型。）
   產完用 Read 看過每一張，確認沒有文字被截斷或壓到頁尾。
5. **推圖到 repo**：複製到 `social/<週二日期>/`，commit、push main。
6. **建 Metricool 草稿**（6 則）：`createScheduledPost`，`blogId` 6989429。
   - `date`：`YYYY-MM-DDT08:30:00+08:00`
   - `info` 為 JSON 字串：`{"autoPublish":true,"draft":true,"firstCommentText":"","hasNotReadNotes":false,"media":[4 張公開網址],"providers":[{"network":"instagram"|"facebook"}],"publicationDate":{"dateTime":"YYYY-MM-DDT08:30:00","timezone":"Asia/Taipei"},"shortener":false,"text":"…", 以及 IG 的 "instagramData":{"type":"POST","autoPublish":true,"showReelOnFeed":true,"isAiGenerated":false} 或 FB 的 "facebookData":{"type":"POST"}}`
   - IG 一定要有 media，否則 `INSTAGRAM:MISSING_MEDIA`。
   - 修改用 `updateScheduledPost`，需目前的 `id` 與 `uuid`（id 每次更新會變），並重送完整內容。
7. **回報**：用 `getScheduledPosts` 確認 6 則都在，列出每則的 ID、日期、文字開頭，並標出「無法查證而略過」的項目。

## 文字規範
- 繁體中文，不用簡體。
- **FB**：約 500–700 字。開頭【參展情報】＋一句重點；條列 3–5 個已查證數據；說明明年展期與地點、買家是誰；結尾 CTA 與三個連結；資料來源；5–6 個 hashtag。
- **IG**：短文案（約 100–150 字）＋「左滑看完整重點 →」＋「LINE 搜尋 @225imowp，或點個人檔案連結洽詢」＋資料來源＋hashtag。IG 貼文不放可點擊連結。
- 前綴固定 `#SunriseExpo`，再加展會與主題標籤。

## 不可違反
- **只用查得到來源的事實**。數字、日期、國家、主管機關說法都要對到原始頁面。查不到就略過，並在回報中列出。不可推測、不可寫「某某工具被用於攻擊」之類未確認的說法。
- 不寫展位價格、報名截止日、補助金額，除非官方頁面明確載有；否則 CTA 一律導向 LINE／表單詢問。
- 台灣官方代理身分：AI EXPO KOREA 為昇揚展覽台灣官方代理；Cybersec Asia、AI Asia 以官網寫法為準，不自行升級稱呼。
- 不公開任何價格、客戶名單、付款資訊；此 repo 為公開。
- 一律維持草稿，**不要**改成直接發布。
- 舊稿（日期已過、未發布的草稿）不要刪，只在回報中列出供 Camille 處理。

## 已知限制
- 展覽官網資訊有時是上一屆數據，文案要寫明「2026 年數據」，並把明年日期另外寫。
- 若 GitHub 推送或 Metricool 授權失敗，停止並在回報最前面說明失敗點，不要用其他圖床取代。
