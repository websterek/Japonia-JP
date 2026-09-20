"""Verify the deployed revision and every full-size photograph over public HTTPS."""
import json, os, time
from urllib.request import Request, urlopen
base=os.environ['SITE_URL'].rstrip('/')+'/'
revision=os.environ['GITHUB_SHA'][:12]
for attempt in range(18):
    try:
        request=Request(base+'manifest.json?v='+revision,headers={'Cache-Control':'no-cache'})
        with urlopen(request,timeout=25) as response:
            manifest=json.load(response)
        assert manifest['revision']==revision,'Older deployment is still cached'
        with urlopen(base+'?v='+revision,timeout=25) as response:
            html=response.read().decode('utf-8')
        assert 'photo-editorial-v1' in html and html.count('<img ')>=15
        for path in manifest['photos']:
            with urlopen(base+path,timeout=25) as response:
                assert response.status==200
                data=response.read(16)
                assert data[:4]==b'RIFF' and data[8:12]==b'WEBP',path
        print(f"VERIFIED PUBLIC SITE: {base}; revision {revision}; {len(manifest['photos'])} photographs return HTTP 200 and valid WebP headers.",flush=True)
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as summary:
            summary.write(f'### Published photographic presentation\n\n[{base}]({base})\n\nVerified revision `{revision}`, the page and all {len(manifest["photos"])} photographs without authentication.\n')
        break
    except Exception as exc:
        print(f'Attempt {attempt+1}: {exc}',flush=True)
        if attempt==17:
            raise
        time.sleep(5)
