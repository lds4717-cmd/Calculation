# 🎮 Python CLI 나만의 퀴즈 게임 (Quiz Game)

> **Codyssey Pre-course 필수 미션 - Python & Git Basic**  
> 외부 라이브러리 없이 Python 3.10+ 표준 문법과 객체 지향 설계(OOP)만을 활용하여 구현한 터미널 기반 퀴즈 프로그램입니다. `state.json` 파일을 통한 데이터 영속성과 예외 방어 로직을 지원합니다.

---

## 📌 1. 프로젝트 개요

- **미션 목표**: 단순 문법 학습을 넘어 입력/출력 흐름 제어, 클래스 기반 역할 분리, JSON 파일 입출력을 통한 데이터 영속성, 그리고 Git 브랜치 전략을 적용한 완성형 콘솔 프로그램 구현
- **개발 환경**: Python 3.10 이상 (표준 라이브러리 `json`, `os` 등만 사용 / 외부 패키지 미사용)
- **핵심 구현 포인트**:
  - `Quiz`와 `QuizGame` 2개 이상의 클래스로 데이터 모델과 게임 제어 로직 분리
  - 프로젝트 루트의 `state.json`(UTF-8)을 통한 퀴즈 목록 및 최고 점수 영구 저장
  - 공백/빈 입력, 문자열/범위 초과 입력, `Ctrl+C`(`KeyboardInterrupt`), `EOFError`, JSON 파일 손상 등 모든 예외 상황에 대한 방어 처리

---

## 💡 2. 퀴즈 주제와 선정 이유

- **선정 주제**: **기계공학 기초 및 Python·Git 핵심 상식 퀴즈** *(※ 본인이 작성한 퀴즈 주제에 맞게 수정하세요)*
- **선정 이유**:
  - 전공 핵심 개념(열역학, 유체역학, 재료역학 기초)과 개발 과정에서 익힌 Python 문법 및 Git 명령어 지식을 퀴즈 형태로 정리하여 학습 내용을 복습하기 위해 선정했습니다.
  - 사용자가 터미널에서 직접 새로운 문제를 추가(`퀴즈 추가`)할 수 있도록 설계하여 학습이 진행될수록 나만의 문제 은행으로 확장할 수 있습니다.

---

## 🚀 3. 실행 방법

### 1) 사전 요구 사항
- **Python 3.10 이상**이 설치되어 있어야 합니다.

### 2) 저장소 복제 및 프로그램 실행
```bash
# 1. 원격 저장소 복제
git clone [https://github.com/lds4717-cmd/codyssey-workspace.git](https://github.com/lds4717-cmd/codyssey-workspace.git)

# 2. 프로젝트 디렉토리 이동
cd codyssey-workspace

# 3. 퀴즈 게임 실행 (환경에 따라 python 또는 python3 사용)
python main.py
```

---

## ⚙️ 4. 기능 목록 및 설계 구조

### 1) 주요 메뉴 기능
| 번호 | 기능명 | 상세 설명 |
| :---: | :--- | :--- |
| **1** | **퀴즈 풀기** | 등록된 퀴즈를 순차 출제하고 1~4번 정답을 입력받아 즉시 정답/오답 여부를 안내합니다. 모든 문제 풀이 후 점수를 계산하여 최고 점수를 갱신합니다. |
| **2** | **퀴즈 추가** | 새로운 문제, 4개의 선택지, 정답 번호(1~4)를 입력받아 `Quiz` 인스턴스로 생성하고 `state.json`에 즉시 저장합니다. |
| **3** | **퀴즈 목록** | 현재 저장된 전체 퀴즈의 번호와 문제 목록을 조회합니다. (등록된 퀴즈가 없을 경우 안내 메시지 출력) |
| **4** | **점수 확인** | 역대 최고 점수와 정답 개수를 확인합니다. (아직 퀴즈를 풀지 않은 경우 예외 안내 출력) |
| **5** | **종료** | 현재 게임 데이터를 안전하게 저장한 뒤 프로그램을 정상 종료합니다. |

