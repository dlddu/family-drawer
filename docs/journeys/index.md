# 여정 mockup 인덱스

> 이 레포에는 mockup 인덱스 형식을 정하는 `design-doc-structure-validator` 가 아직 없다.
> 아래 표는 **임시 인덱스**다. validator 가 형식을 정하면 그 형식으로 옮긴다.
> mockup 단위 규칙: **여정 하나 = 페이지 하나** (`docs/journeys/<journey-id>/index.html`)

| 여정 식별자 | 달성 가치 | 담은 단계 | 담은 화면 (`data-screen`) | 디자인 시스템 | 공개 경로 |
|---|---|---|---|---|---|
| [`JRN-gym-reservation`](./JRN-gym-reservation/index.html) | `VAL-dont-miss-window` · `VAL-official-path-only` · `VAL-says-what-it-did` · `VAL-family-not-solo` · `VAL-findable-later` | `STP-notice-check` · `STP-pick-center` · `STP-prep-account` · `STP-official-apply` · `STP-record-result` · `STP-remind-next` | `home` · `center-list` · `center-detail` · `apply-prep` · `apply-prep-onsite` · `official-handoff` · `official-handoff-blocked` · `result-sheet` · `application-list` · `reminder-settings` | 없음 — **임의 무채색 스타일** | `journeys/JRN-gym-reservation/` |
| [`JRN-recipe-link-collect`](./JRN-recipe-link-collect/index.html) | `VAL-three-tap-keep` · `VAL-findable-later` · `VAL-says-what-it-did` · `VAL-family-not-solo` | `STP-share-from-youtube` · `STP-confirm-save` · `STP-browse-collection` · `STP-open-original` · `STP-fix-entry` | `external-youtube-app` · `os-share-sheet` · `share-receive` · `save-confirm` · `collection-list` · `recipe-detail` · `recipe-detail-actions` · `link-edit` · `delete-confirm-modal` | 없음 — **임의 무채색 스타일** | `journeys/JRN-recipe-link-collect/` |

## 검사 결과 (2026-11-25)

| mockup | 검사기 | 결과 |
|---|---|---|
| `JRN-gym-reservation` | `check_mockup.py` | 실패 0 · 경고 0 (단계 6개 일치 · 화면 10종 · 상태 18개 · 외부 의존 0) |
| `JRN-recipe-link-collect` | `check_mockup.py` | 실패 0 · 경고 0 (단계 5개 일치 · 화면 9종 · 상태 19개 · 외부 의존 0) |

화면 인벤토리와 **의도적 제외** 목록은 [`../handoff/bootstrap-requirements.md`](../handoff/bootstrap-requirements.md) §4 에 있다.

## 로컬에서 보는 방법

브라우저로 `index.html` 파일을 직접 열면 된다(`file://` 로도 동작한다 — 빌드·CDN·외부 폰트 없음).
딥링크: `index.html#STP-confirm-save` · 상태 딥링크: `index.html#STP-confirm-save/duplicate`
