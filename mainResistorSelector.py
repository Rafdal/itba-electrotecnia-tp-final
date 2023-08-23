import itertools

e12series = ['10','12','15','18','22','27','33','39','47','56','68','82']



powerExpRange = range(-3, 4)

def find_closest_combination(target_num):
    closest_combination = None
    closest_diff = float('inf')
    for r in range(2, len(e12series) + 1):
        for combination in itertools.combinations_with_replacement(e12series, r):
            combination_num = sum(map(int, combination))
            for i in powerExpRange:
                num = combination_num * (10 ** i)
                diff = abs(target_num - num)
                if diff < closest_diff:
                    closest_combination = combination
                    closest_diff = diff
                    closest_power = i
                elif diff == 0:
                    return combination, i
    return closest_combination, closest_power

def find_efficient_combination(target_num):
    efficient_combination = None
    efficient_count = float('inf')
    for r in range(2, len(e12series) + 1):
        for combination in itertools.combinations_with_replacement(e12series, r):
            combination_num = sum(map(int, combination))
            for i in powerExpRange:
                num = combination_num * (10 ** i)
                if num == target_num:
                    if len(combination) < efficient_count:
                        efficient_combination = combination
                        efficient_count = len(combination)
                        efficient_power = i
                    elif len(combination) == efficient_count:
                        if combination.count(combination[0]) < efficient_combination.count(efficient_combination[0]):
                            efficient_combination = combination
                            efficient_power = i
                    else:
                        break
            else:
                continue
            break
        else:
            continue
        break
    return efficient_combination, efficient_power

target_num = 5100
closest_combination, closest_power = find_closest_combination(target_num)
efficient_combination, efficient_power = find_efficient_combination(target_num)
print(f"The closest combination to {target_num} is {closest_combination} with a power multiplier of 10^{closest_power}")
print(f"The most efficient combination to {target_num} is {efficient_combination} with a power multiplier of 10^{efficient_power}")