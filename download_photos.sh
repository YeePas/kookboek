#!/bin/bash

API_KEY='563492ad6f91700001000001856722d57d2a4521876523910f1352f7'
FOLDER='fotos'
mkdir -p "$FOLDER"

declare -a tasks=(
    "strozzapreti-alla-norcina-manteca:sausage pasta:italian pasta"
    "house-focaccia-manteca:focaccia bread:italian bread"
    "wild-garlic-en-spinazie-chitarra:green pasta:fresh pasta"
    "kale-en-chili-lumache:rigatoni pasta:pasta bowl"
    "eendenleverparfait-met-dadeljam:pate toast:charcuterie board"
    "chocolade-hazelnoot-tart:chocolate tart:hazelnut dessert"
    "house-made-ricotta:ricotta cheese bowl:fresh cheese"
    "fazzoletti-met-eendenragu:duck pasta:ragu pasta"
    "brown-crab-cacio-e-pepe:seafood pasta:crab pasta"
    "pasta-alla-norcina-guardian:creamy sausage pasta:pasta bowl"
    "tortellini-in-brodo:tortellini soup:pasta soup"
    "langzaam-gegaarde-varkensschouder-met-appel:braised pork:roast pork"
    "rigatoni-met-boerenkoolsaus:green pasta sauce:rigatoni"
)

for task in "${tasks[@]}"; do
    slug=$(echo "$task" | cut -d: -f1)
    term1=$(echo "$task" | cut -d: -f2)
    term2=$(echo "$task" | cut -d: -f3)
    
    found=0
    for term in "$term1" "$term2"; do
        encoded_term=$(echo "$term" | sed 's/ /%20/g')
        response=$(curl -s -H "Authorization: $API_KEY" "https://api.pexels.com/v1/search?query=$encoded_term&per_page=1")
        
        # Extract landscape or original URL
        img_url=$(echo "$response" | grep -o '"landscape":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ -z "$img_url" ]; then
            img_url=$(echo "$response" | grep -o '"original":"[^"]*"' | head -1 | cut -d'"' -f4)
        fi
        
        if [ ! -z "$img_url" ]; then
            # Append params
            sep="?"
            if [[ "$img_url" == *"?"* ]]; then sep="&"; fi
            final_url="${img_url}${sep}w=1200&h=700&fit=crop&auto=compress&cs=tinysrgb"
            
            curl -s -o "$FOLDER/$slug.jpg" "$final_url"
            echo "$slug: Success (Query: \"$term\")"
            found=1
            break
        fi
    done
    
    if [ $found -eq 0 ]; then
        echo "$slug: Failed"
    fi
done
