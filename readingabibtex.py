# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import requests
from collections import Counter

API_TOKEN = token
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}


# %%

# %%

# %%

# %%

# %%

# %%
# %%time
import requests
from collections import Counter

API_TOKEN = token
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}

INPUT_BIBCODES = [
    '2025Galax..13...49M', '2024A&A...689A..86L', '2024A&A...686A.226B',
    '2023A&A...675A.140M', '2023MNRAS.522.6102T', '2021AstL...47..235T',
    '2019A&A...622A..45I', '2009ApJ...700.1148D', '2009ApJ...692.1360H',
    '2007ApJ...660..651N', '2007PASJ...59S.177M', '2005A&A...432L..17S',
    '2004ApJ...613L..61G', '2004MNRAS.347..430B', '2003ApJ...584.1027S',
    '2003ASPC..303..202S', '2001MNRAS.326..553S', '2000astro.ph..7009P',
    '1999ApJ...517..919S', '1998ApJ...499..388E', '1997PASP..109.1093R',
    '1996MNRAS.278..542T', '1995A&A...300..189L', '1993PASP..105.1232H',
    '1990A&A...235..219M', '1990AcA....40..129M', '1988ASSL..145..233M',
    '1987Ap&SS.132....1L', '1987A&A...176..262L'
]

def get_references(bibcode):
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': f'bibcode:{bibcode}',
        'fl': 'reference',
        'fq': 'collection:astronomy',
        'rows': 1
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return docs[0].get('reference', []) if docs else []

# Count how many input bibcodes cite each reference
reference_counter = Counter()

for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    for ref in refs:
        if ref and ref not in INPUT_BIBCODES:
            reference_counter[ref] += 1

# Filter for papers cited by at least 2 input bibcodes
recommendations = [(bib, count) for bib, count in reference_counter.items() if count >= 2]
recommendations.sort(key=lambda x: -x[1])

# Output top results
print("📚 Citation Helper-like recommendations (cited by ≥2 input papers):")
for bib, count in recommendations[:15]:
    print(f"{bib} — cited by {count} input papers")


# %%
