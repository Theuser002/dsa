from typing import List
import numpy as np
class Solution:
    DP = []
    nums1 = []
    nums2 = []

    def baseMax(self, i, j):
        maxBase = self.nums1[i] * self.nums2[j]
        if i == len(self.nums1) - 1:
            for k in range(j, len(self.nums2)):
                maxBase = max(maxBase, self.nums1[i] * self.nums2[k])
        else:
            for k in range(i, len(self.nums1)):
                maxBase = max(maxBase, self.nums1[k] * self.nums2[j])
        return maxBase

    def traverseDP(self,i,j,):
        if self.DP[i][j] is not None:
            return self.DP[i][j]
        if(i == len(self.nums1)-1 or j == len(self.nums2)-1):
            self.DP[i][j] = self.baseMax(i, j)
            return self.DP[i][j]
        self.DP[i][j] = max(
            self.traverseDP(i,   j + 1),
            self.traverseDP(i + 1, j),
            self.traverseDP(i + 1, j + 1),
            (self.traverseDP(i + 1, j + 1) + self.nums1[i] * self.nums2[j]),
            self.nums1[i]*self.nums2[j]
        )
        return self.DP[i][j]

    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        self.DP = [[None for _ in range(len(nums2))] for _ in range(len(nums1))]
        self.nums1 = nums1
        self.nums2 = nums2
        self.traverseDP(0,0)
        arr = np.array(self.DP)
        print(arr)
        return self.DP[0][0]

sln = Solution()
print(sln.maxDotProduct([-5,-1,-2],[3,3,5,5]))
