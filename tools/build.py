"""Static site generator for nahow.de (German). Run: python tools/build.py"""
from pathlib import Path
import html, json, hashlib
import html as _h

R = Path(__file__).resolve().parents[1]
E = html.escape
WEB = json.loads((R / 'assets/web/web-manifest.json').read_text())
used = set()


def _v(f):
    return hashlib.md5((R / f).read_bytes()).hexdigest()[:8]


CSS = '/assets/site.css?v=' + _v('assets/site.css')
JS = '/assets/site.js?v=' + _v('assets/site.js')


def img(name, alt, cls='', eager=False, zoom=False):
    """Optimised web copy of an unchanged original. Every photo may be used once on the whole site."""
    key = next((name + e for e in ('.png', '.jpg') if name + e in WEB), name)
    assert key in WEB, 'unknown image ' + name
    assert key not in used, 'image repeated: ' + key
    used.add(key)
    m = WEB[key]
    stem = m['file'][:-5]
    attrs = 'fetchpriority="high"' if eager else 'loading="lazy"'
    z = f' data-full="/assets/web/lg/{stem}.webp"' if zoom else ''
    return (f'<img class="{cls}" src="/assets/web/{m["file"]}" width="{m["w"]}" height="{m["h"]}" '
            f'alt="{E(alt)}" {attrs} decoding="async"{z}>')


def doc(name):
    f = R / 'assets/documents' / name
    kb = f.stat().st_size / 1024
    return f'/assets/documents/{name}', (f'{kb/1024:.1f} MB' if kb > 1024 else f'{kb:.0f} KB')


NAV = [('Startseite', '/'), ('Projekte', '/projekte/'), ('Über uns', '/ueber-uns/'),
       ('Berichte', '/berichte/'), ('Einblicke', '/einblicke/'), ('Kontakt', '/kontakt/')]


def layout(title, desc, content, active='/'):
    items = ''.join(f'<a href="{u}"{" class=active aria-current=page" if u == active else ""}>{l}</a>' for l, u in NAV)
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#143a2e"><meta name="description" content="{E(desc, quote=True)}"><link rel="canonical" href="https://nahow.de{active}"><link rel="icon" href="/assets/brand/nahow-logo.png"><link rel="stylesheet" href="{CSS}"><title>{title} | NAHOW e.V.</title><script>document.documentElement.className="js"</script></head><body><a href="#inhalt" class="skip">Zum Inhalt springen</a><header class="site-header"><div class="bar"><a class="brand" href="/" aria-label="NAHOW e.V. Startseite"><img class="brand-logo" src="/assets/brand/nahow-logo.png" width="193" height="112" alt=""><span class="brand-copy"><strong>NAHOW e.V.</strong><small>Gemeinsam vor Ort</small></span></a><button class="menu-toggle" aria-label="Menü öffnen" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button><nav class="nav" id="main-nav" aria-label="Hauptnavigation">{items}<a class="nav-cta" href="/unterstuetzen/">Spenden</a></nav></div></header><main id="inhalt">{content}</main><footer class="footer"><div class="foot-grid"><div class="foot-brand"><img src="/assets/brand/nahow-logo.png" width="193" height="112" alt="nahow" loading="lazy"><p>Seit 2008 gemeinsam mit den Menschen in Enwen, Kamerun: für Bildung, Gesundheit, Lebensgrundlagen und Umwelt.</p></div><div><h4>Entdecken</h4><a href="/projekte/">Projekte</a><a href="/ueber-uns/">Über uns</a><a href="/berichte/">Berichte</a><a href="/einblicke/">Einblicke</a></div><div><h4>Mitmachen</h4><a href="/unterstuetzen/">Spenden</a><a href="/ueber-uns/#partner">Partnerschaften</a><a href="/kontakt/">Kontaktformular</a></div><div><h4>Rechtliches</h4><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a></div></div><div class="foot-bottom"><span>© NAHOW e.V. · Eingetragener Verein, Siegburg</span></div></footer><dialog class="lightbox" aria-label="Bildansicht"><button class="lb-close" aria-label="Schließen">×</button><img alt=""></dialog><script src="{JS}" defer></script></body></html>'''


def hero_intro(kicker, title, lead):
    return f'<section class="page-head"><div class="wrap"><span class="eyebrow">{kicker}</span><h1>{title}</h1><p class="lead">{lead}</p></div></section>'


def sec(kicker, title, body, cls='', lead='', id_=''):
    k = f'<span class="eyebrow">{kicker}</span>' if kicker else ''
    t = f'<h2>{title}</h2>' if title else ''
    l = f'<p class="lead">{lead}</p>' if lead else ''
    i = f' id="{id_}"' if id_ else ''
    return f'<section{i} class="section {cls}"><div class="wrap"><div class="sec-head reveal">{k}{t}{l}</div>{body}</div></section>'


