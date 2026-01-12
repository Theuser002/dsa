from typing import List


class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        sum = 0
        def recursive(points, i, j):
            mid = round((i + j)/2)
            if abs(i - j) == 1:
                return max(abs((points[i][1] - points[j][1])), abs((points[i][0] - points[j][0])))
            if i == j: 
                return 0
            return recursive(points, i, mid) + recursive(points, mid, j) 
        
        sum = recursive(points, 0, len(points)-1)
        return sum
    
sln = Solution()
print(sln.minTimeToVisitAllPoints([[1,1],[3,4],[-1,0]]))