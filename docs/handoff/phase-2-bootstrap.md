# 2단계 인계: 저장소 초기화와 검증 결과

> 작성 2026-11-25 · devops 세션 산출물 · 선행 문서 [`bootstrap-requirements.md`](./bootstrap-requirements.md)
> **이 문서는 "저장소에 무엇을 깔았고, 무엇을 일부러 깔지 않았는지"를 적는다.** 앱 코드는 여전히 없다.
> 검증 이력은 과거 기록을 지우지 않고 쌓는다(감사용). **현재 고정 근거는 §1-c 에 있다.**

---

## 0. 저장소 확인 (GitHub API 대조)

| 항목 | 값 | 결과 |
|---|---|---|
| repository ID | `1471208345` | 지정된 값과 일치 |
| 전체 이름 | `dlddu/family-drawer` | 일치 |
| 기본 브랜치 | `main` | 일치 |
| 가시성 | public | — (mockup 공개 여부는 D-10 미결) |

문서 브랜치 `docs/phase-1-product-docs` 는 **PR #1(docs 담당 소유)** 의 head 이고 base 는 `main` 이다.
부트스트랩 PR #2 의 base 도 `main` 이며, 문서 내용의 소유권은 PR #1 에 남는다 — 이 세션은 문서
파일을 고치지 않고, 검증의 **고정 근거만** 문서 쪽 manifest 에 맞춘다.

## 1-a. 1차 검증 — docs 커밋 `5c977db4` (2026-11-25, 과거 기록 · 현재 참조 아님)

`docs/handoff/checksums.txt` 자체 SHA-256 이
`0f168cef944e0fb1ee4503a43243353f8eeee1b9e508e596d7dc49bb6876e476` 로 일치하고,
목록의 16개 파일 해시가 전부 일치했다(`sha256sum -c` 16/16 OK). 목록 16개 + 목록 파일 자신 =
**17개**이며, 이는 그 커밋이 추가한 파일 집합과 정확히 같았다(차집합 0). 당시 `5c977db4` 는
`main`(`86e749b`)의 직계 자식(ahead 1 · behind 0)이었고 문서 전용 PR 은 아직 열려 있지 않았다.

## 1-b. 2차 검증 — docs 커밋 `62394e17` (최상위 가치 3개 재정의 · 과거 기록 · 현재 참조 아님)

PR #1 에 사용자의 신규 세 가치가 반영되어 문서 브랜치가 `5c977db4` → `62394e17` 로 올라갔다
(문서 11개 변경, 추가·삭제된 파일 없음). docs 담당이 같은 커밋에서 manifest 를 재생성해 두었고,
원격에서 그 커밋을 그대로 꺼내 확인했다: `docs/` 17개 · 목록 16줄 · 집합 차집합 0 ·
`sha256sum -c` 16/16 OK · manifest 자체 SHA-256
`e99fb06169ee81cc2c4481ad31df73cf21bad0242bc28040edf6d1647614bffe`.

## 1-c. 현재 검증 — docs 커밋 `2b50bd2a` = PR #1 최종 head (**최종 문서 리비전**)

`62394e17` → `2b50bd2a` 로 한 커밋 더 올라갔다(①사용자 편의성 최우선 정리, ③에 향후 검증 기대
결과 연결 — 문서 12개 변경, 추가·삭제된 파일 없음). 역시 docs 담당이 같은 커밋에서 manifest 를
재생성해 두었고, 원격의 그 커밋을 그대로 꺼내 확인했다.

| 확인 | 결과 |
|---|---|
| PR #1 상태 | open · head `2b50bd2a7a9d3269cb9168c537728627a59b78f7` · base `main` |
| `docs/` 파일 수 | 17개 (파일 집합 변화 없음) |
| manifest 목록 | 16줄, 목록 파일 집합 = `docs/` 실제 집합(자신 제외)과 차집합 0 |
| 목록 해시 | `sha256sum -c` **16/16 OK** |
| manifest 자체 SHA-256 | `e474704f00f0a7b4648934573eb0fda53bd86fda92c786135791852925a4a6b1` |

