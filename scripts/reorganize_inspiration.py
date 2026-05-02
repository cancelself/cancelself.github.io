#!/usr/bin/env python3
"""Reorganize inspiration.md by tradition (H2) -> author (H3), with Dōgen sub-organized
by source (H4) and Shōbōgenzō quotes alphabetized by chapter.

Preserves every quote and attribution verbatim; only restructures.
"""

import re
import sys
from pathlib import Path

INPUT_PATH = Path('/home/user/cancelself.github.io/inspiration.md')

# --- Parse ----------------------------------------------------------------

content = INPUT_PATH.read_text()

m = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
front_matter = m.group(1).rstrip('\n')

body_start = re.search(r'^# Inspiration\s*$', content, re.MULTILINE)
body = content[body_start.end():]

entries = []  # list of (quote_text, attribution_line)
buf = []
for raw in body.splitlines():
    if re.match(r'^##\s', raw):
        buf = []
        continue
    if raw.startswith('— '):
        while buf and buf[0].strip() == '':
            buf.pop(0)
        while buf and buf[-1].strip() == '':
            buf.pop()
        if buf:
            entries.append(('\n'.join(buf), raw))
        buf = []
    else:
        buf.append(raw)

print(f"Parsed {len(entries)} entries", file=sys.stderr)

# --- Categorize ----------------------------------------------------------

def shobogenzo_chapter(attr):
    m = re.search(r'\*Shōbōgenzō\*,\s*"([^"]+)"', attr)
    return m.group(1) if m else None

