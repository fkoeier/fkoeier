# 김혜원

백엔드를 공부하고 있습니다. 주문처럼 두 번 실행되거나 중간에 실패하면 안 되는 요청을 다루는 데 관심이 많습니다.

[이메일](mailto:myjxjx1@naver.com) · [SSOK AI 서버 저장소](https://github.com/200ok-Hongik/200ok-AI)

<br>

## StockClaw

텔레그램으로 승인받아 국내 주식을 주문하는 자동매매 서버\
2026.04 ~ 2026.10 · 비공개 저장소

투자 조건을 등록하면 장중에 서버가 조건을 감시하고, 조건이 맞으면 텔레그램으로 승인을 받아 한국투자증권 OpenAPI로 주문합니다. 조건부 주문과 주문 파이프라인, 승인 흐름, KIS API 연동을 맡았습니다.

- `/조건부주문` 구현: 자연어나 명령어로 받은 조건을 투자 룰로 저장하고, 조건이 맞으면 텔레그램 승인 → 주문 실행까지 연결
- 응답이 타임아웃된 주문은 '확인 불가'로 남기고, 다시 제출하기 전에 KIS 주문 조회로 접수 여부를 확인 (중복 주문 방지)
- 승인 대기 주문은 Redis에 5분 TTL로 저장, 승인 연타와 반복 발동은 Redis `SET NX` 락으로 차단
- 가격제한폭(±30%) 검증을 주문 실행 함수로 모아 수동·자동 주문에 함께 적용, 거절된 주문도 사유와 함께 기록
- KIS 호출에 서킷 브레이커와 재시도 적용, 실전 계좌 초당 20건 제한에 맞춰 호출 간격 조절

`Python` `FastAPI` `PostgreSQL` `Redis` `APScheduler` `Telegram Bot API`

<br>

## SSOK

사진 한 장으로 분리배출 방법을 알려 주는 서비스\
2026.03 ~ 진행 중 · 홍익대학교 졸업 프로젝트 · [AI 서버 저장소](https://github.com/200ok-Hongik/200ok-AI)

물건을 찍으면 품목과 상태를 분석하고, 지역별 배출 규칙과 연결해 버리는 방법을 알려 줍니다. Spring Boot 백엔드가 호출하는 Python AI 서버를 맡았습니다.

- YOLOv8로 물체 위치와 품목을 찾고 GPT Vision으로 내용물·라벨 상태를 판단, 물체별 `itemCode` `states` `bbox` JSON 응답 설계
- 페트병을 투명/유색 2개 클래스로 다시 학습하고, 학습 스크립트를 품목 통합 모델 구조로 정리
- GPT에 보내는 이미지 크기와 출력 JSON을 줄여 응답 시간 단축
- main에 머지하면 EC2로 자동 배포되도록 GitHub Actions 구성

`Python` `FastAPI` `YOLOv8` `OpenAI API` `Docker` `AWS EC2` `GitHub Actions`

<br>

## 기술

- Backend: Python, FastAPI, Java, Spring Boot
- Data: PostgreSQL, MySQL, Redis
- AI: YOLOv8, OpenAI GPT Vision
- Infra: Docker, AWS EC2, GitHub Actions

## 연락처

myjxjx1@naver.com

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fkoeier/fkoeier/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fkoeier/fkoeier/output/github-snake.svg">
  <img alt="GitHub 기여 그래프의 칸을 따라 뱀이 지나가며 기여 기록을 먹는 애니메이션" src="https://raw.githubusercontent.com/fkoeier/fkoeier/output/github-snake.svg">
</picture>
