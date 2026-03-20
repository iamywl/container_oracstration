# CI/CD Pipeline 관련 논문 조사

> CI/CD 파이프라인 최적화, 지속적 배포 전략, DevOps 자동화, 롤백 메커니즘에 관한 논문 정리

---

## BK21 우수 학회/저널 논문

### 1. Uncovering the Benefits and Challenges of Continuous Integration Practices

| 항목 | 내용 |
|------|------|
| **저자** | Marco A. Gerosa et al. |
| **연도** | 2021 |
| **게재지** | **IEEE Transactions on Software Engineering (TSE)** |
| **BK21 등급** | **최우수급 저널** (소프트웨어공학 분야 최상위) |
| **DOI** | 10.1109/TSE.2021.3064953 |

**주요 기여:**
- Martin Fowler가 2006년에 정의한 10가지 CI 핵심 실천 방법의 현대적 유효성을 실증 검증
- CI 실천 방법이 소프트웨어 품질 향상에 미치는 영향을 정량적 분석
- CI 도입 시 이점(빠른 피드백, 품질 향상, 통합 문제 조기 발견)과 과제(테스트 유지보수 부담, 빌드 시간 증가) 식별

---

### 2. A Survey of DevOps Concepts and Challenges

| 항목 | 내용 |
|------|------|
| **저자** | Leonardo Leite, Carla Rocha, Fabio Kon, Dejan Milojicic, Paulo Meirelles |
| **연도** | 2019 |
| **게재지** | **ACM Computing Surveys, Vol. 52, No. 6** |
| **BK21 등급** | **최우수급 저널** (컴퓨터과학 전반 최상위 서베이 저널) |
| **DOI** | 10.1145/3359981 |

**주요 기여:**
- DevOps의 개념적 지도(conceptual map) 개발 — 자동화 도구와 핵심 개념 간 상관관계 제시
- 엔지니어, 관리자, 연구자 관점에서의 DevOps 과제를 체계적으로 조사
- CI/CD 파이프라인 구축 시 고려해야 할 조직 문화, 도구 선택, 프로세스 자동화를 폭넓게 다룸

---

### 3. An Empirical Study of Architecting for Continuous Delivery and Deployment

| 항목 | 내용 |
|------|------|
| **저자** | Mojtaba Shahin, Mansooreh Zahedi, Muhammad Ali Babar, Liming Zhu |
| **연도** | 2019 |
| **게재지** | **Empirical Software Engineering (EMSE), Vol. 24, pp. 1061-1108** |
| **BK21 등급** | **우수급 저널** (소프트웨어공학 실증 연구 분야) |
| **DOI** | 10.1007/s10664-018-9651-4 |

**주요 기여:**
- 19개 조직 21명 실무자 심층 인터뷰 + 91명 전문가 설문조사 기반 실증 연구
- 지속적 전달/배포를 위한 아키텍처링 프로세스 개념적 프레임워크 제시
- 모놀리식 vs 마이크로서비스 아키텍처와 지속적 전달의 호환성 실증 분석
- "작고 독립적인 배포 단위" 원칙이 CI/CD 파이프라인 설계에 핵심임을 입증

---

## 비BK21 논문 (기타 저널/서적/프리프린트)

### 4. Continuous Integration, Delivery and Deployment: A Systematic Review

| 항목 | 내용 |
|------|------|
| **저자** | Mojtaba Shahin, Muhammad Ali Babar, Liming Zhu |
| **연도** | 2017 |
| **게재지** | IEEE Access, Vol. 5, pp. 3909-3943 |
| **분류** | 오픈액세스 저널 (BK21 미포함) |
| **DOI** | 10.1109/ACCESS.2017.2685629 |

**주요 기여:**
- CI/CD 분야 최초의 체계적 문헌 리뷰(SLR) — 69편 논문을 분석하여 접근 방식, 도구, 과제를 분류
- 가장 많이 인용되는 CI/CD 서베이 논문 중 하나

---

### 5. Accelerate: The Science of Lean Software and DevOps (DORA Metrics)

| 항목 | 내용 |
|------|------|
| **저자** | Nicole Forsgren, Jez Humble, Gene Kim |
| **연도** | 2018 |
| **게재지** | IT Revolution Press (서적) / DORA State of DevOps Reports |
| **분류** | 서적/산업 보고서 (학술 학회 아님) |
| **ISBN** | 978-1942788331 |

**주요 기여:**
- DORA Metrics 4가지 핵심 지표 정립: 리드 타임, 배포 빈도, MTTR, 변경 실패율
- 4년간 대규모 데이터 기반 연구로 소프트웨어 전달 성능과 조직 성과 간 인과관계 입증
- DevOps 분야에서 가장 영향력 있는 저작 중 하나 (Google DORA 인수)

---

### 6. Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation

| 항목 | 내용 |
|------|------|
| **저자** | Jez Humble, David Farley |
| **연도** | 2010 |
| **게재지** | Addison-Wesley Professional |
| **분류** | 서적 (학술 학회 아님) |
| **ISBN** | 978-0321601919 |

**주요 기여:**
- "배포 파이프라인(Deployment Pipeline)" 개념을 최초로 체계적으로 정의
- 블루-그린 배포, 카나리 배포 전략과 롤백 메커니즘의 실질적 가이드 제시
- 2011년 Jolt Excellence Award 수상, CI/CD 분야의 바이블적 저서

---

### 7. On Queueing Theory for Large-Scale CI/CD Pipelines Optimization

| 항목 | 내용 |
|------|------|
| **저자** | (미상) |
| **연도** | 2025 |
| **게재지** | arXiv (Preprint, arXiv:2504.18705) |
| **분류** | 프리프린트 (미출판, 학회 미게재) |

**주요 기여:**
- 대기행렬 이론(Queueing Theory)을 CI/CD 파이프라인 최적화에 최초 적용
- M/M/c 대기행렬 모델로 파이프라인 리소스 할당 최적화 문제를 수학적 정식화
- Kubernetes 환경 CI/CD 러너 스케일링에 직접 적용 가능

---

## 요약

| 구분 | 논문 수 | 게재지 |
|------|---------|--------|
| **BK21 최우수급** | 2편 | IEEE TSE, ACM Computing Surveys |
| **BK21 우수급** | 1편 | EMSE |
| **비BK21** | 4편 | IEEE Access, 서적 2편, arXiv 프리프린트 |

## 참고 링크

- [Gerosa et al. (2021) - IEEE TSE](https://ieeexplore.ieee.org/document/9374092/)
- [Leite et al. (2019) - ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3359981)
- [Shahin et al. (2019) - EMSE](https://link.springer.com/article/10.1007/s10664-018-9651-4)
- [Shahin et al. (2017) - IEEE Access](https://ieeexplore.ieee.org/document/7884954/)
- [Forsgren et al. (2018) - IT Revolution](https://itrevolution.com/product/accelerate/)
- [Humble & Farley (2010) - Addison-Wesley](https://www.amazon.com/Continuous-Delivery-Deployment-Automation-Addison-Wesley/dp/0321601912)
- [Queueing Theory (2025) - arXiv](https://arxiv.org/abs/2504.18705)
