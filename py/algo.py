import sys

def coin_change(coins,amount):
    # _min = sys.maxsize

    # def dfs(_count,_sum):        
    #     nonlocal _min
        
    #     if(_sum == amount):
    #         if(_count < _min):
    #             _min = _count
    #         return
    #     elif(_sum > amount):
    #         return
        
    #     for i in range(len(coins)):
    #         dfs(_count + 1,coins[i] + _sum)

    # dfs(0,0)
    # print(_min)
    # return _min

    dp = [(amount + 1)] * (amount + 1)
    
    dp[0] = 0

    for i in range(amount + 1):
        for coin in coins:
            if(i - coin < 0):
                continue
            dp[i] = min(dp[i],1 + dp[i - coin])
    
    return -1 if dp[amount] == amount + 1 else dp[amount]

def permute(nums): 
    res = []
    
    def backtrack(track = []):
        if(len(track) == len(nums)):
            res.append(track[:])
            return
        
        for i in nums:
            if i in track:
                continue
            track.append(i)
            backtrack(track)
            track.remove(i)
    
    def backtrack_swap(first = 0):
        if first == len(nums):
            res.append(nums[:])

        for i in range(first,len(nums)):
            nums[first],nums[i] = nums[i],nums[first]
            backtrack_swap(first + 1)
            nums[first],nums[i] = nums[i],nums[first]

    # backtrack()
    backtrack_swap()

    return res

if __name__ == "__main__":
    coins = [2,5,10]
    # r = coin_change(coins,23)
    # print(r)

    res = permute(coins)
    print(res)

