from typing import List


class Solution:
    def maximizeSquareArea(self, m: int, n: int, hFences: List[int], vFences: List[int]) -> int:
        def all_distances(arr):
            return sorted(set([abs(arr[i] - arr[j]) for i in range(len(arr)) for j in range(i + 1, len(arr))]))
        vL = all_distances(hFences + [1,m])
        hL = all_distances(vFences + [1,n])
        common =  set(vL) & set(hL)
        return max(common)**2 % (10**9 + 7) if len(common) >=1 else -1


        
            