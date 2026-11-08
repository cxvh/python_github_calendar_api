async function getData(name) {
    const token = process.env.GITHUB_TOKEN;
    if (!token) {
        throw new Error("GITHUB_TOKEN 环境变量未配置（函数运行时未读到该变量。请检查 Vercel 项目 Settings → Environment Variables：名称必须精确为 GITHUB_TOKEN，且勾选 Production 环境；任何改动后需重新部署才生效）");
    }

    const query = `query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}`;

    const res = await fetch("https://api.github.com/graphql", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query, variables: { login: name } }),
        signal: AbortSignal.timeout(8000)
    });
    if (!res.ok) {
        throw new Error("GitHub HTTP " + res.status);
    }

    const json = await res.json();
    if (json.errors) {
        throw new Error(json.errors[0].message);
    }

    const calendar = json.data && json.data.user
        && json.data.user.contributionsCollection
        && json.data.user.contributionsCollection.contributionCalendar;
    if (!calendar) {
        throw new Error("未找到该用户的贡献数据");
    }

    return {
        "total": calendar.totalContributions,
        "contributions": calendar.weeks.map(week =>
            week.contributionDays.map(day => ({
                "date": day.date,
                "count": day.contributionCount
            }))
        )
    };
}

const CACHE_TTL = 30 * 60 * 1000;
const cache = new Map();

module.exports = async (req, res) => {
    const user = req.url.split('?')[1];
    const cached = cache.get(user);
    if (cached && Date.now() - cached.time < CACHE_TTL) {
        res.statusCode = 200;
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Content-type', 'application/json');
        res.setHeader('Cache-Control', 's-maxage=1800');
        res.end(cached.body);
        return;
    }
    try {
        const body = JSON.stringify(await getData(user));
        cache.set(user, { body: body, time: Date.now() });
        res.statusCode = 200;
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Content-type', 'application/json');
        res.setHeader('Cache-Control', 's-maxage=1800');
        res.end(body);
    } catch (e) {
        res.statusCode = 502;
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Content-type', 'application/json');
        res.end(JSON.stringify({ "error": String(e && e.message || e) }));
    }
};
