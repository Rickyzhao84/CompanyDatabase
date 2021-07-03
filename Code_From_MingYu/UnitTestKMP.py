from KMP import KMP


def test():
    p1 = "aa"
    t1 = "aaaaaaaa"

    kmp = KMP()
    assert(kmp.search(t1, p1) == [0, 1, 2, 3, 4, 5, 6])

    p2 = ["ab", 'c']
    t2 = ['ab', 'd', 'ab', 'e', 'abf', 'ab', "c"]

    assert(kmp.search(t2, p2) == [5])

    p3 = "aab"
    t3 = "aaabaacbaab"

    assert(kmp.search(t3, p3) == [1, 8])

    print("all test pass")

test()
