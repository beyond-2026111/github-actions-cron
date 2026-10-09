# 关机也能跑的定时任务（GitHub Actions 免费方案）

电脑关机也能自动运行的脚本项目，基于 **GitHub Actions**，公开仓库完全免费。

## 原理

代码推到 GitHub 后，GitHub 的服务器会按设定的时间自动运行脚本，你的电脑关不关机都不影响。运行结果会写回 `log.txt` 并提交到仓库，可以直观看到任务确实在跑。

## 本项目做了什么

`main.py` 每天定时调用免费的"今日诗词" API，把一句古诗追加到 `log.txt`。
你可以把它改成任何你想定时运行的任务（爬虫、数据备份、消息推送、网站监控等）。

## 使用步骤

### 1. 推送到 GitHub

```bash
git init
git add .
git commit -m "init: 定时任务项目"
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

> 仓库建议设为 **Public**（公开），这样 Actions 完全免费无限时。

### 2. 确认 Actions 已启用

进入 GitHub 仓库 → **Settings** → **Actions** → 确保允许 Actions 运行。

### 3. 手动跑一次试试

仓库页面 → **Actions** 标签 → 左侧选 **Scheduled Job** → 点 **Run workflow** → 选 `main` 分支 → **Run workflow**。

等几十秒，运行成功后 `log.txt` 会多一行，说明配置成功。

### 4. 坐等定时运行

默认每天 **北京时间早上 8:00** 自动运行一次，结果会自动提交到仓库。

## 自定义

### 改运行时间

编辑 `.github/workflows/run.yml` 里的 `cron` 表达式（UTC 时间）：

```yaml
schedule:
  - cron: "0 0 * * *"   # 每天 UTC 0:00 = 北京时间 8:00
```

常用例子（UTC，北京时间 = UTC + 8）：

| 需求 | cron | 北京时间 |
|------|------|----------|
| 每天早 8 点 | `0 0 * * *` | 08:00 |
| 每天晚 9 点 | `0 13 * * *` | 21:00 |
| 每小时一次 | `0 * * * *` | 每小时 |
| 每周一早 9 点 | `0 1 * * 1` | 周一 09:00 |

### 改脚本逻辑

直接改 `main.py`，把"获取诗词"换成你想做的事。需要第三方库就写进 `requirements.txt`。

### 需要密钥（如 API Token）

仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**，
然后在 `run.yml` 里用 `${{ secrets.你的变量名 }}` 引用：

```yaml
- name: 运行脚本
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
  run: python main.py
```

脚本里用 `os.environ["API_TOKEN"]` 读取。

## 注意事项

- GitHub 定时任务可能有几分钟延迟，不保证精确到秒。
- 免费额度：公开仓库无限，私有仓库每月 2000 分钟。
- 长期不活动（超过 60 天无提交）的仓库，定时任务会被暂停，需要手动重新启用。
