"""
定时任务示例脚本
功能：调用免费 API 获取一句诗词，并记录到日志文件。
在 GitHub Actions 中定时运行，电脑关机也不影响。
"""

import datetime
import json
import os
import sys
import urllib.request
import urllib.error

LOG_FILE = "log.txt"
API_URL = "https://v1.jinrishici.com/all.json"


def fetch_poem():
    """调用免费的今日诗词 API，返回一句诗和作者信息。"""
    req = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Mozilla/5.0 (scheduled-job)"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    # 该 API 返回字段：content / origin / author / category
    return {
        "content": data.get("content", ""),
        "origin": data.get("origin", ""),
        "author": data.get("author", ""),
    }


def append_log(poem):
    """把本次运行结果追加到日志文件。"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"[{now}] {poem['content']} "
        f"—— {poem['author']}《{poem['origin']}》\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    return line


def main():
    try:
        poem = fetch_poem()
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(f"[ERROR] 获取诗词失败：{e}", file=sys.stderr)
        # 即使 API 失败也写一条日志，证明任务确实跑过
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now}] [ERROR] API 调用失败：{e}\n")
        sys.exit(1)

    line = append_log(poem)
    print(line, end="")
    print(f"已追加到 {os.path.abspath(LOG_FILE)}")


if __name__ == "__main__":
    main()
