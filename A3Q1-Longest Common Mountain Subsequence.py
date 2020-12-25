import sys

def extract_common(l1, l2):

    ''' Extract the common values between two sequences '''

    common = []
    for val_1 in l1:
        for val_2 in l2:
            if val_1 == val_2:
                common.append(val_1)
                break
    return common

def longest_increasing(array):

    ''' Find the longest increasing subsequence of a sequence '''

    output = [1]*len(array)

    for m in range(1, len(array)):
        for n in range(m):
            if array[n] < array[m]:
                output[m] = max(output[m], output[n] + 1)

    return output

def longest_mountain_sequence(sequence):

    ''' Find the longest common mountain subsequence of a sequence '''

    left_to_right = longest_increasing(sequence)
    sequence.reverse()
    right_to_left = longest_increasing(sequence)
    right_to_left.reverse()
    sequence.reverse()

    return max([x + y - 1 for (x, y) in zip(left_to_right, right_to_left)])

def LCMS(a, b):

    ''' The time complexity of this algorithm is
    O(mn) -- extract common factors from two sequences(with length m and n respectively, we assume m >= n) +
    O(mn) -- construct a LCS table +
    O(m+n) -- reconstruct the longest common subsequence from LCS table +
    O(n^2) -- find the longest common mountain subsequence of a sequence
    i.e O(mn + mn + m + n + n^2) = O(n^2)
    '''

    common_a = extract_common(a, b)
    common_b = extract_common(b, common_a)

    a, b = (common_b, common_a) if len(a) < len(b) else (common_a, common_b)

    # construct a LCS table
    m, n = len(a), len(b)
    c = [[0]*(n+1) for q in range(m+1)]

    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                c[i+1][j+1] = c[i][j]+1

            else:
                c[i+1][j+1] = max(c[i][j+1], c[i+1][j])

    # reconstruct the longest common subsequence from LCS table
    longest_subsequence = []
    i, j = m, n
    while i > 0 and j > 0:

        if a[i-1] == b[j-1]:
            longest_subsequence.append(int(a[i-1], 16))
            i -= 1
            j -= 1

        else:
            if c[i-1][j] >= c[i][j-1]:
                i -= 1
            else:
                j -= 1

    return longest_subsequence

num_pair = int(sys.stdin.readline())
for _ in range(num_pair):
    a = sys.stdin.readline().split()
    b = sys.stdin.readline().split()

    lcs = LCMS(a, b)
    print(len(lcs) if (len(lcs) == 0 or len(lcs) == 1) else longest_mountain_sequence(lcs))

