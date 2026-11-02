# 昇揚展覽 每週社群貼文 作業手冊（長文輪播版，2026-11-02 起）

排程每週六早上（台北）自動執行，產出「下週二、三、四」三篇貼文，每篇 FB 與 IG 各一，共 6 則，全部放進 Metricool **草稿**，由 Camille 審核後才發。

## 定位（Camille 的方向，優先於舊版）
- 目標是給台灣 B2B 科技廠商**有用的海外市場資訊**，讓人想追蹤；**不是一直賣展**。
- 先講市場發生什麼事，展會只在最後帶一點，三篇裡最多一篇的**文字**提到展會名稱、日期與連結。
- Camille 沒有要表達的「個人觀點」。**不要編造觀點、不要下產業判斷**，也**不要使用「對台灣廠商的意義」**這個標題或寫法。
- 結尾用「**接下來可以留意**」：只列已知的後續（待公布的日期、待定案的政策、調查結果），不寫判斷與建議。
- **輪播圖與貼文文字必須是同一份內容（Camille 2026-11-02 定案）**：每張內文圖字數要多（每張約 150–250 字，見下方「長文輪播版」），FB 與 IG 的貼文文字＝封面標題＋所有內文頁的文字，一字不差，由 `build_long.py` 從同一份 spec 產生 `texts.json`，不可另寫摘要。
- 每則最後一張圖固定放「詳情請洽昇揚展覽」＋LINE QR code＋官網洽詢頁，不放展名、展期、展館。

## 固定資料
- Metricool 品牌：昇揚展覽 Sunrise Expo，`blogId` = `6989429`；FB 粉專＋IG `sunriseexpo_tw`
- 發文時間：週二、三、四 08:30（Asia/Taipei），`draft: true`、`autoPublish: true`
- 洽詢：LINE 搜尋 `@225imowp`／https://lin.ee/ldTgBgo／表單 https://sunriseexpo.com/contact/
- 圖庫（公開 repo，只放圖與版型）：`Camille8960/sunrise-line-assets`，圖放 `social/<週二日期>-long/`
  公開網址：`https://raw.githubusercontent.com/Camille8960/sunrise-line-assets/main/social/<週二日期>-long/<檔名>.png`
- 展會（只有「帶展會」的那一篇文字才寫；日期以官網為準，寫前先確認）：
  - AI EXPO KOREA 2027／4/14–16／首爾 COEX／https://sunriseexpo.com/event/aiexpokorea/
  - AI Asia 2027／1/20–21／曼谷 QSNCC／https://sunriseexpo.com/event/ai-asia/
  - Cybersec Asia 2027／1/20–21／曼谷 QSNCC／https://sunriseexpo.com/event/cybersec-asia/
  - 稱呼：只有 AI EXPO KOREA 可寫「台灣官方代理」；其他展不寫「官方代理」。
- 最後一張圖的地區字樣（`region`）：週二「韓國 AI 展會」、週三「泰國 AI 展會」、週四「泰國資安展會」。

## 每週主題
- 週二：韓國（AI、半導體、資料中心）
- 週三：東南亞／泰國（AI、資料中心、雲端）
- 週四：資安（韓國或東南亞的事件、政策）
- 先看 `social/` 資料夾與 Metricool 近兩週貼文，**同一主題不要連兩週重複**。

## 每週步驟
1. **查證**：用 WebSearch／WebFetch 找過去 7 天的新聞（優先 Reuters、Bloomberg、Nikkei Asia、Korea Herald／Times、Yonhap、Bangkok Post、The Nation、政府與主辦單位公告）。
   - 每個數字、日期、事件都要對到來源，並記下來源與刊登日期；對不到就不要用。
   - 用語要和來源狀態一致：「提案」不可寫成「已定案」；「預估」不可寫成「公布」；「可能」不可寫成「將會」。
   - 來源沒明說就不寫「第一個」「首次」；不寫未確認的歸因（例如某工具被用於攻擊）。
   - 過去 7 天找不到足夠的可查證新聞，改用近 30 天並寫明日期，回報時說明。