def arrow_link(text, href, cls='link-arrow'):
    return f'<a class="{cls}" href="{href}">{text}<span aria-hidden="true">→</span></a>'


pages = {}

# ───────────────────────────── Startseite ─────────────────────────────
hero = f'''<section class="hero"><div class="hero-text"><span class="eyebrow light">Enwen · Nordwest-Kamerun</span><h1>Veränderung beginnt vor Ort.</h1><p>Seit 2008 engagiert sich NAHOW e.V. gemeinsam mit den Menschen in Enwen für Bildung, Gesundheit, bessere Lebensgrundlagen und eine nachhaltigere Zukunft.</p><div class="actions"><a class="btn btn-crimson" href="/projekte/">Unsere Projekte</a><a class="btn btn-ghost" href="/unterstuetzen/">Spenden</a></div></div><div class="hero-photo">{img("DSC_0495_Enwen-scaled", "Lachendes Kind in Enwen, Kamerun", eager=True)}</div></section>'''

facts = '''<section class="facts"><div class="wrap facts-grid">
<div><b>2008</b><span>Gründung des Vereins</span></div>
<div><b>14.08.2010</b><span>Einweihung der Grundschule in Enwen</span></div>
<div><b>ca. 280</b><span>Kinder nutzen seit 2010 die neuen Schulgebäude</span></div>
<div><b>1.000.000</b><span>Bäume sind unser Ziel (ein Vorhaben, keine Angabe gepflanzter Bäume)</span></div>
</div></section>'''

pillars = sec('Was uns antreibt', 'Aus konkreten Bedürfnissen entstehen tragfähige Lösungen.', '''<div class="pillars">
<a class="pillar reveal" href="/projekte/#bildung"><span class="num">01</span><h3>Bildung</h3><p>Eine wiederaufgebaute Grundschule, ein Ausbildungszentrum für Schneiderinnen und Tischler, IT-Ausbildung für Abiturienten.</p><span class="more">Mehr erfahren →</span></a>
<a class="pillar reveal" href="/projekte/#gesundheit"><span class="num">02</span><h3>Gesundheit &amp; Lebensgrundlagen</h3><p>Solarlampen für rund 200 Haushalte, Toiletten, Unterstützung der Gesundheitsstation und humanitäre Hilfe.</p><span class="more">Mehr erfahren →</span></a>
<a class="pillar reveal" href="/projekte/#umwelt"><span class="num">03</span><h3>Umwelt</h3><p>Aufforstung, effiziente Kocher und Biogas: weniger Brennholz, bessere Luft, langfristig tragfähige Perspektiven.</p><span class="more">Mehr erfahren →</span></a>
</div>''', 'tint')

story = f'''<section class="section"><div class="wrap split"><div class="split-photo reveal">{img("DSC_0329_Enwen-scaled", "Schulkinder in blauen Uniformen in Enwen")}</div><div class="split-text reveal"><span class="eyebrow">Unsere Wurzeln</span><h2>Verbunden mit Enwen.</h2><p>Die Idee zu NAHOW entstand aus einer Reise nach Kamerun, in das Dorf Enwen. Dort sah unser Gründer Tichi Mbanwie aus erster Hand, wie sehr es an Bildung fehlte. Gemeinsam mit den Dorfbewohnern begann er, Lösungen zu entwickeln, die zu den Bedürfnissen vor Ort passen.</p><p>Aus der ersten Schule wurde ein Verein, aus einem Verein ein Netzwerk von Unterstützern, die Projekte in den Bereichen Bildung, Gesundheit und Umwelt möglich machen.</p>{arrow_link("Mehr über NAHOW", "/ueber-uns/")}</div></div></section>'''

