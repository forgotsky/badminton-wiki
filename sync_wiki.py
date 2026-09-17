#!/usr/bin/env python3
"""一键同步：把 vault 里的羽毛球笔记同步到 Quartz wiki 仓库并推送部署。

逻辑：
  1. 清掉 wiki 里旧的羽毛球内容（避免 vault 删了笔记、wiki 还留着）
  2. 拷 3 篇常青 + 45 篇源笔记
  3. 首页：羽毛球主页.md → index.md（加 title/aliases，Dataview 换成手动列表）
  4. git add + commit + push（无变化则跳过）
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VAULT = pathlib.Path("F:/Knowledge")
WIKI = pathlib.Path("F:/badminton-wiki")
CONTENT = WIKI / "content"
SUB = CONTENT / "读书笔记"


def sync() -> None:
    # 1. 清旧
    for p in list(CONTENT.glob("羽毛球*.md")) + list(CONTENT.glob("index.md")):
        p.unlink()
    SUB.mkdir(exist_ok=True)
    for p in SUB.glob("【上古教学视频】*.md"):
        p.unlink()

    # 2. 3 篇常青
    for name in ["羽毛球技术体系.md", "羽毛球七维评估.md", "羽毛球训练课实操手册.md"]:
        shutil.copy(VAULT / "朝阳" / "常青" / name, CONTENT / name)

    # 3. 首页 + 45 篇源笔记
    hp = (VAULT / "朝阳" / "常青" / "羽毛球主页.md").read_text(encoding="utf-8")
    hp = hp.replace("tags: [learning]", "tags: [learning]\naliases: [羽毛球主页]\ntitle: 羽毛球", 1)
    notes = []
    for p in sorted((VAULT / "朝阳" / "3-Resources" / "读书笔记").glob("【上古教学视频】*.md")):
        shutil.copy(p, SUB / p.name)
        notes.append(p.stem)
    links = "\n".join(f"- [[{n}]]" for n in notes)
    hp = re.sub(r"```dataview.*?```", links, hp, flags=re.S)
    (CONTENT / "index.md").write_text(hp, encoding="utf-8")

    print(f"✅ 内容已同步：3 篇常青 + 首页 + {len(notes)} 篇源笔记")


def push() -> None:
    subprocess.run(["git", "add", "-A"], cwd=WIKI, check=True)
    r = subprocess.run(["git", "commit", "-m", "同步：vault 羽毛球笔记更新"], cwd=WIKI)
    if r.returncode != 0:
        print("· 没有变化，跳过推送。")
        return
    subprocess.run(["git", "push", "origin", "v5"], cwd=WIKI, check=True)
    print("✅ 已推送，GitHub Actions 自动部署中（约 1 分钟生效）。")


if __name__ == "__main__":
    sync()
    push()
