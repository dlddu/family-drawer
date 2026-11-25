# 뒤 세션 인계: 최소 부트스트랩 요구

> 작성 2026-11-25 · 1단계(문서) 세션 산출물
> **이 문서는 "코드를 어떻게 쓰라"가 아니라 "문서를 어디에 어떻게 받고, 무엇을 먼저 정해야 코드를 시작할 수 있는지"를 적는다.**
> 1단계는 문서 전용이므로 이 세션은 앱 코드를 만들지 않았다.

---

## 0. 현재 상태 한 줄

문서 11개 + mockup 2개가 **로컬 작업 디렉터리에만** 있다 (`/session/state/workspace/docs/`).
git 저장소로 초기화하지 **않았고**, 원격에 push 하지 **않았다**. 저장소 주소(D-09)가 오면 그 저장소에 그대로 넣으면 된다.

## 1. 문서를 받는 절차 (저장소 주소를 받은 직후)

```
# 1) 사용자가 준 정확한 주소로 clone — 주소를 추측하지 않는다
git clone <사용자가-준-주소> repo && cd repo

# 2) 기존 레포에 docs/ 가 이미 있으면 덮어쓰지 말고 먼저 확인한다
ls docs/ 2>/dev/null

# 3) 1단계 산출물을 옮긴다 (경로 구조를 그대로 유지)
cp -R /session/state/workspace/docs/. ./docs/

# 4) 체크섬으로 전송 검증 (아래 §5 의 값과 비교)
find docs -type f | sort | xargs sha256sum

# 5) mockup 검사기를 다시 돌려 문서-mockup 연결이 살아 있는지 확인
python3 <skill-bundle>/journey-mockup-builder/scripts/check_mockup.py \
  docs/journeys/JRN-gym-reservation/index.html docs/user-journeys/JRN-gym-reservation.md
python3 <skill-bundle>/journey-mockup-builder/scripts/check_mockup.py \
  docs/journeys/JRN-recipe-link-collect/index.html docs/user-journeys/JRN-recipe-link-collect.md
```

브랜치는 기본 브랜치에 바로 쓰지 말고 새 브랜치(예: `docs/phase-1-product-docs`)를 만든다.
**머지·운영 배포는 이 인계 범위 밖이다.**

## 2. 코드를 시작하기 전에 반드시 닫아야 하는 결정

| 순서 | 결정 | 없으면 생기는 일 | 문서 |
|---|---|---|---|
| 1 | **D-02 지원 OS** | 요구 ②의 입구(유튜브 공유 수신)를 구현할 수 없다. Android `ACTION_SEND` 와 iOS Share Extension 은 다른 구조다 | `../decisions/open-questions.md` |
| 2 | **D-03 가족 공유 인프라** | 데이터 계층을 두 번 만든다 (로컬만 → 서버 추가는 재작업) | 같은 문서 |
| 3 | **D-01 자동 신청 허용 여부** | 허용되지 않는 기능을 만들 위험. **문서는 이미 "자동화 범위 0"으로 확정해 두었으니, 그대로 가면 코드 변경은 없다** | 같은 문서 |
| 4 | D-05 제목 조회 방법 | 선택 기능이므로 **없이도 1단계 구현 가능**(AC-R9가 그렇게 쓰여 있다) | 같은 문서 |
| 5 | D-06 접수 기간 데이터 출처 | `기간 미확인` 상태가 1급 상태로 설계되어 있어 **없이도 구현 가능** | 같은 문서 |

→ **1·2번만 닫히면 구현을 시작할 수 있다.** 3·4·5는 현재 문서의 임시 처리로 진행 가능하다.

## 3. 구현이 문서에서 바로 가져갈 수 있는 것

| 필요한 것 | 어디에 있나 |
|---|---|
| 화면 목록 · 라우트 후보 | mockup 의 `data-screen` 값 (아래 §4 표) |
| 화면 상태 (빈·로딩·오류·시트·모달) | mockup 의 `data-state` 값 — 검사기 출력이 단계별 목록을 뽑아 준다 |
| 화면 전이 | mockup 의 `data-go` 값 |
| 완료 조건 | PRD 의 AC-G1~G10 / AC-R1~R10 |
| 사용자에게 보일 문구 | 레시피 PRD §5 피드백 문구표 (10행, 글자 그대로 쓸 것) |
| 링크 파싱 규칙과 기대값 | 레시피 PRD §4 + 테스트 TC-R2 (12행) · TC-R4 (7행) — **그대로 단위 테스트로 옮길 수 있다** |
| 공식 URL 형태 | `https://www.best.or.kr/fmcs/271?center=<센터코드>` (확인된 코드: 부천체육관 `BCS03`, 소사국민체육센터 `BCS01`) |
| 하지 말아야 할 것 | 가치 문서 「범위 밖」 표 + `VAL-official-path-only` |

## 4. 화면 인벤토리 (mockup `data-screen` → 구현 라우트 후보)

### JRN-gym-reservation (6단계 · 화면 10종 · 상태 18개)

