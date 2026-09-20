"""Build a photographic presentation while preserving the existing itinerary."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from urllib.request import Request, urlopen
from hashlib import md5
import io, json, os, shutil, time
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
CACHE = ROOT / '.photo-cache'
UA = 'Japonia-JP presentation/1.0 (https://github.com/websterek/Japonia-JP)'
PHOTOS = {
 'shibuya': ('Shibuya_Crossing_2018_Shibuya_Crossing_Cropped.jpg', 'Shibuya Crossing', 'Kakidai', 'CC BY-SA 4.0'),
 'shibuya_sky': ('A_view_of_Tokyo_city_from_Shibuya_Sky,_Tokyo,_Japan.jpg', 'Widok z Shibuya Sky', 'Joli Rumi', 'CC BY-SA 4.0'),
 'meiji': ('The_entrance_to_Meiji_Jingu,_Tokyo,_Japan.jpg', 'Wejście do Meiji Jingu', 'Joli Rumi', 'CC BY-SA 4.0'),
 'ghibli': ('Ghibli_Museum_2024.JPG', 'Ghibli Museum, Mitaka', 'Fotointheworld', 'CC BY 4.0'),
 'shinjuku': ('Shinjuku_by_night.jpg', 'Shinjuku nocą', 'Bobak', 'CC BY-SA 2.5'),
 'sensoji': ('Kaminarimon_at_Sensōji.jpg', 'Kaminarimon, Sensō-ji', 'Christophe95', 'CC BY-SA 4.0'),
 'akihabara': ('Akihabara_2006-02-23_a.jpg', 'Akihabara, Tokio', 'Noface', 'Public domain'),
 'kiyomizu': ('Kiyomizu-dera,_Kyoto,_November_2016_-01.jpg', 'Kiyomizu-dera, Kioto', 'Martin Falbisoner', 'CC BY-SA 4.0'),
 'pontocho': ('Pontocho_(44953510015).jpg', 'Pontochō wieczorem', 'Benh LIEU SONG', 'CC BY-SA 4.0'),
 'fushimi': ('Fushimi-Inari_Torii.jpg', 'Torii w Fushimi Inari', 'Takipoint123', 'CC BY-SA 4.0'),
 'nintendo': ('Nintendo_Museum_Entrance.jpg', 'Nintendo Museum, Uji', 'Nagomijirap', 'CC BY-SA 4.0'),
 'byodoin': ('Byodoin.jpg', 'Byōdō-in, Uji', 'Cun Cun', 'CC BY-SA 4.0'),
 'arashiyama': ('Arashiyama_Bamboo_Grove.jpg', 'Bambusowy las Arashiyama', 'Mitchwandrew', 'CC BY 4.0'),
 'kinkaku': ('Kinkaku-ji_2009-03-22.jpg', 'Kinkaku-ji, Kioto', 'Kzaral', 'CC BY 2.0'),
 'usj': ('USJ_Super_Nintendo_World_overview.jpg', 'Super Nintendo World, Osaka', 'Jpatokal', 'CC BY-SA 4.0'),
 'usj_alt': ('Super_Nintendo_World_at_Universal_Studies_Japan_20220814.jpg', 'Super Nintendo World', '高砂の浦', 'CC0'),
 'harry': ('Wizarding_World_of_Harry_Potter_USJ.JPG', 'Wizarding World of Harry Potter, USJ', 'Freddo', 'CC BY-SA 4.0'),
 'dotonbori': ('Dotonbori,_Osaka,_at_night,_November_2016.jpg', 'Dōtonbori nocą', 'Martin Falbisoner', 'CC BY-SA 4.0'),
 'osaka_castle': ('Osaka_Castle,_Osaka,_Japan.jpg', 'Zamek Osaka', 'Joli Rumi', 'CC BY-SA 4.0'),
 'nara': ('The_deer_near_Nara_Park_(2).jpg', 'Jelenie w Narze', 'Tokumeigakarinoaoshima', 'CC BY-SA 4.0'),
 'todaiji': ('Todai-ji,_Nara.JPG', 'Tōdai-ji, Nara', 'Løken', 'CC BY-SA 3.0'),
 'hakone': ('LakeAshi_and_MtFuji_Hakone.JPG', 'Jezioro Ashi i Fuji, Hakone', 'Kentagon; korekta: Uu7', 'CC BY-SA 4.0'),
 'owakudani': ('A_view_of_Owakudani_-_a_volcanic_valley_with_active_sulphur_vents_in_Hakone,_Japan.jpg', 'Owakudani, Hakone', 'Joli Rumi', 'CC BY-SA 4.0'),
 'hamarikyu': ('Hamarikyu_Gardens.jpg', 'Hamarikyū Gardens, Tokio', 'Eddy23', 'CC BY-SA 4.0'),
 'station': ('Tokyo_station_from_above.jpg', 'Tokyo Station', 'LR0725', 'CC BY-SA 4.0'),
 'nikko': ('Nikko_Toshogu_Yomeimon_Gate_2024.jpg', 'Brama Yōmeimon, Nikkō', 'Jpatokal', 'CC BY-SA 4.0'),
 'kegon': ('Kegon_Falls,_Nikko_National_Park,_Japan1.jpg', 'Wodospad Kegon, Nikkō', 'Joli Rumi', 'CC BY-SA 4.0'),
 'tsukiji': ('Tsukiji_Outside_Market.jpg', 'Tsukiji Outer Market', 'Jnlin', 'CC BY-SA 3.0'),
 'odaiba': ('Odaiba_at_night.jpg', 'Odaiba i Zatoka Tokijska', 'Brian Kemper', 'CC BY-SA 3.0'),
 'rainbow': ('Rainbow_bridge_from_odaiba.jpg', 'Rainbow Bridge z Odaiby', 'fox kiyo', 'CC BY-SA 2.0')
}
LICENCES = {
 'CC BY-SA 4.0':'https://creativecommons.org/licenses/by-sa/4.0/',
 'CC BY 4.0':'https://creativecommons.org/licenses/by/4.0/',
 'CC BY 2.0':'https://creativecommons.org/licenses/by/2.0/',
 'CC BY-SA 3.0':'https://creativecommons.org/licenses/by-sa/3.0/',
 'CC BY-SA 2.5':'https://creativecommons.org/licenses/by-sa/2.5/',
 'CC BY-SA 2.0':'https://creativecommons.org/licenses/by-sa/2.0/',
 'CC0':'https://creativecommons.org/publicdomain/zero/1.0/',
 'Public domain':'https://commons.wikimedia.org/wiki/Commons:Public_domain'
}
DAY_GALLERIES = [
 [],
 ['shibuya','shibuya_sky'],
 ['meiji','ghibli','shinjuku'],
 ['sensoji','akihabara'],
 ['kiyomizu','pontocho'],
 ['fushimi','nintendo','byodoin'],
 ['arashiyama','kinkaku'],
 ['usj','usj_alt','harry'],
 ['osaka_castle','dotonbori'],
 ['nara','todaiji'],
 ['hakone','owakudani'],
 ['hamarikyu','station'],
 ['nikko','kegon'],
 ['tsukiji','odaiba','rainbow'],
 ['station','shibuya']
]


def download_photo(key, row):
    filename = row[0]
    cache = CACHE / (key + '.jpg')
    if not cache.exists():
        digest = md5(filename.encode('utf-8')).hexdigest()
        encoded = quote(filename, safe='')
        original = f'https://upload.wikimedia.org/wikipedia/commons/{digest[0]}/{digest[:2]}/{encoded}'
        thumbnail = f'https://upload.wikimedia.org/wikipedia/commons/thumb/{digest[0]}/{digest[:2]}/{encoded}/1280px-{encoded}'
        errors = []
        for url in (thumbnail, original):
            for attempt in range(2):
                try:
                    with urlopen(Request(url, headers={'User-Agent': UA}), timeout=45) as response:
                        data = response.read(40 * 1024 * 1024 + 1)
                    if len(data) > 40 * 1024 * 1024:
                        raise ValueError('Image exceeds 40 MB limit')
                    with Image.open(io.BytesIO(data)) as img:
                        img.verify()
                    cache.write_bytes(data)
                    break
                except Exception as exc:
                    errors.append(str(exc))
                    time.sleep(2 + attempt * 3)
            if cache.exists():
                break
        if not cache.exists():
            raise RuntimeError(f'Cannot acquire licensed photograph {key}: {errors}')
    with Image.open(cache) as source:
        img = ImageOps.exif_transpose(source).convert('RGB')
        if min(img.size) < 320:
            raise ValueError(f'Image unexpectedly small: {key}')
        for width, suffix in ((1440, ''), (720, '-small')):
            resized = img.copy()
            resized.thumbnail((width, 1920), Image.Resampling.LANCZOS)
            dest = OUT / 'assets/photos' / f'{key}{suffix}.webp'
            resized.save(dest, 'WEBP', quality=84, method=6)
        print(f'PHOTO OK {key}: {img.width}x{img.height}', flush=True)


def figure(key, extra='', eager=False, slide_index=None):
    filename, title, author, licence = PHOTOS[key]
    classes = 'photograph'
    if extra:
        classes += ' ' + extra
    data = f' data-slide="{slide_index}"' if slide_index is not None else ''
    return f'''<figure class="{classes}"{data}><a class="photo-link" href="assets/photos/{key}.webp" target="_blank" rel="noopener" aria-label="Otwórz zdjęcie: {escape(title)}"><img src="assets/photos/{key}.webp" srcset="assets/photos/{key}-small.webp 720w, assets/photos/{key}.webp 1440w" sizes="(max-width: 700px) 100vw, 55vw" alt="{escape(title)}" loading="{'eager' if eager else 'lazy'}" decoding="async" {'fetchpriority="high"' if eager else ''} width="1440" height="1080"></a><figcaption><span>{escape(title)}</span><a href="#photo-{key}">fot. {escape(author)}</a></figcaption></figure>'''


def gallery(keys, day_index):
    if not keys:
        return ''
    slides = ''.join(figure(key, 'gallery-slide' + (' is-active' if i == 0 else ''), False, i) for i, key in enumerate(keys))
    thumbs = []
    for i, key in enumerate(keys):
        title = PHOTOS[key][1]
        thumbs.append(f'''<button type="button" class="gallery-thumb{' is-active' if i == 0 else ''}" data-gallery-to="{i}" aria-label="Pokaż zdjęcie {i+1}: {escape(title)}" aria-pressed="{'true' if i == 0 else 'false'}"><img src="assets/photos/{key}-small.webp" alt="" loading="lazy" decoding="async"></button>''')
    return f'''<div class="day-gallery" data-gallery tabindex="0" aria-label="Galeria dnia {day_index}"><div class="gallery-stage">{slides}<div class="gallery-controls"><button type="button" class="gallery-arrow gallery-prev" data-gallery-prev aria-label="Poprzednie zdjęcie">←</button><span class="gallery-counter" data-gallery-counter aria-live="polite">1 / {len(keys)}</span><button type="button" class="gallery-arrow gallery-next" data-gallery-next aria-label="Następne zdjęcie">→</button></div></div><div class="gallery-thumbs">{''.join(thumbs)}</div></div>'''


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'assets/photos').mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    for key, row in PHOTOS.items():
        download_photo(key, row)
    soup = BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'), 'html.parser')
    days = soup.select('article.day')
    if len(days) != 15:
        raise ValueError(f'Expected 15 itinerary sections; found {len(days)}. Source structure changed.')
    before_stops = [n.get_text(' ', strip=True) for n in soup.select('.stops li')]
    before_choices = [n.get_text(' ', strip=True) for n in soup.select('.option')]
    for style in soup.find_all('style'):
        style.decompose()
    revision = os.getenv('GITHUB_SHA', 'local')[:12]
    head = BeautifulSoup(f'''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/site.css?v={revision}"><script defer src="assets/site.js?v={revision}"></script><meta name="site-design" content="photo-editorial-gallery-v2"><meta name="site-revision" content="{revision}">''','html.parser')
    for tag in list(head.contents):
        soup.head.append(tag)
    theme = soup.find('meta', attrs={'name':'theme-color'})
    if theme:
        theme['content'] = '#f6f6f2'
    hero = soup.select_one('.hero')
    original_notice = str(hero.select_one('.notice'))
    hero.clear()
    new_hero = f'''<div class="cover-heading"><div><p class="eyebrow">PLAN PODRÓŻY / 2027</p><h1>JAPONIA</h1></div><div class="cover-intro"><p class="cover-dates">26.05 — 09.06</p><p>Od ulic Tokio po ogrody Kioto.<br>Po drodze Osaka, Nara i noc w Hakone.</p><a class="jump" href="#plan">Zobacz plan dzień po dniu <span aria-hidden="true">↘</span></a></div></div><div class="cover-images">{figure('shibuya','cover-main',True)}{figure('kiyomizu','cover-side',True)}</div><div class="cover-footer"><p>TOKIO → KIOTO → OSAKA → HAKONE → TOKIO</p><span>12 pełnych dni zwiedzania · przylot i wylot z Tokio</span></div><details class="flight-note"><summary>Loty i założenia planu</summary>{original_notice}</details>'''
    fragment = BeautifulSoup(new_hero,'html.parser')
    for node in list(fragment.contents):
        hero.append(node)
    navigation=[]
    for index, day in enumerate(days):
        day['id'] = f'dzien-{index}'
        date = day.select_one('.date').get_text(' ',strip=True)
        navigation.append(f'<a href="#dzien-{index}" title="{escape(date)}">{index:02d}</a>')
        header=day.find('header',recursive=False)
        if header is None:
            raise ValueError('Day header not found')
        header.extract()
        body=soup.new_tag('div', attrs={'class':'day-content'})
        for child in list(day.contents):
            body.append(child.extract())
        for note in body.select('p.change'):
            details=soup.new_tag('details',attrs={'class':'day-detail'})
            summary=soup.new_tag('summary')
            summary.string='Uwagi do tego dnia'
            note.replace_with(details)
            details.append(summary)
            details.append(note)
        grid=soup.new_tag('div',attrs={'class':'day-layout'})
        if DAY_GALLERIES[index]:
            grid.append(BeautifulSoup(gallery(DAY_GALLERIES[index], index),'html.parser'))
        else:
            day['class'].append('travel-day')
        grid.append(body)
        day.append(header)
        day.append(grid)
    assert before_stops == [n.get_text(' ', strip=True) for n in soup.select('.stops li')], 'Itinerary text changed'
    assert before_choices == [n.get_text(' ', strip=True) for n in soup.select('.option')], 'Variant text changed'
    nav=BeautifulSoup('<nav class="day-index" aria-label="Wybierz dzień"><span>DZIEŃ</span>'+''.join(navigation)+'</nav>','html.parser')
    soup.select_one('#plan .sectionhead').insert_after(nav)
    for rect in soup.select('.map rect'):
        rect['rx']='0'
    svg=soup.select_one('.map svg')
    if svg:
        svg['viewBox']='0 0 1180 440'
        svg.select_one('rect')['width']='1180'
        svg.select_one('rect')['fill']='#eeefea'
    credits=[]
    for key,(filename,title,author,licence) in PHOTOS.items():
        page='https://commons.wikimedia.org/wiki/File:'+quote(filename,safe='')
        credits.append(f'<li id="photo-{key}"><a href="{page}" target="_blank" rel="noopener">{escape(title)}</a> — {escape(author)} · <a href="{LICENCES[licence]}" target="_blank" rel="noopener">{licence}</a></li>')
    footer=soup.select_one('footer .wrap')
    footer.append(BeautifulSoup('<details class="photo-credits"><summary>Fotografie i autorzy</summary><p>Zdjęcia Wikimedia Commons, z różnych pór roku. Zmiany: zmniejszenie, WebP i kadrowanie w układzie strony. Fotografie zachowują wskazane licencje; autorzy nie są związani z tym planem.</p><ul>'+''.join(credits)+'</ul></details>','html.parser'))
    footer.append(BeautifulSoup('<a class="back-top" href="#start">Wróć na początek ↑</a>','html.parser'))
    (OUT/'index.html').write_text(str(soup),encoding='utf-8')
    shutil.copyfile(ROOT/'presentation/site.css', OUT/'assets/site.css')
    shutil.copyfile(ROOT/'presentation/site.js', OUT/'assets/site.js')
    (OUT/'.nojekyll').write_text('')
    manifest={'design':'photo-editorial-gallery-v2','revision':revision,'photos':[f'assets/photos/{key}.webp' for key in PHOTOS], 'galleries':DAY_GALLERIES}
    (OUT/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
    print(f'BUILT: {len(days)} days, {len(PHOTOS)} locally hosted photographs, revision {revision}',flush=True)

if __name__=='__main__':
    main()
