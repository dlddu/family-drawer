#!/usr/bin/env python3
"""`docs/handoff/checksums.txt`(문서 manifest)를 현재 docs/ 내용으로 다시 만든다.

문서를 **의도적으로** 고쳤을 때만 쓴다. 돌린 뒤에는 새로 찍힌 manifest 자체 해시를
`scripts/verify_docs.py` 의 `HANDOFF_CHECKSUMS_SHA256` 에 옮겨 적고, 그 옆 이력 주석에
근거(PR·커밋)를 한 줄 남겨야 검증이 다시 통과한다. 그 두 값을 함께 고치는 행위가
"문서를 바꾸기로 했다"는 명시적 기록이 된다.

manifest 는 docs 담당 소유다. 부트스트랩이 더한 문서(`verify_docs.BOOTSTRAP_OWNED`)는
목록에서 제외한다 — 그래야 부트스트랩이 문서를 더해도 docs 담당의 고정 해시가 흔들리지 않고,
`--check` 가 "문서가 바뀌었나"만 답한다.

사용: python3 scripts/update_docs_checksums.py [--check]
  --check  파일을 고치지 않고 달라지는지만 본다(종료 코드 1 = 다름)
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_docs import BOOTSTRAP_OWNED  # noqa: E402  (소유 경계의 단일 출처)

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
    skipped = []
    for root, dirs, names in os.walk(DOCS):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for n in sorted(names):
            p = Path(root) / n
            if p == OUT:
                continue
            if p.relative_to(REPO).as_posix() in BOOTSTRAP_OWNED:
                skipped.append(p.relative_to(REPO).as_posix())
                continue
            paths.append(p)

    body = "".join(
        f"{sha256(p)}  {p.relative_to(REPO).as_posix()}\n"
        for p in sorted(paths, key=lambda p: p.relative_to(REPO).as_posix())
    )
    current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""

    if skipped:
        print(f"manifest 범위 밖(부트스트랩 소유) {len(skipped)}개 제외: " + ", ".join(skipped))

    if check_only:
        if body == current:
            print(f"{OUT.relative_to(REPO)} 는 현재 docs/ 와 일치한다 — {len(paths)}개 파일")
            return 0
        print(f"{OUT.relative_to(REPO)} 가 현재 docs/ 와 다르다 — 의도한 변경이면 "
              f"--check 없이 다시 돌릴 것")
        return 1

    if body == current:
        print(f"{OUT.relative_to(REPO)} 는 이미 현재 docs/ 와 일치한다 — 쓰지 않았다")
    else:
        OUT.write_text(body, encoding="utf-8")
        print(f"{OUT.relative_to(REPO)} 갱신 — {len(paths)}개 파일")
    print(f"이 파일의 SHA-256: {sha256(OUT)}")
    print("→ scripts/verify_docs.py 의 HANDOFF_CHECKSUMS_SHA256 과 그 이력 주석을 맞출 것")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
