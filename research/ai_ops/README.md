# AIOps (AI for IT Operations) 관련 논문 조사

> AIOps 플랫폼, LLM 기반 운영 자동화, AI 에이전트 인프라 관리, 지능형 장애 관리에 관한 논문 정리

---

## BK21 우수 학회/저널 논문

### 1. A Survey of AIOps in the Era of Large Language Models

| 항목 | 내용 |
|------|------|
| **저자** | (서베이 논문) |
| **연도** | 2025 |
| **게재지** | **ACM Computing Surveys** |
| **BK21 등급** | **최우수급 저널** (컴퓨터과학 전반 최상위 서베이 저널) |
| **arXiv** | 2507.12472 |

**주요 기여:**
- LLM 시대의 AIOps를 다룬 대규모 서베이 — 183편 논문 분석
- 전통적 AIOps(ML/DL 기반)에서 LLM 기반 AIOps로의 패러다임 전환을 체계적으로 정리
- 장애 탐지, 근본 원인 분석, 자동 복구, 용량 계획 등 AIOps 전 영역에서의 LLM 활용 현황 분류
- 향후 연구 방향(멀티 에이전트, RAG 기반 운영 지식 활용 등) 제시

---

### 2. RCACopilot: Automatic Root Cause Analysis via Large Language Models

| 항목 | 내용 |
|------|------|
| **저자** | Chen et al. (Microsoft) |
| **연도** | 2024 |
| **게재지** | **EuroSys '24 (European Conference on Computer Systems)** |
| **BK21 등급** | **우수급 학회** (시스템 분야) |
| **arXiv** | 2305.15778 |

**주요 기여:**
- LLM을 활용한 자동 근본 원인 분석(Root Cause Analysis) 시스템 제안
- Microsoft 프로덕션 환경에서 실전 검증 — 실제 인시던트 데이터 기반
- 인시던트 로그, 메트릭, 알림 데이터를 LLM에 제공하여 근본 원인을 자동 추론
- 기존 규칙 기반 / ML 기반 RCA 대비 정확도와 속도 향상 입증

---

### 3. A Survey of AIOps Methods for Failure Management

| 항목 | 내용 |
|------|------|
| **저자** | Notaro, Cardoso, Gerndt |
| **연도** | 2021 |
| **게재지** | **ACM Transactions on Intelligent Systems and Technology (TIST)** |
| **BK21 등급** | **우수급 저널** (ACM Transactions 시리즈) |
| **DOI** | 10.1145/3483424 |

**주요 기여:**
- AIOps 장애 관리(Failure Management) 분야의 체계적 서베이
- 장애 예측, 탐지, 진단, 복구의 4단계를 프레임워크로 정리
- 각 단계별 ML/DL 기법 적용 현황과 성능 비교
- AIOps 연구의 주요 과제(데이터 품질, 레이블 부족, 설명 가능성)를 식별

---

## 비BK21 논문 (기타 학회/프리프린트)

### 4. AI for IT Operations (AIOps) on Cloud Platforms: Reviews, Opportunities and Challenges

| 항목 | 내용 |
|------|------|
| **저자** | Cheng et al. (Salesforce AI) |
| **연도** | 2023 |
| **게재지** | arXiv (Preprint, arXiv:2304.04661) |
| **분류** | 프리프린트 (미출판) |

**주요 기여:**
- 클라우드 플랫폼에서의 AIOps 전체 파이프라인 종합 리뷰
- 이상 탐지, 장애 예측, 근본 원인 분석, 자동 복구 등 주요 AIOps 태스크를 체계적으로 분류
- Salesforce 실무 경험을 바탕으로 한 산업 관점의 과제와 기회 제시

---

### 5. MOYA: Engineering LLM Powered Multi-agent Framework for Autonomous CloudOps

| 항목 | 내용 |
|------|------|
| **저자** | Parthasarathy, Vaidhyanathan et al. |
| **연도** | 2025 |
| **게재지** | CAIN 2025 (International Conference on AI Engineering) |
| **분류** | 신규 학회 (BK21 미포함) |
| **수상** | Best Paper 후보 |
| **arXiv** | 2501.08243 |

