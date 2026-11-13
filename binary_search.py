def find_number(sorted_nums, target):
    left = 0
    right = len(sorted_nums) - 1

    while left <= right:
        # TODO 1: Find the middle index
        mid = (left + right) // 2

        # TODO 2: Check if the middle element is the target
        if sorted_nums[mid] == target:
            return mid

        # TODO 3: Search the right half
        elif sorted_nums[mid] < target:
            left = mid + 1

        # TODO 4: Search the left half
        else:
            right = mid - 1

    # Target not found
    return -1