2. **寫 spec JSON**：格式見 `social/tools/spec_2026-11-03-long.json`。每篇欄位：`file_prefix`、`region`、`label`（如「市場觀察｜韓國」）、`title`（純文字標題，白話一句）、`title_html`（封面用，重點用 `<em>`，用 `<br>` 控制換行，不要在詞中間斷）、`sub`（一句說明）、`pages`（內文頁，**3 頁**：①②為「發生什麼事」依主題分段，③為「接下來可以留意」；每頁有 `tag`、`heading`、`paras` 段落陣列）、`src`（資料參考，含來源與日期）、`hashtags`。
   - 每頁 `paras` 寫成完整句子，總字數約 150–250 字；內容全部要有來源，來源沒說的不寫，不補背景、不寫判斷。
   - 圖與文字共用同一份 spec，所以**所有要出現在貼文裡的字都寫在 spec 裡**。
3. **產圖**：`python3 -I social/tools/build_long.py <spec.json> <輸出資料夾>`（需 `pip install --break-system-packages segno`；Playwright 已預裝）。每篇輸出 5 張（封面、3 頁內文、聯絡頁）與 `texts.json`（含 `fb`、`ig` 全文）。
   用 Read 把每篇拼成總覽圖檢查：文字不溢出（內文頁底部要留空，來源小字不被蓋住）、不要在詞中間換行、沒有簡體字、QR code 可掃（`cv2.QRCodeDetector` 應解出 LINE 網址）。
4. **推圖**：複製到 `social/<週二日期>-market/`，commit、push main（直接推 main，不要開分支）。推完用 curl 確認網址回 200。
5. **建 Metricool 草稿（6 則）**：先用 `getScheduledPosts` 看該週已有哪些貼文，避免重複建。`createScheduledPost`：
   - `date`：`YYYY-MM-DDT08:30:00+08:00`
   - `info`（JSON 字串）：`{"autoPublish":true,"draft":true,"firstCommentText":"","hasNotReadNotes":false,"media":[5 張公開網址],"providers":[{"network":"facebook"|"instagram"}],"publicationDate":{"dateTime":"YYYY-MM-DDT08:30:00","timezone":"Asia/Taipei"},"shortener":false,"text":"texts.json 的 fb 或 ig 全文，不改字", 以及 FB 的 "facebookData":{"type":"POST"} 或 IG 的 "instagramData":{"type":"POST","autoPublish":true,"showReelOnFeed":true,"isAiGenerated":false}}`
   - FB 與 IG 各一則，同一組 5 張圖；IG 一定要有圖。
   - 修改用 `updateScheduledPost`（需 id 與 uuid，id 每次更新會變），重送完整內容。
   - 如果有呼叫沒回應，先 `getScheduledPosts` 確認是否已建立，再決定要不要重建，不要重複建。
6. **驗證與回報**：用 `getScheduledPosts` 確認 6 則都在、全為草稿、各 5 張圖；用 SendUserMessage 回報（簡短）：每則的日期、平台、標題，主要來源，無法查證而略過的項目，需要 Camille 確認的事。

## 文字規範（繁體中文，不用簡體）
- **FB 與 IG 的貼文文字＝圖上文字**，直接用 `texts.json`，不要自己改寫或縮寫。結構：`【市場觀察】標題` → 副標一句 → 各內文頁（`■ 小標` 加段落）→ 「想了解{地區}展會的參展方式？詳情請洽昇揚展覽」＋LINE＋官網洽詢 → `資料參考：…` → 5 個 hashtag（`#SunriseExpo` 開頭）。
- FB 的聯絡行帶連結；IG 不放可點擊連結（腳本已處理）。
- 展會名稱、日期、網址**預設不寫**（Camille 2026-11-02 確認這個版本）。若某週要帶展會，先在回報中提出，由 Camille 決定。
- 不用 emoji；不用「對台灣廠商的意義」。

## 不可違反
- 一律維持草稿，**不要**改成直接發布。
- 只用查得到來源的事實；不寫展位價格、報名截止日、補助金額。
- 舊稿（日期已過、未發布的草稿，或同時段的其他草稿）**不要刪**，只在回報中列出供 Camille 處理。
- 此 repo 為公開：不放價格、客戶名單、付款資訊、個資。
- GitHub 推送或 Metricool 失敗時停止，在回報最前面說明失敗點與已完成到哪一步，不要用其他圖床取代。

## Camille 隨手提供的素材（不屬於每週排程）
Camille 之後會不定時在對話裡丟想法（展覽攻略、廠商常問的問題、現場照片）。那是**額外貼文**，由當下對話用同一套版型製作，放進 Metricool 草稿，不在這個排程裡處理。