timeline_items = [
    ('2008', 'Vereinsgründung', 'Im September 2008 wird NAHOW e.V. gegründet und beginnt, Spenden für eine Schule in Enwen zu sammeln.'),
    ('2010', 'Grundschule eingeweiht', 'Am 14. August 2010 wird die wiederaufgebaute Grundschule übergeben, dazu das Fußballfeld mit einem Freundschaftsspiel.'),
    ('2012', 'Ausbildungszentrum', 'Ein Zentrum für junge Schneiderinnen und Tischler eröffnet Perspektiven nach der Grundschule.'),
    ('2013', 'Solarstrom für Enwen', 'Solarlampensets ersetzen Kerosinlampen in Haushalten, verbunden mit dem Bau von Toiletten.'),
    ('2016–17', 'Gesundheit', 'Schultoiletten, Unterstützung der Gesundheitsstation und eine Bedarfsanalyse für das Health Centre.'),
    ('2018', 'Humanitäre Hilfe', 'Wegen der Krise in der Region liegt der Schwerpunkt auf akuter Hilfe für Familien.'),
    ('Heute', 'Aufforstung &amp; IT-Ausbildung', 'Das 1.000.000-Bäume-Projekt, effiziente Kocher und IT-Ausbildung für Abiturienten.'),
]
timeline = '<ol class="timeline">' + ''.join(
    f'<li class="reveal"><span class="t-year">{y}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for y, t, d in timeline_items) + '</ol>'
history = sec('Unser Weg', 'Von der ersten Schule zur Aufforstung.', timeline, 'tint', 'Die wichtigsten Stationen, belegt durch unsere Berichte.')

reports_teaser = sec('Transparenz', 'Nachvollziehbar, was mit Spenden geschieht.', f'''<div class="report-strip reveal"><p>Zu unseren großen Projekten gibt es ausführliche Abschlussberichte mit Chronik, Kosten und Ergebnissen. Sie stehen öffentlich als PDF zur Verfügung.</p><div class="strip-actions">{arrow_link("Alle Berichte ansehen", "/berichte/")}</div></div>''')

cta = '''<section class="cta"><div class="wrap cta-flex"><div><h2>Unterstützung, die vor Ort ankommt.</h2><p>Ob Spende, Partnerschaft oder Engagement: jeder Beitrag hilft, die Arbeit in Enwen weiterzuführen.</p></div><a class="btn btn-light" href="/unterstuetzen/">NAHOW unterstützen</a></div></section>'''

pages['/'] = layout('Gemeinsam vor Ort', 'NAHOW e.V. engagiert sich seit 2008 in Enwen, Kamerun, für Bildung, Gesundheit, Lebensgrundlagen und Umwelt.',
                    hero + facts + pillars + story + history + reports_teaser + cta, '/')

# ───────────────────────────── Projekte ─────────────────────────────


def chips(items):
    return '<ul class="chips">' + ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in items) + '</ul>'


def project(id_, status, year, title, text, chip_items, pdf=None, photo=None, reverse=False, plain=''):
    badge = f'<span class="badge {"live" if status == "Laufend" else ""}">{status}</span>'
    pdfl = ''
    if pdf:
        href, size = doc(pdf[0])
        pdfl = f'<a class="link-arrow" href="{href}" target="_blank" rel="noopener">{pdf[1]} <small>(PDF, {size})</small><span aria-hidden="true">↗</span></a>'
    media = f'<div class="p-photo">{photo}</div>' if photo else f'<div class="p-photo p-plain"><span>{plain or year}</span></div>'
    return (f'<article class="project{" reverse" if reverse else ""} reveal" id="{id_}">{media}<div class="p-body"><div class="p-meta">{badge}<span>{year}</span></div>'
            f'<h3>{title}</h3>{text}{chips(chip_items) if chip_items else ""}{pdfl}</div></article>')


current = (
    project('umwelt', 'Laufend', 'Heute', 'Das 1.000.000-Bäume-Projekt',
            '<p>Unser Ziel ist es, in und um Enwen eine Million Bäume zu pflanzen. Das ist ein Vorhaben, keine Angabe bereits gepflanzter Bäume. Aufforstung schützt die Umwelt und stärkt die Lebensgrundlagen der Menschen.</p><p>Zwei weitere Schwerpunkte ergänzen das Projekt: <b>effiziente Kocher</b>, die den Holzverbrauch senken und die Gesundheit schützen, sowie <b>Biogas</b> aus organischen Abfällen als nachhaltige Energiequelle.</p>',
            [('Ziel', '1.000.000 Bäume'), ('Schwerpunkte', 'Aufforstung · Kocher · Biogas')],
            photo=img('DSC_0249_Enwen-scaled', 'Grüne Hügel bei Enwen, Kamerun'))
    + project('it', 'Laufend', 'Heute', 'IT-Ausbildung für Abiturienten',
              '<p>Mit einer IT-Ausbildung möchten wir jungen Menschen mit Abitur zusätzliche berufliche Perspektiven eröffnen. Möchten Sie das Projekt unterstützen oder mehr erfahren? Schreiben Sie uns über das Kontaktformular.</p>',
              [], photo=None, reverse=True, plain='IT'))