def categorize(attr):
    # Quotes that mention Dōgen but whose original speaker is someone else —
    # check these BEFORE the generic Dōgen pattern.
    if re.search(r'^— Kashyapa Bodhisattva', attr):
        return ('Mahāyāna', 'Kashyapa Bodhisattva', None)
    if re.search(r'^— Nāgārjuna', attr):
        return ('Mahāyāna', 'Nāgārjuna', None)
    if re.search(r'Buddha quoted from the \*Lotus Sutra', attr):
        return ('Mahāyāna', 'Lotus Sutra', None)
    if re.search(r'attrib\. Buddha, quoted in Dōgen', attr):
        return ('Mahāyāna', 'Buddha (in Dōgen)', None)
    # Sutra quoted in Dōgen Shōbōgenzō, Kaiin Zammai chapter — keep with Dōgen
    if re.search(r'quoted in Dōgen, \*Shōbōgenzō\*, "Kaiin Zammai"', attr):
        return ('Japanese Zen', 'Dōgen', ('Shōbōgenzō', 'Kaiin Zammai'))

    # Dōgen — Japanese Zen
    if re.search(r'^— (attrib\. )?Dōgen, \*Shōbōgenzō\*', attr):
        return ('Japanese Zen', 'Dōgen', ('Shōbōgenzō', shobogenzo_chapter(attr)))
    if re.search(r'^— Dōgen, \*Fukan Zazengi\*', attr):
        return ('Japanese Zen', 'Dōgen', ('Fukan Zazengi', None))
    if re.search(r'^— Dōgen, \*Gakudō Yōjinshū\*', attr):
        return ('Japanese Zen', 'Dōgen', ('Gakudō Yōjinshū', None))
    if re.search(r'^— Dōgen, verse.*\*Eihei Kōroku\*', attr):
        return ('Japanese Zen', 'Dōgen', ('Eihei Kōroku', None))

    # Other Japanese Zen
    if re.search(r'Sōtō Zen liturgy', attr):
        return ('Japanese Zen', 'Sōtō Liturgy', None)
    if re.search(r'^— Keizan', attr):
        return ('Japanese Zen', 'Keizan', None)
    if re.search(r'Hakuun Yasutani', attr):
        return ('Japanese Zen', 'Hakuun Yasutani', None)

    # Chinese Chan
    if re.search(r'Wumen Huikai', attr):
        return ('Chinese Chan', 'Wumen Huikai', None)
    if re.search(r'Mazu Daoyi', attr):
        return ('Chinese Chan', 'Mazu Daoyi', None)
    if re.search(r'^— Huineng', attr) or re.search(r'\*Platform Sutra.*Huineng', attr):
        return ('Chinese Chan', 'Huineng', None)
    if re.search(r'attrib\. Hongzhi', attr):
        return ('Chinese Chan', 'Hongzhi Zhengjue', None)
    if re.search(r'\*Book of Serenity', attr):
        return ('Chinese Chan', 'Book of Serenity', None)
    if re.search(r'Dongshan Liangjie', attr):
        return ('Chinese Chan', 'Dongshan Liangjie', None)
    if re.search(r'attrib\. Yunmen', attr):
        return ('Chinese Chan', 'Yunmen', None)
    if re.search(r'Bai Juyi', attr):
        return ('Chinese Chan', 'Bai Juyi', None)
    if re.search(r'Han-shan', attr):
        return ('Chinese Chan', 'Han-shan', None)

    # Vietnamese Zen
    if re.search(r'Thich Nhat Hanh', attr):
        return ('Vietnamese Zen', 'Thich Nhat Hanh', None)

    # American Zen
    if re.search(r'Shunryu Suzuki', attr):
        return ('American Zen', 'Shunryu Suzuki', None)
    if re.search(r'Charlotte Joko Beck', attr):
        return ('American Zen', 'Charlotte Joko Beck', None)
    if re.search(r'Dainin Katagiri', attr):
        return ('American Zen', 'Dainin Katagiri', None)
    if re.search(r'Joseph Goldstein', attr):
        return ('American Zen', 'Joseph Goldstein', None)
    if re.search(r'Bernie Glassman', attr):
        return ('American Zen', 'Bernie Glassman', None)
    if re.search(r'Shinshu Roberts', attr):
        return ('American Zen', 'Shinshu Roberts', None)

    # Theravāda
    if re.search(r'Ajahn Chah', attr):
        return ('Theravāda', 'Ajahn Chah', None)
    pali_keys = (r'Anattalakkhana|Maraṇasati|Kaccānagotta|Dhammacakkappavattana|'
                 r'Dhammapada|Sutta Nipāta|Cūḷakammavibhanga|Mahāhatthipadopama|'
                 r'Bojjhaṅga|Satipaṭṭhāna|Aggañña|Mahāsaccaka|Ariyapariyesanā|'
                 r'Aṅgulimāla|Acela|Brahmāyācana|Pali Canon|Pali arahant')
    if re.search(pali_keys, attr):
        return ('Theravāda', 'Pali Canon', None)

    # Mahāyāna
    if re.search(r'Kashyapa Bodhisattva', attr):
        return ('Mahāyāna', 'Kashyapa Bodhisattva', None)
    if re.search(r'^— Nāgārjuna', attr):
        return ('Mahāyāna', 'Nāgārjuna', None)
    if re.search(r'\*Diamond Sutra', attr):
        return ('Mahāyāna', 'Diamond Sutra', None)
    if re.search(r'\*Lotus Sutra', attr) or re.search(r'Buddha quoted from the \*Lotus', attr):
        return ('Mahāyāna', 'Lotus Sutra', None)
    if re.search(r'\*Laṅkāvatāra Sūtra', attr):
        return ('Mahāyāna', 'Laṅkāvatāra Sūtra', None)
    if re.search(r'attrib\. Buddha, quoted in Dōgen', attr):
        return ('Mahāyāna', 'Buddha (in Dōgen)', None)
    if re.search(r'\*Sange Mon|Mahāyāna repentance verse|dedication of merit', attr):
        return ('Mahāyāna', 'Liturgy', None)

    # Other Eastern
    if re.search(r'\*Bhagavad Gita', attr):
        return ('Other Eastern', 'Bhagavad Gita', None)
    if re.search(r'\*Tao Te Ching', attr):
        return ('Other Eastern', 'Tao Te Ching', None)
    if re.search(r'^— Li Si', attr):
        return ('Other Eastern', 'Li Si', None)

    # Western Religious
    if re.search(r'recollection of William Blake', attr):
        return ('Western Religious', 'William Blake', None)
    if re.search(r'^— Job ', attr) or re.search(r'^— Isaiah', attr) or re.search(r'^— Ecclesiastes', attr):
        return ('Western Religious', 'Hebrew Bible', None)
    if re.search(r'^— Matthew', attr):
        return ('Western Religious', 'New Testament', None)
    if re.search(r'Meister Eckhart', attr):
        return ('Western Religious', 'Meister Eckhart', None)

    # Western Philosophy
    if re.search(r'^— Plato', attr):
        return ('Western Philosophy', 'Plato', None)
    if re.search(r'Friedrich Nietzsche', attr):
        return ('Western Philosophy', 'Friedrich Nietzsche', None)
    if re.search(r'James George Frazer', attr):
        return ('Western Philosophy', 'James George Frazer', None)

    # Modern
    if re.search(r'Donald Knuth', attr):
        return ('Modern', 'Donald Knuth', None)
    if re.search(r'Cory Booker', attr):
        return ('Modern', 'Cory Booker', None)

    # Source pending
    if attr.strip() == '— source pending':
        return ('Source Pending', None, None)

    # Uncategorized — paraphrase of Shakyamuni Buddha's awakening
    if re.search(r'paraphrase of Shakyamuni', attr):
        return ('Uncategorized', None, None)

    # General attrib. Buddha (source pending)
    if re.search(r'attrib\. Buddha \(source pending\)', attr):
        return ('Source Pending', None, None)

    return None


