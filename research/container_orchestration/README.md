# Container Orchestration 관련 논문 조사

> 컨테이너 오케스트레이션 아키텍처, Kubernetes 스케줄링, 클러스터 관리, 프레임워크 비교에 관한 논문 정리

---

## BK21 우수 학회/저널 논문

### 1. Custom Scheduling in Kubernetes: A Survey on Common Problems and Solution Approaches

| 항목 | 내용 |
|------|------|
| **저자** | Scheinecker et al. |
| **연도** | 2022 |
| **게재지** | **ACM Computing Surveys** |
| **BK21 등급** | **최우수급 저널** (컴퓨터과학 전반 최상위 서베이 저널) |
| **DOI** | 10.1145/3544788 |

**주요 기여:**
- Kubernetes 커스텀 스케줄러 연구 동향을 체계적으로 정리
- 스케줄링 문제 유형별(자원 최적화, 지연 시간, 에너지 효율 등) 솔루션 분류
- 기본 스케줄러의 한계와 이를 극복하기 위한 확장 방법론 제시

---

### 2. Large-scale Cluster Management at Google with Borg

| 항목 | 내용 |
|------|------|
| **저자** | Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune, John Wilkes |
| **연도** | 2015 |
| **게재지** | **EuroSys '15 (European Conference on Computer Systems)** |
| **BK21 등급** | **우수급 학회** (시스템 분야) |
| **DOI** | 10.1145/2741948.2741964 |

**주요 기여:**
- Google의 대규모 클러스터 관리 시스템 Borg의 아키텍처를 최초로 공개
- Kubernetes의 직접적 전신 — Pod, Label, Service 등 핵심 개념의 원형 제시
- 수만 대 머신, 수십만 개 Job을 관리하는 프로덕션 시스템의 10년간의 운영 경험 공유
- 리소스 활용률 최적화, 장애 격리, 우선순위 기반 선점(preemption) 메커니즘 설명

---

### 3. Omega: Flexible, Scalable Schedulers for Large Compute Clusters

| 항목 | 내용 |
|------|------|
| **저자** | Malte Schwarzkopf, Andy Konwinski, Michael Abd-El-Malek, John Wilkes |
| **연도** | 2013 |
| **게재지** | **EuroSys '13 (European Conference on Computer Systems)** |
| **BK21 등급** | **우수급 학회** (시스템 분야) |
| **수상** | Best Student Paper Award |
| **DOI** | 10.1145/2465351.2465386 |

**주요 기여:**
- 공유 상태(Shared-state) 기반 병렬 스케줄링 아키텍처 제안
- 중앙집중식(Borg) vs 2-level(Mesos) vs 공유 상태(Omega) 스케줄링 비교 분석
- 낙관적 동시성 제어(Optimistic Concurrency Control)를 클러스터 스케줄링에 적용
- Kubernetes 스케줄러 설계에 직접적 영향을 미친 핵심 논문

---

## 비BK21 논문 (기타 저널/매거진)

### 4. Borg, Omega, and Kubernetes: Lessons Learned from Three Container-Management Systems

| 항목 | 내용 |
|------|------|
| **저자** | Brendan Burns, Brian Grant, David Oppenheimer, Eric Brewer, John Wilkes |
| **연도** | 2016 |
| **게재지** | ACM Queue, Vol. 14, No. 1 |
| **분류** | ACM 매거진 (학술 학회/저널이 아닌 실무 매거진) |

**주요 기여:**
- Borg → Omega → Kubernetes로 이어지는 10년간의 교훈 정리
- 컨테이너 오케스트레이션의 핵심 설계 원칙(선언적 API, 컨트롤 루프, 분리된 관심사)을 체계화
- 세 시스템에서 반복된 실수와 개선 사항을 솔직하게 공유

---

### 5. Container-based Cluster Orchestration Systems: A Taxonomy and Future Directions

| 항목 | 내용 |
|------|------|
| **저자** | Rodriguez, Buyya |
| **연도** | 2019 |
| **게재지** | Software: Practice and Experience (SPE), Wiley |
| **분류** | 일반 저널 (BK21 미포함) |
| **DOI** | 10.1002/spe.2660 |

**주요 기여:**
- 컨테이너 오케스트레이션 시스템 분류 체계(Taxonomy) 제안
- 배포, 스케줄링, 네트워킹, 스토리지, 모니터링 등 기능별 분류 프레임워크 제시
- Docker Swarm, Kubernetes, Mesos, Nomad 등 주요 시스템 비교 분석

---

### 6. Comprehensive Feature Comparison of Container Orchestration Frameworks

| 항목 | 내용 |
|------|------|
| **저자** | Truyen et al. |
| **연도** | 2019 |
| **게재지** | Applied Sciences (MDPI), Vol. 9, No. 5 |
| **분류** | MDPI 저널 (BK21 미포함) |

**주요 기여:**
- Docker Swarm / Kubernetes / Mesos 3대 프레임워크의 기능 비교
- 네트워킹, 스토리지, 보안, 스케줄링, 서비스 디스커버리 등 카테고리별 상세 비교표 제공
- 연구소/기업 환경에서 프레임워크 선택 시 참고할 수 있는 실용적 가이드

---

### 7. A Survey of Kubernetes Scheduling Algorithms

| 항목 | 내용 |
|------|------|
| **저자** | Zhong, Buyya |
| **연도** | 2023 |
| **게재지** | Journal of Cloud Computing (JCC), Springer |
| **분류** | 일반 저널 (BK21 미포함) |
| **DOI** | 10.1186/s13677-023-00471-1 |

**주요 기여:**
- Kubernetes 스케줄링 알고리즘을 세대별로 분류 (1세대: 기본 스케줄러 → 2세대: 확장 스케줄러 → 3세대: ML 기반)
- 각 세대별 알고리즘의 장단점, 적용 시나리오를 비교
- 향후 연구 방향(강화학습 기반 스케줄링, 이기종 클러스터 최적화) 제시

---

## 요약

| 구분 | 논문 수 | 게재지 |
|------|---------|--------|
| **BK21 최우수급** | 1편 | ACM Computing Surveys |
| **BK21 우수급** | 2편 | EuroSys (2편) |
| **비BK21** | 4편 | ACM Queue, SPE, MDPI Applied Sciences, JCC |

## 논문 간 관계

```
[Omega, EuroSys 2013]     [Borg, EuroSys 2015]
 공유상태 스케줄링    ────>   대규모 클러스터 관리
        │                        │
        └───────┬────────────────┘
                v
   [Borg, Omega, K8s Lessons, 2016]
     10년간의 교훈 정리
                │
                v
   [Kubernetes Scheduling Survey, 2023]
     스케줄링 알고리즘 세대별 분류
                │
                v
   [Custom Scheduling, ACM CSUR 2022]
     커스텀 스케줄러 연구 동향
```

## 참고 링크

- [Custom Scheduling - ACM CSUR](https://dl.acm.org/doi/full/10.1145/3544788)
- [Borg - EuroSys 2015](https://dl.acm.org/doi/10.1145/2741948.2741964)
- [Omega - EuroSys 2013](https://dl.acm.org/doi/10.1145/2465351.2465386)
- [Borg, Omega, K8s - ACM Queue](https://queue.acm.org/detail.cfm?id=2898444)
- [Orchestration Taxonomy - SPE](https://onlinelibrary.wiley.com/doi/10.1002/spe.2660)
- [Feature Comparison - MDPI](https://www.mdpi.com/2076-3417/9/5/931)
- [K8s Scheduling Survey - JCC](https://link.springer.com/article/10.1186/s13677-023-00471-1)
