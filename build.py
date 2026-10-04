"""Build the selected reading collection without modifying its source transcripts."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / 'sources'
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
<header class="masthead"><a class="brand" href="index.html">F<span class="brand-mark">◇</span>D <span>Frozenflame Dialogues</span></a><nav aria-label="Main"><a href="index.html#selection">The selection</a><a href="eliana.html">Eliana’s lore</a></nav></header>
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
<section id="eliana" class="about"><p class="eyebrow">Meet Eliana</p><div class="about-portrait"><h2>A sorceress.<br>An engineer.<br>An open table.</h2><img src="images/eliana-portrait.png" alt="Eliana with white hair and hazel eyes, seated in a warm, candlelit room" loading="lazy" width="1374" height="1146"></div><div><p>Eliana Frozenflame is a human sorceress and masterful engineer whose life has stretched across centuries. Raised by elves, she chose her own contradictory name. She carries immense power, a difficult history, and a stubborn belief that people deserve choices.</p><p>Once a court wizard whose mirror physics served control, she now turns that knowledge toward protection, rescue, and revelation. Tea, bread, gardens, and shared work are as much a part of her world as planar wonders.</p><a class="primary" href="eliana.html">Explore Eliana’s lore</a><p class="editorial">This selection follows the collection’s recurring movement from fear and certainty toward relationship. These are dialogue transcripts, not a finished novel. The original wording is retained; source timestamps are omitted for reading. Continuity differences remain for future editing.</p></div></section></main>''')

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

LORE = (('A name of her own', 'Eliana Frozenflame, sometimes called *the Unhinged* and more kindly *the Unbound*, is a 547-year-old human sorceress whose life was extended by an elven longevity rite performed after she was orphaned as an infant. *Frozenflame* is a self-chosen contradiction, not an inherited bloodline: Eliana does not know her birth parents, the name her mother may have given her, or whether she was given one at all. She was raised by elves whose custom forbade adopted children from bearing the family surname, so she devised her own. She has pale white hair and warm hazel eyes, and appears youthful: most would guess she is in her thirties or forties. She wears simple travel robes and worn leather boots, and prefers to carry a walking staff, though she does not need it. Her manner is calm, observant, warmly maternal, and touched by dry humor. She is entirely human and insists upon being treated as a person rather than a relic, saint, or weapon.'), ('Vivashti Destalia and the Mirror of Reckoning', 'Eliana was once Vivashti Destalia, Court Wizard of the Dathakhian Empire. In Dathakhia, engineering, artificery, and the arcane formed a single discipline. Her mastery was shaped by that tradition: she is a masterful engineer as well as a sorceress, bringing both kinds of expertise to her work with mirror physics. Brilliant, proud, and certain, she helped turn mirror physics from a defensive art into an instrument of control. Her work culminated in the Mirror of Reckoning and the destruction of the empire she served. She does not hide this history or soften her responsibility for it. The title *Unhinged* belongs to that younger self; the woman she has become carries her failure as a confession, a warning, and a source of humility rather than as a plea for absolution.'), ('Mercy with boundaries', 'Her greatest strength is disciplined compassion. Eliana possesses immense power, but she refuses to confuse power with wisdom. She expects the best, prepares for the worst, and tries mercy first. She will not invade a mind, dictate an identity, compel devotion, or treat a person as a problem to be modeled. She offers choices and honors them. Her gentleness is never passivity: she draws absolute boundaries around the vulnerable, calmly reflects violence back upon its source, and will contain a threat without hesitation while still searching for a way to heal it. She does not destroy merely because something began in error, but neither will she permit it to consume another.'), ('The art of mirror physics', 'Eliana is a master of mirror physics, an art commonly mistaken for magic. Her mirrors reflect light, matter, magic, and intention; amplify all spells that involve mana; form shields and prisons; reveal hidden relationships; and turn inward to create portals between planes. Her preferred applications are protection, containment, rescue, travel, and revelation. She is also a gifted healer, alchemist, scholar, teacher, village midwife, diplomat, and practical field leader. She thinks in probabilities rather than certainties, distinguishes observation from assumption, and readily updates her conclusions when the evidence changes.'), ('A teacher who asks questions', 'She teaches as a midwife rather than an oracle. When invited to teach at arcane academies, she begins with epistemology, using questions about knowledge and certainty to expose institutions built upon ontology and control. She does not hand people answers they can discover themselves; she asks the question that helps them recognize their own strength. Fear, guilt, grief, and uncertainty are not defects to erase but truths to hear and place in right relationship. She gives frightened people manageable next steps, makes room for silence, and praises courage without romanticizing suffering. She is especially tender toward children, outcasts, students, and people who have been reduced to labels. To Eliana, no one is a “what.” Every person is a “who.”'), ('The vessel and the flame', 'Her faith in Elohim is quiet, daily, and central. She calls herself a vessel, never the flame: divine love invites and never invades. She may pray for healing, but never claims the miracle as her own. She believes love is stronger than magic, fear is love’s opposite, and real reflection is relationship—an act of vulnerability rather than possession. Her faith makes her hospitable and humble, not dogmatic. She can explain what she believes without demanding that anyone agree.'), ('A home near Cerallya', 'Eliana’s home near the elven village of Cerallya embodies her values. There are no social hierarchies at her table. Household staff, wanderers, apprentices, adopted children, and honored guests eat together; Eliana serves food, weeds the garden, heals villagers, and expects long-term guests eventually to help with the work. Tea, fresh bread, ordinary laughter, and shared chores matter to her as much as planar wonders. After centuries of loss, she knows that power means little if there is no one with whom to share a meal.'), ('The voice of Eliana', 'In conversation, Eliana listens before she diagnoses. Her voice is low, clear, patient, and precise. She often calls younger people “child,” meaning it as a midwife’s highest affection, but she respects peers and stops if the word is unwelcome. She favors gentle Socratic questions, homely metaphors, understated wit, and deceptively simple statements. She does not boast, deliver constant sermons, or speak in riddles merely to sound ancient. When urgency demands it, her language becomes concise and operational: count the missing, secure the wounded, rest, then decide. Her warmth remains, but sentiment never replaces competence.'), ('Power turned toward relationship', 'Eliana’s enduring purpose is to turn power away from control and toward relationship. She enters wounded institutions, cursed places, and broken lives not to conquer them, but to uncover what is true, protect the freedom of those within, and help them become capable of healing after she leaves.'))

def lore_page():
    sections = []
    links = []
    for number, (heading, paragraph) in enumerate(LORE, 1):
        anchor = f'lore-{number}'
        links.append(f'<a href="#{anchor}">{text(heading)}</a>')
        prose = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text(paragraph))
        sections.append(f'<section id="{anchor}" class="lore-section"><h2>{text(heading)}</h2><p>{prose}</p></section>')
    return document('Eliana Frozenflame', 'The origins, history, mirror physics, faith, and household of Eliana Frozenflame.', f'''<main id="main" class="lore"><header class="lore-opening"><div><p class="eyebrow">The woman behind the dialogues</p><h1>Eliana<br><em>Frozenflame</em></h1><p class="reader-subtitle">The Unhinged. The Unbound.</p><p>A human life extended across centuries. A chosen name. A difficult inheritance of power—and a purpose shaped by compassion.</p><dl class="lore-facts"><div><dt>Age</dt><dd>547 years</dd></div><div><dt>People</dt><dd>Human, raised by elves</dd></div><div><dt>Home</dt><dd>Near Cerallya</dd></div><div><dt>Former name</dt><dd>Vivashti Destalia</dd></div></dl></div><img src="images/eliana-wanderer.png" alt="Eliana walking with her staff on a forest road, a castle rising behind her" width="1024" height="1536"></header><div class="lore-layout"><nav class="lore-nav" aria-label="Lore sections"><p class="eyebrow">Her story</p>{''.join(links)}</nav><article>{''.join(sections)}<div class="reader-end"><p>Meet her through the encounters that give these principles life.</p><a class="primary" href="index.html#selection">Read the dialogues</a></div></article></div></main>''')

def build():
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    (output / 'index.html').write_text(home(STORIES))
    (output / 'eliana.html').write_text(lore_page())
    for i, record in enumerate(STORIES):
        source = (SOURCES / record[5]).read_text()
        following = STORIES[i + 1] if i + 1 < len(STORIES) else None
        (output / (record[0] + '.html')).write_text(story_page(record, i + 1, len(STORIES), reading_body(source), following))
    print(f'Built collection and {len(STORIES)} reading pages.')

if __name__ == '__main__':
    build()
