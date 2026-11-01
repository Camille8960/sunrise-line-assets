#!/usr/bin/env python3
"""昇揚 每週社群輪播圖產生器（市場資訊版）
用法: python3 -I build_week.py spec.json outdir
spec.json 格式見 social/tools/spec_2026-11-03-market.json
每篇 4 張: 封面 / 1 發生什麼事 / 2 接下來看什麼 / 聯絡（固定）
依賴: playwright、segno、同資料夾的 render_market.py（輸出 1080x1350 PNG）
"""
import json, sys, os, io, base64, subprocess, tempfile
import segno

LINE_URL = "https://line.me/R/ti/p/@225imowp"
GOLD = "#F2A93B"

def qr_uri():
    q = segno.make(LINE_URL, error="m")
    b = io.BytesIO()
    q.save(b, kind="png", scale=12, border=1, dark="#15171D", light="#FFFFFF")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

sp = lambda h: f'<div style="height:{h}px"></div>'
tag = lambda t: f'<div class=tag>{t}</div>'
lead = lambda t: f'<div class=p style="margin-top:32px">{t}</div>'

def item(n, t, d):
    return (f'<div class=item><div class=num>{n}</div><div><div class=it>{t}</div>'
            f'<div class=id>{d}</div></div></div>')

def cover(c):
    return (sp(220) + tag(c["tag"]) + f'<div class=h1>{c["title_html"]}</div>'
            f'<div class=sub>{c["sub_html"]}<br><b style="color:{GOLD}">3 張圖看懂 →</b></div>')

def section(s, top):
    h = sp(top) + tag(s["tag"]) + lead(s["lead"])
    for it in s["items"]:
        h += item(it["n"], it["t"], it["d"])
    if s.get("box"):
        h += f'<div class=box style="margin-top:32px">{s["box"]}</div>'
    return h

def last(region, uri):
    return (sp(150) + f'<div class=h2>想了解<em>{region}</em><br>的參展方式？</div>'
      '<div class=box style="margin-top:56px">'
      '<div style="font-size:56px;font-weight:900">詳情請洽<b>昇揚展覽</b></div>'
      '<div style="display:flex;gap:48px;align-items:center;margin-top:40px">'
      f'<img src="{uri}" style="width:270px;height:270px;border-radius:14px;flex:none">'
      '<div style="font-size:40px;line-height:1.6">'
      '<div style="font-size:30px;color:#B9B4A9">LINE 官方帳號</div><b>@225imowp</b>'
      '<div style="font-size:30px;color:#B9B4A9;margin-top:22px">官網洽詢</div>sunriseexpo.com/contact'
      '</div></div></div>'
      '<div class=cta><div class=t>追蹤昇揚，每週整理海外市場大事</div>'
      '<div class=d>昇揚展覽 SUNRISE EXPO</div></div>')

def main(spec_path, out):
    spec = json.load(open(spec_path, encoding="utf-8"))
    uri = qr_uri()
    posts = []
    for p in spec["posts"]:
        bg, wt = p["background"], p["watch"]
        slides = [
            {"html": cover(p["cover"])},
            {"html": section(bg, 90 if bg.get("box") else 110), "src": bg["src"]},
            {"html": section(wt, 200), "src": wt["src"]},
            {"html": last(p["region"], uri)},
        ]
        posts.append({"key": p["file_prefix"], "slides": slides})
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_render.json")
    json.dump({"posts": posts}, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.check_call([sys.executable, "-I", os.path.join(here, "render_market.py"), tmp, out])
    os.remove(tmp)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
