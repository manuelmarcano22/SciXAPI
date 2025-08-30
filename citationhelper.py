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



API_TOKEN = token
HEADERS = {'Authorization': f'Bearer {API_TOKEN}'}



INPUT_BIBCODES = [
    '2024MNRAS.531.1496S',
    '2024PhRvD.109j3514Y'
]

INPUT_BIBCODES = ['2025arXiv250800186C',
  '2024A&A...692A.187G',
  '2024AJ....168..288A',
  '2024A&A...687A.113V',
  '2024MEcEv..15.1024D',
  '2024ApJ...963..146T',
  '2023ApJ...953..127B',
  '2023MNRAS.520..599G',
  '2022NatSR..1212276G',
  '2021arXiv211203779K',
  '2021A&A...650A.109P',
  '2021JAEE...34...13P',
  '2020svos.conf..329S',
  '2018AJ....156..131N',
  '2014PhRvE..90e2910G',
  '2014PhRvD..89j4059B',
  '2010Bioin..26.2778G',
  '2010SHPSA..41...86E',
  '1985ApJ...295..143M']



def get_references(bibcode):
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': f'bibcode:{bibcode}',
        'fl': 'reference',
        'fq': 'collection:astronomy',
        'rows': 1
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error retrieving {bibcode}: {response.status_code}")
        return []

    docs = response.json().get('response', {}).get('docs', [])
    if docs and 'reference' in docs[0]:
        return docs[0]['reference']
    return []

# Step 1: Fetch and collect references
all_references = []
for bibcode in INPUT_BIBCODES:
    refs = get_references(bibcode)
    if refs:
        all_references.extend(refs)
    else:
        print(f"No references found for {bibcode}")

# Step 2: Count and rank
ref_counter = Counter(all_references)
recommended = [
    (bib, count) for bib, count in ref_counter.items()
    if bib and bib not in INPUT_BIBCODES
]

# Step 3: Output top recommended
recommended = sorted(recommended, key=lambda x: x[1], reverse=True)

print("\nRecommended citations (co-cited with your input bibcodes):")
for bib, count in recommended[:10]:
    print(f"{bib} (cited {count} times)")


# %%
import requests
from collections import Counter

token="k2zRbQStkuH0SLXRl3wAujbTY4bpjoWrkILapzbD"



HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}



INPUT_BIBCODES = ['2025Galax..13...49M',
  '2024A&A...689A..86L',
  '2024A&A...686A.226B',
  '2023A&A...675A.140M',
  '2023MNRAS.522.6102T',
  '2021AstL...47..235T',
  '2019A&A...622A..45I',
  '2009ApJ...700.1148D',
  '2009ApJ...692.1360H',
  '2007ApJ...660..651N',
  '2007PASJ...59S.177M',
  '2005A&A...432L..17S',
  '2004ApJ...613L..61G',
  '2004MNRAS.347..430B',
  '2003ApJ...584.1027S',
  '2003ASPC..303..202S',
  '2001MNRAS.326..553S',
  '2000astro.ph..7009P',
  '1999ApJ...517..919S',
  '1998ApJ...499..388E',
  '1997PASP..109.1093R',
  '1996MNRAS.278..542T',
  '1995A&A...300..189L',
  '1993PASP..105.1232H',
  '1990A&A...235..219M',
  '1990AcA....40..129M',
  '1988ASSL..145..233M',
  '1987Ap&SS.132....1L',
  '1987A&A...176..262L']

# %%
import requests
from collections import Counter

# Replace this with your actual API token
API_TOKEN = token
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# Your input list of bibcodes (manuscript draft bibliography)
INPUT_BIBCODES = [
    '2024MNRAS.531.1496S',
    '2024PhRvD.109j3514Y'
]

INPUT_BIBCODES = ['2025Galax..13...49M',
  '2024A&A...689A..86L',
  '2024A&A...686A.226B',
  '2023A&A...675A.140M',
  '2023MNRAS.522.6102T',
  '2021AstL...47..235T',
  '2019A&A...622A..45I',
  '2009ApJ...700.1148D',
  '2009ApJ...692.1360H',
  '2007ApJ...660..651N',
  '2007PASJ...59S.177M',
  '2005A&A...432L..17S',
  '2004ApJ...613L..61G',
  '2004MNRAS.347..430B',
  '2003ApJ...584.1027S',
  '2003ASPC..303..202S',
  '2001MNRAS.326..553S',
  '2000astro.ph..7009P',
  '1999ApJ...517..919S',
  '1998ApJ...499..388E',
  '1997PASP..109.1093R',
  '1996MNRAS.278..542T',
  '1995A&A...300..189L',
  '1993PASP..105.1232H',
  '1990A&A...235..219M',
  '1990AcA....40..129M',
  '1988ASSL..145..233M',
  '1987Ap&SS.132....1L',
  '1987A&A...176..262L']



