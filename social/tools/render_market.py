# 昇揚社群週報 輪播圖產生器
# 用法: python3 render.py week.json outdir
# week.json: {"posts":[{"key":"p1","slides":[{"html":"<div class=tag>..</div>...","src":"資料來源..."}]}]}
# 可用 class: tag, h1/h2 (含 <em> 強調色), sub, p, big, biglabel, item>num+it/id, cols>col>h3/k/p, box(<b>), cta>t/d
import asyncio, json, sys, os
from playwright.async_api import async_playwright
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Noto Sans CJK TC',sans-serif;color:#F4F1EA;
 background:#15171D;position:relative;overflow:hidden}
.glow{position:absolute;right:-260px;top:-260px;width:760px;height:760px;border-radius:50%;
 background:radial-gradient(circle,rgba(242,169,59,.30),rgba(242,169,59,0) 65%)}
.wrap{position:absolute;inset:0;padding:96px 88px 0 88px;display:flex;flex-direction:column}
.tag{display:inline-block;align-self:flex-start;font-size:34px;font-weight:700;color:#15171D;background:#F2A93B;
 padding:10px 26px;border-radius:8px;letter-spacing:2px}
.h1{font-size:92px;font-weight:900;line-height:1.28;margin-top:56px;letter-spacing:1px}
.h1 em{font-style:normal;color:#F2A93B}
.h2{font-size:62px;font-weight:900;line-height:1.3;margin-top:44px}
.h2 em{font-style:normal;color:#F2A93B}
.sub{font-size:36px;line-height:1.6;color:#B9B4A9;margin-top:40px}
.p{font-size:38px;line-height:1.7;color:#E6E2D8;margin-top:36px}
.big{font-size:150px;font-weight:900;color:#F2A93B;line-height:1;margin-top:64px;letter-spacing:-2px}
.biglabel{font-size:40px;color:#B9B4A9;margin-top:20px}
.item{display:flex;gap:30px;margin-top:64px;align-items:flex-start}
.num{flex:none;width:76px;height:76px;border-radius:50%;background:#F2A93B;color:#15171D;font-size:42px;font-weight:900;
 display:flex;align-items:center;justify-content:center}
.it{font-size:52px;font-weight:700;line-height:1.3}
.id{font-size:38px;line-height:1.55;color:#B9B4A9;margin-top:10px}
.cols{display:flex;gap:28px;margin-top:48px}
.col{flex:1;border:2px solid #3A3D46;border-radius:18px;padding:36px 32px}
.col h3{font-size:44px;color:#F2A93B;font-weight:900}
.col .k{font-size:28px;color:#8E897F;margin-top:26px;letter-spacing:1px}
.col p{font-size:38px;line-height:1.55;margin-top:8px}
.box{margin-top:44px;border-left:8px solid #F2A93B;background:#1F222A;padding:30px 36px;font-size:38px;line-height:1.6}
.box b{color:#F2A93B}
.cta{margin-top:auto;margin-bottom:150px;border-top:2px solid #3A3D46;padding-top:40px}
.cta .t{font-size:46px;font-weight:900}
.cta .d{font-size:36px;color:#B9B4A9;margin-top:14px;line-height:1.5}
.foot{position:absolute;left:88px;right:88px;bottom:64px;display:flex;justify-content:space-between;
 font-size:28px;letter-spacing:6px;color:#8E897F}
.src{position:absolute;left:88px;right:88px;bottom:112px;font-size:26px;line-height:1.5;color:#6F6B63}
"""
def page(inner, idx, total, src=None):
    s = f'<div class="src">{src}</div>' if src else ''
    return f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="glow"></div><div class="wrap">{inner}</div>{s}
<div class="foot"><span>SUNRISE EXPO</span><span>{idx} / {total}</span></div></body></html>"""
async def main(path, out):
    data=json.load(open(path)); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350})
        for post in data["posts"]:
            n=len(post["slides"])
            for i,sl in enumerate(post["slides"],1):
                await pg.set_content(page(sl["html"],i,n,sl.get("src"))); await pg.wait_for_timeout(150)
                await pg.screenshot(path=f"{out}/{post['key']}_{i}.png")
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
