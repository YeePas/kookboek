const https = require('https');
const API_KEY = '563492ad6f91700001000001856722d57d2a4521876523910f1352f7';
const url = 'https://api.pexels.com/v1/search?query=pasta&per_page=1';
const options = { headers: { 'Authorization': API_KEY } };
https.get(url, options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        console.log('Status code:', res.statusCode);
        console.log('Headers:', res.headers);
        console.log('Data:', data);
    });
}).on('error', console.error);