done = (
    project('bildung', 'Abgeschlossen', '2008–2010', 'Eine Grundschule für Enwen',
            '<p>Die staatliche Grundschule in Enwen bestand aus einem einzigen Schulraum, mehrere Behelfsgebäude waren eingestürzt oder einsturzgefährdet. Gemeinsam mit den Dorfbewohnern baute NAHOW Klassenzimmer und Büros neu auf.</p><p>Am 14. August 2010 wurde die Schule feierlich übergeben. Das Fußballfeld davor stiftete Michael Althof; es trägt seinen Namen: „The Michael Althof Football Field“.</p>',
            [('Kosten', '26.475,09 €'), ('Einweihung', '14.08.2010'), ('Kinder', 'ca. 280')],
            ('projektendbericht_schule.pdf', 'Projektendbericht Schule'),
            img('new-field_Enwen', 'Die Schule in Enwen mit dem neu hergerichteten Fußballfeld'))
    + project('ausbildung', 'Abgeschlossen', '2012', 'Ausbildungszentrum für Schneiderinnen und Tischler',
              '<p>Jährlich schließen rund 50 Kinder die Grundschule in Enwen ab, doch weiterführende Schulen sind weit entfernt und unbezahlbar. Das Ausbildungszentrum gibt jungen Menschen, besonders Mädchen, eine berufliche Perspektive.</p><p>Ergänzend gibt es Ernährungsberatung und Aufklärung. Als nächster Schritt war geplant, Kochsäcke sowie Schul- und Ausbildungsuniformen herzustellen, damit Absolventinnen eine Chance auf Beschäftigung haben.</p>',
              [('Kosten', '36.910,87 €'), ('Bericht', '05.05.2012')],
              ('projektendbericht_ausbildungszentrum.pdf', 'Projektendbericht Ausbildungszentrum'),
              img('DSC_0293_Enwen-scaled', 'Neu gefertigte Schulbänke im Ausbildungszentrum'), reverse=True)
    + project('solar', 'Abgeschlossen', '2012–2013', 'Solarstrom für Enwen',
              '<p>In den rund 200 Haushalten Enwens wurde abends mit Kerosinlampen gearbeitet. Solarlampensets sorgen für sicheres, sauberes Licht. Wer ein Set erhielt, baute im Gegenzug eine Toilette, denn über 80 % der Haushalte hatten bisher keine.</p>',
              [('Kosten', '35.013,57 €'), ('Haushalte', 'ca. 200')],
              ('projektbericht-solarzentrum.pdf', 'Projektendbericht Solarstrom'),
              img('DSC_0239_Enwen', 'Kinder in Schuluniform in Enwen'))
    + project('gesundheit', 'Abgeschlossen', '2016–2017', 'Schultoiletten und Gesundheitsstation',
              '<p>2016 verbesserte NAHOW die Schultoiletten und unterstützte die örtliche Gesundheitsstation. Eine Bedarfsanalyse von 2017 zeigt, was fehlt: Das Health Centre betreut mindestens 60 Patientinnen und Patienten im Monat, hat aber nur eine Hilfskraft und keinen festen Arzt.</p>',
              [('Bedarfsanalyse', '2017')],
              ('Report-on-Enwai-Health-Centre.pdf', 'Need assessment (englisch)'),
              img('IMG_8277_Enwen', 'Kinder und Besucherin in Enwen'), reverse=True)
    + project('hilfe', 'Abgeschlossen', '2017–2018', 'Humanitäre Hilfe',
              '<p>Mit Partnerorganisationen verteilte NAHOW wiederverwendbare Hygieneartikel an Frauen und Mädchen sowie Betten und Medikamente an Familien und spendete Schulbücher und Tafeln.</p>',
              [], ('Statusbericht-Nahow-2018.pdf', 'Statusbericht 2018'),
              img('DSC_0544_Enwen-scaled', 'Kinder in Enwen'))
)

situation = '''<aside class="notice reveal"><h3>Aktuelle Lage in der Region</h3><p>Nach unserem Statusbericht vom Februar 2018 sind Schulen im englischsprachigen Teil Kameruns seit Oktober 2016 weitgehend geschlossen. Schule und Ausbildungszentrum in Enwen blieben damals bis auf Weiteres geschlossen; NAHOW konzentrierte sich auf humanitäre Hilfe. Mehr dazu im Bericht.</p></aside>'''

projects = (hero_intro('Unsere Arbeit', 'Projekte in Enwen.', 'Von der ersten Schule bis zur Aufforstung: Das haben wir gemeinsam mit den Menschen vor Ort erreicht, und das haben wir vor.')
            + '<nav class="subnav" aria-label="Projektbereiche"><div class="wrap"><a href="#laufend">Laufende Projekte</a><a href="#abgeschlossen">Abgeschlossene Projekte</a><a href="/berichte/">Berichte</a></div></nav>'
            + sec('Aktuell', 'Laufende Projekte', current, id_='laufend')
            + sec('Rückblick', 'Abgeschlossene Projekte', done + situation, 'tint', id_='abgeschlossen')
            + cta)
