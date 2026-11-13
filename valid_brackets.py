def is_valid_brackets(text):
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}

    for char in text:
        # TODO 1: Check for opening brackets
        if char in ("(", "{", "["):
            stack.append(char)

        # TODO 2: Check for closing brackets
        elif char in pairs:
            if not stack:
                return False

            top = stack.pop()

            if top != pairs[char]:
                return False

    # TODO 3: All brackets must be matched
    return len(stack) == 0
