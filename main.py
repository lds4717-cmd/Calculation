import json
import os
import time


class MiniNPUSimulator:
    def __init__(self, epsilon: float = 1e-9):
        self.epsilon = epsilon
        self.filters = {}
        self.patterns = {}

    def normalize_label(self, raw_label: str) -> str:
        """라벨 정규화: '+', 'cross' -> 'Cross' / 'x', 'X' -> 'X'"""
        cleaned = str(raw_label).strip().lower()
        if cleaned in ("+", "cross"):
            return "Cross"
        if cleaned == "x":
            return "X"
        return str(raw_label).strip()

    def mac_operation(self, pattern: list[list[float]], filter_matrix: list[list[float]]) -> float:
        """외부 라이브러리 없이 순수 반복문으로 N x N MAC(Multiply-Accumulate) 연산 수행"""
        n = len(pattern)
        total = 0.0
        for i in range(n):
            for j in range(n):
                total += pattern[i][j] * filter_matrix[i][j]
        return total

    def measure_mac_time(
        self, pattern: list[list[float]], filter_matrix: list[list[float]], repeats: int = 10
    ) -> float:
        """순수 MAC 연산 구간만 repeats회 반복 측정 후 평균 시간(ms) 반환"""
        start = time.perf_counter()
        for _ in range(repeats):
            self.mac_operation(pattern, filter_matrix)
        end = time.perf_counter()
        avg_ms = ((end - start) / repeats) * 1000.0
        return avg_ms

    def judge_scores(
        self, score_a: float, score_b: float, label_a: str = "A", label_b: str = "B"
    ) -> str:
        """허용오차(epsilon) 기반 점수 비교 및 동점(UNDECIDED) 판정"""
        if abs(score_a - score_b) < self.epsilon:
            return "UNDECIDED"
        return label_a if score_a > score_b else label_b

    def read_matrix_from_console(self, title: str, n: int = 3) -> list[list[float]]:
        """모드 1: 콘솔에서 n x n 행렬을 한 줄씩(공백 구분) 검증하며 입력받기"""
        print(f"\n{title} ({n}줄 입력, 공백 구분)")
        matrix = []
        row_idx = 0
        while row_idx < n:
            try:
                raw = input(f"  {row_idx + 1}행: ").strip()
                if not raw:
                    print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                    continue
                parts = raw.split()
                if len(parts) != n:
                    print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                    continue
                row = [float(x) for x in parts]
                matrix.append(row)
                row_idx += 1
            except ValueError:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
        return matrix

    def validate_square_matrix(self, matrix: list, expected_n: int) -> bool:
        """2차원 배열이 expected_n x expected_n 크기인지 검증"""
        if not isinstance(matrix, list) or len(matrix) != expected_n:
            return False
        for row in matrix:
            if not isinstance(row, list) or len(row) != expected_n:
                return False
        return True

    def run_mode_1(self):
        """모드 1: 사용자 입력 (3x3)"""
        print("\n#----------------------------------------")
        print("# [1] 필터 입력")
        print("#----------------------------------------")
        filter_a = self.read_matrix_from_console("필터 A", n=3)
        filter_b = self.read_matrix_from_console("필터 B", n=3)

        print("\n#----------------------------------------")
        print("# [2] 패턴 입력")
        print("#----------------------------------------")
        pattern = self.read_matrix_from_console("패턴", n=3)

        score_a = self.mac_operation(pattern, filter_a)
        score_b = self.mac_operation(pattern, filter_b)
        avg_time_ms = self.measure_mac_time(pattern, filter_a, repeats=10)
        verdict = self.judge_scores(score_a, score_b, label_a="A", label_b="B")

        print("\n#----------------------------------------")
        print("# [3] MAC 결과")
        print("#----------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/10회): {avg_time_ms:.4f} ms")
        if verdict == "UNDECIDED":
            print(f"판정: 판정 불가 (|A-B| < {self.epsilon})")
        else:
            print(f"판정: {verdict}")

    def run_mode_2(self, filepath: str = "data.json"):
        """모드 2: data.json 분석 및 성능/결과 리포트 출력"""
        if not os.path.exists(filepath):
            print(f"\n[오류] '{filepath}' 파일을 찾을 수 없습니다. 프로젝트 루트에 data.json을 배치해 주세요.")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"\n[오류] data.json 로드 실패: {e}")
            return

        raw_filters = data.get("filters", {})
        raw_patterns = data.get("patterns", {})

        print("\n#----------------------------------------")
        print("# [1] 필터 로드")
        print("#----------------------------------------")
        normalized_filters = {}
        for size_key, filter_dict in raw_filters.items():
            normalized_filters[size_key] = {}
            for f_key, matrix in filter_dict.items():
                std_label = self.normalize_label(f_key)
                normalized_filters[size_key][std_label] = matrix
            loaded_labels = ", ".join(normalized_filters[size_key].keys())
            print(f"✓ {size_key} 필터 로드 완료 ({loaded_labels})")

        print("\n#----------------------------------------")
        print("# [2] 패턴 분석 (라벨 정규화 적용)")
        print("#----------------------------------------")
        total_tests = 0
        passed_tests = 0
        failed_cases = []
        sample_by_size = {}

        for pat_key, pat_info in raw_patterns.items():
            total_tests += 1
            print(f"\n--- {pat_key} ---")

            # 패턴 키(size_{N}_{idx})에서 크기 N 추출
            parts = pat_key.split("_")
            if len(parts) < 3 or parts[0] != "size" or not parts[1].isdigit():
                reason = f"잘못된 패턴 키 형식 ({pat_key})"
                print(f"판정: FAIL ({reason})")
                failed_cases.append((pat_key, reason))
                continue

            n = int(parts[1])
            size_key = f"size_{n}"
            input_matrix = pat_info.get("input")
            expected_raw = pat_info.get("expected", "")
            expected_label = self.normalize_label(expected_raw)

            # 필터 존재 및 크기 검증
            if size_key not in normalized_filters:
                reason = f"{size_key} 필터가 존재하지 않음"
                print(f"판정: FAIL ({reason})")
                failed_cases.append((pat_key, reason))
                continue

            cross_filter = normalized_filters[size_key].get("Cross")
            x_filter = normalized_filters[size_key].get("X")

            if (
                not self.validate_square_matrix(input_matrix, n)
                or not self.validate_square_matrix(cross_filter, n)
                or not self.validate_square_matrix(x_filter, n)
            ):
                reason = f"필터와 패턴 크기 불일치 (기대 크기: {n}x{n})"
                print(f"판정: FAIL ({reason})")
                failed_cases.append((pat_key, reason))
                continue

            if n not in sample_by_size:
                sample_by_size[n] = (input_matrix, cross_filter)

            score_cross = self.mac_operation(input_matrix, cross_filter)
            score_x = self.mac_operation(input_matrix, x_filter)
            verdict = self.judge_scores(score_cross, score_x, label_a="Cross", label_b="X")

            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")

            if verdict == expected_label:
                passed_tests += 1
                print(f"판정: {verdict} | expected: {expected_label} | PASS")
            else:
                if verdict == "UNDECIDED":
                    reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
                else:
                    reason = f"예측 불일치 (판정: {verdict}, 기대: {expected_label})"
                print(f"판정: {verdict} | expected: {expected_label} | FAIL ({reason})")
                failed_cases.append((pat_key, reason))

        print("\n#----------------------------------------")
        print("# [3] 성능 분석 (평균/10회)")
        print("#----------------------------------------")
        print(f"{'크기':<10} {'평균 시간(ms)':<16} {'연산 횟수(N²)'}")
        print("-" * 42)

        # 3x3 기본 샘플 준비 후 3, 5, 13, 25 크기별 성능 측정
        dummy_3x3_pat = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        dummy_3x3_flt = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        sample_by_size[3] = (dummy_3x3_pat, dummy_3x3_flt)

        for n in sorted(sample_by_size.keys()):
            pat_m, flt_m = sample_by_size[n]
            avg_ms = self.measure_mac_time(pat_m, flt_m, repeats=10)
            ops = n * n
            print(f"{f'{n}x{n}':<10} {avg_ms:<16.4f} {ops}")

        print("\n#----------------------------------------")
        print("# [4] 결과 요약")
        print("#----------------------------------------")
        print(f"총 테스트: {total_tests}개")
        print(f"통과: {passed_tests}개")
        print(f"실패: {len(failed_cases)}개")
        if failed_cases:
            print("실패 케이스:")
            for cid, reason in failed_cases:
                print(f"  - {cid}: {reason}")


def main():
    simulator = MiniNPUSimulator(epsilon=1e-9)
    try:
        while True:
            print("\n=== Mini NPU Simulator ===")
            print("[모드 선택]")
            print("1. 사용자 입력 (3x3)")
            print("2. data.json 분석")
            print("3. 종료")
            choice = input("선택: ").strip()

            if choice == "1":
                simulator.run_mode_1()
            elif choice == "2":
                simulator.run_mode_2("data.json")
            elif choice == "3":
                print("프로그램을 종료합니다.")
                break
            else:
                print("입력 오류: 1, 2, 3 중 하나를 입력하세요.")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 시뮬레이터를 안전하게 종료합니다.")


if __name__ == "__main__":
    main()