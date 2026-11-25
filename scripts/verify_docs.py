#!/usr/bin/env python3
"""저장소 문서 최소 검증 — 표준 라이브러리만 쓰고, 앱 스택에 의존하지 않는다.

1단계(문서) 산출물이 깨지지 않았는지만 본다. 앱 코드·플랫폼이 정해지면
(`docs/decisions/open-questions.md` D-02·D-03) 그때 unit·e2e 검사가 별도로 붙는다.

모드:
  handoff   문서 manifest(`docs/handoff/checksums.txt`)의 목록 해시 + manifest 자체의 고정 근거
  links     문서 간 상대 링크가 실제 파일을 가리키는지 + 고립 문서 없는지
  mockups   여정 mockup 과 여정 문서의 단계 일치, 분기 상태 참조, 외부 의존 0건
  all       위 전부 (기본값)

사용: python3 scripts/verify_docs.py [handoff|links|mockups|all]
실패는 종료 코드 1. 아직 만들어지지 않은 알려진 자리(§PENDING)는 경고로만 알린다.
"""

from __future__ import annotations

import hashlib
import html.parser
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"

# ── 고정 상수 ────────────────────────────────────────────────────────────────
# `docs/handoff/checksums.txt`(문서 manifest) 자체의 SHA-256. 이 값이 맞아야
# "그 체크섬 목록이 그 목록"임이 보장된다 — 목록만 고치고 파일을 함께 고치는
# 변조를 막는다. manifest 와 그 안의 문서는 docs 담당 소유이고, 이 상수는
# 부트스트랩이 "어느 manifest 를 검증 근거로 삼는지" 선언하는 자리다.
#
# 갱신 절차(문서를 의도적으로 고쳤을 때):
#   1) docs 담당이 문서를 고치고 `python3 scripts/update_docs_checksums.py` 로 manifest 재생성
#   2) 출력된 SHA-256 을 아래 값으로 옮겨 적고, 근거(PR·커밋)를 이력에 한 줄 남긴다
#
# 고정 근거 이력 (감사용 — 지우지 않는다):
#   0f168cef944e0fb1ee4503a43243353f8eeee1b9e508e596d7dc49bb6876e476
#       docs 커밋 5c977db4 (1단계 최초 인계, 2026-11-25) — 현재 참조 아님
#   e99fb06169ee81cc2c4481ad31df73cf21bad0242bc28040edf6d1647614bffe
#       docs 커밋 62394e17 (가치 3개 재정의, 2026-11-25) — 현재 참조 아님
#   e474704f00f0a7b4648934573eb0fda53bd86fda92c786135791852925a4a6b1
#       docs 커밋 2b50bd2a = PR #1 최종 head (①편의성 최우선 정리 + ③ 검증 기대 결과 연결,
#       2026-11-25, **최종 문서 리비전**) — **현재 참조**
HANDOFF_CHECKSUMS_SHA256 = "e474704f00f0a7b4648934573eb0fda53bd86fda92c786135791852925a4a6b1"
CHECKSUMS = DOCS / "handoff" / "checksums.txt"

# manifest 범위 밖인 부트스트랩 소유 문서. docs 담당의 manifest 는 1단계 문서 17개를
# 덮고, 여기 적힌 파일은 그 목록에 들어가지 않는다 — 그래서 manifest 재생성
# (`update_docs_checksums.py`)도 이 파일을 건너뛴다. 소유 경계를 코드로 못박아,
# 부트스트랩이 문서를 더해도 docs 담당의 고정 해시가 흔들리지 않게 한다.
BOOTSTRAP_OWNED = {"docs/handoff/phase-2-bootstrap.md"}

# 인계 문서 §7 이 "아직 없다"고 적어 둔 자리. `design-doc-structure-validator`
# 스킬이 형식을 정하는 파일이라 이 세션에서 임의로 만들지 않았다. 링크가 이들을
# 가리키면 실패가 아니라 경고다.
PENDING = {"docs/index.html", "docs/reader.html"}

# 링크 검사에서 진입점으로 보는 파일(다른 문서가 가리키지 않아도 고립이 아니다).
ENTRYPOINTS = {"README.md", "docs/README.md"}

DOC_SUFFIXES = {".md", ".html"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}

MD_LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_ATTR_LINK = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL  {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"  WARN  {msg}")


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def rel(p: Path) -> str:
    return p.relative_to(REPO).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def doc_files() -> list[Path]:
    out = []
    for root, dirs, names in os.walk(DOCS):
        dirs[:] = [d for d in dirs if d != ".git"]
        for n in sorted(names):
            p = Path(root) / n
            if p.suffix.lower() in DOC_SUFFIXES:
                out.append(p)
    return sorted(out)


