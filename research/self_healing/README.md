# Self-Healing Systems 관련 논문 조사

> 컨테이너/클라우드 환경의 자기 치유(Self-Healing), 장애 내성(Fault Tolerance), 카오스 엔지니어링에 관한 논문 정리

---

## BK21 우수 학회/저널 논문

### 1. Failure Diagnosis in Microservice Systems: A Comprehensive Survey and Analysis

| 항목 | 내용 |
|------|------|
| **저자** | Shenglin Zhang, Sibo Xia, Wenzhao Fan, Binpeng Shi, Xiao Xiong, Zhenyu Zhong, Minghua Ma, Yongqian Sun, Dan Pei |
| **연도** | 2024 / 2025 |
| **게재지** | **ACM Transactions on Software Engineering and Methodology (TOSEM)** |
| **BK21 등급** | **최우수급 저널** (소프트웨어공학 분야 최상위) |
| **arXiv** | 2407.01710 |

**주요 기여:**
- 2003년부터 현재까지 98편의 관련 논문을 체계적으로 분석한 포괄적 서베이
- 장애 진단 기법을 사용 데이터 유형(로그, 메트릭, 트레이스, 멀티모달)에 따라 4가지로 분류
- 장애 감지(detection) → 근본 원인 분석(RCA) → 장애 예측(prediction) 파이프라인 정리
- 공개 데이터셋, 툴킷, 평가 메트릭을 종합 정리하여 실무 적용 가이드 제공

---

### 2. Automating Chaos Experiments in Production

| 항목 | 내용 |
|------|------|
| **저자** | Ali Basiri, Niosha Behnam, Ruud de Rooij, Lorin Hochstein, Luke Kosewski, Justin Reynolds, Casey Rosenthal |
| **연도** | 2019 |
| **게재지** | **ICSE-SEIP '19 (International Conference on Software Engineering: Software Engineering in Practice)** |
| **BK21 등급** | **최우수급 학회** (소프트웨어공학 분야 최상위, ICSE) |

**주요 기여:**
- Netflix 프로덕션 환경에서의 자동화된 카오스 실험 프레임워크 설계 및 구현
- 카오스 실험을 CI/CD 파이프라인에 통합하는 방향성 제시
- 실험 정의 → 실행 → 결과 분석을 자동화하여 대규모 분산 시스템의 복원력을 지속적으로 검증

---

### 3. Large-scale Cluster Management at Google with Borg

| 항목 | 내용 |
|------|------|
| **저자** | Abhishek Verma, Luis Pedrosa, Madhukar R. Korupolu, David Oppenheimer, Eric Tune, John Wilkes |
| **연도** | 2015 |
| **게재지** | **EuroSys '15 (European Conference on Computer Systems)** |
| **BK21 등급** | **우수급 학회** (시스템 분야) |

**주요 기여:**
- Google Borg의 장애 복구 메커니즘과 Self-Healing 설계 원칙 공개
- 장애 복구 시간을 최소화하는 런타임 기능 및 상관 장애(correlated failures) 방지 스케줄링
- 선언적 작업 명세, 조정 루프(reconciliation loop) 기반 자동 복구 아키텍처
- *(Container Orchestration 분야와 중복 — Self-Healing 관점에서 재분석)*

---

## 비BK21 논문 (기타 저널/매거진/프리프린트)

### 4. Chaos Engineering

| 항목 | 내용 |
|------|------|
| **저자** | Ali Basiri, Niosha Behnam, Ruud de Rooij, Lorin Hochstein, Luke Kosewski, Justin Reynolds, Casey Rosenthal |
| **연도** | 2016 |
| **게재지** | IEEE Software, Vol. 33, No. 3, pp. 35-41 |
| **분류** | 일반 저널 (BK21 미포함) |

**주요 기여:**
- 카오스 엔지니어링의 개념과 원칙을 학술적으로 정의한 최초의 논문
- 분산 시스템의 정상 상태(steady state) 가설을 검증하는 실험 방법론 제시
- Netflix Chaos Monkey, Chaos Kong 등 실제 적용 사례를 통한 실증적 효과 검증
- 이후 카오스 엔지니어링 분야 전체의 이론적 토대