def get_references(bibcode):
    """Returns a list of references (papers this paper cites)."""
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': f'bibcode:{bibcode}',
        'fl': 'reference',
        'rows': 1,
        'fq': 'collection:astronomy'
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return docs[0].get('reference', []) if docs else []

def get_citations(bibcode):
    """Returns a list of citing papers (that cite this paper)."""
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': f'citations({bibcode})',
        'fl': 'bibcode',
        'rows': 200,  # you can increase this if needed
        'fq': 'collection:astronomy'
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return [doc['bibcode'] for doc in docs]

# === Collect references and citations ===
related_bibcodes = []

for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    cits = get_citations(bib)
    print(f"Retrieved {len(refs)} references and {len(cits)} citations for {bib}")
    related_bibcodes.extend(refs)
    related_bibcodes.extend(cits)

# === Aggregate and count ===
counts = Counter(related_bibcodes)

# Remove any None entries and original inputs
for bib in INPUT_BIBCODES:
    counts.pop(bib, None)
counts.pop(None, None)

# === Output top recommendations ===
print("\n🔍 Recommended papers (cited by or citing your inputs):")
for bib, count in counts.most_common(10):
    print(f"{bib} — related {count} times")


# %%
response.json()

# %%
import requests
from collections import defaultdict, Counter

#API_TOKEN = 'your_ads_api_token_here'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}


INPUT_BIBCODES = ['2025arXiv250800186C',
  '2024A&A...692A.187G',
  '2024AJ....168..288A',
  '2024A&A...687A.113V',
  '2024MEcEv..15.1024D',
  '2024ApJ...963..146T',
  '2023ApJ...953..127B',
  '2023MNRAS.520..599G',
  '2022NatSR..1212276G',
  '2021arXiv211203779K',
  '2021A&A...650A.109P',
  '2021JAEE...34...13P',
  '2020svos.conf..329S',
  '2018AJ....156..131N',
  '2014PhRvE..90e2910G',
  '2014PhRvD..89j4059B',
  '2010Bioin..26.2778G',
  '2010SHPSA..41...86E',
  '1985ApJ...295..143M']

def get_references(bibcode):
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': f'bibcode:{bibcode}',
        'fl': 'reference',
        'rows': 1,
        'fq': 'collection:astronomy'
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return docs[0].get('reference', []) if docs else []

def get_citations(bibcode):
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': f'citations({bibcode})',
        'fl': 'bibcode',
        'rows': 200,
        'fq': 'collection:astronomy'
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return [doc['bibcode'] for doc in docs]

# === Track references and citations per bibcode
references_per_paper = defaultdict(list)
citations_per_paper = defaultdict(list)

for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    cits = get_citations(bib)
    print(f"{bib}: {len(refs)} refs, {len(cits)} cites")

    for r in refs:
        if r and r not in INPUT_BIBCODES:
            references_per_paper[r].append(bib)
    for c in cits:
        if c and c not in INPUT_BIBCODES:
            citations_per_paper[c].append(bib)

# === Combine all recommended bibcodes
all_related = set(references_per_paper) | set(citations_per_paper)

# === Output top results by total frequency
combined_counts = {
    bib: len(references_per_paper.get(bib, [])) + len(citations_per_paper.get(bib, []))
    for bib in all_related
}
top_bibcodes = sorted(combined_counts.items(), key=lambda x: -x[1])[:10]

# === Output
print("\n🔍 Recommended papers (detailed counts):")
for bib, total in top_bibcodes:
    from_refs = len(references_per_paper.get(bib, []))
    from_cits = len(citations_per_paper.get(bib, []))
    print(f"{bib} — cites  {from_cits} input paper(s), in reference lists of {from_refs} paper(s)")


# %%
import requests
from collections import defaultdict

#API_TOKEN = 'your_ads_api_token_here'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}