### 2) 클래스 및 예외 처리 설계
- **`Quiz` 클래스**: 개별 퀴즈의 속성(`question`, `choices`, `answer`)을 정의하고, 문제 출력 및 정답 검증 메서드를 담당합니다.
- **`QuizGame` 클래스**: 전체 퀴즈 목록(`quizzes`)과 최고 점수(`best_score`)를 관리하며, 메뉴 출력, 사용자 입력 검증, 파일 저장/불러오기를 담당합니다.
- **공통 입력 및 예외 처리**:
  - 입력값 앞뒤 공백 제거(`strip()`), 빈 입력(`Enter`), 숫자 변환 실패(`abc`), 허용 범위 초과(`0`, `9`) 시 안내 메시지 출력 후 재입력 유도
  - 실행 중 `Ctrl+C`(`KeyboardInterrupt`) 또는 `EOFError` 발생 시 비정상 종료 없이 안전하게 데이터 저장 후 종료

---

## 📂 5. 파일 구조

```text
codyssey-workspace/
├── main.py                  # 프로그램 진입점 및 Quiz, QuizGame 클래스 정의
├── state.json               # 퀴즈 목록 및 최고 점수 영속성 저장 파일 (UTF-8)
├── .gitignore               # Git 추적 제외 목록 (__pycache__, .vscode 등)
├── README.md                # 프로젝트 기술 문서 및 실행 가이드
└── docs/
    └── screenshots/         # 실행 결과 및 Git 워크플로우 증빙 스크린샷
        ├── env_setup.png    # 개발 환경 설정 (VS Code, Python 버전, Git 설정)
        ├── menu.png         # 메인 메뉴 및 예외 입력 처리 화면
        ├── play.png         # 퀴즈 풀기 및 점수 결과 화면
        ├── add_quiz.png     # 퀴즈 추가 및 퀴즈 목록 조회 화면
        ├── score.png        # 점수 확인 및 프로그램 재시작 후 데이터 유지 화면
        └── git_log.png      # git log --oneline --graph 브랜치 병합 이력
```

---

## 💾 6. 데이터 파일 설명 (`state.json`)

- **파일 경로**: 프로젝트 루트 디렉토리 (`./state.json`)
- **인코딩**: `UTF-8` (`ensure_ascii=False` 적용으로 한글 데이터 가독성 확보)
- **역할**: 프로그램을 종료하고 다시 실행해도 사용자가 추가한 퀴즈와 최고 점수가 소실되지 않도록 상태를 영구 저장합니다.
- **파일 예외 복구 정책**:
  - 첫 실행 시 `state.json`이 없으면 코드 내 정의된 **기본 퀴즈 5개**로 자동 초기화합니다.
  - 파일이 손상되었거나 읽기/쓰기 오류가 발생한 경우 `try/except`로 예외를 포착해 안내 메시지를 출력하고 기본 퀴즈 데이터로 복구합니다.

### 데이터 스키마 구조
```json
{
  "quizzes": [
    {
      "question": "Python의 창시자는?",
      "choices": [
        "Guido",
        "Linus",
        "Bjarne",
        "James"
      ],
      "answer": 1
    }
  ],
  "best_score": 3
}
```
- `quizzes` (`list[dict]`): 각 퀴즈의 문제(`question`: `str`), 선택지 4개(`choices`: `list[str]`), 정답 번호(`answer`: `int`, `1~4`)를 담은 리스트
- `best_score` (`int`): 역대 플레이 중 달성한 최고 점수(또는 최고 정답 수)

---

## 📸 7. 실행 결과 및 Git 워크플로우 증빙

> *(※ `docs/screenshots/` 폴더에 각 캡처 이미지를 저장한 뒤 아래 경로와 파일명을 맞춰주세요.)*

### 1) 개발 환경 및 Git 설정 (`env_setup.png`)
![개발 환경 설정](./docs/screenshots/env_setup.png)

### 2) 프로그램 실행 결과 (메뉴 / 퀴즈 풀기 / 퀴즈 추가 / 점수 확인)
| 메인 메뉴 화면 | 퀴즈 풀기 화면 |
| :---: | :---: |
| ![메인 메뉴](./docs/screenshots/menu.png) | ![퀴즈 풀기](./docs/screenshots/play.png) |

| 퀴즈 추가 및 목록 화면 | 점수 확인 및 재시작 유지 화면 |
| :---: | :---: |
| ![퀴즈 추가](./docs/screenshots/add_quiz.png) | ![점수 확인](./docs/screenshots/score.png) |

### 3) Git 커밋 및 브랜치 병합 이력 (`git log --oneline --graph`)
- `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` 명령어 활용 및 기능 단위 커밋(10회 이상) 수행 완료
![Git 로그 그래프](./docs/screenshots/git_log.png)
