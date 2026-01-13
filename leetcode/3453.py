from typing import List


class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        halfArea = 0
        maxY = 0
        minY = 0
        for square in squares:
            halfArea += square[2]**2/2
            maxY = max(maxY, square[1] + square[2])
            minY = min(minY, square[1])
        def isMoreThanHalf(y):
            areaUnderY = 0
            for square in squares:
                if square[1] < y:
                    areaUnderY += square[2] * min(y- square[1], square[2])
            return areaUnderY >= halfArea

        while (maxY-minY) > 10**-5:
            mid = (maxY+minY)/2
            if(isMoreThanHalf(mid)):
                maxY = mid
            else:
                minY = mid
        return minY
    
sln = Solution()
print(sln.separateSquares([[0,0,1],[2,2,1]]))