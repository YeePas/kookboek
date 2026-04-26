const fs = require('fs');
const https = require('https');
const path = require('path');

const API_KEY = process.env.PEXELS_API_KEY;

const tasks = [
    { slug: 'strozzapreti-alla-norcina-manteca', primary: 'italian sausage pasta bowl', fallback: 'pasta sausage' },
    { slug: 'house-focaccia-manteca', primary: 'focaccia bread olive oil', fallback: 'focaccia bread' },
    { slug: 'wild-garlic-en-spinazie-chitarra', primary: 'green pasta handmade', fallback: 'spinach pasta' },
    { slug: 'kale-en-chili-lumache', primary: 'kale pasta rigatoni', fallback: 'rigatoni pasta' },
    { slug: 'eendenleverparfait-met-dadeljam', primary: 'liver pate toast', fallback: 'charcuterie pate' },
    { slug: 'chocolade-hazelnoot-tart', primary: 'chocolate hazelnut tart', fallback: 'chocolate tart' },
    { slug: 'house-made-ricotta', primary: 'fresh ricotta cheese bowl', fallback: 'ricotta cheese' },
    { slug: 'fazzoletti-met-eendenragu', primary: 'duck ragu pasta', fallback: 'pasta ragu' },
    { slug: 'brown-crab-cacio-e-pepe', primary: 'crab pasta', fallback: 'seafood pasta' },
    { slug: 'pasta-alla-norcina-guardian', primary: 'pasta alla norcina', fallback: 'sausage cream pasta' },
    { slug: 'tortellini-in-brodo', primary: 'tortellini soup', fallback: 'tortellini broth' },
    { slug: 'langzaam-gegaarde-varkensschouder-met-appel', primary: 'braised pork shoulder', fallback: 'roast pork' },
    { slug: 'rigatoni-met-boerenkoolsaus', primary: 'rigatoni green sauce', fallback: 'rigatoni pasta' }
];

async function fetchJson(url) {
    return new Promise((resolve, reject) => {
        const options = {
            headers: { 'Authorization': API_KEY }
        };
        https.get(url, options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

function downloadFile(url, dest) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            if (res.statusCode === 301 || res.statusCode === 302) {
                downloadFile(res.headers.location, dest).then(resolve).catch(reject);
                return;
            }
            if (res.statusCode !== 200) {
               return reject(new Error('Status ' + res.statusCode));
            }
            const file = fs.createWriteStream(dest);
            res.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve();
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
}

async function run() {
    for (const task of tasks) {
        let photoUrl = null;
        try {
            let data = await fetchJson('https://api.pexels.com/v1/search?query=' + encodeURIComponent(task.primary) + '&per_page=1&orientation=landscape');
            if (data && data.photos && data.photos.length > 0) {
                photoUrl = data.photos[0].src.landscape || data.photos[0].src.large;
            }
        } catch (e) {}
        
        if (!photoUrl) {
            try {
                let data = await fetchJson('https://api.pexels.com/v1/search?query=' + encodeURIComponent(task.fallback) + '&per_page=1&orientation=landscape');
                if (data && data.photos && data.photos.length > 0) {
                    photoUrl = data.photos[0].src.landscape || data.photos[0].src.large;
                }
            } catch (e) {}
        }

        if (photoUrl) {
            const urlObj = new URL(photoUrl);
            urlObj.searchParams.set('w', '800');
            const dest = path.join('fotos', task.slug + '.jpg');
            try {
                await downloadFile(urlObj.toString(), dest);
                console.log(task.slug + ': Success');
            } catch (err) {
                console.log(task.slug + ': Failed (Download error)');
            }
        } else {
            console.log(task.slug + ': Failed (No photo found)');
        }
    }
}
run();