| 단계 | 화면 (`data-screen`) | 상태 (`data-state`) | 근거 |
|---|---|---|---|
| `STP-notice-check` | `home` | `window-closed`, `unknown-period`, `loading`, `load-error` | AC-G2 · 분기표(접수 전·기간 미확인) · 네트워크 화면의 기본 상태(가정) |
| `STP-pick-center` | `center-list`, `center-detail` | `detail`, `stale`, `empty` | AC-G8(확인일·오래된 정보) · 목록 화면의 빈 상태(가정) |
| `STP-prep-account` | `apply-prep`, `apply-prep-onsite` | `ready`, `minor`, `foreigner` | AC-G3, AC-G4, AC-G5 · 분기표(14세 미만·외국인) |
| `STP-official-apply` | `official-handoff`, `official-handoff-blocked` | `leaving`, `error`, `maintenance` | AC-G1, AC-G9 · 분기표(열기 실패·점검·마감) |
| `STP-record-result` | `result-sheet`, `application-list` | `list`, `resume`, `saved` | AC-G6, AC-G10 · 분기표(중도 이탈 이어하기) |
| `STP-remind-next` | `reminder-settings` | `no-date`, `permission-denied` | AC-G7 · 분기표(기간 미확인·알림 권한 거부) |

### JRN-recipe-link-collect (5단계 · 화면 9종 · 상태 19개)

| 단계 | 화면 (`data-screen`) | 상태 (`data-state`) | 근거 |
|---|---|---|---|
| `STP-share-from-youtube` | `external-youtube-app`(외부 앱, 구현 범위 밖), `os-share-sheet`(OS 제공), `share-receive` | `app-list`, `receiving` | AC-R1 · 여정 진입 맥락 |
| `STP-confirm-save` | `save-confirm` | `duplicate`, `invalid-not-youtube`, `invalid-no-id`, `resume`, `title-failed`, `saved`, `offline` | AC-R2~R4, AC-R7, AC-R9 · 분기표 6행 |
| `STP-browse-collection` | `collection-list` | `filtered`, `empty`, `no-results`, `loading` | AC-R8, AC-R10 · 빈 상태 ≠ 0건 |
| `STP-open-original` | `recipe-detail` | `web-fallback`, `unavailable` | AC-R5, AC-R6 · 분기표(앱 미설치·삭제/비공개) |
| `STP-fix-entry` | `recipe-detail-actions`, `link-edit`, `delete-confirm-modal`, `collection-list` | `edit-link`, `edit-duplicate`, `delete-confirm`, `deleted` | AC-R6 · 되돌릴 수 없는 행동 뒤 확인 모달 원칙 |

### 의도적 제외 (mockup 에 그리지 않은 것 + 사유)

| 제외 | 사유 |
|---|---|
| 온보딩·로그인·회원가입 화면 | 1단계 범위 밖. 공유 수신 경로에서 인증을 요구하지 않는 것이 AC-R1 요건 |
| 공식 사이트(best.or.kr) 내부 화면 전체 | 우리 구현 화면이 아니다. 앱은 외부 브라우저로 넘긴다 (AC-G1) |
| 유튜브 앱 내부 화면 | 외부 앱. `external-youtube-app` 은 여정 입구를 설명하기 위한 **맥락용 1장**만 그렸다 |
| 설정·도움말 화면 본문 | AC-G5 의 고정 문구 위치만 중요하고, 화면 자체는 두 핵심 흐름 밖. `data-offpath` 로 표시 |
| 가족 구성원 관리/초대 화면 | D-03·D-07 미결정. 지금 그리면 가정이 구현 기준이 된다 |
| 태그 선택 시트·날짜 피커 내부 | OS/프레임워크 기본 컴포넌트에 의존. `data-offpath` 로 표시 |
| 다크 모드 | 디자인 시스템 없음. mockup 은 임의 무채색 스타일이다 |

## 5. 산출물 목록과 체크섬

→ [`checksums.txt`](./checksums.txt) (SHA-256). 전송 후 §1-4 단계로 비교할 것.

## 6. 뒤 세션이 하지 말아야 할 것 (이 세션의 제약을 이어받음)

- 추측한 원격 주소에 push, 새 저장소 생성
- 실제 예약·결제·계정 생성
- 공식 사이트에 자동 요청 반복 (테스트는 스텁으로)
- 비밀 값(API 키 등)을 저장소에 커밋
- 머지·운영 배포

## 7. 문서 체계에 남은 일

| 남은 일 | 담당 |
|---|---|
| `docs/index.html` (허브) · `docs/reader.html` (리더) 생성 | `design-doc-structure-validator` — **이 세션에 설치되어 있지 않다.** 현재 mockup 의 문서 복귀 링크는 규약대로 `../../reader.html?doc=...` 를 가리키지만 대상 파일이 없어, 대체로 여정 문서 직접 링크를 함께 넣어 두었다 |
| 디자인 시스템 토큰 정의 후 mockup `:root` 교체 | 디자인 담당 또는 뒤 세션 |
| 가치 소유자 지정 (D-08 고아 가치 🔴 해소) | 사용자 |
| 상태 추적 월 파일 갱신 | 다음 변경 때 `product/family-app-gym-recipes-doc-tracker/YYYY-MM.md` |
