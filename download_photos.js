const fs = require('fs');
const https = require('https');
const path = require('path');

const API_KEY = '563492ad6f91700001000001856722d57d2a4521876523910f1352f7';
const FOLDER = 'fotos';

const tasks = [
    { slug: 'strozzapreti-alla-norcina-manteca', terms: ['sausage pasta','italian pasta'] },
    { slug: 'house-focaccia-manteca', terms: ['focaccia bread','italian bread'] },
    { slug: 'wild-garlic-en-spinazie-chitarra', terms: ['green pasta','fresh pasta'] },
    { slug: 'kale-en-chili-lumache', terms: ['rigatoni pasta','pasta bowl'] },
    { slug: 'eendenleverparfait-met-dadeljam', terms: ['pate toast','charcuterie board'] },
    { slug: 'chocolade-hazelnoot-tart', terms: ['chocolate tart','hazelnut dessert'] },
    { slug: 'house-made-ricotta', terms: ['ricotta cheese bowl','fresh cheese'] },
    { slug: 'fazzoletti-met-eendenragu', terms: ['duck pasta','ragu pasta'] },
    { slug: 'brown-crab-cacio-e-pepe', terms: ['seafood pasta','crab pasta'] },
    { slug: 'pasta-alla-norcina-guardian', terms: ['creamy sausage pasta','pasta bowl'] },
    { slug: 'tortellini-in-brodo', terms: ['tortellini soup','pasta soup'] },
    { slug: 'langzaam-gegaarde-varkensschouder-met-appel', terms: ['braised pork','roast pork'] },
    { slug: 'rigatoni-met-boerenkoolsaus', terms: ['green pasta sauce','rigatoni'] }
];

if (!fs.existsSync(FOLDER)) {
    fs.mkdirSync(FOLDER);
}

function fetchJson(url) {
    return new Promise((resolve, reject) => {
        const options = { headers: { 'Authorization': API_KEY } };
        https.get(url, options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(new Error(`Failed to parse JSON: ${data.substring(0, 100)}`));
                }
            });
        }).on('error', reject);
    });
}

function downloadImage(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);
        https.get(url, (res) => {
            if (res.statusCode !== 200) {
                reject(new Error(`Status: ${res.statusCode}`));
                return;
            }
            res.pipe(file);
            file.on('finish', () => { file.close(); resolve(); });
        }).on('error', (err) => { 
            fs.unlink(dest, () => {}); 
            reject(err); 
        });
    });
}

async function run() {
    for (const task of tasks) {
        let success = false;
        let queryUsed = '';
        for (const term of task.terms) {
            try {
                const searchUrl = `https://api.pexels.com/v1/search?query=${encodeURIComponent(term)}&per_page=1`;
                const data = await fetchJson(searchUrl);
                if (data.photos && data.photos.length > 0) {
                    const photo = data.photos[0];
                    const baseUrl = photo.src.landscape || photo.src.large || photo.src.original;
                    const sep = baseUrl.includes('?') ? '&' : '?';
                    const finalUrl = `${baseUrl}${sep}w=1200&h=700&fit=crop&auto=compress&cs=tinysrgb`;
                    await downloadImage(finalUrl, path.join(FOLDER, `${task.slug}.jpg`));
                    queryUsed = term;
                    success = true;
                    break;
                }
            } catch (err) {
                // Silently try next term
            }
        }
        if (success) {
            console.log(`${task.slug}: Success (Query: "${queryUsed}")`);
        } else {
            console.log(`${task.slug}: Failed`);
        }
    }
}

run();
