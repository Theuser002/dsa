from typing import List


class Solution:

    def separateSquares(self, squares: List[List[int]]) -> float:
        def area(s, y_max=None):
            if y_max is None or y_max >= (s[1] + s[2]):
                return s[2] * s[2]
            return s[2] * max(0, y_max - s[1])

        target_area = sum([area(s) for s in squares]) / 2

        # sort squares by top y
        squares.sort(key=lambda s: s[1] + s[2])

        y_max, y_min = squares[0][1], squares[0][1]
        for s in squares:
            y_max = max(y_max, s[1] + s[2])
            y_min = min(y_min, s[1])

        # binary search
        y_mid = y_min
        prev_y_mid = float("-inf")
        while y_max >= y_min:
            y_mid = (y_max + y_min) / 2
            below_area = sum([area(s, y_mid) for s in squares])

            # print(y_mid, y_min, y_max, abs(below_area - target_area))

            if abs(below_area - target_area) <= 10**-5:
                break
            elif below_area > target_area:
                y_max = y_mid
            else:
                y_min = y_mid

            if y_mid == prev_y_mid:
                break
            else:
                prev_y_mid = y_mid
        # print(y_mid)
        # fine-tune
        # Find y_max of squares has s[1] below y_mid if y_max < y_mid -> return y_max
        y_max = float("-inf")

        accumulated_area = 0
        for s in squares:
            if s[1] + s[2] <= y_mid:
                y_max = max(y_max, s[1] + s[2])
                accumulated_area += area(s)

        if abs(accumulated_area - target_area) <= 10**-5:
            return y_max

        return y_mid


if __name__ == "__main__":
    solu = Solution()

    squares = [
        [522261215, 954313664, 225462],
        [628661372, 718610752, 10667],
        [619734768, 941310679, 44788],
        [352367502, 656774918, 289036],
        [860247066, 905800565, 100123],
        [817623994, 962847576, 71460],
        [691552058, 782740602, 36271],
        [911356, 152015365, 513881],
        [462847044, 859151855, 233567],
        [672324240, 954509294, 685569],
    ]

    print(solu.separateSquares(squares))

    # print(solu.separateSquares([[1,1,2],[2,3,1]]))  # 2.0
    # print(solu.separateSquares([[0,0,4],[1,1,2],[2,2,1]]))  # 2.0
    # print(solu.separateSquares([[0,0,1],[0,1,1],[1,0,1],[1,1,1]]))  # 1.0