# --- Bucket --------------------------------------------------------------

buckets = {}
unmatched = []
for quote, attr in entries:
    cat = categorize(attr)
    if cat is None:
        unmatched.append((quote, attr))
        continue
    tradition, author, sub = cat
    buckets.setdefault(tradition, {})
    if author is None:
        buckets[tradition].setdefault('_direct', []).append((quote, attr, sub))
    else:
        if isinstance(sub, tuple):
            work, chapter = sub
            buckets[tradition].setdefault(author, {}).setdefault(work, []).append(
                (quote, attr, chapter)
            )
        else:
            buckets[tradition].setdefault(author, []).append((quote, attr, sub))

if unmatched:
    print(f"\n!!! {len(unmatched)} UNMATCHED entries:", file=sys.stderr)
    for q, a in unmatched:
        print(f"  ATTR: {a}", file=sys.stderr)
        print(f"  Q: {q[:100]!r}...", file=sys.stderr)
    sys.exit(1)


# --- Emit ----------------------------------------------------------------

TRADITION_ORDER = [
    'Chinese Chan',
    'Japanese Zen',
    'Vietnamese Zen',
    'American Zen',
    'Theravāda',
    'Mahāyāna',
    'Other Eastern',
    'Western Religious',
    'Western Philosophy',
    'Modern',
    'Source Pending',
    'Uncategorized',
]

AUTHOR_ORDER = {
    'Chinese Chan': [
        'Huineng', 'Mazu Daoyi', 'Bai Juyi', 'Han-shan',
        'Dongshan Liangjie', 'Yunmen', 'Hongzhi Zhengjue',
        'Wumen Huikai', 'Book of Serenity',
    ],
    'Japanese Zen': [
        'Dōgen', 'Keizan', 'Hakuun Yasutani', 'Sōtō Liturgy',
    ],
    'Vietnamese Zen': ['Thich Nhat Hanh'],
    'American Zen': [
        'Shunryu Suzuki', 'Charlotte Joko Beck',
        'Dainin Katagiri', 'Bernie Glassman',
        'Joseph Goldstein', 'Shinshu Roberts',
    ],
    'Theravāda': ['Pali Canon', 'Ajahn Chah'],
    'Mahāyāna': [
        'Diamond Sutra', 'Lotus Sutra', 'Laṅkāvatāra Sūtra',
        'Nāgārjuna', 'Kashyapa Bodhisattva', 'Buddha (in Dōgen)', 'Liturgy',
    ],
    'Other Eastern': ['Bhagavad Gita', 'Tao Te Ching', 'Li Si'],
    'Western Religious': [
        'Hebrew Bible', 'New Testament', 'Meister Eckhart', 'William Blake',
    ],
    'Western Philosophy': [
        'Plato', 'Friedrich Nietzsche', 'James George Frazer',
    ],
    'Modern': ['Donald Knuth', 'Cory Booker'],
}

DOGEN_WORK_ORDER = ['Shōbōgenzō', 'Fukan Zazengi', 'Gakudō Yōjinshū', 'Eihei Kōroku']


blocks = []
blocks.append(front_matter + '\n\n# Inspiration')

emitted = 0
for tradition in TRADITION_ORDER:
    if tradition not in buckets:
        continue
    blocks.append(f'## {tradition}')

    if tradition in ('Source Pending', 'Uncategorized'):
        for quote, attr, _ in buckets[tradition].get('_direct', []):
            blocks.append(quote + '\n\n' + attr)
            emitted += 1
        continue

    for author in AUTHOR_ORDER.get(tradition, []):
        if author not in buckets[tradition]:
            continue
        blocks.append(f'### {author}')
        author_data = buckets[tradition][author]

        if isinstance(author_data, dict):
            for work in DOGEN_WORK_ORDER:
                if work not in author_data:
                    continue
                blocks.append(f'#### {work}')
                quotes = author_data[work]
                if work == 'Shōbōgenzō':
                    # Sort by chapter (None sorts last)
                    quotes_sorted = sorted(
                        quotes,
                        key=lambda x: (x[2] is None, (x[2] or '').lower())
                    )
                else:
                    quotes_sorted = quotes
                for quote, attr, _ in quotes_sorted:
                    blocks.append(quote + '\n\n' + attr)
                    emitted += 1
        else:
            for quote, attr, _ in author_data:
                blocks.append(quote + '\n\n' + attr)
                emitted += 1

result = '\n\n\n'.join(blocks) + '\n'

print(f"Emitted {emitted} entries (input had {len(entries)})", file=sys.stderr)
assert emitted == len(entries), f"MISMATCH: {emitted} != {len(entries)}"

# Print to stdout — caller redirects
sys.stdout.write(result)
