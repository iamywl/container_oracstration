# Auto-Scaling 관련 논문 조사

> 컨테이너/클라우드 환경의 오토 스케일링 알고리즘, 예측 기반 스케일링, 비용 최적화에 관한 논문 정리

---

## BK21 우수 학회/저널 논문

> 이 분야는 비교적 최근(2020년 이후) 활발히 연구되고 있으며, BK21 최우수/우수급 학회에 게재된 논문이 제한적이다. 아래 ACM TOIT 논문이 가장 근접한 수준이다.

### 1. Cost-Efficient Container Orchestration for Heterogeneous Resources

| 항목 | 내용 |
|------|------|
| **저자** | Zhong, Buyya et al. |
| **연도** | 2020 |
| **게재지** | **ACM Transactions on Internet Technology (TOIT)** |
| **BK21 등급** | **우수급 저널** (ACM Transactions 시리즈) |
| **DOI** | 10.1145/3378447 |

**주요 기여:**
- 이기종 자원 환경(heterogeneous resources)에서의 비용 효율적 Kubernetes 오케스트레이션 프레임워크 제안
- 클라우드/온프레미스 혼합 환경에서의 컨테이너 배치 및 스케일링 최적화
- 비용 모델과 자원 활용률을 동시에 고려한 스케줄링 알고리즘 설계

---

## 비BK21 논문 (기타 저널/학회)

### 2. KOSMOS: Vertical and Horizontal Resource Autoscaling for Kubernetes

| 항목 | 내용 |
|------|------|
| **저자** | Baresi et al. |
| **연도** | 2021 |
| **게재지** | ICSOC (International Conference on Service-Oriented Computing) / Springer |
| **분류** | 일반 국제 학회 (BK21 미포함) |

**주요 기여:**
- 수평(HPA) + 수직(VPA) 스케일링을 통합한 하이브리드 오토스케일링 프레임워크 KOSMOS 제안
- CPU 사용량 44% 절감 달성
- Kubernetes 환경에서 두 스케일링 방식의 충돌 문제를 해결하는 조정 메커니즘 설계
- 실제 Kubernetes 클러스터에서 실험 검증

---

### 3. Machine Learning Based Auto-Scaling for Containerized Applications

| 항목 | 내용 |
|------|------|
| **저자** | Imdoukh et al. |
| **연도** | 2020 |
| **게재지** | Neural Computing and Applications, Springer |
| **분류** | 일반 저널 (BK21 미포함) |
| **DOI** | 10.1007/s00521-019-04507-z |

**주요 기여:**
- LSTM 기반 워크로드 예측을 활용한 컨테이너 프로액티브 오토스케일링 제안
- 과거 메트릭 데이터로 미래 부하를 예측하여 사전 스케일링 수행
- 리액티브 방식(임계치 기반) 대비 응답 시간 및 자원 낭비 감소 효과 입증

---

### 4. Proactive Autoscaling for Cloud-Native Applications Using Machine Learning

| 항목 | 내용 |
|------|------|
| **저자** | Marie-Magdelaine, Ahmed |
| **연도** | 2020 |
| **게재지** | IEEE GLOBECOM (Global Communications Conference) |
| **분류** | 일반 국제 학회 (BK21 미포함) |
| **DOI** | 10.1109/GLOBECOM42002.2020.9322147 |

**주요 기여:**
- 클라우드 네이티브 환경에서 ML 기반 프로액티브 오토스케일링 파이프라인 제안
- 워크로드 패턴 분류 + 부하 예측을 결합한 2단계 접근법
- Kubernetes HPA의 반응형 한계를 극복하는 선제적 스케일링 전략

---

### 5. Cost-Efficient Container Auto-Scaling: A Four-Phase Approach

| 항목 | 내용 |
|------|------|
| **저자** | Sheganaku et al. |
| **연도** | 2023 |
| **게재지** | Future Generation Computer Systems (FGCS), Elsevier |
| **분류** | 일반 저널 (BK21 미포함) |