**주요 기여:**
- LLM 기반 멀티 에이전트 CloudOps 프레임워크 MOYA 제안
- 여러 AI 에이전트가 협력하여 클라우드 인프라를 자율적으로 운영하는 아키텍처
- 인시던트 대응, 용량 계획, 배포 관리 등 운영 태스크를 에이전트에게 위임
- 실제 클라우드 운영 시나리오에서 실험 검증

---

### 6. KubeIntellect: LLM-Orchestrated Agent Framework for Kubernetes Management

| 항목 | 내용 |
|------|------|
| **저자** | Ardebili, Bartolini |
| **연도** | 2025 |
| **게재지** | arXiv (Preprint, arXiv:2509.02449) |
| **분류** | 프리프린트 (미출판) |

**주요 기여:**
- LLM 기반 Kubernetes 관리 에이전트 프레임워크 KubeIntellect 제안
- 자연어 명령으로 Kubernetes 클러스터를 관리하는 AI 에이전트 시스템
- kubectl 명령어 생성, 장애 진단, 자원 최적화 제안 등을 LLM이 자율 수행
- 본 프로젝트의 MCP Server와 유사한 컨셉으로, AI 기반 컨테이너 운영의 최신 연구 방향

---

### 7. AIOps Solutions for Incident Management: Technical Guidelines and Literature Review

| 항목 | 내용 |
|------|------|
| **저자** | (문헌 리뷰) |
| **연도** | 2024 |
| **게재지** | arXiv (Preprint, arXiv:2404.01363) |
| **분류** | 프리프린트 (미출판) |

**주요 기여:**
- AIOps 인시던트 관리의 기술적 가이드라인 및 문헌 리뷰
- 인시던트 라이프사이클(탐지 → 분류 → 진단 → 해결 → 사후분석)별 AIOps 기법 정리
- 실무 적용을 위한 기술 선택 가이드라인 제시

---

## 요약

| 구분 | 논문 수 | 게재지 |
|------|---------|--------|
| **BK21 최우수급** | 1편 | ACM Computing Surveys |
| **BK21 우수급** | 2편 | EuroSys, ACM TIST |
| **비BK21** | 4편 | CAIN, arXiv(3편) |

> **참고:** AIOps는 최근 급성장 중인 분야로, LLM 등장 이후(2023~) 연구가 폭발적으로 증가하고 있다. 아직 프리프린트 단계인 논문이 많으나, ACM Computing Surveys, EuroSys 등 BK21 학회/저널에서도 본격적으로 다뤄지기 시작했다.

## 연구 동향

```
[전통적 AIOps]                          [LLM 기반 AIOps]
 ML/DL 기반 장애 관리              ────>  LLM 기반 자동 진단/복구
 (Notaro 2021, Cheng 2023)              (RCACopilot 2024)
                                              │
                                    ┌─────────┴──────────┐
                                    v                      v
                           [단일 에이전트]           [멀티 에이전트]
                           KubeIntellect 2025       MOYA 2025
                                    │                      │
                                    └──────────┬───────────┘
                                               v
                                    [LLM 시대 AIOps 서베이]
                                     ACM CSUR 2025
```

## 참고 링크

- [AIOps Survey - ACM CSUR 2025](https://arxiv.org/abs/2507.12472)
- [RCACopilot - EuroSys 2024](https://arxiv.org/abs/2305.15778)
- [AIOps Failure Management - ACM TIST](https://dl.acm.org/doi/10.1145/3483424)
- [AIOps on Cloud - Salesforce](https://arxiv.org/abs/2304.04661)
- [MOYA Multi-agent - CAIN 2025](https://arxiv.org/abs/2501.08243)
- [KubeIntellect - arXiv](https://arxiv.org/abs/2509.02449)
- [AIOps Incident Management - arXiv](https://arxiv.org/html/2404.01363v1)
