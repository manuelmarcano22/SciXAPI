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
# import the requests package and set your token in a variable for later use
import requests
from urllib.parse import urlencode, quote_plus
import json
token="k2zRbQStkuH0SLXRl3wAujbTY4bpjoWrkILapzbD"

# %%


resultslib = requests.get("https://api.adsabs.harvard.edu/v1/biblib/libraries",
                       headers={'Authorization': 'Bearer ' + token})
len(resultslib.json()['libraries'])



# %%
resultslib.json()['libraries'][13]

# %%


# get the data for the library created above
resultsdos = requests.get(f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{resultslib.json()['libraries'][13]['id']}?rows=100",
                       headers={'Authorization': 'Bearer ' + token})
resultsdos.json()



# %%
len(resultsdos.json()['documents'])

# %%

query = 'doi:10.48550/arXiv.2508.00186'
#encoded_query = urlencode({'q': query, "fl": "title, bibcode, author, identifier"})
encoded_query = urlencode({"q":query,
                           "fl": "title, bibcode, author, identifier",
                           "rows": 2
                          })
results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                       headers={'Authorization': 'Bearer ' + token})

# format the response in a nicely readable format
results.json()


# %%
# add a bibcode
payload = {"doi": ["10.48550/arXiv.2508.00186"], "action": "add"}


# add a query by posting search parameters
payload = {"params": {"q": query}, 
           "action": "add"}
results = requests.post(f"https://api.adsabs.harvard.edu/v1/biblib/query/{resultslib.json()['libraries'][2]['id']}", 
                        headers={'Authorization': 'Bearer ' + token},
                        data=json.dumps(payload))
results.json()



# %%


# get the data for the library created above
resultsdos = requests.get(f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{resultslib.json()['libraries'][2]['id']}?rows=100",
                       headers={'Authorization': 'Bearer ' + token})
resultsdos.json()



# %%
len(resultsdos.json()['documents'])

# %%

# %%


from urllib.parse import urlencode, quote_plus

# accented letters, special characters, and spaces need to be encoded
query = {"q": "author:martínez neutron star"}

encoded_query = urlencode(query)
print(encoded_query)

# note that the colon (:) may be encoded, depending on the algorithm you use. Your request 
# should accept either the unencoded colon (:) or the encoded version (%3A)




# %%


encoded_query = urlencode({"q": "abstract:(white NEAR1 dwarf NEAR5 brown)",
                           "fl": "title, bibcode, author, identifier",
                           "rows": 2
                          })
results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                       headers={'Authorization': 'Bearer ' + token})

# format the response in a nicely readable format
results.json()



# %%

# %%
encoded_query

# %%
