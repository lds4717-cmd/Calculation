# 🧠 Mini NPU Simulator (MAC 연산 기반 패턴 판별 계산기)

> **Codyssey Pre-course 필수 미션 - Computer Science**  
> AI 전용 하드웨어(NPU)의 핵심 연산인 **MAC(Multiply-Accumulate)** 원리를 외부 라이브러리(NumPy 등) 없이 순수 Python 표준 문법만으로 구현하고, 데이터 크기($3\times3 \sim 25\times25$)에 따른 시간 복잡도($O(N^2)$)와 수치 비교 정책을 검증하는 콘솔 시뮬레이터입니다.

---

## 🚀 1. 실행 방법

### 1) 개발 환경 및 제약 조건
- **Python 버전**: Python 3.8 이상 (권장: Python 3.10+)
- **사용 라이브러리**: Python 표준 라이브러리(`json`, `time`)만 사용 (외부 벡터화 라이브러리 미사용)
- **필수 데이터 파일**: 프로젝트 루트 디렉토리 내 `data.json` 위치

### 2) 실행 절차 및 모드 선택
```bash
# 1. 프로젝트 디렉토리 이동
cd codyssey-workspace

# 2. 시뮬레이터 실행
python main.py
```

프로그램 실행 후 아래 두 가지 모드 중 원하는 번호를 선택하여 실행합니다.
- **`1`번 (사용자 입력 모드)**: $3\times3$ 크기의 필터 2개(A, B)와 입력 패턴 1개를 공백으로 구분해 한 줄씩 직접 입력하여 MAC 점수, 판정 결과, 평균 연산 시간을 확인합니다.
- **`2`번 (data.json 분석 모드)**: 루트 경로의 `data.json`에서 $5\times5$, $13\times13$, $25\times25$ 필터와 테스트 패턴을 일괄 로드하여 라벨 정규화, PASS/FAIL 판정, 크기별 성능 분석표, 최종 결과 요약을 출력합니다.

---

## ⚙️ 2. 구현 요약

### 1) MAC(Multiply-Accumulate) 연산 구현 개요
- 2차원 입력 패턴 $P$와 필터 $F$ (크기 $N \times N$)에 대해 이중 반복문을 순회하며 동일 위치 원소끼리 곱하고 누적합을 구합니다.
$$\text{Score} = \sum_{i=0}^{N-1} \sum_{j=0}^{N-1} P[i][j] \times F[i][j]$$
- 외부 라이브러리 없이 순수 반복문으로 구현하여 $N \times N$ 행렬의 원소 접근 및 연산 횟수($N^2$)를 직관적으로 계측할 수 있도록 설계했습니다.

### 2) 라벨 정규화(Label Normalization) 방식
- `data.json` 내부에서 혼용되는 표기(`'+'`, `'cross'`, `'x