INPUT_BIBCODES = ['2025Galax..13...49M',
  '2024A&A...689A..86L',
  '2024A&A...686A.226B',
  '2023A&A...675A.140M',
  '2023MNRAS.522.6102T',
  '2021AstL...47..235T',
  '2019A&A...622A..45I',
  '2009ApJ...700.1148D',
  '2009ApJ...692.1360H',
  '2007ApJ...660..651N',
  '2007PASJ...59S.177M',
  '2005A&A...432L..17S',
  '2004ApJ...613L..61G',
  '2004MNRAS.347..430B',
  '2003ApJ...584.1027S',
  '2003ASPC..303..202S',
  '2001MNRAS.326..553S',
  '2000astro.ph..7009P',
  '1999ApJ...517..919S',
  '1998ApJ...499..388E',
  '1997PASP..109.1093R',
  '1996MNRAS.278..542T',
  '1995A&A...300..189L',
  '1993PASP..105.1232H',
  '1990A&A...235..219M',
  '1990AcA....40..129M',
  '1988ASSL..145..233M',
  '1987Ap&SS.132....1L',
  '1987A&A...176..262L']



def get_potential_citers(bibcodes):
    """Get all papers that cite at least one of the input bibcodes."""
    query = " OR ".join([f"citations({b})" for b in bibcodes])
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': query,
        'fl': 'bibcode,reference',
        'fq': 'collection:astronomy',
        'rows': 500  # increase if needed
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return docs

# Step 1: Get all possible citers
citers = get_potential_citers(INPUT_BIBCODES)

# Step 2: Count how many input bibcodes each citing paper references
overlap_counter = defaultdict(int)
for doc in citers:
    ref_list = doc.get('reference', [])
    overlap = len(set(ref_list) & set(INPUT_BIBCODES))
    if overlap > 0:
        overlap_counter[doc['bibcode']] = overlap

# Step 3: Output top results
sorted_citers = sorted(overlap_counter.items(), key=lambda x: -x[1])

print("🔍 Papers that cite the most of your input bibcodes:")
for bib, count in sorted_citers[:10]:
    print(f"{bib} — cites {count} of your input papers")


# %%
import requests
from collections import defaultdict

API_TOKEN = token
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

INPUT_BIBCODES = ['2025Galax..13...49M',
  '2024A&A...689A..86L',
  '2024A&A...686A.226B',
  '2023A&A...675A.140M',
  '2023MNRAS.522.6102T',
  '2021AstL...47..235T',
  '2019A&A...622A..45I',
  '2009ApJ...700.1148D',
  '2009ApJ...692.1360H',
  '2007ApJ...660..651N',
  '2007PASJ...59S.177M',
  '2005A&A...432L..17S',
  '2004ApJ...613L..61G',
  '2004MNRAS.347..430B',
  '2003ApJ...584.1027S',
  '2003ASPC..303..202S',
  '2001MNRAS.326..553S',
  '2000astro.ph..7009P',
  '1999ApJ...517..919S',
  '1998ApJ...499..388E',
  '1997PASP..109.1093R',
  '1996MNRAS.278..542T',
  '1995A&A...300..189L',
  '1993PASP..105.1232H',
  '1990A&A...235..219M',
  '1990AcA....40..129M',
  '1988ASSL..145..233M',
  '1987Ap&SS.132....1L',
  '1987A&A...176..262L']



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

def get_potential_citers(bibcodes):
    """Get all papers that cite at least one of the input bibcodes."""
    query = " OR ".join([f"citations({b})" for b in bibcodes])
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': query,
        'fl': 'bibcode,reference',
        'fq': 'collection:astronomy',
        'rows': 500
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return docs

# === PART 1: Who cites the input bibcodes (reverse)
citers = get_potential_citers(INPUT_BIBCODES)
cites_input = defaultdict(int)  # paper → number of input bibcodes it cites

for doc in citers:
    ref_list = doc.get('reference', [])
    overlap = len(set(ref_list) & set(INPUT_BIBCODES))
    if overlap > 0:
        cites_input[doc['bibcode']] = overlap

# === PART 2: Who is cited by the input bibcodes (forward)
cited_by_input = defaultdict(int)  # paper → number of input papers that cite it

for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    for r in refs:
        if r and r not in INPUT_BIBCODES:
            cited_by_input[r] += 1

# === COMBINE BOTH SETS
all_related = set(cites_input) | set(cited_by_input)

