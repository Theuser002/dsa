class Solution:
    def maximizeSquareHoleArea(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        def findMaxConsecutiveLength(arr):
            arr.sort()
            maxLength = 0
            temp = 1
            for i in range(1, len(arr)):
                if (arr[i] - arr[i-1]) == 1:
                    temp += 1
                else:
                    maxLength = max(maxLength, temp)
                    temp = 1
            maxLength = max(maxLength, temp)
            return maxLength
        maxConHBars = findMaxConsecutiveLength(hBars)
        maxConVBars = findMaxConsecutiveLength(vBars)

        return (min(maxConHBars, maxConVBars)+1) ** 2