**주요 기여:**
- 비용 최소화를 목표로 한 4단계 컨테이너 오토스케일링 프레임워크 제안
  1. 워크로드 분석 → 2. 자원 추정 → 3. 스케일링 결정 → 4. 비용 최적화
- SLA 위반 없이 인프라 비용을 최소화하는 최적화 모델 제시

---

### 6. Horizontal Pod Autoscaling in Kubernetes: An Experimental Analysis

| 항목 | 내용 |
|------|------|
| **저자** | Nguyen et al. |
| **연도** | 2020 |
| **게재지** | Sensors (MDPI), Vol. 20, No. 16 |
| **분류** | MDPI 저널 (BK21 미포함) |

**주요 기여:**
- Kubernetes HPA(Horizontal Pod Autoscaler)의 동작을 실험적으로 분석한 기초 연구
- HPA의 스케일링 지연, 과/과소 프로비저닝 문제를 정량적으로 측정
- HPA 파라미터 튜닝이 성능에 미치는 영향을 실험적으로 검증

---

### 7. Auto-Scaling Techniques for Cloud-Native Applications: A Comprehensive Survey

| 항목 | 내용 |
|------|------|
| **저자** | (서베이 논문) |
| **연도** | 2024 |
| **게재지** | Sensors (MDPI), Vol. 24, No. 17 |
| **분류** | MDPI 저널 (BK21 미포함) |

**주요 기여:**
- 오토스케일링 기법 전반을 망라한 종합 서베이 (리액티브, 프로액티브, 하이브리드)
- 리액티브(임계치 기반) vs 프로액티브(예측 기반) vs 하이브리드 방식 비교
- ML/DL 기반 오토스케일링 기법의 최신 연구 동향 정리

---

## 요약

| 구분 | 논문 수 | 게재지 |
|------|---------|--------|
| **BK21 우수급** | 1편 | ACM TOIT |
| **비BK21** | 6편 | ICSOC, NCA, GLOBECOM, FGCS, Sensors(2편) |

> **참고:** 컨테이너 오토스케일링은 비교적 최근 연구 분야로, BK21 최우수급 학회(SOSP, OSDI, EuroSys 등)에 단독 주제로 게재된 논문이 적다. 관련 연구는 주로 클러스터 관리/스케줄링 논문의 하위 주제로 다뤄지는 경우가 많다 (→ Container Orchestration 분야의 Borg, Omega 논문 참조).

## 연구 동향

```
[리액티브 스케일링]              [프로액티브 스케일링]
 임계치 기반 (K8s HPA)     ────>  ML/LSTM 기반 예측
 (Nguyen 2020)                  (Imdoukh 2020, Marie-Magdelaine 2020)
        │                               │
        └──────────┬────────────────────┘
                   v
          [하이브리드 스케일링]
           수평+수직 통합 (KOSMOS 2021)
                   │
                   v
          [비용 최적화 스케일링]
           (Sheganaku 2023, Zhong 2020)
```

## 참고 링크

- [Cost-Efficient Orchestration - ACM TOIT](https://dl.acm.org/doi/10.1145/3378447)
- [KOSMOS - ICSOC](https://link.springer.com/chapter/10.1007/978-3-030-91431-8_59)
- [ML Auto-Scaling - NCA](https://link.springer.com/article/10.1007/s00521-019-04507-z)
- [Proactive Autoscaling - GLOBECOM](https://ieeexplore.ieee.org/document/9322147)
- [Cost-Efficient Auto-Scaling - FGCS](https://www.sciencedirect.com/science/article/abs/pii/S0167739X22002850)
- [K8s HPA Analysis - Sensors](https://www.mdpi.com/1424-8220/20/16/4621)
- [Auto-Scaling Survey - Sensors](https://www.mdpi.com/1424-8220/24/17/5551)
