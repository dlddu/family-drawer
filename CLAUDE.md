# 저장소 지침

가족용 앱 `family-drawer`. 1단계는 **문서 전용**이었고 2단계는 **저장소 초기화**까지다.
앱 코드는 아직 없다. 먼저 [`README.md`](README.md) → [`docs/README.md`](docs/README.md) →
[`docs/handoff/phase-2-bootstrap.md`](docs/handoff/phase-2-bootstrap.md) 순으로 읽는다.

## 지키는 것

- **미결정을 단정하지 않는다.** `docs/decisions/open-questions.md` 의 D-01~D-10 중
  특히 D-02(지원 OS)·D-03(가족 공유 인프라)는 사용자만 정한다. 프레임워크·언어·DB·배포 대상을
  고르는 변경은 그 결정을 인용할 수 있을 때만 한다.
- **1단계 문서 17개는 manifest(`docs/handoff/checksums.txt`)로 고정되어 있고, manifest 와 그
  문서는 docs 담당 소유다.** 그 파일들을 고치려면
  `python3 scripts/update_docs_checksums.py`(먼저 `--check`)로 manifest 를 다시 만들고,
  출력된 SHA-256 을 `scripts/verify_docs.py` 의 `HANDOFF_CHECKSUMS_SHA256` 에 옮겨 적은 뒤 그 옆
  이력 주석에 근거(PR·커밋)를 한 줄 남긴다. 과거 값은 감사용으로 지우지 않는다. 두 값을 함께
  고치는 것이 "문서를 바꾸기로 했다"는 명시적 기록이다.
- **부트스트랩이 더하는 문서는 `verify_docs.BOOTSTRAP_OWNED` 에 선언한다.** manifest 범위 밖으로
  빠져 docs 담당의 고정 해시를 흔들지 않는다. 그 밖의 새 문서는 자유롭게 더할 수 있고, 검증기가
  "manifest 에 없는 문서"로 알린다.
- **푸시 전에 검증을 돌린다.** `python3 scripts/verify_docs.py` — 의존성 설치가 필요 없다.
- **필수 체크는 `pr-gate` 하나다.** 체크를 더할 때는 job 을 만들고 `.github/workflows/pr.yml` 의
  `pr-gate.needs` 에 넣는다. 브랜치 보호(main ruleset) 설정은 건드리지 않는다.
- **통과만 하는 빈 테스트 job 을 두지 않는다.** PR 화면에서 "테스트 통과"로 잘못 읽힌다.
- **mockup 은 단일 정적 파일이다.** 외부 폰트·CDN·빌드를 넣지 않는다(`file://` 로 열려야 한다).
  단계를 고치면 여정 문서의 `STP-*` 와 순서까지 맞춘다 — 검증기가 대조한다.

## 하지 않는 것

- 실제 예약·결제·계정 생성·로그인, 공식 사이트(best.or.kr)로 자동 신청·반복 요청 (자동화 범위 0, D-01)
- 비밀 값(API 키 등) 커밋 — 필요해지면 보관 위치를 먼저 정한다(D-05)
- 머지·운영 배포, 다른 저장소(flux-cd-apps 등) 변경, Flux 등록·적용 — 별도 승인 범위
- 가족 구성원 수·명단을 가정한 설계 (역할 기준으로 쓴다, D-07)

## 다음 단계

D-02·D-03 이 닫히면 devops 플러그인의 `k3s-app-bootstrap` 스킬로 이미지 발행(`image.yml`)·
`deploy/` kustomize·e2e 를 이어서 깐다. 무엇이 왜 아직 없는지는
`docs/handoff/phase-2-bootstrap.md` §3 에 있다.
