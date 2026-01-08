class Solution:
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        dp = [[None for _ in range(len(nums2))] for _ in range(len(nums1))]

        def find_dp(i, j):
            nonlocal dp

            if dp[i][j] is not None:
                return dp[i][j]
            
            dp[i][j] = max(
                nums1[i] * nums2[j],
                nums1[i] * nums2[j] + find_dp(i-1, j-1),
                find_dp(i-1, j),
                find_dp(i, j-1)
            )

            return dp[i][j]

        # build base cases
        t = float('-inf')
        for j in range(len(nums2)):
            t = max(t, nums1[0] * nums2[j])
            dp[0][j] = t
        
        t = float('-inf')
        for i in range(len(nums1)):
            t = max(t, nums1[i] * nums2[0])
            dp[i][0] = t

        find_dp(len(nums1)-1, len(nums2)-1)

        return dp[len(nums1)-1][len(nums2)-1]

