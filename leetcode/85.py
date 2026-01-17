from typing import List


class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        DP = [[{"xy":[],"area":0} for _ in range(len(matrix[0]) + 1)] for _ in range(len(matrix)+1) ]
        # DP[0][0] = {"ulCorner":[0,0],"lrCorner":[0,0], "area":matrix[0][0]}
        def addArea(DP, i, j):
            print(i, j, matrix[i][j])
            if matrix[i][j] == "1":
                if len(DP[i][j]["xy"]) == 0:
                    maxArea = max([DP[i-1][j], DP[i][j-1]], key=lambda x: (x.get("area", 0),len(x.get("list",[])))).copy()
                    print(maxArea)
                    if maxArea.get("area") == 0:
                        DP[i][j]["xy"].append({"ulCorner":[i,j],"lrCorner":[i,j]}) 
                        DP[i][j]["area"] = 1
                        print(DP[i][j])
                        return
                    else:
                        for param in maxArea.get("xy"):
                            isRectangle = True if (param["ulCorner"][0] <= i and param["ulCorner"][1] <= j) else False
                            for x in range(param["ulCorner"][0], i + 1):
                                for y in range(param["ulCorner"][1], j + 1):
                                    if matrix[x][y] != "1":
                                        isRectangle = False
                            if isRectangle:
                                param["lrCorner"] = [i, j]
                            else:
                                DP[i][j] = maxArea.copy()
                                if(maxArea.get("area") == 1):
                                    DP[i][j]["xy"].append({"ulCorner":[i,j],"lrCorner":[i,j]})
                                    break

                    DP[i][j] = maxArea.copy()
                    DP[i][j]["area"] = (maxArea["xy"][0]["lrCorner"][0] - maxArea["xy"][0]["ulCorner"][0] + 1) * (maxArea["xy"][0]["lrCorner"][1]-maxArea["xy"][0]["ulCorner"][1] +1)
                    print(DP[i][j])
                    return
            else:
                maxArea = max([DP[i-1][j], DP[i][j-1]], key=lambda x: x.get("area", 0)).copy()
                DP[i][j] = maxArea
                print(DP[i][j])
                return

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                    addArea(DP, i, j) 
                # if matrix[i][j] == "1":
        return 0

    
sln = Solution()
print(sln.maximalRectangle([["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]))