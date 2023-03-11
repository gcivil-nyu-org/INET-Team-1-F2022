class Solution:
    #example 1 
    #result =[(1&6)^(1&5)^(2&6)^(2&5)^(3&6)^(3&5)]
                \     /     \    /      \     /
    #           (1&(6^5)) ^ (2&(6^5)) ^ (3&(6^5))   
                   \            |           /
                    \           |          /
                     \          |         /
                      \         |        /
    #                  ((1^2^3) & (6^5))
    def getXORSum(self, a, b):
        x = 0 
        for i in range(len(a)):
            x = x ^ a[i]
        y = 0 
        for j in range(len(b)):
            y = y ^ b[j]
        return x & y

#Tc: O(m,n)
#SC: O(1)

#mine TLE
class Solution:
    def getXORSum(self, arr1: List[int], arr2: List[int]) -> int:
        
        i = 0 
        j = 0
        k = 0
        ans  = 0 
        temp = [0]*(len(arr1)*len(arr2))
        
        if len(arr2) < len(arr1):
            while i < len(arr1):

                temp[k] = arr1[i] & arr2[j]

                j += 1
                k += 1
                if j == len(arr2):
                    i += 1
                    j = 0
        else:
            while i < len(arr2):

                temp[k] = arr2[i] & arr1[j]

                j += 1
                k += 1
                if j == len(arr1):
                    i += 1
                    j = 0
        print(temp)
        
        for i in range(len(temp)):
            ans = ans ^ temp[i]
            
        return ans