pages['/projekte/'] = layout('Unsere Projekte', 'Projekte von NAHOW e.V. in Enwen, Kamerun: Grundschule, Ausbildungszentrum, Solarstrom, Gesundheit und Aufforstung.', projects, '/projekte/')

# ───────────────────────────── Über uns ─────────────────────────────
def _member(i, n, r, photo=None, alt=''):
    pic = f'<span class="member-photo">{img(photo, alt)}</span>' if photo else f'<span class="mono-circle">{i}</span>'
    return f'<article class="member reveal">{pic}<h3>{n}</h3><p>{r}</p></article>'


team = '<div class="team">' + _member('TM', 'Tichi Mbanwie', 'Vorsitzender', 'DSC_0468_Enwen', 'Porträt von Tichi Mbanwie') + _member('MA', 'Michael Althof', 'Kassenwart', 'althof', 'Porträt von Michael Althof') + _member('VM', 'Vyvian Mbanwie', 'Koordinator USA', 'vyvian', 'Porträt von Vyvian Mbanwie') + '</div>'

press = '<div class="press">' + ''.join(
    f'<figure class="reveal">{img(n, a, zoom=True)}<figcaption>{c}</figcaption></figure>' for n, a, c in [
        ('Generalanzeiger-Bonn-002_Enwen', 'Zeitungsartikel: Dem Heimatdorf etwas zurückgeben', 'General-Anzeiger Bonn: „Dem Heimatdorf etwas zurückgeben“'),
        ('Nahow_Presse_Generalanzeiger_Bonn', 'Zeitungsartikel: Die neue Sporthalle wird schon genutzt', 'General-Anzeiger Bonn: „Die neue Sporthalle wird schon genutzt“'),
        ('Nahow_Presse_Blickpunkt_Schaufenster', 'Zeitungsartikel: Endlich Licht im Haus', 'Blickpunkt Schaufenster: „Endlich Licht im Haus“'),
    ]) + '</div>'

about = hero_intro('Über uns', 'Verwurzelt in Enwen.', 'NAHOW e.V. verbindet langfristiges Engagement mit der Zusammenarbeit vor Ort.')
about += f'<section class="banner">{img("DSC_0554_Enwen-scaled", "Das NAHOW-Team nach einem Fußballspiel in Enwen")}</section>'
about += sec('Geschichte', 'Aus einer Reise wurde eine Aufgabe.', '''<div class="prose two-col reveal"><p>Die Geschichte von NAHOW begann mit einer einfachen Idee und dem Wunsch, in benachteiligten Gemeinschaften etwas zu bewegen. Unser Gründer Tichi Mbanwie wollte Menschen helfen, ein besseres Leben zu führen und dabei die Umwelt zu schützen.</p><p>Die Inspiration kam auf einer Reise nach Kamerun, in das Dorf Enwen. Dort sah er aus erster Hand die Herausforderungen der Gemeinschaft: Armut, mangelnde Bildung und Umweltprobleme.</p><p>Im September 2008 wurde der Verein gegründet. Im Laufe der Jahre kamen weitere Unterstützer und Freiwillige hinzu, und die Projekte erweiterten sich auf Bildung, Gesundheit und Umwelt.</p><p>Heute konzentrieren wir uns auf die Aufforstung von Enwen und die Förderung effizienter Kocher. Mit unserem aktuellen Projekt streben wir an, 1.000.000 Bäume zu pflanzen.</p></div>''')
about += sec('Mission und Werte', 'Was uns leitet.', '''<div class="values">
<div class="reveal"><h3>Bildung &amp; Gesundheit</h3><p>Unsere bisherigen Aktivitäten konzentrierten sich auf die Unterstützung von Bildung und Gesundheit. Wir haben Bildungsprogramme umgesetzt und die Lebensbedingungen vieler Menschen verbessert.</p></div>
<div class="reveal"><h3>Umweltschutz</h3><p>Nun setzen wir einen neuen Schwerpunkt: Aufforstung, effiziente Kocher und Biogas sollen den Holzverbrauch senken und die Gesundheit der Gemeinschaften verbessern.</p></div>
<div class="reveal"><h3>Gemeinsam vor Ort</h3><p>Wir arbeiten eng mit den Dorfbewohnern zusammen und entwickeln Lösungen, die zu ihren Bedürfnissen passen und langfristig tragen.</p></div></div>''', 'tint')
culture = '<div class="strip">' + ''.join(f'<figure class="reveal{" wide" if c == "wide" else ""}">{img(n, a, c, zoom=True)}</figure>' for n, a, c in [
    ('DSC_0723_Enwen-scaled', 'Gruppenbild in traditioneller Festkleidung in Enwen', 'wide'),
    ('DSC_0469_Enwen-scaled', 'Lächelnder Mann in traditioneller Kleidung', ''),
    ('DSC_0477_Enwen', 'Traditionelle Kleidung und Kopfbedeckung in Enwen', ''),
]) + '</div>'
about += sec('Kultur', 'Enwen: Menschen und Traditionen', culture, 'tint', 'Festliche Kleidung und Kopfbedeckungen gehören zum Alltag und zu den Feiern im Dorf. Zum Vergrößern anklicken.')
about += sec('Menschen hinter NAHOW', 'Das Team', team)
about += sec('Presse', 'NAHOW in den Medien', press, 'tint', 'Zeitungsausschnitte. Zum Vergrößern anklicken.')
about += sec('Partnerschaften', 'Unsere Unterstützer und Sponsoren', '''<div class="prose narrow reveal"><p>Werden Sie Teil unserer Mission und unterstützen Sie unsere Baumprojekte in Kamerun! Als Sponsor haben Sie die Möglichkeit, sich auf nahow.de zu präsentieren und Ihren Beitrag für den Umweltschutz sichtbar zu machen. Ihr Firmenlogo binden wir mit Link zu Ihrer Website hier ein.</p><p>Wir informieren Sie gern ausführlich über die Möglichkeiten einer Sponsorschaft.</p>''' + arrow_link('Sponsorschaft anfragen', '/kontakt/') + '</div>', id_='partner')
about += cta
pages['/ueber-uns/'] = layout('Über NAHOW', 'Die Geschichte, die Werte und das Team von NAHOW e.V.', about, '/ueber-uns/')

