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
from pyzotero import zotero

# %%
# import the requests package and set your token in a variable for later use
from pyzotero import zotero
import requests
from urllib.parse import urlencode, quote_plus
import json
import numpy as np


# %% [markdown]
# # Functions to get ads data and make it a zotero item

# %%
def get_ads_data_fromdoi(doi, ads_token=None,verbose=False):
    """Retrieve bibliographic data from ADS API"""

    if 'arXiv.' in doi:
        print(doi)
        arxivID = doi.split('arXiv.')[-1]
        query = f'arXiv:{arxivID}'
        
    else:
        query = f'doi:{doi}'
    
    #query = f'doi:{doi}'
    encoded_query = urlencode({"q":query,
                               'fl': 'bibcode,title,author,pub,year,volume,issue,page,doi,abstract,keyword,bibgroup,property',
                               "rows": 1
                              })
    try:
        results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                               headers={'Authorization': 'Bearer ' + ads_token})

        data = results.json()
        #print(data)
        #status= data['responseHeader']['status']
        #print(status)
        results.raise_for_status()
        if data['response']['numFound'] > 0:
            return data['response']['docs'][0]
        else:
            print(f"No data found for doi: {doi}")
            return None
            
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ADS data: {e}")
        return None


# %%
def get_ads_data(bibcode, ads_token=None):
    """Retrieve bibliographic data from ADS API"""
    
    # ADS API endpoint for bibliographic data
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Add token if provided (recommended for higher rate limits)
    if ads_token:
        headers['Authorization'] = f'Bearer {ads_token}'
    
    # Request specific fields we need for Zotero
    params = {
        'q': f'bibcode:{bibcode}',
        'fl': 'bibcode,title,author,pub,year,volume,issue,page,doi,abstract,keyword,bibgroup,property',
        'rows': 1
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['response']['numFound'] > 0:
            return data['response']['docs'][0]
        else:
            print(f"No data found for bibcode: {bibcode}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ADS data: {e}")
        return None


# %%
def ads_to_zotero_item(ads_data):
    """Convert ADS data to Zotero item format"""
    
    if not ads_data:
        return None
    
    # Determine item type based on publication info
    pub = ads_data.get('pub', '').lower()
    if any(keyword in pub for keyword in ['conf', 'proceedings', 'meeting']):
        item_type = 'conferencePaper'
    elif any(keyword in pub for keyword in ['arxiv', 'eprint']):
        item_type = 'preprint'
    else:
        item_type = 'journalArticle'
    
    # Create Zotero item
    item = {
        'itemType': item_type,
        'title': ads_data.get('title', [''])[0] if ads_data.get('title') else '',
        'abstractNote': ads_data.get('abstract', ''),
        'date': str(ads_data.get('year', '')) if ads_data.get('year') else '',
        'url': f"https://ui.adsabs.harvard.edu/abs/{ads_data.get('bibcode', '')}",
        'extra': f"ADS Bibcode: {ads_data.get('bibcode', '')}"
    }
    
    # Add authors
    if ads_data.get('author'):
        item['creators'] = []
        for author in ads_data['author']:
            # Split "Last, First" format
            if ', ' in author:
                last, first = author.split(', ', 1)
            else:
                # Handle cases where there's no comma
                parts = author.split()
                if len(parts) > 1:
                    last = parts[-1]
                    first = ' '.join(parts[:-1])
                else:
                    last = author
                    first = ''
            
            item['creators'].append({
                'creatorType': 'author',
                'firstName': first,
                'lastName': last
            })
    
    # Add publication info based on item type
    if item_type == 'journalArticle':
        item['publicationTitle'] = ads_data.get('pub', '')
        item['volume'] = ads_data.get('volume', '')
        item['issue'] = ads_data.get('issue', '')
        
        # Handle page numbers
        if ads_data.get('page'):
            pages = ads_data['page'][0] if isinstance(ads_data['page'], list) else ads_data['page']
            item['pages'] = pages
            
    elif item_type == 'conferencePaper':
        item['proceedingsTitle'] = ads_data.get('pub', '')
        
    elif item_type == 'preprint':
        item['repository'] = 'arXiv' if 'arxiv' in ads_data.get('pub', '').lower() else ads_data.get('pub', '')
    
    # Add DOI if available
    if ads_data.get('doi'):
        item['DOI'] = ads_data['doi'][0] if isinstance(ads_data['doi'], list) else ads_data['doi']
    
    # Add keywords as tags
    if ads_data.get('keyword'):
        item['tags'] = [{'tag': keyword} for keyword in ads_data['keyword']]
    
    return item


# %%
zoter_api_key  = "nmFgeksljyc2aMp8EVekGCTO"
zoter_group_id = "6092707" #The library called manuelads
library_type = 'group' #if personal user from https://github.com/urschrei/pyzotero

token="k2zRbQStkuH0SLXRl3wAujbTY4bpjoWrkILapzbD" # This is for ads/scix

# %% [markdown]
# # Get all the libraries in ADS

# %%
resultslib = requests.get("https://api.adsabs.harvard.edu/v1/biblib/libraries",
                       headers={'Authorization': 'Bearer ' + token})
len(resultslib.json()['libraries'])



# %%
listadslibraries = [i['name'] for i in resultslib.json()['libraries']]

# %% [markdown]
# # Check the names of the collection and create if not created

# %%
zot = zotero.Zotero(zoter_group_id, library_type, zoter_api_key) # local=True for read access to local Zotero

listanames = []
for i in zot.collections():
    #print(i['data']['name'])
    listanames.append(i['data']['name'])

#print(listanames)

#listadslibraries = ['WhiteDwarfBinaries','BrownDwarfs']
for namelibads in listadslibraries:
    if namelibads in listanames:
        print(namelibads,'exists in Zotero')
    else:
        diccolection = [{"name":f"{namelibads}"}]
        zot.create_collection(diccolection)
        print('created',namelibads)

for createinads in list(set(listanames) - set(listadslibraries)):
    print(f"created {createinads} in Scix")
    
    payload = {"name": f"{createinads}", 
               "description": "Zotero Library", 
               "public": False, 
               "bibcode": []}
    results = requests.post("https://api.adsabs.harvard.edu/v1/biblib/libraries",
                            headers={'Authorization': 'Bearer ' + token}, 
                            data=json.dumps(payload))
    results.json()


#len(resultslib.json()['libraries'])






# %% [markdown]
# # Now check the things in SciX and Zotero for each library. If the doi not there then add it to the collection. 

# %%
zot = zotero.Zotero(zoter_group_id, library_type, zoter_api_key) # local=True for read access to local Zotero

for scixlib in resultslib.json()['libraries']:
    namelib = scixlib['name']
    idlib = scixlib['id']
    #print('name',namelib,idlib)
    resultsdos = requests.get(f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{idlib}?rows=500",
                       headers={'Authorization': 'Bearer ' + token},
                             params={
                                       'fl': 'bibcode,doi',
                                   })
    bibcodeslib = resultsdos.json()['documents']
    listadoisscix = []
    listabibcodescondoi = []
    for v in resultsdos.json()['solr']['response']['docs']:
        if 'doi' in v.keys():
            listadoisscix.append(v['doi'][0])
            listabibcodescondoi.append(v['bibcode'])
            #print('doit')
    #print(len(listadoisscix))
    #listadoisscix = [v['doi'][0]  for v in resultsdos.json()['solr']['response']['docs']]

    for i in zot.collections():
    #checj if something:
        if i['data']['name'] == namelib:
            print(i['data']['name'],namelib)
            itemsincol = zot.collection_items(i['data']['key'])
            listadedois = []
            for itemcol in itemsincol:
                if 'DOI' in itemcol['data'].keys():
                    listadedois.append(itemcol['data']['DOI'])
            doistoadd = list(set(listadoisscix)-set(listadedois)) 
            print('to add zotero',len(doistoadd))
            for doi in doistoadd:
                if doi not in listadedois:
                    #print('Not in Zotero')
                    t = get_ads_data_fromdoi(doi,ads_token=token,verbose=False)
                    itemz = ads_to_zotero_item(t)
                    # Set collection directly in the item
                    if itemz != None:
                        itemz['collections'] = [i['key']]
                        responsezotcreate = zot.create_items([itemz])
            doistoaddscix = list(set(listadedois)-set(listadoisscix)) 
            print('to add to scix',len(doistoaddscix))
            for doi in doistoaddscix:
                if doi not in listadoisscix:
                    #print('aaaaa',doi)
                    toaddtoscix = get_ads_data_fromdoi(doi,ads_token=token,verbose=False)
                    if toaddtoscix is not None:
                        #print(toaddtoscix)
                    
                        # add a bibcode
                        #payload = {"bibcode": [f"{doi}"], "action": "add"} Doesnt work for ariv doi
                        payload = {"bibcode": [f"{toaddtoscix['bibcode']}"], "action": "add"}
                        results = requests.post(f"https://api.adsabs.harvard.edu/v1/biblib/documents/{idlib}", 
                                                headers={'Authorization': 'Bearer ' + token},
                                                data=json.dumps(payload))
                        #results.json()
                        
                        
                                                
                                        
                    
    
                

                    
    
        

# %%
toaddtoscix

# %% [markdown]
# # So DOIs get added later to scix?

# %%

# %%

# %%

# %%

# %%
results.json()

# %%

# %%
doi

# %%
doistoaddscix[0] == doi

# %%
doi

# %%
listadoisscix

# %%

# %%

# %%

# %%

# %%
doi = '10.48550/arXiv.2508.09742'
ads_token = token

if 'arXiv.' in doi:
    print(doi)
    arxivID = doi.split('arXiv.')[-1]
    query = f'arXiv:{arxivID}'
    
else:
    query = f'doi:{doi}'
encoded_query = urlencode({"q":query,
                           'fl': 'bibcode,title,author,pub,year,volume,issue,page,doi,abstract,keyword,bibgroup,property',
                           "rows": 1
                          })
results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + ads_token})

