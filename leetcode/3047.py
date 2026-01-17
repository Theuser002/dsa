from typing import List


class Solution:
    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        overlappingAreas = set()
        maxArea = 0
        for i in range(0, len(bottomLeft)):
            for j in range(i+1, len(bottomLeft)):
                potentialTopRight = [min(topRight[i][0], topRight[j][0]), min(topRight[i][1], topRight[j][1])]
                potentialBottomLeft = [max(bottomLeft[i][0], bottomLeft[j][0]), max(bottomLeft[i][1], bottomLeft[j][1])]
                if potentialTopRight[0] <= potentialBottomLeft[0] or potentialTopRight[1] <= potentialBottomLeft[1]:
                    continue
                maxArea = max(maxArea, min((potentialTopRight[0] - potentialBottomLeft[0]),(potentialTopRight[1] - potentialBottomLeft[1]))**2)
        return maxArea