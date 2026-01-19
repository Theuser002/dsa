from typing import List

# TLE


class Solution:
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        m, n = len(mat), len(mat[0])

        dp = {}

        def find_dp(i, j, k):
            nonlocal dp

            if (i, j, k) in dp:
                return dp[(i, j, k)]

            A = max(
                find_dp(i, j, k - 1),
                find_dp(i + 1, j, k - 1),
                find_dp(i, j + 1, k - 1),
                find_dp(i + 1, j + 1, k - 1),
            )
            dp[(i, j, k - 1)] = A

            if A == k - 1:
                area = sum(mat[a][b] for a in range(i, i + k) for b in range(j, j + k))
                if area <= threshold:
                    dp[(i, j, k - 1)] = k

            # print(i, j, k - 1, dp[(i, j, k - 1)])

            return dp[(i, j, k - 1)]

        # base cases
        for i in range(m):
            for j in range(n):
                dp[(i, j, 1)] = 1 if mat[i][j] <= threshold else 0

        ans = 0

        if m > n:
            for i in range(m - n):
                ans = max(ans, find_dp(i, 0, min(m, n)))
        elif m < n:
            for j in range(n - m):
                ans = max(ans, find_dp(0, j, min(m, n)))
        else:
            ans = find_dp(0, 0, m)

        return ans


if __name__ == "__main__":
    solution = Solution()

    # mat = [[1, 1, 3, 2, 4, 3, 2],
    #        [1, 1, 3, 2, 4, 3, 2],
    #        [1, 1, 3, 2, 4, 3, 2]]
    mat = [[1, 1, 3, 2, 4, 3, 2], [1, 1, 3, 2, 4, 3, 2], [1, 1, 3, 2, 4, 3, 2]]
    threshold = 4

    print(solution.maxSideLength(mat, threshold))

# Use prefix sum