# ───────────────────────────── Berichte ─────────────────────────────


def rep(file, title, meta):
    href, size = doc(file)
    return f'<a class="doc reveal" href="{href}" target="_blank" rel="noopener"><span class="doc-ico">PDF</span><span class="doc-body"><strong>{title}</strong><small>{meta} · {size}</small></span><span class="doc-go" aria-hidden="true">↗</span></a>'


berichte = hero_intro('Transparenz', 'Berichte und Dokumente.', 'Was wir gebaut haben, was es gekostet hat und was wir gelernt haben: unsere Berichte stehen öffentlich zur Verfügung.')
berichte += sec('Projektberichte', 'Abschlussberichte', '<div class="docs">' +
                rep('projektendbericht_schule.pdf', 'Projektendbericht Schule', 'August 2010 · Wiederaufbau der Grundschule') +
                rep('projektendbericht_ausbildungszentrum.pdf', 'Projektendbericht Ausbildungszentrum', 'Mai 2012 · Schneiderei und Tischlerei') +
                rep('projektbericht-solarzentrum.pdf', 'Projektendbericht Solarstrom für Enwen', 'März 2013 · Solarlampen und Toiletten') + '</div>')
berichte += sec('Berichte und Briefe', 'Reisen, Lage und Bedarf', '<div class="docs">' +
                rep('kamerunreisebericht-dec.-2013.pdf', 'Kamerun-Reisebericht', 'Dezember 2013') +
                rep('Statusbericht-Nahow-2018.pdf', 'Statusbericht 2018', 'Februar 2018 · Lage in der Region') +
                rep('Report-on-Enwai-Health-Centre.pdf', 'Need assessment of Ewai Health Centre', '2017 · englisch') + '</div>', 'tint')
berichte += sec('Presse und Weiteres', 'Medien und Hintergrund', '<div class="docs">' +
                rep('Pressemitteilung_Lichtblicke_Unterschleisheim.pdf', 'Pressemitteilung Lichtblicke Unterschleißheim', 'Benefizkonzert') +
                rep('Hessnatur-Blog-12_07_05.pdf', 'Hessnatur-Blog', 'Artikel, Juli 2012') +
                rep('U.S.-Department-of-State.pdf', 'U.S. Department of State: Cameroon 2017 Human Rights Report', 'englisch') + '</div>')
pages['/berichte/'] = layout('Berichte', 'Projektberichte und Dokumente von NAHOW e.V.', berichte, '/berichte/')

