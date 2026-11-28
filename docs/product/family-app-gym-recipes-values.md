# family-app-gym-recipes 제품 가치 문서

> 이 문서는 **최상위 문서**다. PRD·Acceptance Criteria·테스트·여정 문서는 모두 이 문서를 판단 기준으로 쓴다.
> 상태: **초안 (v0.4)** · 최종 수정일 2026-11-25

**본문은 제품 소유자와 최상위 가치 세 개(유형·설명)까지다.**
가치를 어떻게 판정하는지(하위 기준·제약), 지금 단계가 어디까지인지(대상 사용자·제품 목표·제품 범위),
v0.1 의 가치 6개가 어디로 갔는지(이동 표)는 **부록**에 있다 — 내용은 그대로 옮겼고 삭제한 것은 없다.

→ **부록**: [`family-app-gym-recipes-values-appendix.md`](./family-app-gym-recipes-values-appendix.md)
→ 사실 근거: [`docs/research/facility-and-link-findings.md`](../research/facility-and-link-findings.md)
→ 미결정 사항: [`docs/decisions/open-questions.md`](../decisions/open-questions.md)

---

## 제품 소유자

- **미지정 (사용자 확인 필요)** — 이 세션에서 소유자가 지정되지 않았다.
  product-doc-engineer 기준으로 이는 **고아 가치(orphan value)** 위험이며, 상태 추적 문서에 기록되어 있다.
  임시로 "요청한 가족 구성원"을 소유자로 가정하지 **않는다** (책임 소재를 문서가 지어내면 안 된다).
  → `open-questions.md` **D-08**

---

## 제품 가치