그래서 이 브랜치는 `2b50bd2a` 를 **강제 push 없이 정상 병합**하고(`main` 머지는 하지 않는다),
`verify_docs.py` 의 `HANDOFF_CHECKSUMS_SHA256` 을 위 값으로 갱신했다(이전 두 값은 이력 주석에
남긴다). `update_docs_checksums.py --check` 가 "manifest = 현재 docs/" 를 확인하므로
**재생성은 하지 않았다** — 문서와 manifest 는 docs 담당 소유다.

검증은 1회성으로 끝내지 않고 CI 에 있다 — `scripts/verify_docs.py handoff` 가 매 PR 에서 같은
17개를 다시 확인한다. 목록만 고쳐 넘어가는 변조는 manifest 자체 해시를 검증기 상수로 못박아 막는다.

### 소유 경계

manifest 는 docs 담당 소유다. 부트스트랩이 더한 문서(이 파일)는
`verify_docs.BOOTSTRAP_OWNED` 로 선언해 manifest 범위에서 제외했다 — 그래서 부트스트랩이 문서를
더해도 docs 담당의 고정 해시가 흔들리지 않고, `update_docs_checksums.py --check` 는 "문서가
바뀌었나"만 답한다.

## 2. 이번에 깐 것

| 산출물 | 무엇 | 왜 지금 가능한가 |
|---|---|---|
| `.github/workflows/pr.yml` | PR 단일 필수 체크 `pr-gate` 오케스트레이터 | 스택과 무관. 게이트 이름·`if: always()` + `toJSON(needs)` 판정은 `k3s-app-bootstrap` 규약 그대로 |
| `.github/workflows/checks.yml` | `handoff` · `docs` · `mockups` 세 job (`workflow_call`, head SHA 체크아웃) | 검사 대상이 문서뿐이라 플랫폼 중립 |
| `scripts/verify_docs.py` | 표준 라이브러리만 쓰는 문서 검증기 | 설치 의존성 0 |
| `scripts/update_docs_checksums.py` | 문서를 의도적으로 고칠 때 쓰는 manifest 재생성기(`--check` 로 정합만 확인 가능, 부트스트랩 소유 문서는 제외) | — |
| `README.md` | 저장소 색인(문서 지도 · 검증 방법 · 미결정 · 범위 밖) | 기존 1줄 제목을 보존한 채 확장 |
| `CLAUDE.md` | 뒤 세션용 저장소 지침(제약을 이어받게) | — |
| `.gitignore` · `.gitattributes` · `.editorconfig` | OS·편집기 산출물 제외, 줄바꿈 LF 고정 | 스택 항목은 비워 둠 |

`docs/` 아래 1단계 산출물 17개(manifest 포함)는 **부트스트랩이 한 바이트도 고치지 않았다** —
현재 내용은 PR #1 의 최종 docs 커밋 `2b50bd2a` 그대로이고, 이 브랜치가 더한 `docs/` 파일은 이 문서
하나다. 검증기의 `handoff` 모드가 그 사실을 매 PR 에서 다시 증명한다.

### 검증기가 보는 것

| 모드 | 검사 |
|---|---|
| `handoff` | manifest 자체 해시(고정 근거) + 목록 16개 파일 해시 + 부트스트랩 소유·manifest 밖 문서 안내 |
| `links` | 문서 간 상대 링크가 실제 파일을 가리키는지, 어느 문서에서도 닿지 않는 고립 문서가 없는지 |
| `mockups` | mockup `data-step` 이 여정 문서의 `STP-*` 와 순서까지 일치, `data-go` 전이 대상(단계/상태) 존재, 단계 안 `data-state` 중복 없음, 외부 자원 참조 0건, `docs/journeys/index.md` 등재 |

현재 결과: 실패 0 · 경고 0. mockup 수치가 문서가 주장하는 값과 같다 —
`JRN-gym-reservation` 단계 6 · 화면 10 · 상태 18, `JRN-recipe-link-collect` 단계 5 · 화면 9 · 상태 19.
검증기는 네 가지 고의 변조(문서 내용 수정 · 끊어진 링크 · 여정 단계 추가 · 체크섬 목록만 재생성)에
대해 모두 실패를 내는 것으로 확인했다.

## 3. 일부러 깔지 않은 것과 그 이유