# ── handoff ─────────────────────────────────────────────────────────────────
def check_handoff() -> None:
    print("[handoff] 인계 체크섬")
    if not CHECKSUMS.is_file():
        fail(f"{rel(CHECKSUMS)} 가 없다 — 1단계 인계 산출물이 빠졌다")
        return

    actual = sha256(CHECKSUMS)
    if actual == HANDOFF_CHECKSUMS_SHA256:
        ok(f"{rel(CHECKSUMS)} 자체 해시가 고정 근거와 일치")
    else:
        fail(f"{rel(CHECKSUMS)} 자체 해시 불일치 — 문서 manifest 가 고정 근거와 다르다\n"
             f"          기대 {HANDOFF_CHECKSUMS_SHA256}\n"
             f"          실제 {actual}\n"
             f"          문서를 의도적으로 고쳤다면 scripts/update_docs_checksums.py 를 돌리고 "
             f"verify_docs.py 의 HANDOFF_CHECKSUMS_SHA256 을 함께 갱신할 것"
             f"(이력 주석에 근거 PR·커밋을 남긴다)")

    listed = 0
    for lineno, line in enumerate(CHECKSUMS.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            fail(f"{rel(CHECKSUMS)}:{lineno} 형식이 '<sha256>  <경로>' 가 아니다")
            continue
        want, name = parts[0], parts[1].strip().lstrip("*")
        target = REPO / name
        listed += 1
        if not target.is_file():
            fail(f"manifest 에 있는 {name} 파일이 없다")
        elif sha256(target) != want:
            fail(f"{name} 내용이 manifest 의 해시와 다르다")
    ok(f"목록 {listed}개 파일 + checksums.txt = {listed + 1}개 검증")

    covered = {"docs/handoff/checksums.txt"} | {
        ln.split(None, 1)[1].strip()
        for ln in CHECKSUMS.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#") and len(ln.split(None, 1)) == 2
    }
    uncovered = [rel(p) for p in doc_files() if rel(p) not in covered]
    owned = [n for n in uncovered if n in BOOTSTRAP_OWNED]
    extra = [n for n in uncovered if n not in BOOTSTRAP_OWNED]
    if owned:
        print(f"  info  부트스트랩 소유 문서 {len(owned)}개(manifest 범위 밖, 설계대로): "
              + ", ".join(owned))
    if extra:
        print(f"  info  manifest 에 없는 문서 {len(extra)}개(검증 대상 아님 — docs 담당이 "
              f"manifest 를 재생성하면 포함된다): " + ", ".join(extra))


# ── links ───────────────────────────────────────────────────────────────────
def extract_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    found = []
    if path.suffix.lower() == ".md":
        found += MD_LINK.findall(text)
        found += HTML_ATTR_LINK.findall(text)
    else:
        found += HTML_ATTR_LINK.findall(text)
    return found


def check_links() -> None:
    print("[links] 문서 간 링크와 고립 문서")
    files = doc_files() + sorted(REPO.glob("*.md"))
    files = [p for p in files if p.is_file()]
    referenced: set[str] = set()
    checked = 0

    for path in files:
        for raw in extract_links(path):
            if EXTERNAL.match(raw) or raw.startswith("#") or not raw.strip():
                continue
            target = raw.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                name = resolved.relative_to(REPO).as_posix()
            except ValueError:
                fail(f"{rel(path)} → {raw} 가 저장소 밖을 가리킨다")
                continue
            checked += 1
            if resolved.is_dir():
                referenced.add(name)
                continue
            if not resolved.exists():
                if name in PENDING:
                    warn(f"{rel(path)} → {name} (인계 §7 의 미생성 자리)")
                else:
                    fail(f"{rel(path)} → {raw} 대상 파일이 없다")
                continue
            referenced.add(name)
    ok(f"상대 링크 {checked}건 확인 (문서 {len(files)}개)")

    orphans = [rel(p) for p in doc_files()
               if rel(p) not in referenced and rel(p) not in ENTRYPOINTS]
    if orphans:
        fail("어느 문서에서도 링크되지 않은 문서(고립): " + ", ".join(orphans))
    else:
        ok("고립 문서 없음 — 모든 문서가 색인·상호 링크로 닿는다")


# ── mockups ─────────────────────────────────────────────────────────────────
class MockupParser(html.parser.HTMLParser):
    """`data-step` 섹션별로 화면·상태·전이를 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.journey: str | None = None
        self.doc_attr: str | None = None
        self.steps: list[str] = []
        self.states: dict[str, list[str]] = {}
        self.screens: dict[str, list[str]] = {}
        self.gos: list[str] = []
        self.resources: list[str] = []
        self._stack: list[tuple[str, str | None]] = []
        self._step: str | None = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        opened_step = None

        if "data-journey" in a and self.journey is None:
            self.journey = a["data-journey"]
            self.doc_attr = a.get("data-doc")
        if "data-step" in a:
            opened_step = a["data-step"]
            self.steps.append(opened_step)
            self.states.setdefault(opened_step, [])
            self.screens.setdefault(opened_step, [])
            self._step = opened_step
        if "data-state" in a and self._step:
            self.states[self._step].append(a["data-state"])
        if "data-screen" in a and self._step:
            self.screens[self._step].append(a["data-screen"])
        if "data-go" in a:
            self.gos.append(a["data-go"])
        # 외부 자원 참조(빌드·CDN·폰트 0건이어야 한다)
        if tag in {"script", "link", "img", "iframe", "source", "video", "audio", "embed"}:
            for key in ("src", "href"):
                if a.get(key):
                    self.resources.append(f"<{tag} {key}={a[key]}>")

        if tag not in VOID_TAGS:
            self._stack.append((tag, opened_step))

    def handle_endtag(self, tag):
        while self._stack:
            name, opened_step = self._stack.pop()
            if opened_step is not None:
                self._step = None
            if name == tag:
                break


def journey_steps_from_doc(doc: Path) -> list[str]:
    seen: list[str] = []
    for m in re.finditer(r"STP-[a-z0-9-]+", doc.read_text(encoding="utf-8")):
        if m.group(0) not in seen:
            seen.append(m.group(0))
    return seen


def check_mockups() -> None:
    print("[mockups] 여정 mockup ↔ 여정 문서")
    mockups = sorted((DOCS / "journeys").glob("*/index.html"))
    if not mockups:
        fail("docs/journeys/<여정-id>/index.html mockup 이 하나도 없다")
        return

    index_md = DOCS / "journeys" / "index.md"
    index_text = index_md.read_text(encoding="utf-8") if index_md.is_file() else ""

    for mockup in mockups:
        jid = mockup.parent.name
        print(f"  — {jid}")
        parser = MockupParser()
        parser.feed(mockup.read_text(encoding="utf-8"))

        if parser.journey != jid:
            fail(f"{jid}: main[data-journey]={parser.journey!r} 가 디렉터리 이름과 다르다")

        doc = DOCS / "user-journeys" / f"{jid}.md"
        if not doc.is_file():
            fail(f"{jid}: 여정 문서 {rel(doc)} 가 없다")
            continue

        doc_steps = journey_steps_from_doc(doc)
        if parser.steps == doc_steps:
            ok(f"{jid}: 단계 {len(parser.steps)}개가 여정 문서와 순서까지 일치")
        else:
            fail(f"{jid}: 단계가 여정 문서와 다르다\n"
                 f"          mockup {parser.steps}\n"
                 f"          문서   {doc_steps}")

        for step, states in parser.states.items():
            dup = {s for s in states if states.count(s) > 1}
            if dup:
                fail(f"{jid}: {step} 안에 같은 data-state 가 중복 — {sorted(dup)}")

        bad = []
        for go in parser.gos:
            step, _, state = go.partition("/")
            if step not in parser.states:
                bad.append(go)
            elif state and state not in parser.states[step]:
                bad.append(go)
        if bad:
            fail(f"{jid}: 가리키는 대상이 없는 data-go — {sorted(set(bad))}")
        else:
            ok(f"{jid}: data-go 전이 {len(parser.gos)}건 모두 존재하는 단계/상태를 가리킨다")

        if parser.resources:
            fail(f"{jid}: 외부/별도 자원 참조가 있다(단일 파일·file:// 동작 요건) — {parser.resources}")
        else:
            screens = sorted({s for v in parser.screens.values() for s in v})
            states = sum(len(v) for v in parser.states.values())
            ok(f"{jid}: 외부 의존 0건 · 화면 {len(screens)}종 · 상태 {states}개")

        if index_md.is_file() and jid not in index_text:
            fail(f"{jid}: docs/journeys/index.md 인덱스에 없다")


def main() -> int:
    mode = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    modes = {"handoff": [check_handoff], "links": [check_links],
             "mockups": [check_mockups],
             "all": [check_handoff, check_links, check_mockups]}
    if mode not in modes:
        print(__doc__)
        return 2
    for fn in modes[mode]:
        fn()
        print()
    if warnings:
        print(f"경고 {len(warnings)}건 (실패 아님)")
    if failures:
        print(f"실패 {len(failures)}건")
        return 1
    print("통과")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
