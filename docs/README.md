# family-app-gym-recipes — 1단계 제품 문서

가족용 앱의 **1단계 제품 문서 묶음**이다. 이 단계는 **문서 전용**이며 앱 코드 구현·부트스트랩은 뒤의 별도 세션이 맡는다.

다루는 두 요구:
1. **부천도시공사 헬스장 신청** — 확인해 보니 실제 체계는 시간 단위 "예약"이 아니라 월 단위 **수강신청/회원등록**이다 (근거 문서 A-1-4)
2. **유튜브 앱 공유로 받은 링크를 엄마의 요리 레시피로 모아 다시 열기**

> ⚠️ 이 문서들은 **초안**이다. 사용자 결정이 필요한 10개 항목은 [`decisions/open-questions.md`](./decisions/open-questions.md) 에 분리해 두었고,
> 확정된 사실과 가정은 [`research/facility-and-link-findings.md`](./research/facility-and-link-findings.md) 에서 `[확인]`/`[가정]` 으로 구분했다.
> 이 세션에서 **실제 예약·결제·계정 생성·로그인은 수행하지 않았다.**

---

## 읽는 순서

| # | 문서 | 무엇이 들어 있나 |
|---|---|---|
| 1 | [`research/facility-and-link-findings.md`](./research/facility-and-link-findings.md) | 사실 근거. 시설·인증·공식 예약 경로·자동화 가능 범위, YouTube 링크 형태. **확인/가정 구분 + 출처 URL + 확인일** |
| 2 | [`product/family-app-gym-recipes-values.md`](./product/family-app-gym-recipes-values.md) | **최상위 문서.** 제품 목표·범위(안/밖)·**최상위 가치 3개**(편의성·직관적 UX·사용자 조작 없는 진단)와 하위 기준·제약, 가족 역할 정의 |
| 3 | [`user-journeys/JRN-gym-reservation.md`](./user-journeys/JRN-gym-reservation.md) | 여정 ① 헬스 수강신청 (6단계, 분기 9건) |
| 4 | [`user-journeys/JRN-recipe-link-collect.md`](./user-journeys/JRN-recipe-link-collect.md) | 여정 ② 레시피 링크 모으기 (5단계, 분기 11건) |
| 5 | [`product/family-app-gym-recipes-prd-gym-reservation.md`](./product/family-app-gym-recipes-prd-gym-reservation.md) | PRD ① + AC-G1~G10 (테스트 가능한 수용 기준) |
| 6 | [`product/family-app-gym-recipes-prd-recipe-links.md`](./product/family-app-gym-recipes-prd-recipe-links.md) | PRD ② + AC-R1~R10 + **사용자가 보는 피드백 문구표 10행** |
| 7 | [`product/family-app-gym-recipes-test-gym-reservation.md`](./product/family-app-gym-recipes-test-gym-reservation.md) | 테스트 시나리오 ① TC-G1~G10 (13개) |
| 8 | [`product/family-app-gym-recipes-test-recipe-links.md`](./product/family-app-gym-recipes-test-recipe-links.md) | 테스트 시나리오 ② TC-R1~R10 (12개, 링크 정규화 12행·오류 7행 데이터 주도) |
| 9 | [`journeys/index.md`](./journeys/index.md) | 여정 mockup 인덱스 + 검사 결과 |
| 10 | [`decisions/open-questions.md`](./decisions/open-questions.md) | 미결정 D-01~D-10. 각 항목의 임시 처리와 "정하는 데 필요한 것" |
| 11 | [`handoff/bootstrap-requirements.md`](./handoff/bootstrap-requirements.md) | 뒤 세션 인계: 문서 받는 절차, 최소 부트스트랩 요구, 화면 인벤토리, 의도적 제외 |
| 12 | [`product/family-app-gym-recipes-doc-tracker/index.md`](./product/family-app-gym-recipes-doc-tracker/index.md) | 문서 체계 상태 추적 (연결 매트릭스·위험 진단) |

### 눌러볼 수 있는 mockup

- [`journeys/JRN-gym-reservation/index.html`](./journeys/JRN-gym-reservation/index.html) — 6단계 · 화면 10종 · 상태 18개
- [`journeys/JRN-recipe-link-collect/index.html`](./journeys/JRN-recipe-link-collect/index.html) — 5단계 · 화면 9종 · 상태 19개

브라우저로 파일을 직접 열면 동작한다 (`file://` OK — 빌드·CDN·외부 폰트 없음).

---

## 문서 연결 구조

```
사실 근거 (research/)                     ← 모든 "확인" 주장의 출처
   │
   ▼
가치 문서 (values)  ──── VAL-* ─────┐
   │                                │
   ├─► 여정 (JRN-*, STP-*) ─────────┤     ← 여정은 가치를 달성하는 흐름
   │        │                       │
   │        └─► mockup (data-step / data-screen / data-state)
   │                                │
   └─► PRD ──► AC-G*/AC-R* ─────────┘     ← AC 는 가치를 달성한다고 명시
              │
              └─► 테스트 (TC-G*/TC-R*)    ← 테스트는 AC 를 검증한다
```

현재 끊어진 화살표는 **없다**. 다만 ① 가치 소유자가 미지정이라 "고아 가치" 위험이 열려 있고(D-08),
② 가치 ③의 **B군 하위 기준**(상관 ID·오류율·반복 실패 감지)은 1단계 PRD 에 AC 가 없다 — 둘 다 상태 추적 문서에 기록돼 있다.

## 핵심 설계 결정 두 가지

1. **자동 예약은 1단계 범위 밖이다 (범위 0).**
   공식 API 근거를 찾지 못했고 약관의 자동화 조항을 확인하지 못했다. `robots.txt` 가 `Allow: /` 인 것은 공개 페이지 크롤링 규칙일 뿐 **로그인 후 신청 자동화 허가가 아니다.**
   앱은 ①접수 기간 알림 ②사전 준비 체크 ③공식 경로 딥링크 ④결과 수동 기록까지만 한다. 바꾸려면 운영기관 확인(D-01)이 먼저다.

2. **지원 OS·인프라는 확정하지 않았다.**
   플랫폼 의존 AC 는 OS 중립 문장으로 쓰고 `[OS 결정 대기]` 로 표시했다. 가족 공유는 1단계에서 "로컬 + 내보내기"로 축소했고, 그 한계를 화면 문구로 드러내게 설계했다 (D-02, D-03, D-04).

## 저장 위치

이 문서 묶음은 **로컬 작업 디렉터리에만** 있다. 사용자가 이미 만든 저장소의 주소가 확인되지 않아 원격에 쓰지 않았고, 새 저장소도 만들지 않았으며 git 초기화도 하지 않았다.
주소가 오면 [`handoff/bootstrap-requirements.md`](./handoff/bootstrap-requirements.md) §1 절차대로 옮기고 [`handoff/checksums.txt`](./handoff/checksums.txt) 로 검증한다.
