# Monitoring System 관련 논문 조사

> 컨테이너/마이크로서비스 모니터링, 분산 추적, 이상 탐지, 관측성(Observability)에 관한 논문 정리

---

## BK21 우수 학회/저널 논문

### 1. REPLICAWATCHER: Training-less Anomaly Detection in Containerized Microservices

| 항목 | 내용 |
|------|------|
| **저자** | (NDSS 2024 논문) |
| **연도** | 2024 |
| **게재지** | **NDSS (Network and Distributed System Security Symposium)** |
| **BK21 등급** | **최우수급 학회** (보안/시스템 분야 4대 학회) |

**주요 기여:**
- 학습(Training) 없이 레플리카 비교만으로 이상 탐지하는 새로운 패러다임 제시
- Precision 91%, Recall 98% 달성
- 컨테이너 환경의 레플리카 특성을 활용한 경량 이상 탐지 — 기존 ML 기반 대비 학습 데이터 불필요
- 마이크로서비스 환경에서 실시간 장애 감지 가능성을 크게 확장

---

### 2. Enjoy Your Observability: An Industrial Survey of Microservice Tracing and Analysis

| 항목 | 내용 |
|------|------|
| **저자** | (산업 현장 인터뷰 기반) |
| **연도** | 2022 |
| **게재지** | **Empirical Software Engineering (EMSE)** |
| **BK21 등급** | **우수급 저널** (소프트웨어공학 실증 연구 분야) |
| **DOI** | 10.1007/s10664-021-10063-9 |

**주요 기여:**
- 10개 기업 실무자 인터뷰 기반 산업 현장의 추적(Tracing)/분석 현황 서베이
- 분산 추적 도구 도입의 실질적 이점과 과제를 실증적으로 규명
- 관측성(Observability)의 3대 축(Logs, Metrics, Traces) 간 통합의 어려움을 실무 관점에서 분석

---

## 비BK21 논문 (기타 저널/보고서/프리프린트)

### 3. Dapper, a Large-Scale Distributed Systems Tracing Infrastructure

| 항목 | 내용 |
|------|------|
| **저자** | Benjamin H. Sigelman et al. (Google) |
| **연도** | 2010 |
| **게재지** | Google Technical Report |
| **분류** | 기업 기술 보고서 (학술 학회 미게재) |

**주요 기여:**
- 분산 추적 시스템의 시초 — OpenTelemetry, Zipkin, Jaeger 등 모든 현대 추적 시스템의 원형
- Span, Trace, Annotation 개념을 정의하여 분산 시스템 관측의 표준 어휘를 확립
- Google 내부 프로덕션 환경에서 운영된 실전 검증 시스템
- 분산 추적 분야에서 가장 많이 인용되는 논문 중 하나

---

### 4. A Survey on Observability of Distributed Edge & Container-Based Microservices

| 항목 | 내용 |
|------|------|
| **저자** | (IEEE Access 서베이) |
| **연도** | 2022 |
| **게재지** | IEEE Access |
| **분류** | 오픈액세스 저널 (BK21 미포함) |
| **DOI** | 10.1109/ACCESS.2022.3189135 |

**주요 기여:**
- 엣지/컨테이너 환경 관측성에 대한 포괄적 서베이
- Logs, Metrics, Traces 3축 관측성 모델을 체계적으로 정리
- 컨테이너 환경 특유의 모니터링 과제(동적 스케일링, 짧은 생명주기)를 분류

---

### 5. Detecting and Localizing Anomalies in Container Clusters Using Markov Models

| 항목 | 내용 |
|------|------|
| **저자** | (HMM 기반 이상 탐지 연구) |
| **연도** | 2020 |
| **게재지** | Electronics (MDPI), Vol. 9, No. 1 |
| **분류** | MDPI 저널 (BK21 미포함) |

**주요 기여:**
- 계층적 HMM(Hidden Markov Model) 기반 컨테이너 클러스터 이상 탐지 및 위치 특정
- 클러스터 → 노드 → 컨테이너 순으로 이상 원인을 계층적으로 추적하는 모델 제안
- 컨테이너 메트릭 시계열 데이터의 상태 전이 패턴 분석

---

### 6. Anomaly Detection and Diagnosis for Container-Based Microservices with Performance Monitoring

| 항목 | 내용 |
|------|------|
| **저자** | (ICA3PP 2018 논문) |
| **연도** | 2018 |
| **게재지** | ICA3PP (International Conference on Algorithms and Architectures for Parallel Processing) / Springer |
| **분류** | 일반 국제 학회 (BK21 미포함) |

**주요 기여:**
- 모니터링 + ML + 결함 주입(Fault Injection)을 통합한 이상 탐지 시스템 제안
- 성능 모니터링 데이터에서 자동으로 이상을 감지하고 원인을 진단하는 파이프라인 구축
- 컨테이너 기반 마이크로서비스 환경에 특화된 진단 프레임워크

---

### 7. Tracing and Metrics Design Patterns for Monitoring Cloud-native Applications

| 항목 | 내용 |
|------|------|
| **저자** | (arXiv 프리프린트) |
| **연도** | 2025 |
| **게재지** | arXiv (Preprint, arXiv:2510.02991) |
| **분류** | 프리프린트 (미출판) |

**주요 기여:**
- 클라우드 네이티브 모니터링 디자인 패턴을 최초로 체계화
- 추적(Tracing)과 메트릭(Metrics) 설계 시 반복적으로 나타나는 패턴을 정리하여 재사용 가능한 가이드 제공

---

## 요약

| 구분 | 논문 수 | 게재지 |
|------|---------|--------|
| **BK21 최우수급** | 1편 | NDSS |
| **BK21 우수급** | 1편 | EMSE |
| **비BK21** | 5편 | Google Tech Report, IEEE Access, MDPI Electronics, ICA3PP, arXiv |

## 참고 링크

- [REPLICAWATCHER - NDSS 2024](https://www.ndss-symposium.org/ndss-paper/replicawatcher-training-less-anomaly-detection-in-containerized-microservices/)
- [Enjoy Your Observability - EMSE](https://link.springer.com/article/10.1007/s10664-021-10063-9)
- [Dapper - Google Research](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/)
- [Observability Survey - IEEE Access](https://ieeexplore.ieee.org/document/9837035/)
- [HMM Anomaly Detection - MDPI](https://www.mdpi.com/2079-9292/9/1/64)
- [Container Anomaly Detection - ICA3PP](https://link.springer.com/chapter/10.1007/978-3-030-05063-4_42)
- [Tracing Design Patterns - arXiv](https://arxiv.org/html/2510.02991v1)
