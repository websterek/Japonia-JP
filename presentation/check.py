"""Browser checks and screenshots of the built site."""
import json, shutil, threading
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PREVIEW=ROOT/'preview';PREVIEW.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'_site')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
report=[]
with sync_playwright() as p:
    chrome=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    browser=p.chromium.launch(executable_path=chrome,headless=True,args=['--no-sandbox'])
    for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile'),(360,800,'small-mobile')]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(url,wait_until='networkidle',timeout=60000)
        page.evaluate("document.querySelectorAll('img').forEach(i => i.loading='eager')")
        page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 300)",timeout=60000)
        page.evaluate('document.fonts.ready')
        result=page.evaluate('''() => ({width: innerWidth, contentWidth:document.documentElement.scrollWidth, images:document.images.length, imagesLoaded:[...document.images].every(i=>i.naturalWidth>300), days:document.querySelectorAll('article.day').length, font:getComputedStyle(document.querySelector('h1')).fontFamily, radius:getComputedStyle(document.querySelector('.photo-link')).borderRadius, ubuntuLoaded:[...document.fonts].some(f=>f.family.includes('Ubuntu') && f.status==='loaded')})''')
        assert result['contentWidth']<=width+1,result
        assert result['images']>=15 and result['imagesLoaded'],result
        assert result['days']==15,result
        assert 'Ubuntu' in result['font'] and result['radius']=='0px',result
        assert not errors,errors
        page.screenshot(path=str(PREVIEW/f'{label}-cover.png'))
        page.locator('#dzien-5').scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        page.screenshot(path=str(PREVIEW/f'{label}-day.png'))
        report.append(result)
        print('BROWSER CHECK:',json.dumps(result),flush=True)
        page.close()
    browser.close()
server.shutdown()
(PREVIEW/'checks.json').write_text(json.dumps(report,indent=2))
