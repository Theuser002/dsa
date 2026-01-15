from typing import List


class Solution:
    def maximizeSquareHoleArea(
        self, n: int, m: int, hBars: List[int], vBars: List[int]
    ) -> int:
        def max_consecutive(arr):
            res = 1
            t = 1
            for i in range(len(arr) - 1):
                if arr[i + 1] - arr[i] > 1:
                    t = 1
                else:
                    t += 1
                    res = max(res, t)
            return res

        return (
            min(max_consecutive(sorted(hBars)), max_consecutive(sorted(vBars))) + 1
        ) ** 2
