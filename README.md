# 김혜원

외부 API와 연결된 서버에서 요청이 실패하거나 겹쳐도 상태가 꼬이지 않게 만드는 일에 관심이 있는 백엔드 개발자입니다.

[이메일](mailto:myjxjx1@naver.com) · [SSOK AI 서버 저장소](https://github.com/200ok-Hongik/200ok-AI)

<br>

## StockClaw

텔레그램 승인 기반 국내 주식 자동매매 백엔드\
2026.04 – 2026.10 · 한이음 ICT 멘토링 팀 프로젝트 · 저장소 비공개

텔레그램으로 등록한 투자 조건을 서버가 감시하다가, 조건이 맞으면 사용자 승인을 받아 한국투자증권(KIS) OpenAPI로 주문하는 서비스입니다. 저는 주문 실행과 승인 흐름, 증권 API 연동을 맡았습니다.

- **주문 승인 흐름**: 조건이 충족되면 텔레그램으로 승인 카드를 보내고, 승인하면 주문, 거절하거나 5분 동안 응답이 없으면 만료되게 했습니다. 승인 대기 주문은 TTL과 함께 Redis에 저장해 서버가 재시작돼도 사라지지 않습니다.
- **중복 주문 방지**: Redis `SET NX` 실행 락으로 같은 주문이 두 번 실행되는 것을 막고, 주문 응답이 타임아웃되면 증권사 주문 내역을 다시 조회한 뒤 재주문 여부를 정합니다.
- **증권 API 안정화**: KIS 호출에 서킷 브레이커, 지수 백오프와 지터를 둔 재시도, 실전·모의 계좌별 호출 간격 제한을 적용했습니다.
- 미체결 주문 취소, 체결 알림, 비상정지 시 승인 대기 주문 정리를 구현했습니다.

`Python` `FastAPI` `PostgreSQL` `Redis` `APScheduler` `Telegram Bot API`

<br>

## SSOK

사진 한 장으로 분리배출 방법을 알려 주는 서비스\
2026.03 – 진행 중 · 홍익대학교 졸업 프로젝트 · [AI 서버 저장소](https://github.com/200ok-Hongik/200ok-AI)

버리려는 물건을 찍으면 품목과 상태를 분석하고, 지역별 배출 규칙과 연결해 버리는 방법을 안내합니다. 저는 Spring Boot 백엔드가 호출하는 Python AI 서버를 맡았습니다.

- **판정 파이프라인**: YOLOv8로 물체 위치와 품목을 찾고, GPT Vision으로 내용물·라벨 같은 상태를 판단해 물체별 `itemCode` · `states` · `bbox` JSON으로 돌려줍니다. 백엔드가 이 값으로 배출 규칙을 조회할 수 있게 응답 형식을 정했습니다.
- **YOLO 학습**: 페트병을 투명·유색 2개 클래스로 다시 학습하고, 학습 스크립트를 품목 통합 모델 구조로 정리했습니다.
- **응답 속도와 배포**: GPT로 보내는 이미지 크기와 출력 JSON을 줄여 응답 시간을 단축했고, main에 머지하면 EC2로 자동 배포되도록 GitHub Actions를 구성했습니다.

`Python` `FastAPI` `YOLOv8` `OpenAI API` `Docker` `AWS EC2` `GitHub Actions`

<br>

## 기술

- **Backend**: Python, FastAPI, Java, Spring Boot
- **Data**: PostgreSQL, MySQL, Redis
- **AI**: YOLOv8, OpenAI GPT Vision
- **Infra**: Docker, AWS EC2, GitHub Actions

## 연락처

myjxjx1@naver.com

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fkoeier/fkoeier/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fkoeier/fkoeier/output/github-snake.svg">
  <img alt="GitHub 기여 그래프의 칸을 따라 뱀이 지나가며 기여 기록을 먹는 애니메이션" src="https://raw.githubusercontent.com/fkoeier/fkoeier/output/github-snake.svg">
</picture>
