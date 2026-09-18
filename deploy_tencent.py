#!/usr/bin/env python3
"""把 Quartz 构建产物部署到腾讯云 COS。

前置（一次性）：
  1. pip install coscmd
  2. coscmd config -a <SecretId> -s <SecretKey> -b <桶名-AppId> -r <地域>
     例：coscmd config -a AKIDxxxx -s xxxx -b mywiki-1234567890 -r ap-guangzhou
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WIKI = pathlib.Path("F:/badminton-wiki")


def main() -> None:
    print("1/2 构建中 ...")
    subprocess.run(["npx", "quartz", "build"], cwd=WIKI, check=True)

    print("2/2 上传到腾讯云 COS ...")
    # -r 递归、-s 同步、--delete 删掉远端多出来的旧文件
    subprocess.run(
        ["coscmd", "upload", "-rs", "--delete", "public/", "/"],
        cwd=WIKI,
        check=True,
    )
    print("✅ 已上传，你的域名应该能看到更新了（CDN 缓存可能要等几十秒）。")


if __name__ == "__main__":
    main()