# ───────────────────────────── Unterstützen ─────────────────────────────
support = hero_intro('Unterstützen', 'Gemeinsam mehr möglich machen.', 'Ob Spende, Partnerschaft oder ehrenamtliches Engagement: jede Form der Unterstützung hilft, die Arbeit in Enwen weiterzuführen.')
support += sec('Spenden', 'Direkt an NAHOW e.V.', '''<div class="donate-grid"><div class="bank reveal"><span class="eyebrow">Banküberweisung</span><h3>Spendenkonto</h3><dl><dt>Kontoinhaber</dt><dd>NAHOW e.V.</dd><dt>IBAN</dt><dd class="mono">DE65 7001 0080 0849 5288 05</dd><dt>BIC</dt><dd>PBNKDEFF</dd><dt>Bank</dt><dd>Postbank</dd></dl></div><div class="donate-side reveal"><h3>Andere Wege, sich einzubringen</h3><p>Sie möchten NAHOW mit Know-how, Netzwerken oder einer Projektpartnerschaft unterstützen? Schreiben Sie uns über das Kontaktformular.</p><a class="btn btn-crimson" href="/kontakt/">Kontakt aufnehmen</a></div></div>''')
support += f'''<section class="section tint"><div class="wrap split"><div class="split-photo reveal">{img("Nahow_Spenden-scaled", "Gedenktafel im gestifteten Klassenraum in Enwen", zoom=True)}</div><div class="split-text reveal"><span class="eyebrow">Wirkung vor Ort</span><h2>Ihre Unterstützung wird sichtbar.</h2><p>Spenderinnen und Spender werden in Enwen sichtbar gewürdigt. Im Klassenraum, den der Verein Lichtblicke stiftete, erinnert eine Tafel daran, wer ihn möglich gemacht hat.</p>{arrow_link("Projekte ansehen", "/projekte/")}</div></div></section>'''
pages['/unterstuetzen/'] = layout('Unterstützen und spenden', 'NAHOW e.V. unterstützen: Spendenkonto, Partnerschaft und Engagement.', support, '/unterstuetzen/')

# ───────────────────────────── Kontakt ─────────────────────────────
contact = hero_intro('Kontakt', 'Schreiben Sie uns.', 'Für Fragen zu NAHOW, Projektideen, Unterstützung oder Presseanfragen.') + sec('Kontaktformular', 'Ihre Nachricht an NAHOW e.V.', '<div class="form-wrap"><form class="contact-form" action="/kontakt/senden.php" method="post"><div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" required maxlength="120" autocomplete="name"></div><div class="field"><label for="f-mail">Ihre E-Mail-Adresse</label><input id="f-mail" name="email" type="email" required maxlength="200" autocomplete="email"></div><div class="field"><label for="f-msg">Nachricht</label><textarea id="f-msg" name="message" rows="8" required maxlength="5000"></textarea></div><div class="hp" aria-hidden="true"><label>Bitte leer lassen<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div><input type="hidden" name="ts" value="" id="f-ts"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>Ich habe die <a href="/datenschutz/">Datenschutzerklärung</a> gelesen und bin damit einverstanden, dass meine Angaben zur Bearbeitung der Anfrage per E-Mail an NAHOW e.V. übermittelt werden.</span></label><button class="btn btn-crimson" type="submit">Nachricht senden</button></form></div>')
pages['/kontakt/'] = layout('Kontakt', 'Kontaktieren Sie NAHOW e.V. über das Kontaktformular.', contact, '/kontakt/')
pages['/kontakt/danke/'] = layout('Nachricht gesendet', 'Ihre Nachricht an NAHOW e.V. wurde gesendet.', hero_intro('Kontakt', 'Vielen Dank.', 'Ihre Nachricht wurde gesendet. Wir melden uns so bald wie möglich bei Ihnen.') + '<section class="section"><div class="wrap"><a class="btn btn-crimson" href="/">Zur Startseite</a></div></section>', '/kontakt/')
pages['/kontakt/fehler/'] = layout('Nachricht nicht gesendet', 'Die Nachricht konnte nicht gesendet werden.', hero_intro('Kontakt', 'Das hat leider nicht geklappt.', 'Bitte prüfen Sie Ihre Angaben und versuchen Sie es erneut. Falls das Problem bleibt, versuchen Sie es später noch einmal.') + '<section class="section"><div class="wrap"><a class="btn btn-crimson" href="/kontakt/">Zurück zum Formular</a></div></section>', '/kontakt/')

# ───────────────────────────── Rechtliches ─────────────────────────────


def _paras(path, start, stop):
    L = [l.strip() for l in (R / path).read_text(encoding='utf-8').split('\n')]
    return L[start:stop]


def _render(lines):
    return ''.join('<p>' + _h.escape(l) + '</p>' for l in lines if l)


def _block(lines):
    return '<p>' + '<br>'.join(_h.escape(l).replace('(at)', '@') for l in lines if l) + '</p>'