`k3s-app-bootstrap` 스킬은 이미지 발행(`image.yml`) · kind e2e · `deploy/base`+overlays ·
flux-cd-apps 등록까지 한 번에 깐다. 그 입력이 **아직 결정되지 않은 제품 결정에 걸려 있다.**

| 깔지 않은 것 | 막는 결정 | 임의로 정하면 생기는 일 |
|---|---|---|
| Dockerfile · `image.yml` · 이미지 태그 파이프라인 | D-02 지원 OS · D-03 인프라 | 모바일 앱이면 컨테이너 이미지가 아예 필요 없다. 지금 고르면 스택을 문서가 아니라 CI 가 결정해 버린다 |
| `deploy/` kustomize base·overlays(prod·e2e·preview) | D-03 | 배포 대상(k3s)이 필요한지부터가 미결 |
| `port` · `health_path` · 노출 방식(internal/public) · Sablier · PVC | D-02 · D-03 | 서버가 있다는 가정이 들어간다 |
| flux-cd-apps 등록(`cluster/`, `apps/`) | 위 전부 + **이번 범위 밖**(다른 저장소 변경·Flux 적용) | — |
| lint·unit·e2e job | D-02(언어·테스트 러너) | 통과만 하는 빈 job 은 PR 화면에서 "테스트 통과"로 잘못 읽힌다 — 그래서 자리만 TODO 로 남겼다 |

D-02·D-03 이 닫히면 `k3s-app-bootstrap` 을 이어서 돌리면 된다. 새 job 은
`pr.yml` 의 `pr-gate.needs` 에 더하기만 하면 되고, **브랜치 보호 설정은 다시 손대지 않는다**
(필수 체크가 `pr-gate` 하나인 이유).

## 4. 남은 결정 (사용자)

| # | 결정 | 필요한 것 | 닫히면 |
|---|---|---|---|
| 1 | **D-02 지원 OS / 플랫폼** | 가족 구성원이 실제로 쓰는 기기 목록 | 프레임워크·언어·테스트 러너·공유 수신 입구 확정 → 코드 시작 |
| 2 | **D-03 가족 공유 인프라** | 1단계에 기기 간 동기화가 필요한지에 대한 판단 | 데이터 계층 확정, k3s 배포 필요 여부 확정 |
| 3 | D-10 GitHub Pages 공개 | 가족 정보가 든 문서를 공개 경로에 둘지 | mockup 공개 URL |
| 4 | D-08 가치 소유자 | 이름 한 줄 | 문서 체계 🔴 고아 가치 해소 |

D-01 · D-04 · D-05 · D-06 · D-07 은 문서의 임시 처리(자동화 범위 0 · 로컬 알림 ·
제목 없이 저장 성립 · `기간 미확인` 1급 상태 · 역할 기준 설계)로 **없이도 1단계 구현이 가능**하다.

## 5. 아직 남은 문서 자리

[`bootstrap-requirements.md`](./bootstrap-requirements.md) §7 의 `docs/index.html`(허브) ·
`docs/reader.html`(리더)은 **이번에도 만들지 않았다.** 형식을 정하는
`design-doc-structure-validator` 스킬이 이 세션에도 설치되어 있지 않아, 임의 형식으로 만들면
나중에 그 스킬이 정하는 규약과 충돌한다. mockup 의 문서 복귀 링크는 지금도 여정 문서를 직접
가리키는 대체 링크로 동작하며, 검증기는 이 두 경로를 "미생성 자리"로 알고 경고만 낸다
(`scripts/verify_docs.py` 의 `PENDING`).

## 6. 뒤 세션이 이어받는 제약

1단계 §6 제약을 그대로 잇는다: 추측한 주소에 push · 새 저장소 생성 · 실제 예약·결제·계정 생성 ·
공식 사이트 자동 반복 요청 · 비밀 값 커밋 · 머지 · 운영 배포를 하지 않는다.
여기에 2단계가 더하는 것: **다른 저장소(flux-cd-apps 등) 변경과 Flux 등록·적용은 별도 승인 범위**이고,
`docs/` 의 1단계 산출물은 체크섬을 함께 갱신하지 않는 한 고치지 않는다.
