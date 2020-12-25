import sys

def all_poss(options, recharge, seg_cost):

    new_option = []
    for p_cost, ending_batt, prev_mode in options:

        # petrol mode
        p_new_cost = p_cost + seg_cost
        p_new_batt = min(100, ending_batt + recharge - (prev_mode != 0))
        new_option.append([p_new_cost, p_new_batt, 0])

        # battery mode
        if (ending_batt >= 11) or ((ending_batt >= 10) and (prev_mode == 1)):
            b_new_batt = ending_batt - seg_cost - (prev_mode != 1)
            new_option.append([p_cost, b_new_batt, 1])

    return new_option


def optimized(new_option):

    i = 0
    while i < len(new_option) - 1:

        petrol_1, current_batt_1, mode_1 = new_option[i]

        j = i + 1
        while j < len(new_option):
            petrol_2, current_batt_2, mode_2 = new_option[j]

            if mode_1 == mode_2:
                # discard those options with higher petrol cost and less battery left
                if petrol_1 >= petrol_2 and current_batt_1 <= current_batt_2:
                    new_option.pop(i)
                    break

                elif petrol_2 >= petrol_1 and current_batt_2 <= current_batt_1:
                    new_option.pop(j)

            # i: battery, j: petrol
            elif mode_1 == 1 and mode_2 == 0:
                # as you need the starting point to be the same in the next segment
                # put - 1 at the end to switch battery from petrol or the other way around to achieve that
                if petrol_1 >= petrol_2 and current_batt_1 <= current_batt_2 - 1:
                    new_option.pop(i)
                    break

                elif petrol_2 >= petrol_1 and current_batt_2 <= current_batt_1 - 1:
                    new_option.pop(j)

            j += 1
        i += 1

    return new_option

def driving_mode(batt, num_seg, data):

    recharge = [0.1 * num[0] * num[1] for num in data]
    seg_cost = [0.2 * val[0] for val in data]
    # store an option in format: [total cost of petrol, battery left, chosen mode]
    final_options = [[0, batt, -1]]

    # 0: petrol, 1: battery
    for seg in range(num_seg):
        # list all possibilities
        available_options = all_poss(final_options, recharge[seg], seg_cost[seg])

        # filter available possibilities
        final_options = optimized(available_options)

    # calculate the minimum cost
    min_cost = sum(seg_cost)
    for cost_p, b_level, mode in final_options:
        cost = cost_p + max(0, batt - b_level)
        if cost < min_cost:
            min_cost = cost

    return min_cost

num_line = int(sys.stdin.readline())
for _ in range(num_line):
    s = sys.stdin.readline().split()
    batt, num_seg = float(s[0]), int(s[1])
    data = []
    for i in range(num_seg):
        data.append([float(t) for t in s[i + 2].split(':')])
    # print(driving_mode(batt, num_seg, data))
    print('%.2f' % driving_mode(batt, num_seg, data))