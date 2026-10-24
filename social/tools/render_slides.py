import asyncio, html, os, sys
from playwright.async_api import async_playwright

# 用法：python3 -I render_slides.py <posts.json> <輸出資料夾>
import json
POSTS = json.load(open(sys.argv[1],encoding='utf-8'))
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{font-family:'Noto Sans CJK TC','Noto Sans TC',sans-serif}
body{width:1080px;height:1350px;background:#0b1730;color:#fff;position:relative;overflow:hidden}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 85% 8%,#1d3a78 0,#0b1730 55%)}
.bar{position:absolute;left:0;top:0;width:18px;height:100%;background:#c8102e}
.wrap{position:absolute;left:90px;right:80px;top:90px;bottom:120px;display:flex;flex-direction:column}
.tag{display:inline-block;align-self:flex-start;background:#c8102e;padding:10px 26px;font-size:34px;font-weight:700;letter-spacing:2px}
.foot{position:absolute;left:90px;right:80px;bottom:44px;display:flex;justify-content:space-between;font-size:26px;color:#9fb0d0;letter-spacing:2px}
h1{font-size:104px;line-height:1.25;font-weight:900;margin-top:auto}
h1 em{font-style:normal;color:#ff4d6a}
.sub{font-size:48px;margin-top:44px;color:#dbe5ff;font-weight:500;line-height:1.4;border-left:8px solid #c8102e;padding-left:28px}
.swipe{margin-top:auto;font-size:34px;color:#9fb0d0}
h2{font-size:64px;font-weight:900;margin-top:36px}
.rows{margin-top:34px;display:flex;flex-direction:column;gap:24px}
.row{background:rgba(255,255,255,.07);border-left:8px solid #c8102e;padding:22px 34px}
.big{font-size:62px;font-weight:900;color:#ff4d6a;line-height:1.1}
.desc{font-size:34px;color:#dbe5ff;margin-top:8px;line-height:1.4}
.n{display:flex;gap:30px;align-items:flex-start}
.num{flex:none;width:72px;height:72px;border-radius:50%;background:#c8102e;font-size:42px;font-weight:900;text-align:center;line-height:72px}
.n .t{font-size:46px;font-weight:900;line-height:1.25}
.n .d{font-size:35px;color:#dbe5ff;margin-top:8px;line-height:1.45}
.cta{margin-top:auto;margin-bottom:auto}
.cta .k{font-size:40px;color:#ff4d6a;font-weight:700;letter-spacing:2px}
.cta .e{font-size:92px;font-weight:900;margin-top:16px;line-height:1.2}
.cta .d{font-size:56px;margin-top:24px;color:#dbe5ff}
.cta .m{font-size:40px;margin-top:40px;color:#dbe5ff;line-height:1.5}
.cta .l{font-size:36px;margin-top:44px;background:#c8102e;display:inline-block;padding:16px 34px;font-weight:700}
.src{font-size:25px;color:#8fa1c4;line-height:1.5;margin-top:36px}
"""

def page(inner, pg, total=4):
    return f"""<!doctype html><html lang="zh-TW"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="bg"></div><div class="bar"></div><div class="wrap">{inner}</div>
<div class="foot"><span>SUNRISE EXPO 昇揚展覽</span><span>{pg} / {total}</span></div></body></html>"""

def slides(p):
    h=html.escape
    s1=f'<span class="tag">{h(p["tag"])}</span><h1>{p["cover"][0]}</h1><div class="sub">{h(p["cover"][1])}</div><div class="swipe">左滑看重點 →</div>'
    rows="".join(f'<div class="row"><div class="big">{h(a)}</div><div class="desc">{h(b)}</div></div>' for a,b in p["s2"][1])
    s2=f'<span class="tag">{h(p["tag"])}</span><h2>{h(p["s2"][0])}</h2><div class="rows">{rows}</div>'
    nrows="".join(f'<div class="n"><div class="num">{i+1}</div><div><div class="t">{h(a)}</div><div class="d">{h(b)}</div></div></div>' for i,(a,b) in enumerate(p["s3"][1]))
    s3=f'<span class="tag">{h(p["tag"])}</span><h2>{h(p["s3"][0])}</h2><div class="rows" style="gap:36px">{nrows}</div>'
    c=p["s4"]
    s4=f'<span class="tag">{h(p["tag"])}</span><div class="cta"><div class="k">想直接接觸買家？</div><div class="e">{h(c[0])}</div><div class="d">{h(c[1])}</div><div class="m">{h(c[2])}</div><div class="l">{h(c[3])}</div><div class="src">{h(c[4])}</div></div>'
    return [s1,s2,s3,s4]

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for name,p in POSTS.items():
            for i,inner in enumerate(slides(p),1):
                await pg.set_content(page(inner,i))
                await pg.wait_for_timeout(150)
                await pg.screenshot(path=f"{OUT}/{name}_{i}.png")
        await b.close()
asyncio.run(main())
print(sorted(os.listdir(OUT)))