def _imp_html():
    L = _paras('tools/legal/impressum-original.txt', 0, 100)
    return (_block(L[1:6]) + '<p>Kontakt: <a href="/kontakt/">Zum Kontaktformular</a></p>' + _block(L[8:10]) + _block([L[10]])
            + '<h3>' + _h.escape(L[11]) + '</h3>' + _render([L[12]]) + '<h3>' + _h.escape(L[13]) + '</h3>' + _render([L[14]]))


def _dsg_html():
    L = _paras('tools/legal/datenschutz-original.txt', 0, 100)
    s = _render(L[1:4]) + '<h3>I. Informationen über uns als Verantwortliche</h3>' + _render([L[9]])
    s += _block([l for l in L[10:17] if not l.startswith(('Telefon', 'E-Mail'))]) + '<p>Kontakt: <a href="/kontakt/">Zum Kontaktformular</a></p>'
    s += '<h3>II. Rechte der Nutzer und Betroffenen</h3>' + _render(L[18:26])
    return s


def legal_page(kicker, title, body):
    return f'<section class="section legal"><div class="wrap"><div class="sec-head"><span class="eyebrow">{kicker}</span><h1>{title}</h1></div><div class="prose narrow">{body}</div></div></section>'


pages['/impressum/'] = layout('Impressum', 'Impressum und Anbieterkennzeichnung von NAHOW e.V.', legal_page('Impressum', 'NAHOW e.V.', _imp_html()), '/impressum/')
pages['/datenschutz/'] = layout('Datenschutz', 'Datenschutzerklärung von NAHOW e.V.', legal_page('Datenschutz', 'Datenschutzerklärung', _dsg_html() + '''<h3>III. Informationen zur Datenverarbeitung auf dieser Website</h3><p>Diese Website ist statisch aufgebaut. Sie verwendet keine Cookies, keine Analyse- oder Trackingdienste, keine Nutzerkonten und lädt keine Schriftarten, Karten oder Videos von Drittanbietern. Beim Aufruf verarbeitet der Hostinganbieter technisch notwendige Zugriffsdaten (z. B. IP-Adresse, Datum und Uhrzeit, aufgerufene Seite) in Server-Logdateien, um den Betrieb und die Sicherheit der Website zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO).</p><p>Wenn Sie das Kontaktformular nutzen, werden Ihr Name, Ihre E-Mail-Adresse und Ihre Nachricht per E-Mail an den Verein übermittelt und ausschließlich zur Bearbeitung Ihrer Anfrage verwendet (Art. 6 Abs. 1 lit. b bzw. f DSGVO). Die Angaben werden nicht auf dem Server gespeichert und nicht an Dritte weitergegeben.</p>'''), '/datenschutz/')

# ───────────────────────────── Einblicke (zuletzt: bekommt alle übrigen Fotos) ─────────────────────────────
SKIP = ('DSC_0322', 'althof', 'vyvian', 'DSC_0004', 'DSC_0340', 'DSC_0471', 'DSC_0482', 'DSC_0535', 'shield_', 'Footballfield', 'Tafel', 'P1040905',
        'Kinder1', '100_5729', 'IMG_1241', 'IMG_1242', 'Africa-map', 'Generalanzeiger', 'Nahow_Presse', 'Nahow_Spenden',
        'nahow_image_collage', 'Spende_Sekundarschule')
names = [k for k in sorted(WEB) if k not in used and not any(s in k for s in SKIP)]
masonry = ''.join(f'<figure class="g-item">{img(k, "Foto aus Enwen, Kamerun", zoom=True)}</figure>' for k in names)
gal = hero_intro('Einblicke', 'Momente aus Enwen.', 'Fotos aus den Projekten und dem Alltag vor Ort. Zum Vergrößern anklicken.') + f'<section class="section"><div class="wrap"><div class="masonry">{masonry}</div></div></section>'
pages['/einblicke/'] = layout('Einblicke und Fotos', 'Fotos aus den Projekten von NAHOW e.V. in Enwen, Kamerun.', gal, '/einblicke/')

for path, d in pages.items():
    out = R / path.strip('/') / 'index.html' if path != '/' else R / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(d, encoding='utf-8')
(R / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(
    f'<url><loc>https://nahow.de{p}</loc></url>' for p in pages if p not in ('/kontakt/danke/', '/kontakt/fehler/')) + '</urlset>', encoding='utf-8')
(R / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://nahow.de/sitemap.xml\n', encoding='utf-8')
print('Generated', len(pages), 'pages;', len(used), 'distinct photos used, none repeated;', len(names), 'in gallery')
