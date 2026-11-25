# family-drawer

가족이 "놓치면 다시 하기 번거로운 일"을 놓치지 않게 돕는 가족용 앱 저장소.
현재 상태는 **1단계(제품 문서) 완료 + 2단계 저장소 초기화**이며, **앱 코드는 아직 없다.**

두 가지 요구를 다룬다.

1. **부천도시공사 헬스 수강신청** — 시간 단위 "예약"이 아니라 월 단위 수강신청/회원등록이다
2. **유튜브 공유로 받은 링크를 요리 레시피로 모아 다시 열기**

---

## 문서부터 읽는다

| 들어가는 곳 | 무엇이 있나 |
|---|---|
| [`docs/README.md`](docs/README.md) | **1단계 문서 색인 — 읽는 순서가 여기 있다** (사실 근거 → 가치 → 여정 → PRD → 테스트) |
| [`docs/decisions/open-questions.md`](docs/decisions/open-questions.md) | 미결정 D-01~D-10. 코드를 시작하기 전에 **D-02(지원 OS)·D-03(가족 공유 인프라)** 가 닫혀야 한다 |
| [`docs/handoff/bootstrap-requirements.md`](docs/handoff/bootstrap-requirements.md) | 1단계 → 2단계 인계: 화면 인벤토리(`data-screen`·`data-state`), 의도적 제외, 구현이 바로 가져갈 수 있는 것 |
| [`docs/handoff/phase-2-bootstrap.md`](docs/handoff/phase-2-bootstrap.md) | 2단계(이 저장소 초기화)가 한 일 · 검증 결과 · **다음 단계에 남긴 결정** |
| [`docs/journeys/index.md`](docs/journeys/index.md) | 눌러볼 수 있는 여정 mockup 2개 (단일 HTML, `file://` 로 열린다) |

mockup 은 브라우저로 파일을 직접 열면 동작한다 — 빌드·CDN·외부 폰트가 없다.

```
docs/
  research/        사실 근거([확인]/[가정] 구분 + 출처 + 확인일)
  product/         가치 문서 · PRD(AC-G1~G10 / AC-R1~R10) · 테스트 시나리오 · 문서 체계 상태 추적
  user-journeys/   여정 2개 (JRN-*, 단계 STP-*)
  journeys/        여정별 mockup (여정 하나 = 페이지 하나)
  decisions/       열린 질문
  handoff/         단계 간 인계 + 체크섬
scripts/           문서 검증기(표준 라이브러리만)
.github/workflows/ PR 단일 필수 체크 `pr-gate`
```

## 검증을 돌린다

의존성 설치가 필요 없다. python3 만 있으면 된다.

```bash
python3 scripts/verify_docs.py            # 전부
python3 scripts/verify_docs.py handoff    # 문서 manifest(17개)가 고정 근거와 같은지
python3 scripts/verify_docs.py links      # 문서 간 링크 · 고립 문서
python3 scripts/verify_docs.py mockups    # mockup 단계·상태가 여정 문서와 맞는지
```

PR 에서는 같은 검사가 `checks / handoff · docs · mockups` 로 돌고, 브랜치 보호가 요구하는
체크는 그것들을 모은 **`pr-gate` 하나**다. 체크를 더 붙일 때는 job 을 만들고
`.github/workflows/pr.yml` 의 `pr-gate.needs` 에 넣는다 — 브랜치 보호 설정은 건드리지 않는다.

### 문서 manifest 와 소유 경계

`docs/handoff/checksums.txt` 가 문서 manifest(1단계 문서 17개)이고, 그 파일 **자체의 SHA-256** 을
`scripts/verify_docs.py` 의 `HANDOFF_CHECKSUMS_SHA256` 이 고정 근거로 들고 있다 — 목록만 고치고
파일을 함께 고치는 변조가 막힌다. manifest 와 그 안의 문서는 **docs 담당 소유**이고, 부트스트랩이
더한 문서(`verify_docs.BOOTSTRAP_OWNED`)는 manifest 범위 밖이다.

문서를 **의도적으로** 고쳤다면:

```bash
python3 scripts/update_docs_checksums.py --check   # 먼저 정합 여부만 본다(쓰지 않는다)
python3 scripts/update_docs_checksums.py           # 다르면 manifest 재생성
# 출력된 SHA-256 을 scripts/verify_docs.py 의 HANDOFF_CHECKSUMS_SHA256 에 옮겨 적고,
# 그 옆 이력 주석에 근거(PR·커밋)를 한 줄 남긴다 — 과거 값은 감사용으로 지우지 않는다.
```

현재 고정 근거: manifest `e474704f…a4a6b1` = docs 커밋 `2b50bd2a`(PR #1 최종 head, **최종 문서 리비전**).
이전 근거 `0f168cef…6e476`(docs `5c977db4`, 최초 인계)와 `e99fb061…14bffe`(docs `62394e17`, 가치 3개 재정의)는
이력에만 남아 있고 **현재 참조가 아니다** — 이력은 `scripts/verify_docs.py` 주석에 그대로 있다.

## 아직 정하지 않은 것 (추측하지 않는다)

| 미결정 | 막는 것 |
|---|---|
| D-02 지원 OS / 플랫폼 | 공유 수신 입구(Android `ACTION_SEND` vs iOS Share Extension), 프레임워크·언어, 테스트 러너 |
| D-03 가족 공유 인프라 | 데이터 계층(로컬 전용 vs 동기화), 배포 대상 유무, 컨테이너 이미지·매니페스트 |
| D-10 GitHub Pages 공개 | mockup 공개 경로 (가족 정보가 든 문서를 공개할지는 따로 판단이 필요하다) |

그래서 이 저장소에는 아직 Dockerfile·`deploy/`·이미지 발행 워크플로가 없다.
D-02·D-03 이 닫히면 devops 플러그인의 `k3s-app-bootstrap` 스킬로 이어서 깐다.

## 하지 않는 것

- 실제 예약·결제·계정 생성 (공식 경로로 넘기고 결과를 수동 기록하는 데까지만)
- 공식 사이트 자동 신청·반복 요청 (자동화 범위 0 — D-01)
- 비밀 값(API 키 등) 커밋
