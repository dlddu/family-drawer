#!/usr/bin/env python3
"""`docs/handoff/checksums.txt` 를 현재 docs/ 내용으로 다시 만든다.

1단계 인계 산출물을 **의도적으로** 고쳤을 때만 쓴다. 돌린 뒤에는 새로 찍힌
`docs/handoff/checksums.txt` 자체 해시를 `scripts/verify_docs.py` 의
`HANDOFF_CHECKSUMS_SHA256` 에 옮겨 적어야 검증이 다시 통과한다. 그 두 값을 함께
고치는 행위가 "문서를 바꾸기로 했다"는 명시적 기록이 된다.

사용: python3 scripts/update_docs_checksums.py [--check]
  --check  파일을 고치지 않고 달라지는지만 본다(종료 코드 1 = 다름)
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
OUT = DOCS / "handoff" / "checksums.txt"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    paths = []
    for root, dirs, names in os.walk(DOCS):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for n in sorted(names):
            p = Path(root) / n
            if p != OUT:
                paths.append(p)

    body = "".join(
        f"{sha256(p)}  {p.relative_to(REPO).as_posix()}\n"
        for p in sorted(paths, key=lambda p: p.relative_to(REPO).as_posix())
    )
    current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""

    if check_only:
        if body == current:
            print(f"{OUT.relative_to(REPO)} 는 현재 docs/ 와 일치한다")
            return 0
        print(f"{OUT.relative_to(REPO)} 가 현재 docs/ 와 다르다 — 의도한 변경이면 "
              f"--check 없이 다시 돌릴 것")
        return 1

    OUT.write_text(body, encoding="utf-8")
    print(f"{OUT.relative_to(REPO)} 갱신 — {len(paths)}개 파일")
    print(f"이 파일의 새 SHA-256: {sha256(OUT)}")
    print("→ scripts/verify_docs.py 의 HANDOFF_CHECKSUMS_SHA256 을 위 값으로 바꿀 것")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
