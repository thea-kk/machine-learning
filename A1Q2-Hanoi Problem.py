import sys


def determine_direction(n, begin, end):
    ''' Rationale: the moving direction of disk 1 is opposite to
    the moving direction of the biggest disk that is not on the destination peg if it is an even number disk;
    if it is an odd number disk, their moving directions are the same。
    '''

    direction = ''
    if (end - begin == 1) or (end - begin == -2):

        if (n % 2) == 0:
            direction = 'counterclockwise'
        else:
            direction = 'clockwise'
    else:

        if (n % 2) == 0:
            direction = 'clockwise'
        else:
            direction = 'counterclockwise'

    return direction


def check_impossible(disk):
    ''' Rationale: if there are two consecutive odd number disks OR
    two consecutive even number disks on the same peg, then it is impossible to reach
    the final stage based on the rules.
    '''

    global IMPOSSIBLE

    for peg in disk:
        remainder = []
        for num in peg:
            remainder.append(num % 2)

            if len(remainder) == 2:

                if len(set(remainder)) == 1:
                    IMPOSSIBLE = True

                else:
                    del remainder[0]


def hanoi_info(disk):
    ''' Collect the information about the initial stage of the disk.
    E.g. the total number of disks, the destination of all disks, the moving direction of disk 1
    '''

    # odd_even (a flag) : to check if the first moving disk is found (i.e. 1: no found, 0: found)
    # biggest_n: a list of disks representing the maximum value on each peg
    disk_info = {'total_disk': 0, 'destination': 0, 'odd_even': 1, 'direction': '', 'biggest_n': []}
    disk_info[0] = disk_info['destination']

    for peg in disk:

        if peg:
            disk_info['biggest_n'].append(max(peg))

            if disk_info['total_disk'] < max(peg):
                disk_info['total_disk'] = max(peg)
                disk_info['destination'] = disk.index(peg)

        for num in peg:
            disk_info[num] = disk.index(peg)

    # determine moving direction of disk 1
    if len(disk_info['biggest_n']) > 1:
        disk_info['biggest_n'].sort()
        disk_info['direction'] = determine_direction(disk_info['biggest_n'][-2], disk_info[disk_info['biggest_n'][-2]],
                                                     disk_info[disk_info['biggest_n'][-1]])

    del disk_info['biggest_n']

    return disk_info


def tower_hanoi(n, begin, end, info, disk):
    ''' The time complexity of this algorithm can be concluded into a function, T(n) = T(n-1) + 2n + c (where c > 1).
    By using the substitution method, we can work out that O(n) = n^2.
    '''
    global COUNT, START, IMPOSSIBLE

    if n == 0:
        return

    if begin == end:
        # disk n is already on the destination peg
        # Next step: move disk n-1 to the destination peg
        tower_hanoi(n - 1, info[n - 1], end, info, disk)

    else:
        # disk n is not on the destination peg
        # Next step: move disk 1 to disk n-1 to the auxiliary peg
        tower_hanoi(n - 1, info[n - 1], 3 - begin - end, info, disk)

        # check the possibility of current state after each movement
        check_impossible(disk)

        # find the first moving disk
        if info['odd_even']:

            info['odd_even'] = 0

            if n == 1:
                START = 'odd'

            else:
                START = 'even'

        # move disk 1 to disk n to the destination peg, which involves 2^(n-1)-1+1 move
        for i in range(1, n + 1):
            disk[info[i]].remove(i)
            info[i] = end
        disk[end].extend(range(1, n + 1))
        disk[end].sort()
        COUNT += 2 ** (n - 1)


pegs = {0: 'A', 1: 'B', 2: 'C'}
num_line = int(sys.stdin.readline())
for _ in range(num_line):
    disk = [[int(t) for t in s.split()] for s in sys.stdin.readline().split(',')]
    COUNT = 0
    START = ''
    IMPOSSIBLE = False
    about_disk = hanoi_info(disk)
    tower_hanoi(about_disk['total_disk'], about_disk['destination'], about_disk['destination'], about_disk, disk)

    if IMPOSSIBLE:
        result = 'impossible'
    elif COUNT == 0:
        result = ' '.join((pegs[about_disk['destination']], str(COUNT)))
    else:
        result = ' '.join((pegs[about_disk['destination']], str(COUNT), START, about_disk['direction']))

    print(result)