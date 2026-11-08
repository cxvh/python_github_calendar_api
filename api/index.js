const HEADERS = {
    "accept": "text/html",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
};

function listSplit(items, n) {
    const result = [];
    for (let i = 0; i < items.length; i += n) {
        result.push(items.slice(i, i + n));
    }
    return result;
}

async function getData(name) {
    const res = await fetch("https://github.com/users/" + name + "/contributions", {
        headers: HEADERS,
        signal: AbortSignal.timeout(8000)
    });
    if (!res.ok) {
        throw new Error("GitHub HTTP " + res.status);
    }
    const html = await res.text();

    const pattern = /data-date="(\d{4}-\d{2}-\d{2})" id="contribution-day-component-\d-\d{1,2}" data-level="(\d+)"/g;
    const matches = [...html.matchAll(pattern)];

    const datemap = {};
    for (const m of matches) {
        datemap[m[1]] = m[2];
    }
    const datadate = matches.map(m => m[1]).sort();

    const datalist = [];
    let datacount = 0;
    for (const item of datadate) {
        const itemObj = { "date": item, "count": parseInt(datemap[item], 10) };
        datalist.push(itemObj);
        datacount += itemObj.count;
    }

    const datalistsplit = listSplit(datalist, 7);
    return {
        "total": datacount,
        "contributions": datalistsplit
    };
}

module.exports = async (req, res) => {
    const user = req.url.split('?')[1];
    try {
        const data = await getData(user);
        res.statusCode = 200;
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Content-type', 'application/json');
        res.end(JSON.stringify(data));
    } catch (e) {
        res.statusCode = 502;
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Content-type', 'application/json');
        res.end(JSON.stringify({ "error": String(e && e.message || e) }));
    }
};