---

### 5. Borg, Omega, and Kubernetes: Lessons Learned from Three Container-Management Systems

| 항목 | 내용 |
|------|------|
| **저자** | Brendan Burns, Brian Grant, David Oppenheimer, Eric Brewer, John Wilkes |
| **연도** | 2016 |
| **게재지** | Communications of the ACM, Vol. 59, No. 5 |
| **분류** | ACM 매거진 (학술 학회/저널이 아닌 실무 매거진) |

**주요 기여:**
- Borg → Omega → Kubernetes 10년 진화 과정에서의 Self-Healing 설계 원칙 정리
- 선언적 구성(declarative configuration)과 조정 루프(reconciliation loop) 기반 자기 치유 아키텍처의 이론적 기반 확립
- 컨테이너를 관리의 기본 단위로 사용하는 패러다임 제시

---

### 6. AI-Driven Self-Healing Container Orchestration Framework for Energy-Efficient Kubernetes Clusters

| 항목 | 내용 |
|------|------|
| **저자** | (ResearchGate/EmergingPub 게재) |
| **연도** | 2025 |
| **게재지** | Scholarly Review (EmergingPub) |
| **분류** | 비주류 저널 (BK21 미포함) |

**주요 기여:**
- AI/ML 기반 예측적 장애 감지(predictive fault detection) + 실시간 이상 탐지를 결합한 Self-Healing 프레임워크 제안
- 에너지 효율성과 장애 내성을 동시에 최적화하는 다목적 접근법
- 반응적(reactive) → 능동적(proactive) Self-Healing으로의 패러다임 전환 시도

---

### 7. Self-Healing vs Inherent Fault Tolerance: A Resilience Study of Kubernetes and Serverless

| 항목 | 내용 |
|------|------|
| **저자** | (ResearchGate 게재) |
| **연도** | 2024 |
| **게재지** | ResearchGate Publication |
| **분류** | 비주류 저널 (BK21 미포함) |

**주요 기여:**
- Kubernetes Self-Healing vs Serverless 내재적 장애 내성을 실증적으로 비교
- Pod 자동 재시작, Health Probe, 자동 스케일링 등의 Self-Healing 기능을 정량적 측정
- 워크로드 특성에 따른 플랫폼 선택 기준 제시

---

## 요약

| 구분 | 논문 수 | 게재지 |
|------|---------|--------|
| **BK21 최우수급** | 2편 | ACM TOSEM, ICSE-SEIP |
| **BK21 우수급** | 1편 | EuroSys |
| **비BK21** | 4편 | IEEE Software, Communications of ACM, ResearchGate(2편) |

## 연구 동향

```
[규칙 기반 Self-Healing]                 [카오스 엔지니어링]
 선언적 구성 + 조정 루프                   장애 주입 실험 방법론
 (Borg 2015, K8s 2016)                   (Basiri 2016)
        │                                      │
        v                                      v
 [장애 진단 고도화]                    [자동화된 카오스 실험]
 로그/메트릭/트레이스 기반               CI/CD 파이프라인 통합
 (Zhang, TOSEM 2025)                    (Basiri, ICSE 2019)
        │                                      │
        └──────────────┬───────────────────────┘
                       v
              [AI 기반 Self-Healing]
               예측적 장애 감지 + 자동 복구
               (AI-Driven Framework 2025)
```

## 참고 링크

- [Failure Diagnosis - ACM TOSEM](https://dl.acm.org/doi/10.1145/3715005)
- [Automating Chaos - ICSE-SEIP](https://dl.acm.org/doi/10.1109/ICSE-SEIP.2019.00012)
- [Borg - EuroSys 2015](https://dl.acm.org/doi/10.1145/2741948.2741964)
- [Chaos Engineering - IEEE Software](https://dl.acm.org/doi/abs/10.1109/MS.2016.60)
- [Borg, Omega, K8s - Communications of ACM](https://dl.acm.org/doi/10.1145/2890784)