combined = []
for bib in all_related:
    cites_n = cites_input.get(bib, 0)
    cited_by_n = cited_by_input.get(bib, 0)
    score = cites_n + cited_by_n
    combined.append((bib, cites_n, cited_by_n, score))

# === Sort and print
combined_sorted = sorted(combined, key=lambda x: -x[3])

print("🔍 Recommended papers (combined analysis):")
for bib, cites, cited_by, score in combined_sorted[:15]:
    print(f"{bib} — cites {cites} input paper(s), cited by {cited_by} input paper(s)")


# %%
# %%time
import requests
from collections import defaultdict

API_TOKEN = token
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

INPUT_BIBCODES = ['2025Galax..13...49M',
  '2024A&A...689A..86L',
  '2024A&A...686A.226B',
  '2023A&A...675A.140M',
  '2023MNRAS.522.6102T',
  '2021AstL...47..235T',
  '2019A&A...622A..45I',
  '2009ApJ...700.1148D',
  '2009ApJ...692.1360H',
  '2007ApJ...660..651N',
  '2007PASJ...59S.177M',
  '2005A&A...432L..17S',
  '2004ApJ...613L..61G',
  '2004MNRAS.347..430B',
  '2003ApJ...584.1027S',
  '2003ASPC..303..202S',
  '2001MNRAS.326..553S',
  '2000astro.ph..7009P',
  '1999ApJ...517..919S',
  '1998ApJ...499..388E',
  '1997PASP..109.1093R',
  '1996MNRAS.278..542T',
  '1995A&A...300..189L',
  '1993PASP..105.1232H',
  '1990A&A...235..219M',
  '1990AcA....40..129M',
  '1988ASSL..145..233M',
  '1987Ap&SS.132....1L',
  '1987A&A...176..262L']

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

def get_potential_citers(bibcodes):
    query = " OR ".join([f"citations({b})" for b in bibcodes])
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': query,
        'fl': 'bibcode,reference',
        'fq': 'collection:astronomy',
        'rows': 500
    }
    r = requests.get(url, headers=HEADERS, params=params)
    docs = r.json().get('response', {}).get('docs', [])
    return docs

# === Part 1: Papers that cite multiple input papers
citers = get_potential_citers(INPUT_BIBCODES)
cites_input = defaultdict(int)

for doc in citers:
    ref_list = doc.get('reference', [])
    overlap = len(set(ref_list) & set(INPUT_BIBCODES))
    if overlap > 0:
        cites_input[doc['bibcode']] = overlap

# === Part 2: Papers cited by input papers
cited_by_input = defaultdict(int)

for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    for r in refs:
        if r and r not in INPUT_BIBCODES:
            cited_by_input[r] += 1

# === Combine
all_related = set(cites_input) | set(cited_by_input)
combined = []

for bib in all_related:
    cites_n = cites_input.get(bib, 0)
    cited_by_n = cited_by_input.get(bib, 0)
    combined.append((bib, cites_n, cited_by_n))

# === Sort by cited_by count (descending)
combined_sorted = sorted(combined, key=lambda x: -x[2])

# === Output
print("🔍 Recommended papers (sorted by 'cited by' count):")
for bib, cites, cited_by in combined_sorted[:15]:
    print(f"{bib} — cites {cites} input paper(s), cited by {cited_by} input paper(s)")


# %% [markdown]
# # Citations

# %%
# %%time
import requests
from collections import Counter

API_TOKEN = token
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

INPUT_BIBCODES = ['2025Galax..13...49M',
  '2024A&A...689A..86L',
  '2024A&A...686A.226B',
  '2023A&A...675A.140M',
  '2023MNRAS.522.6102T',
  '2021AstL...47..235T',
  '2019A&A...622A..45I',
  '2009ApJ...700.1148D',
  '2009ApJ...692.1360H',
  '2007ApJ...660..651N',
  '2007PASJ...59S.177M',
  '2005A&A...432L..17S',
  '2004ApJ...613L..61G',
  '2004MNRAS.347..430B',
  '2003ApJ...584.1027S',
  '2003ASPC..303..202S',
  '2001MNRAS.326..553S',
  '2000astro.ph..7009P',
  '1999ApJ...517..919S',
  '1998ApJ...499..388E',
  '1997PASP..109.1093R',
  '1996MNRAS.278..542T',
  '1995A&A...300..189L',
  '1993PASP..105.1232H',
  '1990A&A...235..219M',
  '1990AcA....40..129M',
  '1988ASSL..145..233M',
  '1987Ap&SS.132....1L',
  '1987A&A...176..262L']

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

