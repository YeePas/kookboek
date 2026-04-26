import urllib.request
import json
import os
import time

API_KEY = '563492ad6f91700001000001856722d57d2a4521876523910f1352f7'
FOLDER = 'fotos'

tasks = [
    {'slug': 'strozzapreti-alla-norcina-manteca', 'terms': ['sausage pasta','italian pasta']},
    {'slug': 'house-focaccia-manteca', 'terms': ['focaccia bread','italian bread']},
    {'slug': 'wild-garlic-en-spinazie-chitarra', 'terms': ['green pasta','fresh pasta']},
    {'slug': 'kale-en-chili-lumache', 'terms': ['rigatoni pasta','pasta bowl']},
    {'slug': 'eendenleverparfait-met-dadeljam', 'terms': ['pate toast','charcuterie board']},
    {'slug': 'chocolade-hazelnoot-tart', 'terms': ['chocolate tart','hazelnut dessert']},
    {'slug': 'house-made-ricotta', 'terms': ['ricotta cheese bowl','fresh cheese']},
    {'slug': 'fazzoletti-met-eendenragu', 'terms': ['duck pasta','ragu pasta']},
    {'slug': 'brown-crab-cacio-e-pepe', 'terms': ['seafood pasta','crab pasta']},
    {'slug': 'pasta-alla-norcina-guardian', 'terms': ['creamy sausage pasta','pasta bowl']},
    {'slug': 'tortellini-in-brodo', 'terms': ['tortellini soup','pasta soup']},
    {'slug': 'langzaam-gegaarde-varkensschouder-met-appel', 'terms': ['braised pork','roast pork']},
    {'slug': 'rigatoni-met-boerenkoolsaus', 'terms': ['green pasta sauce','rigatoni']}
]

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

headers = {
    'Authorization': API_KEY,
    'User-Agent': 'Pexels/Python'
}

for task in tasks:
    found = False
    used_query = ""
    for term in task['terms']:
        try:
            query = term.replace(" ", "%20")
            url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                res_data = response.read().decode()
                data = json.loads(res_data)
                if data.get('photos'):
                    photo = data['photos'][0]
                    base_url = photo['src'].get('landscape') or photo['src'].get('large') or photo['src'].get('original')
                    sep = '&' if '?' in base_url else '?'
                    img_url = f"{base_url}{sep}w=1200&h=700&fit=crop&auto=compress&cs=tinysrgb"
                    
                    img_req = urllib.request.Request(img_url)
                    with urllib.request.urlopen(img_req) as img_response:
                        with open(os.path.join(FOLDER, f"{task['slug']}.jpg"), 'wb') as f:
                            f.write(img_response.read())
                    used_query = term
                    found = True
                    break
        except Exception as e:
            print(f"Error for {term}: {e}")
            pass
        time.sleep(1)
    
    if found:
        print(f"{task['slug']}: Success (Query: \"{used_query}\")")
    else:
        print(f"{task['slug']}: Failed")
