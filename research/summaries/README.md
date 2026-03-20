# 논문 요약본 (전체 42편)

> Container Orchestration Platform 개발을 위한 분야별 논문 요약 — 링크 포함

---

## 1. Container Orchestration (7편)

### BK21 우수 학회/저널

| # | 논문 | 저자 | 연도 | 게재지 | BK21 | 요약 | 링크 |
|---|------|------|:----:|--------|:----:|------|------|
| 1 | Custom Scheduling in Kubernetes: A Survey on Common Problems and Solution Approaches | Scheinecker et al. | 2022 | ACM Computing Surveys | 최우수 | K8s 커스텀 스케줄러 연구 동향 서베이. 스케줄링 문제 유형별(자원 최적화, 지연 시간, 에너지 효율) 솔루션을 분류하고 기본 스케줄러의 한계를 극복하는 확장 방법론 제시. | [링크](https://dl.acm.org/doi/full/10.1145/3544788) |
| 2 | Large-scale Cluster Management at Google with Borg | Verma et al. | 2015 | EuroSys | 우수 | Google Borg 아키텍처 최초 공개. K8s의 직접적 전신으로 Pod, Label, Service 등 핵심 개념의 원형을 제시. 수만 대 머신에서 수십만 개 Job을 관리하는 10년간의 운영 경험 공유. | [링크](https://dl.acm.org/doi/10.1145/2741948.2741964) |
| 3 | Omega: Flexible, Scalable Schedulers for Large Compute Clusters | Schwarzkopf et al. | 2013 | EuroSys (Best Student Paper) | 우수 | 공유 상태 기반 병렬 스케줄링 아키텍처 제안. 중앙집중식(Borg) vs 2-level(Mesos) vs 공유 상태(Omega) 스케줄링을 비교하고, 낙관적 동시성 제어를 클러스터 스케줄링에 적용. | [링크](https://dl.acm.org/doi/10.1145/2465351.2465386) |

### 비BK21

| # | 논문 | 저자 | 연도 | 게재지 | 요약 | 링크 |
|---|------|------|:----:|--------|------|------|
| 4 | Borg, Omega, and Kubernetes: Lessons Learned | Burns et al. | 2016 | ACM Queue | Borg→Omega→K8s 10년간의 교훈 정리. 선언적 API, 컨트롤 루프, 관심사 분리 등 핵심 설계 원칙을 체계화. | [링크](https://queue.acm.org/detail.cfm?id=2898444) |
| 5 | Container-based Cluster Orchestration Systems: A Taxonomy | Rodriguez, Buyya | 2019 | SPE (Wiley) | 오케스트레이션 시스템 분류 체계 제안. 배포, 스케줄링, 네트워킹, 스토리지 등 기능별 분류 프레임워크 제시. Docker Swarm, K8s, Mesos, Nomad 비교. | [링크](https://onlinelibrary.wiley.com/doi/10.1002/spe.2660) |
| 6 | Comprehensive Feature Comparison of Container Orchestration Frameworks | Truyen et al. | 2019 | Applied Sciences (MDPI) | Docker Swarm / K8s / Mesos 3대 프레임워크 기능 비교. 네트워킹, 스토리지, 보안, 서비스 디스커버리 카테고리별 상세 비교표 제공. | [링크](https://www.mdpi.com/2076-3417/9/5/931) |
| 7 | A Survey of Kubernetes Scheduling Algorithms | Zhong, Buyya | 2023 | JCC (Springer) | K8s 스케줄링 알고리즘 세대별 분류 (기본 → 확장 → ML 기반). 강화학습 기반 스케줄링, 이기종 클러스터 최적화 등 향후 연구 방향 제시. | [링크](https://link.springer.com/article/10.1186/s13677-023-00471-1) |

---

## 2. CI/CD Pipeline (7편)

### BK21 우수 학회/저널

| # | 논문 | 저자 | 연도 | 게재지 | BK21 | 요약 | 링크 |
|---|------|------|:----:|--------|:----:|------|------|
| 1 | Uncovering the Benefits and Challenges of Continuous Integration Practices | Gerosa et al. | 2021 | IEEE TSE | 최우수 | Fowler의 10가지 CI 핵심 실천 방법의 현대적 유효성을 실증 검증. CI 도입의 이점(빠른 피드백, 품질 향상)과 과제(테스트 유지보수 부담, 빌드 시간 증가)를 정량 분석. | [링크](https://ieeexplore.ieee.org/document/9374092/) |
| 2 | A Survey of DevOps Concepts and Challenges | Leite et al. | 2019 | ACM Computing Surveys | 최우수 | DevOps 개념적 지도(conceptual map) 개발. 자동화 도구와 핵심 개념 간 상관관계를 제시하고 엔지니어/관리자/연구자 관점의 과제를 체계적으로 조사. | [링크](https://dl.acm.org/doi/abs/10.1145/3359981) |
| 3 | An Empirical Study of Architecting for Continuous Delivery and Deployment | Shahin et al. | 2019 | EMSE | 우수 | 19개 조직 21명 실무자 심층 인터뷰 + 91명 설문 기반 실증 연구. 모놀리식 vs 마이크로서비스와 지속적 전달의 호환성을 분석. "작고 독립적인 배포 단위" 원칙이 핵심임을 입증. | [링크](https://link.springer.com/article/10.1007/s10664-018-9651-4) |

### 비BK21

| # | 논문 | 저자 | 연도 | 게재지 | 요약 | 링크 |
|---|------|------|:----:|--------|------|------|
| 4 | CI, Delivery and Deployment: A Systematic Review | Shahin et al. | 2017 | IEEE Access | CI/CD 분야 최초의 체계적 문헌 리뷰(SLR). 69편 논문을 분석하여 접근 방식, 도구, 과제를 분류. 가장 많이 인용되는 CI/CD 서베이 논문 중 하나. | [링크](https://ieeexplore.ieee.org/document/7884954/) |
| 5 | Accelerate: The Science of Lean Software and DevOps | Forsgren, Humble, Kim | 2018 | IT Revolution (서적) | DORA Metrics 4가지 핵심 지표(리드 타임, 배포 빈도, MTTR, 변경 실패율)를 정립. 소프트웨어 전달 성능과 조직 성과 간 인과관계를 입증. | [링크](https://itrevolution.com/product/accelerate/) |
| 6 | Continuous Delivery: Reliable Software Releases | Humble, Farley | 2010 | Addison-Wesley (서적) | "배포 파이프라인" 개념을 최초로 체계적으로 정의. 블루-그린 배포, 카나리 배포, 롤백 메커니즘의 실질적 가이드. 2011년 Jolt Award 수상, CI/CD 분야의 바이블. | [링크](https://www.amazon.com/Continuous-Delivery-Deployment-Automation-Addison-Wesley/dp/0321601912) |
| 7 | On Queueing Theory for Large-Scale CI/CD Pipelines Optimization | - | 2025 | arXiv (프리프린트) | 대기행렬 이론을 CI/CD 파이프라인 최적화에 최초 적용. M/M/c 모델로 파이프라인 리소스 할당 최적화 문제를 수학적 정식화. K8s CI/CD 러너 스케일링에 적용 가능. | [링크](https://arxiv.org/abs/2504.18705) |

---

## 3. Monitoring System (7편)

### BK21 우수 학회/저널

| # | 논문 | 저자 | 연도 | 게재지 | BK21 | 요약 | 링크 |
|---|------|------|:----:|--------|:----:|------|------|
| 1 | REPLICAWATCHER: Training-less Anomaly Detection in Containerized Microservices | - | 2024 | NDSS | 최우수 | 학습 없이 레플리카 비교만으로 이상 탐지하는 새로운 패러다임. Precision 91%, Recall 98% 달성. ML 기반 대비 학습 데이터 불필요한 경량 이상 탐지. | [링크](https://www.ndss-symposium.org/ndss-paper/replicawatcher-training-less-anomaly-detection-in-containerized-microservices/) |
| 2 | Enjoy Your Observability: An Industrial Survey of Microservice Tracing and Analysis | - | 2022 | EMSE | 우수 | 10개 기업 실무자 인터뷰 기반 추적/분석 현황 서베이. 관측성 3대 축(Logs, Metrics, Traces) 간 통합의 어려움을 실무 관점에서 분석. | [링크](https://link.springer.com/article/10.1007/s10664-021-10063-9) |

### 비BK21

| # | 논문 | 저자 | 연도 | 게재지 | 요약 | 링크 |
|---|------|------|:----:|--------|------|------|
| 3 | Dapper, a Large-Scale Distributed Systems Tracing Infrastructure | Sigelman et al. (Google) | 2010 | Google Tech Report | 분산 추적 시스템의 시초. OpenTelemetry, Zipkin, Jaeger 등 모든 현대 추적 시스템의 원형. Span, Trace, Annotation 개념을 정의하여 표준 어휘 확립. | [링크](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) |
| 4 | A Survey on Observability of Distributed Edge & Container-Based Microservices | - | 2022 | IEEE Access | 엣지/컨테이너 환경 관측성 포괄적 서베이. Logs, Metrics, Traces 3축 관측성 모델 체계적 정리. 컨테이너 환경 특유의 모니터링 과제 분류. | [링크](https://ieeexplore.ieee.org/document/9837035/) |
| 5 | Detecting and Localizing Anomalies in Container Clusters Using Markov Models | - | 2020 | Electronics (MDPI) | 계층적 HMM 기반 컨테이너 클러스터 이상 탐지. 클러스터→노드→컨테이너 순 계층적 추적 모델. 메트릭 시계열의 상태 전이 패턴 분석. | [링크](https://www.mdpi.com/2079-9292/9/1/64) |
| 6 | Anomaly Detection and Diagnosis for Container-Based Microservices | - | 2018 | ICA3PP (Springer) | 모니터링 + ML + 결함 주입을 통합한 이상 탐지 시스템. 성능 모니터링 데이터에서 자동으로 이상 감지 및 원인 진단 파이프라인. | [링크](https://link.springer.com/chapter/10.1007/978-3-030-05063-4_42) |
| 7 | Tracing and Metrics Design Patterns for Monitoring Cloud-native Applications | - | 2025 | arXiv (프리프린트) | 클라우드 네이티브 모니터링 디자인 패턴을 최초로 체계화. 추적/메트릭 설계 시 반복 패턴을 정리하여 재사용 가능한 가이드 제공. | [링크](https://arxiv.org/html/2510.02991v1) |

---

## 4. Auto-Scaling (7편)

### BK21 우수 학회/저널

| # | 논문 | 저자 | 연도 | 게재지 | BK21 | 요약 | 링크 |
|---|------|------|:----:|--------|:----:|------|------|
| 1 | Cost-Efficient Container Orchestration for Heterogeneous Resources | Zhong, Buyya et al. | 2020 | ACM TOIT | 우수 | 이기종 자원 환경에서의 비용 효율적 K8s 오케스트레이션. 클라우드/온프레미스 혼합 환경의 컨테이너 배치 및 스케일링 최적화. 비용 모델과 자원 활용률을 동시에 고려. | [링크](https://dl.acm.org/doi/10.1145/3378447) |

### 비BK21

| # | 논문 | 저자 | 연도 | 게재지 | 요약 | 링크 |
|---|------|------|:----:|--------|------|------|
| 2 | KOSMOS: Vertical and Horizontal Resource Autoscaling for Kubernetes | Baresi et al. | 2021 | ICSOC (Springer) | HPA + VPA 통합 하이브리드 오토스케일링 프레임워크. CPU 44% 절감 달성. 두 스케일링 방식의 충돌 문제 해결 조정 메커니즘 설계. | [링크](https://link.springer.com/chapter/10.1007/978-3-030-91431-8_59) |
| 3 | Machine Learning Based Auto-Scaling for Containerized Applications | Imdoukh et al. | 2020 | Neural Computing and Applications | LSTM 기반 워크로드 예측 활용 프로액티브 오토스케일링. 과거 메트릭으로 미래 부하를 예측하여 사전 스케일링. 리액티브 대비 응답 시간 및 자원 낭비 감소. | [링크](https://link.springer.com/article/10.1007/s00521-019-04507-z) |
| 4 | Proactive Autoscaling for Cloud-Native Applications Using ML | Marie-Magdelaine, Ahmed | 2020 | IEEE GLOBECOM | ML 기반 프로액티브 오토스케일링 파이프라인. 워크로드 패턴 분류 + 부하 예측 2단계 접근. K8s HPA의 반응형 한계를 극복하는 선제적 전략. | [링크](https://ieeexplore.ieee.org/document/9322147) |
| 5 | Cost-Efficient Container Auto-Scaling: A Four-Phase Approach | Sheganaku et al. | 2023 | FGCS (Elsevier) | 비용 최소화 4단계 오토스케일링: 워크로드 분석→자원 추정→스케일링 결정→비용 최적화. SLA 위반 없이 인프라 비용 최소화. | [링크](https://www.sciencedirect.com/science/article/abs/pii/S0167739X22002850) |
| 6 | Horizontal Pod Autoscaling in Kubernetes: An Experimental Analysis | Nguyen et al. | 2020 | Sensors (MDPI) | K8s HPA 동작의 실험적 분석. 스케일링 지연, 과/과소 프로비저닝 문제를 정량적 측정. HPA 파라미터 튜닝의 성능 영향 실험 검증. | [링크](https://www.mdpi.com/1424-8220/20/16/4621) |
| 7 | Auto-Scaling Techniques for Cloud-Native Applications: A Comprehensive Survey | - | 2024 | Sensors (MDPI) | 오토스케일링 기법 종합 서베이. 리액티브 vs 프로액티브 vs 하이브리드 비교. ML/DL 기반 최신 연구 동향 정리. | [링크](https://www.mdpi.com/1424-8220/24/17/5551) |

---

## 5. Self-Healing (7편)

### BK21 우수 학회/저널

| # | 논문 | 저자 | 연도 | 게재지 | BK21 | 요약 | 링크 |
|---|------|------|:----:|--------|:----:|------|------|
| 1 | Failure Diagnosis in Microservice Systems: A Comprehensive Survey | Zhang et al. | 2025 | ACM TOSEM | 최우수 | 98편 논문 분석 포괄적 서베이. 장애 진단 기법을 데이터 유형별(로그, 메트릭, 트레이스, 멀티모달) 4가지로 분류. 공개 데이터셋/툴킷/평가 메트릭 정리. | [링크](https://dl.acm.org/doi/10.1145/3715005) |
| 2 | Automating Chaos Experiments in Production | Basiri et al. | 2019 | ICSE-SEIP | 최우수 | Netflix 프로덕션 자동화 카오스 실험 프레임워크. 실험 정의→실행→결과 분석 자동화. 카오스 엔지니어링을 CI/CD 파이프라인에 통합하는 방향성 제시. | [링크](https://dl.acm.org/doi/10.1109/ICSE-SEIP.2019.00012) |
| 3 | Large-scale Cluster Management at Google with Borg | Verma et al. | 2015 | EuroSys | 우수 | Borg의 장애 복구 메커니즘과 Self-Healing 설계 원칙. 선언적 작업 명세, 조정 루프 기반 자동 복구 아키텍처. 상관 장애 방지 스케줄링. | [링크](https://dl.acm.org/doi/10.1145/2741948.2741964) |

### 비BK21

| # | 논문 | 저자 | 연도 | 게재지 | 요약 | 링크 |
|---|------|------|:----:|--------|------|------|
| 4 | Chaos Engineering | Basiri et al. | 2016 | IEEE Software | 카오스 엔지니어링의 개념과 원칙을 학술적으로 정의한 최초의 논문. Netflix Chaos Monkey 등 실제 적용 사례를 통한 실증적 효과 검증. 이후 분야 전체의 이론적 토대. | [링크](https://dl.acm.org/doi/abs/10.1109/MS.2016.60) |
| 5 | Borg, Omega, and Kubernetes: Lessons Learned | Burns et al. | 2016 | Communications of ACM | Self-Healing 관점에서의 10년 진화. 선언적 구성 + 조정 루프 기반 자기 치유 아키텍처의 이론적 기반 확립. | [링크](https://dl.acm.org/doi/10.1145/2890784) |
| 6 | AI-Driven Self-Healing Container Orchestration Framework | - | 2025 | EmergingPub | AI/ML 기반 예측적 장애 감지 + 실시간 이상 탐지 결합 Self-Healing 프레임워크. 에너지 효율성과 장애 내성을 동시 최적화. 반응적→능동적 Self-Healing 전환. | - |
| 7 | Self-Healing vs Inherent Fault Tolerance | - | 2024 | ResearchGate | K8s Self-Healing vs Serverless 내재적 장애 내성 실증 비교. Pod 자동 재시작, Health Probe, 자동 스케일링 기능을 정량적 측정. 워크로드별 플랫폼 선택 기준 제시. | - |

---

## 6. AIOps (7편)

### BK21 우수 학회/저널

| # | 논문 | 저자 | 연도 | 게재지 | BK21 | 요약 | 링크 |
|---|------|------|:----:|--------|:----:|------|------|
| 1 | A Survey of AIOps in the Era of Large Language Models | - | 2025 | ACM Computing Surveys | 최우수 | LLM 시대 AIOps 대규모 서베이 — 183편 논문 분석. 전통적 AIOps(ML/DL)에서 LLM 기반으로의 패러다임 전환 정리. 멀티 에이전트, RAG 기반 운영 지식 활용 등 향후 연구 방향 제시. | [링크](https://arxiv.org/abs/2507.12472) |
| 2 | RCACopilot: Automatic Root Cause Analysis via LLMs | Chen et al. (Microsoft) | 2024 | EuroSys | 우수 | LLM 기반 자동 근본 원인 분석 시스템. Microsoft 프로덕션 환경에서 실전 검증. 인시던트 로그/메트릭/알림을 LLM에 제공하여 자동 추론. 규칙/ML 기반 RCA 대비 정확도 향상. | [링크](https://arxiv.org/abs/2305.15778) |
| 3 | A Survey of AIOps Methods for Failure Management | Notaro, Cardoso, Gerndt | 2021 | ACM TIST | 우수 | AIOps 장애 관리 체계적 서베이. 장애 예측→탐지→진단→복구 4단계 프레임워크. ML/DL 기법 적용 현황과 주요 과제(데이터 품질, 레이블 부족, 설명 가능성) 식별. | [링크](https://dl.acm.org/doi/10.1145/3483424) |

### 비BK21

| # | 논문 | 저자 | 연도 | 게재지 | 요약 | 링크 |
|---|------|------|:----:|--------|------|------|
| 4 | AIOps on Cloud Platforms: Reviews, Opportunities and Challenges | Cheng et al. (Salesforce) | 2023 | arXiv (프리프린트) | 클라우드 AIOps 전체 파이프라인 종합 리뷰. 이상 탐지, 장애 예측, RCA, 자동 복구 등 주요 태스크 분류. 산업 관점의 과제와 기회 제시. | [링크](https://arxiv.org/abs/2304.04661) |
| 5 | MOYA: Engineering LLM Powered Multi-agent Framework for Autonomous CloudOps | Parthasarathy et al. | 2025 | CAIN (Best Paper 후보) | LLM 기반 멀티 에이전트 CloudOps 프레임워크. 여러 AI 에이전트가 협력하여 인프라를 자율 운영. 인시던트 대응, 용량 계획, 배포 관리 등을 에이전트에 위임. | [링크](https://arxiv.org/abs/2501.08243) |
| 6 | KubeIntellect: LLM-Orchestrated Agent Framework for Kubernetes | Ardebili, Bartolini | 2025 | arXiv (프리프린트) | LLM 기반 K8s 관리 에이전트 프레임워크. 자연어 명령으로 클러스터 관리. kubectl 명령 생성, 장애 진단, 자원 최적화를 LLM이 자율 수행. | [링크](https://arxiv.org/abs/2509.02449) |
| 7 | AIOps Solutions for Incident Management | - | 2024 | arXiv (프리프린트) | 인시던트 라이프사이클(탐지→분류→진단→해결→사후분석)별 AIOps 기법 정리. 실무 적용 기술 선택 가이드라인 제시. | [링크](https://arxiv.org/html/2404.01363v1) |

---

## 통계 요약

| 분야 | BK21 최우수 | BK21 우수 | 비BK21 | 합계 |
|------|:-----------:|:---------:|:------:|:----:|
| Container Orchestration | 1 | 2 | 4 | 7 |
| CI/CD Pipeline | 2 | 1 | 4 | 7 |
| Monitoring System | 1 | 1 | 5 | 7 |
| Auto-Scaling | - | 1 | 6 | 7 |
| Self-Healing | 2 | 1 | 4 | 7 |
| AIOps | 1 | 2 | 4 | 7 |
| **합계** | **7** | **8** | **27** | **42** |
