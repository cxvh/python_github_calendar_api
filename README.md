# GitHub 贡献日历 API

获取 GitHub 用户贡献日历数据的 API。基于 GitHub 官方 GraphQL API，部署于 Vercel，Node.js 零依赖。

## API 用法

```
GET https://你的域名/api/?用户名
```

示例：

```
https://githubapicalendar.allapi.cc/api/?cxvh
```

返回格式：

```json
{
  "total": 24,
  "contributions": [
    [
      { "date": "2025-11-09", "count": 0 },
      { "date": "2025-11-10", "count": 3 }
    ]
  ]
}
```

- `total`：年度总贡献数
- `contributions`：按周分组（每周 7 天）

## 特性

- Node.js 零依赖（内置 fetch，无需 npm install）
- 数据源为 GitHub 官方 GraphQL API，稳定可靠
- 30 分钟缓存（函数内存 + Vercel CDN），避免频繁请求导致超时
- 请求失败返回 `502` + 错误信息 JSON

## 部署到 Vercel

### ① 生成 GitHub Token

1. 打开 https://github.com/settings/tokens
2. 点击 Generate new token (classic)，**所有 scope 都不勾选**（仅读取公开数据）
3. 复制生成的 Token（只显示一次）

### ② 部署项目

1. Fork 本仓库
2. 打开 [Vercel](https://vercel.com/)，点击 New Project 导入 Fork 的仓库，直接 Deploy

### ③ 配置环境变量（必须）

1. 项目 → Settings → Environment Variables → Add
2. 填写：
   - Type：**Secret**
   - Name：`GITHUB_TOKEN`
   - Value：第①步生成的 Token
   - Environments：勾选 **Production**
3. 重新部署（Deployments → Redeploy）使环境变量生效

### ④ 验证

访问 `https://你的域名/api/?你的GitHub用户名`，返回 JSON 数据即部署成功。

## 注意

- Vercel 项目 Settings → Node.js Version 建议选择 26.x
- 环境变量任何改动后需重新部署才生效
- 若返回 `{"error":"GITHUB_TOKEN 环境变量未配置"}`，按报错信息中的指引检查环境变量名称与 Production 勾选
