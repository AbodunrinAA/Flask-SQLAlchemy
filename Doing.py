from math import sqrt


def sort_by_last_letter(arg):
    def last_letter(s):
        return s[-1]
    return sorted(arg, key=last_letter, reverse=True)


def raise_to_power(arg):
    def power(x):
        return pow(x, arg)
    return power

