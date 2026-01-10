class Solution:
    
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        DP = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
        asciiSumOfTwoWords = sum(ord(c) for c in s1) + sum(ord(c) for c in s2)
        for i, c1 in enumerate(s1):
            for j, c2 in enumerate(s2):
                if c1 == c2:
                    DP[i+1][j+1] = DP[i][j] + ord(c2)
                else:
                    DP[i+1][j+1] = max(DP[i+1][j], DP[i][j+1])
        biggestCommonSum =  DP[len(s1)][len(s2)]
        
        return asciiSumOfTwoWords - 2*biggestCommonSum

sln = Solution()
print(sln.minimumDeleteSum("sea","eat"))
print(sln.minimumDeleteSum("delete","leet"))