data = results.json()

# %%
data

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %% [markdown]
# # Extra

# %%
responsezotcreate

# %%
resultsdos.json()['solr']['response']['docs']

# %%
t

# %%

# %%

# %%
resultsdos = requests.get(f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{idlib}?rows=100",
                   headers={'Authorization': 'Bearer ' + token},
                         params={
                                   'fl': 'bibcode,doi',
                               })


doislib = resultsdos.json()['documents']


# %%

# %%
uno = [1,2,3]
dos = [1,2,3]

# %%
main_list = list(set(uno)-set(dos))

# %%
main_list

# %%
resultslib.json()['libraries'][0]['id']

# %%
# get the data for the library created above
resultsdos = requests.get(f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{resultslib.json()['libraries'][2]['id']}?rows=100",
                       headers={'Authorization': 'Bearer ' + token})
resultsdos.json()


# %%
resultsdos.json()['documents'][0]

# %%
bibcode = resultsdos.json()['documents'][0]

ads_url = "https://api.adsabs.harvard.edu/v1/export/custom"
headers = {'Authorization': f'Bearer {token}'}

data = {
    'bibcode': [bibcode],
    'format': '%T\\n%A\\n%J, %V, %p (%Y)'  # Custom format
}

response = requests.post(ads_url, headers=headers, json=data)


# %%
response.json()

# %%
item = response.json()['export']

# %%
item

# %%
i

# %%

# %%
collection_name = namelibads
for collection in zot.collections():
    if collection['data']['name'] == collection_name:
        print(collection['key'])

#print(f"Collection '{collection_name}' not found")


# %%
collection['key']

# %%
item

# %%

# %%
diccolection = [{"name":"WhiteDwarfBinaries"}]
diccolection

# %%

# %%



# %%

# %%
itemz = ads_to_zotero_item(t)

# %%

# %%
itemz

# %%

# %%
response

# %%
