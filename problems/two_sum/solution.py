def twoSum(nums, target):
    mapa = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in mapa: return [mapa[diff], i]
        mapa[n] = i
