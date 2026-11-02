#!/usr/bin/env python3
"""昇揚 每週社群輪播圖產生器（長文版：每張字多，貼文文字＝圖文內容）
用法: python3 -I build_long.py spec.json outdir
輸出: outdir/<prefix>_1..5.png 與 outdir/texts.json（FB/IG 貼文文字，由同一份 spec 產生，與圖上文字一致）
每篇: 封面 / 內文頁（每頁 標籤+小標+段落）/ 聯絡頁（固定）
"""
import json, sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_week import qr_uri, last, sp, tag, GOLD
P = lambda t: f'<div style="font-size:40px;line-height:1.7;color:#E6E2D8;margin-top:36px">{t}</div>'

def cover(p):
    return (sp(150) + tag(p["label"]) + f'<div class=h1 style="font-size:84px">{p["title_html"]}</div>'
            f'<div class=sub>{p["sub"]}<br><b style="color:{GOLD}">滑動看完整內容 →</b></div>')

def page(pg):
    h = sp(70) + tag(pg["tag"]) + f'<div class=h2 style="font-size:54px">{pg["heading"]}</div>'
    for t in pg["paras"]:
        h += P(t)
    return h

def contact_text(region):
    return (f"想了解{region}的參展方式？\n詳情請洽昇揚展覽\nLINE：@225imowp（https://lin.ee/ldTgBgo）\n官網洽詢：https://sunriseexpo.com/contact/")

def post_text(p, ig=False):
    out = [f"【{p['label'].split('｜')[0]}】{p['title']}", "", p["sub"]]
    for pg in p["pages"]:
        out += ["", f"■ {pg['tag']}｜{pg['heading']}"] + pg["paras"]
    out += ["", contact_text(p["region"]), "", p["src"], "", p["hashtags"]]
    t = "\n".join(out)
    if ig:  # IG 文字不放可點擊連結
        t = t.replace("LINE：@225imowp（https://lin.ee/ldTgBgo）", "LINE：@225imowp").replace("官網洽詢：https://sunriseexpo.com/contact/", "官網洽詢：sunriseexpo.com/contact")
    return t

def main(spec_path, out):
    spec = json.load(open(spec_path, encoding="utf-8")); uri = qr_uri()
    posts, texts = [], {}
    for p in spec["posts"]:
        slides = [{"html": cover(p)}]
        for i, pg in enumerate(p["pages"]):
            s = {"html": page(pg)}
            if i == len(p["pages"]) - 1: s["src"] = p["src"]
            slides.append(s)
        slides.append({"html": last(p["region"], uri)})
        posts.append({"key": p["file_prefix"], "slides": slides})
        texts[p["file_prefix"]] = {"fb": post_text(p), "ig": post_text(p, True), "n_slides": len(slides)}
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_render.json")
    json.dump({"posts": posts}, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.check_call([sys.executable, "-I", os.path.join(here, "render_market.py"), tmp, out])
    os.remove(tmp)
    json.dump(texts, open(os.path.join(out, "texts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