# Count references across all input papers
reference_counter = Counter()

for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    filtered = [r for r in refs if r and r not in INPUT_BIBCODES]
    reference_counter.update(filtered)

# Output: Most cited papers not in the input list
print("🔍 Most frequently cited (not in your input list):")
for bib, count in reference_counter.most_common(15):
    print(f"{bib} — cited by {count} input paper(s)")


# %%
# 

# %%
# %%time
import requests
from collections import defaultdict

API_TOKEN = token
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}



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

def get_potential_citers(bibcodes):
    query = " OR ".join([f"citations({b})" for b in bibcodes])
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': query,
        'fl': 'bibcode,reference',
        'fq': 'collection:astronomy',
        'rows': 500
    }
    r = requests.get(url, headers=HEADERS, params=params)
    return r.json().get('response', {}).get('docs', [])

# === Phase 1: Cited-by analysis (papers cited by inputs)
ref_counter = defaultdict(set)
for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    for ref in refs:
        if ref and ref not in INPUT_BIBCODES:
            ref_counter[ref].add(bib)

# === Phase 2: Cites-input analysis (papers that cite multiple inputs)
cites_inputs = defaultdict(set)
citers = get_potential_citers(INPUT_BIBCODES)
for doc in citers:
    citing_bib = doc['bibcode']
    ref_list = doc.get('reference', [])
    overlap = set(ref_list) & INPUT_BIBCODES
    if overlap:
        cites_inputs[citing_bib].update(overlap)

# === Combine and score
recommendations = defaultdict(lambda: {'cited_by': 0, 'cites': 0})
for bib, inputs in ref_counter.items():
    recommendations[bib]['cited_by'] = len(inputs)
for bib, inputs in cites_inputs.items():
    recommendations[bib]['cites'] = len(inputs)

# === Compute total score and sort
scored = [
    (bib, data['cited_by'], data['cites'], data['cited_by'] + data['cites'])
    for bib, data in recommendations.items()
]
scored = sorted(scored, key=lambda x: -x[3])  # sort by total score

# === Output
print("📚 Citation Helper Recommendations (cited and/or citing):")
for bib, cited_by, cites, score in scored[:15]:
    print(f"{bib} — cited by {cited_by} input(s), cites {cites} input(s), total score: {score}")


# %%
# %%time
import requests
from collections import defaultdict



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

def get_citers_of_inputs(bibcodes):
    query = " OR ".join([f"citations({b})" for b in bibcodes])
    url = 'https://api.adsabs.harvard.edu/v1/search/query'
    params = {
        'q': query,
        'fl': 'bibcode,reference',
        'fq': 'collection:astronomy',
        'rows': 500
    }
    r = requests.get(url, headers=HEADERS, params=params)
    return r.json().get('response', {}).get('docs', [])

# Track papers cited by inputs
ref_counter = defaultdict(set)
for bib in INPUT_BIBCODES:
    refs = get_references(bib)
    for r in refs:
        if r and r not in INPUT_BIBCODES:
            ref_counter[r].add(bib)

# Track papers that cite inputs
cites_inputs = defaultdict(set)
citers = get_citers_of_inputs(INPUT_BIBCODES)
for doc in citers:
    citing_bib = doc['bibcode']
    ref_list = doc.get('reference', [])
    overlap = set(ref_list) & INPUT_BIBCODES
    if overlap:
        cites_inputs[citing_bib].update(overlap)

# Combine scores
recommendations = defaultdict(lambda: {'cited_by': 0, 'cites': 0})
for bib, cited_by_set in ref_counter.items():
    recommendations[bib]['cited_by'] = len(cited_by_set)
for bib, cites_set in cites_inputs.items():
    recommendations[bib]['cites'] = len(cites_set)

# Compute total score
scored = [
    (bib, data['cited_by'], data['cites'], data['cited_by'] + data['cites'])
    for bib, data in recommendations.items()
]
scored = sorted(scored, key=lambda x: -x[3])  # by total score

# Output
print("📚 Citation Helper Recommendations:")
for bib, cited_by, cites, score in scored[:15]:
    print(f"{bib} — cited by {cited_by}, cites {cites}, total score: {score}")

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
