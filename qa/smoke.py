import asyncio, sys, json
from playwright.async_api import async_playwright
URL=sys.argv[1]
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=await br.new_page(viewport={'width':1360,'height':1100}); errs=[]
    pg.on('pageerror',lambda e:errs.append('PE '+str(e))); pg.on('console',lambda m: errs.append(m.type+' '+m.text) if m.type in('error','warning') else None)
    await pg.goto(URL); await pg.wait_for_timeout(500); print('pre',errs)
    await pg.click('#tapBtn'); 
    try: await pg.wait_for_function("window.__rangekit.ready()",timeout=60000)
    except Exception as e: print('notready',e)
    r=await pg.evaluate("""()=>{const f=window.__rangekit,F=f.fits(); return {load:document.getElementById('load').textContent,status:document.getElementById('status').textContent,
      best:[F.best.tr,F.best.score], asWritten:F.asWritten.score, keys:F.keys.map(k=>k.shift+':'+Math.round(k.score)).join(' '), key:JSON.stringify(f.detectKey(f.melody(),[]))}}""")
    print(json.dumps(r,indent=1))
    await pg.click('#play'); await pg.wait_for_timeout(3000); print('playing',await pg.evaluate("()=>window.__rangekit.playing()"), await pg.evaluate("()=>(window.__schedLog||[]).length"))
    await pg.click('#play')
    w=await pg.evaluate("async()=>{const r=await window.__rangekit.exportWavBytes({}); return {name:r.name,frames:r.frames,n:r.bytes.length}}"); print(w)
    m=await pg.evaluate("()=>{const r=window.__rangekit.exportMidBytes(); return {name:r.name,n:r.bytes.length}}"); print(m)
    c=await pg.evaluate("()=>{const r=window.__rangekit.exportSheetBytes(); return {name:r.name,t:new TextDecoder().decode(r.bytes)}}"); print(c['name']); print(c['t'][:1500])
    s=await pg.evaluate("async()=>{const r=await window.__rangekit.exportStemsBytes(); return {name:r.name,n:r.zip.length,files:r.files.map(f=>f.name)}}"); print(s)
    await pg.screenshot(path='/workspace/rangekit/qa/out/smoke.png',full_page=True)
    print('ERRS',errs[:20]); await br.close()
asyncio.run(main())
