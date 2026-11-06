from pathlib import Path, PurePosixPath
from zipfile import ZipFile
from html import escape
import re

def main():
    root = Path('dist')
    bundle = Path('BHS-Brand-Assets.zip')
    if not bundle.is_file():
        print('Brand asset bundle not yet uploaded; retaining current design.')
        return
    names = ['reception','hero-welcome','story-counseling','group-veterans-families','group-adhd-parents','group-family-support','medication-management','therapy-counseling','psychiatric-evaluations','tms','spravato','substance-use-treatment','medication-assisted-treatment','telehealth']
    expected = {'assets/images/'+n+'.webp' for n in names} | {'assets/logo-fitchburg.webp'}
    with ZipFile(bundle) as archive:
        entries = {e.filename:e for e in archive.infolist() if not e.is_dir()}
        if not expected.issubset(entries):
            raise RuntimeError('Incomplete brand asset bundle')
        for name in sorted(expected):
            rel = PurePosixPath(name)
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('Unsafe asset path')
            if entries[name].file_size > 10000000:
                raise ValueError('Asset exceeds size limit')
            target = root.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))
    def src(name):
        return 'assets/images/'+name+'.webp'
    def figure(name,alt,cls=''):
        return f'<figure class="{cls}"><img src="{src(name)}" alt="{escape(alt)}" width="1536" height="1024" loading="lazy" decoding="async"></figure>'
    services = ['medication-management','therapy-counseling','psychiatric-evaluations','tms','spravato','substance-use-treatment','medication-assisted-treatment','telehealth']
    groups = ['veterans-families','adhd-parents','family-support']
    pages = {n+'.html':n for n in services}
    pages.update({'group-'+n+'.html':'group-'+n for n in groups})
    pages.update({'about.html':'reception','support-groups.html':'group-veterans-families','group-spanish-language.html':'group-family-support'})
    for page in root.glob('*.html'):
        text = page.read_text(encoding='utf-8')
        text = text.replace('assets/logo.png','assets/logo-fitchburg.webp')
        text = re.sub(r'<figcaption>.*?</figcaption>','',text,flags=re.S)
        default = pages.get(page.name,'reception')
        text = re.sub(r'https://images\.pexels\.com/photos/[^\s"<>]+',lambda m:src(default),text)
        text = re.sub(r'(<img[^>]*src="assets/images/[^"]+"[^>]*alt=")[^"]*',r'\1Care, community, and service illustration',text)
        def card_image(match):
            card = match.group(0)
            link = re.search(r'href="([^"]+)\.html"',card)
            if not link: return card
            slug = link.group(1)
            name = slug if slug in services else slug if slug.startswith('group-') and slug[6:] in groups else None
            if name:
                card = re.sub(r'(<img[^>]*src=")[^"]+',lambda m:m.group(1)+src(name),card)
            return card
        text = re.sub(r'<a class="(?:card|communitytile|groupcard)"[^>]*>.*?</a>',card_image,text,flags=re.S)
        if page.name == 'index.html':
            text = re.sub(r'<figure class="joyphoto">.*?</figure>',lambda m:figure('hero-welcome','A welcoming reception scene','joyphoto'),text,flags=re.S)
            text = text.replace('More connection.<br>More possibility.<br><em>More room to be you.</em>','Thoughtful care.<br><em>Meaningful connection.</em>')
            text = text.replace('For the moments that matter, and the everyday moments in between. Discover thoughtful mental health care and a community-centered vision, close to home.','Mental health care and community support, here in Fitchburg. Explore your options in a welcoming, community-centered setting.')
            text = text.replace('Friends enjoying a joyful walk outdoors','A welcoming reception scene')
            story = '<section class="storyblock brand-story" id="our-story"><div><span class="label">A WELCOMING APPROACH TO CARE</span><h2>A place to feel welcome.<br><em>A team to help you move forward.</em></h2><p>Finding support should begin with feeling heard. Our approach brings thoughtful behavioral healthcare and community connection into the same local story.</p><p>Explore treatment options, learn about our planned support groups, or simply ask a question. You can take the next step at your own pace.</p><a class="textlink" href="about.html">Get to know BHS Fitchburg ↗</a></div>'+figure('story-counseling','Comfortable seating arranged for a conversation','story-image')+'</section>'
            text = re.sub(r'<section class="storyblock" id="our-story">.*?</section>',lambda m:story,text,flags=re.S)
            text = re.sub(r'<figure class="pathphoto">.*?</figure>',lambda m:figure('reception','A bright reception and seating area','pathphoto'),text,flags=re.S)
            def service_image(match):
                card = match.group(0)
                slug = re.search(r'href="([^"]+)\.html"',card).group(1)
                if slug not in services: return card
                card = re.sub(r'<span class="careicon">.*?</span>','',card,flags=re.S)
                start = card.find('>')+1
                return card[:start]+figure(slug,slug.replace('-',' ').title()+' illustration','care-photo')+'<div class="care-body">'+card[start:-4]+'</div></a>'
            text = re.sub(r'<a class="caretile"[^>]*>.*?</a>',service_image,text,flags=re.S)
            text = text.replace('THE HEART OF OUR FITCHBURG VISION','SUPPORT GROUPS · COMMUNITY AT BHS FITCHBURG').replace('Find your people.<br><em>Feel more connected.</em>','Connection is<br><em>part of our story.</em>')
            text = re.sub(r'(<img src="assets/images/hero-welcome\.webp"[^>]*?)loading="lazy"',r'\1loading="eager" fetchpriority="high"',text)
        text = text.replace('Stock photographs do not depict BHS staff or patients.','')
        page.write_text(text,encoding='utf-8')
    credits = root/'photo-credits.html'
    if credits.exists():
        text = credits.read_text(encoding='utf-8')
        body = '<main id="main"><section class="pageintro"><span class="label">WEBSITE VISUALS</span><h1>Care & community.</h1><p>Website imagery illustrates service and community themes. For information about the location, providers, services, or equipment, please contact the Fitchburg office.</p></section></main>'
        credits.write_text(re.sub(r'<main id="main">.*?</main>',lambda m:body,text,flags=re.S),encoding='utf-8')
    css = '''
/* Approved horizontal identity and local imagery */
.brand img{width:330px;height:auto;max-height:105px;object-fit:contain}footer img{width:265px;height:auto}header{gap:28px}.joyphoto{border-radius:28px;overflow:hidden}.joyphoto img{object-position:66% center}.brand-story{align-items:center;gap:7%;padding:85px 6%}.brand-story .story-image{border-radius:14px;overflow:hidden}.story-image img{width:100%;height:420px;object-fit:cover}.brand-story p{max-width:590px}.caregrid{grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}.caretile{padding:0;overflow:hidden;background:#fffdf8!important;min-height:0}.caretile .care-photo{margin:0;width:100%;background:#e8ede7}.care-photo img{width:100%;height:220px;object-fit:cover;display:block}.care-body{padding:25px;display:flex;flex-direction:column;flex:1}.care-body h3{font-size:21px;line-height:1.25}.care-body p{font-size:14px}.care-body .discover{padding-top:20px;margin-top:auto}.communitytile img{height:280px;object-position:center}.pathphoto img{object-position:center}.communityspot{background:#ffe8cf}.communityintro h2{font-family:Georgia,serif;font-size:clamp(38px,4vw,60px)}.joyhero h1{font-family:Georgia,serif;font-weight:400;letter-spacing:-.035em}.joytag{display:none}.sunshape{display:none}.joyvisual{padding:0}.joyhero{align-items:center}.joyphoto img{height:540px}.story-image img,.care-photo img,.communitytile img{max-width:100%}@media(max-width:1200px){.brand img{width:275px}nav{gap:17px}.caregrid{grid-template-columns:repeat(2,minmax(0,1fr))}.care-photo img{height:265px}}@media(max-width:780px){.brand img{width:250px;max-height:85px}.brand-story{padding:55px 6%}.brand-story .story-image img{height:330px}.joyphoto img{height:390px;object-position:70% center}.communitytile img{height:265px}footer img{width:225px}}@media(max-width:600px){.caregrid{grid-template-columns:1fr}.care-photo img{height:240px}.brand img{width:225px}.care-body{padding:25px}.joyhero h1{font-size:44px}.joyphoto img{height:330px}}
'''
    with (root/'assets/style.css').open('a',encoding='utf-8') as stream:
        stream.write(css)
    for page in root.glob('*.html'):
        for image in re.findall(r'<img[^>]*src="([^"]+)"',page.read_text(encoding='utf-8')):
            if not image.startswith(('http:','https:','data:')) and not (root/image).is_file():
                raise RuntimeError('Missing image '+image+' in '+page.name)
    print('Applied approved logo and 14 images; checked local image references.')

if __name__ == '__main__':
    main()
