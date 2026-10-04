"""Build the selected reading collection without modifying its source transcripts."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT.parent
STORIES = (
    ('doric', 'Doric', 'A home without walls', 'A guarded druid and a wandering sorceress meet in the woods. Their conversation turns toward chosen names, vulnerability, and the wonder that survives experience.', 'Forest · Identity · Wonder', 'Doric - transcript.html', 'Begin here for a quiet introduction to Eliana’s way of seeing people.'),
    ('keira', 'Keira', 'Beyond the performance', 'An artifact hunt becomes a rescue. In the aftermath, two very different women talk about power, service, and the possibility of a life beyond performance.', 'Dungeon · Rescue · Hospitality', 'Keira - transcript.html', 'A more intimate encounter, ending with an invitation rather than an arrival.'),
    ('elias', 'Elias', 'A better quest', 'An orphan sets out with a wooden sword to prove he is a hero. Eliana offers another path: a home, a demanding desert initiation, and the freedom to become himself.', 'Mentorship · Desert · Belonging', 'Elias - transcript.html', 'The collection’s longer coming-of-age journey, from borrowed heroics to patient courage.'),
    ('godsblood', 'Godsblood Academy', 'The question beneath certainty', 'An academy mistakes a chosen name for a divine bloodline. Eliana’s response becomes a lesson in evidence, humility, and the difference between knowing and assuming.', 'Academy · Knowledge · Humility', 'Godsblood Academy - transcript.html', 'The institutional encounter: a classroom learning to question its own certainty.'),
    ('keres', 'Keres', 'Conversations in Hell', 'Eliana visits the Demon Lord for conversation rather than conquest. Beneath the armor of power and fear, she finds the abandoned boy—and offers an invitation to love.', 'Hell · Identity · Love', 'keres-eliana-frozenflame.html', 'The closing encounter turns the collection’s central question toward a sovereign who has made fear his refuge.'),
)

def text(value):
    return html.escape(value, quote=True)

def reading_body(source):
    """Keep the original prose and speaker attribution; remove export timestamps."""
    match = re.search(r'<main>(.*?)</main>', source, re.S)
    if not match:
        raise ValueError('Transcript has no main reading section')
    body = match.group(1)
    body = re.sub(r'<span class="date">.*?</span>', '', body, flags=re.S)
    return body

def document(title, description, content):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{text(title)} · Frozenflame Dialogues</title><meta name="description" content="{text(description)}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230c1822'/%3E%3Cpath d='M16 4 23 16 16 28 9 16Z' fill='%23d6ad73'/%3E%3Cpath d='M16 9v14' stroke='%230c1822' stroke-width='2'/%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to content</a>
<header class="masthead"><a class="brand" href="index.html">F<span class="brand-mark">◇</span>D <span>Frozenflame Dialogues</span></a><nav aria-label="Main"><a href="index.html#selection">The selection</a><a href="index.html#eliana">Eliana</a></nav></header>
{content}<footer class="site-footer"><a href="index.html">Frozenflame Dialogues</a><span>Selected fantasy dialogues · A reading collection</span></footer></body></html>'''

def cards(records):
    result = []
    for number, (slug, name, title, desc, tags, filename, note) in enumerate(records, 1):
        result.append(f'''<a class="story-card" href="{slug}.html"><span class="story-number">0{number}</span><div><p class="eyebrow">{text(name)}</p><h3>{text(title)}</h3><p>{text(desc)}</p><span class="tags">{text(tags)}</span></div><span class="read-link">Read the dialogue</span></a>''')
    return ''.join(result)

def home(records):
    return document('Selected readings', 'Five fantasy dialogues following Eliana Frozenflame through forest, dungeon, desert, academy, and Hell.', f'''
<main id="main"><section class="opening"><div class="opening-copy"><p class="eyebrow">Eliana Frozenflame · Selected readings</p><h1>Power gives way<br>to <em>relationship.</em></h1><p class="intro">A forest encounter. A rescue in the dark. A young man’s better quest. An academy learning to ask questions. A Demon Lord learning to lay down fear.</p><a class="primary" href="doric.html">Begin with Doric</a></div><figure class="cover"><img src="images/cover.png" alt="A warm cottage doorway reflected in still water in a twilight forest"><figcaption>Five encounters. One open door.</figcaption></figure></section>
<section class="selection" id="selection"><div class="section-heading"><div><p class="eyebrow">The selection</p><h2>Five ways into the story</h2></div><p>Read in this order, or follow the encounter that draws you in.</p></div><div class="story-list">{cards(records)}</div></section>
<section id="eliana" class="about"><p class="eyebrow">Meet Eliana</p><h2>A sorceress.<br>A midwife.<br>An open table.</h2><div><p>Eliana Frozenflame is a human sorceress whose life has stretched across centuries. Raised by elves, she chose her own contradictory name. She carries immense power, a difficult history, and a stubborn belief that people deserve choices.</p><p>Once a court wizard whose mirror physics served control, she now turns that knowledge toward protection, rescue, and revelation. Tea, bread, gardens, and shared work are as much a part of her world as planar wonders.</p><p class="editorial">This selection follows the collection’s recurring movement from fear and certainty toward relationship. These are dialogue transcripts, not a finished novel. The original wording is retained; source timestamps are omitted for reading. Continuity differences remain for future editing.</p></div></section></main>''')

def story_page(record, number, total, body, next_record):
    slug, name, title, desc, tags, filename, note = record
    # Count only prose, without markup, to give a transparent reading estimate.
    words = len(re.findall(r'\S+', html.unescape(re.sub(r'<[^>]+>', ' ', body))))
    minutes = max(1, round(words / 220))
    chapters = re.findall(r'<section class="chapter">(.*?)</section>', body, re.S)
    toc = ''
    if chapters:
        links = []
        for idx, chapter in enumerate(chapters, 1):
            title_match = re.search(r'<h2>(.*?)</h2>', chapter, re.S)
            chapter_title = re.sub(r'<[^>]+>', '', title_match.group(1))
            links.append(f'<a href="#chapter-{idx}">{chapter_title}</a>')
            body = body.replace('<section class="chapter">' + chapter, f'<section class="chapter" id="chapter-{idx}">' + chapter, 1)
        toc = '<nav class="chapters" aria-label="Chapters">' + ''.join(links) + '</nav>'
    next_link = f'<a class="primary" href="{next_record[0]}.html">Continue with {text(next_record[1])}</a>' if next_record else '<a class="primary" href="index.html#selection">Return to the collection</a>'
    return document(name, desc, f'''<main id="main" class="reader"><div class="reader-heading"><a class="back" href="index.html#selection">The collection</a><p class="eyebrow">Dialogue {number:02d} of {total:02d} · About {minutes} minutes</p><h1>{text(name)}</h1><p class="reader-subtitle">{text(title)}</p><p class="reader-intro">{text(desc)}</p><p class="reading-note">{text(note)}</p>{toc}</div><div class="transcript">{body}</div><div class="reader-end"><p>You’ve reached the end of this dialogue.</p>{next_link}<a class="back" href="#main">Back to the beginning</a></div></main>''')

def build():
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    (output / 'index.html').write_text(home(STORIES))
    for i, record in enumerate(STORIES):
        source = (SOURCES / record[5]).read_text()
        following = STORIES[i + 1] if i + 1 < len(STORIES) else None
        (output / (record[0] + '.html')).write_text(story_page(record, i + 1, len(STORIES), reading_body(source), following))
    print(f'Built collection and {len(STORIES)} reading pages.')

if __name__ == '__main__':
    build()