최상위 가치는 **세 개**이고, **① 사용자 편의성이 최우선**이다.
우선순위가 부딪힐 때의 판단과 "가치가 아니라 범위인 것"은 부록 [§D 가치 우선순위와 경계](./family-app-gym-recipes-values-appendix.md#d-가치-우선순위와-경계)에 있다.

### `VAL-least-effort` ① 가장 적은 손으로 끝낸다 (사용자 편의성 최우선)

- **유형**: 구체적
- **설명**: 같은 일을 하는 데 **누르는 횟수, 입력하는 글자 수, 다시 하는 횟수**를 최소로 만든다.
  특히 **실패한 뒤 처음부터 다시 입력하게 만들지 않는다** — 받은 내용·고른 값·쓴 메모는 실패해도 남아 있어야 한다.
  찾아 들어가는 수고도 편의에 포함한다: 주소를 외우거나 메뉴를 헤매지 않고 한 번에 목적지에 닿아야 한다.
  이 가치는 기능을 더하는 가치가 아니라 **단계를 덜어내는 가치**다.
- **상세 기준**: 하위 기준 ①-1~①-6 과 현 단계 기능 범위 경계 → 부록 [§E-1](./family-app-gym-recipes-values-appendix.md#e-1-val-least-effort--가장-적은-손으로-끝낸다)

### `VAL-obvious-to-everyone` ② 설명 없이도 다음 행동이 보인다 (직관적 UX)

- **유형**: 추상적
- **설명**: 나이가 많은 가족 구성원이 **아무 설명도 듣지 않고** 처음 열어도, ㉠ 지금 무슨 상태인지 ㉡ 다음에 무엇을 누르면 되는지
  ㉢ 누른 결과가 어떻게 됐는지를 화면만 보고 안다. 판정 기준은 "익숙한 말 / 눈에 띄는 글씨와 버튼 / 다음 행동과 결과" 셋이다.
- **상세 기준**: 하위 기준 ②-1~②-6 과 제약 ②-C1 → 부록 [§E-2](./family-app-gym-recipes-values-appendix.md#e-2-val-obvious-to-everyone--설명-없이도-다음-행동이-보인다)

### `VAL-diagnosable-without-the-user` ③ 사용자가 설명하지 않아도 진단된다

- **유형**: 추상적
- **설명**: 문제가 생겼을 때 **가족이 로그를 모으거나 "이게 안 돼요"를 반복 설명하지 않아도** 개발자가 재현·원인 파악에
  필요한 맥락을 얻는 것을 목표로 한다. 이상적으로는 **사용자가 문의하기 전에** 앱 쪽이 먼저 알아챈다.
  사용자가 해야 할 조작은 **최소**여야 한다. 진단에 자격증명과 가족의 개인 콘텐츠는 넣지 않는다.
- **상세 기준**: A군(1단계 AC 가 이미 만족시키는 것) · B군(기대 결과만 적고 1단계에서 구현·검증하지 않는 것, `AC-G11`·`AC-R11`) · 제약 ③-C1·③-C2 → 부록 [§E-3](./family-app-gym-recipes-values-appendix.md#e-3-val-diagnosable-without-the-user--사용자가-설명하지-않아도-진단된다)

---

## 연결 문서

| 문서 | 경로 |
|---|---|
| **부록 — 상세 기준·범위·이동 표** | [`family-app-gym-recipes-values-appendix.md`](./family-app-gym-recipes-values-appendix.md) |
| PRD — 헬스 수강신청 보조 | [`family-app-gym-recipes-prd-gym-reservation.md`](./family-app-gym-recipes-prd-gym-reservation.md) |
| PRD — 레시피 링크 보관함 | [`family-app-gym-recipes-prd-recipe-links.md`](./family-app-gym-recipes-prd-recipe-links.md) |
| 테스트 — 헬스 수강신청 보조 | [`family-app-gym-recipes-test-gym-reservation.md`](./family-app-gym-recipes-test-gym-reservation.md) |
| 테스트 — 레시피 링크 보관함 | [`family-app-gym-recipes-test-recipe-links.md`](./family-app-gym-recipes-test-recipe-links.md) |
| 여정 — 헬스 수강신청 | [`../user-journeys/JRN-gym-reservation.md`](../user-journeys/JRN-gym-reservation.md) |
| 여정 — 레시피 링크 모으기 | [`../user-journeys/JRN-recipe-link-collect.md`](../user-journeys/JRN-recipe-link-collect.md) |
| 문서 체계 상태 | [`family-app-gym-recipes-doc-tracker/index.md`](./family-app-gym-recipes-doc-tracker/index.md) |

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v0.1 | 2026-11-25 | 최초 작성. 가치 6개, 범위 정의, 소유자 미지정 위험 기록 |
| v0.2 | 2026-11-25 | 최상위 가치를 3개로 재정의(①편의성 ②직관적 UX ③사용자 조작 없는 진단). 기존 6개는 하위 기준·제약으로 이동(이동 표 추가). 진단 맥락의 **수집·전송 수단**을 범위 밖으로 명시. 요구·범위·기존 결정(D-01~D-10)과 AC·단계·테스트 식별자는 변경 없음 |
| v0.3 | 2026-11-25 | 원문 대조 후 두 곳 조정. ⑴ **공식 경로를 가치·제약에서 제거** — 현 단계 **기능 범위**로만 설명하고(①-6 범위 메모 + 「범위 밖」 표) **① 사용자 편의성이 최우선**임을 명시. 하위 기준 **①-6**(찾아 들어가는 수고 제거) 추가. ⑵ **③-B군에 향후 검증 가능한 기대 결과**를 적고 `AC-G11`·`AC-R11` 로 최소 연결 — 구현·운영·검증된 것으로 적지 않는다. 자동 예약·결제는 여전히 범위 밖, 새 SDK·개인정보 수집 결정 없음 |
| v0.4 | 2026-11-25 | **본문을 소유자 + 최상위 가치 3개(유형·설명)로 줄였다.** 대상 사용자·제품 목표·제품 범위·가치 우선순위·하위 기준·제약·가치↔요구 대응·가치 이동 표는 [부록](./family-app-gym-recipes-values-appendix.md)으로 옮겼다. **세 가치의 의미와 상세 기준은 그대로 보존** — 가치 ID·하위 기준 번호·제약·범위·근거·결정 변경 없음 |
