def checker_O2(opcodes_list):
    """
    given a list of opcodes checks that the 
    """
    filtered_l = list(filter(lambda s: any(s.startswith(x)
                      for x in "34578"), opcodes_list))
    format_l = list(map(lambda s: s[0], filtered_l))
    correct_indexes = []

    for i in range(len(format_l)):

        if format_l[i] == "3":
            found_else = False
            found_endif = False
            indent_level = 0

            for j in range(i+1, len(format_l)):
                if format_l[j] == "3":
                    indent_level += 1
                elif format_l[j] == "4" and indent_level == 0:
                    # its his else
                    found_else = True
                    correct_indexes.append(j)
                elif format_l[j] == "5":
                    if indent_level == 0:
                        # its his endif
                        if not found_else:
                            return False
                        found_endif = True
                        correct_indexes.append(j)
                        break
                    else:
                        indent_level -= 1

            if not found_else or not found_endif:
                return False

        elif format_l[i] == "7":
            indent_level = 0
            found_endwhile = False

            for j in range(i+1, len(format_l)):
                if format_l[j] == "7":
                    indent_level += 1
                elif format_l[j] == "8":
                    if indent_level == 0:
                        found_endwhile = True
                        correct_indexes.append(j)
                        break
                    else:
                        indent_level -= 1

            if not found_endwhile:
                return False

        else:
            if not i in correct_indexes:
                return False

    return True


def checker(opcodes_list):
    filtered_l = list(filter(lambda s: any(s.startswith(x)
                      for x in "34578"), opcodes_list))
    format_l = list(map(lambda s: s[0], filtered_l))

    if_stack = []
    else_stack = []
    while_stack = []
    op_stack = []  # an if cannot interrupt a while and viceversa

    for opc in format_l:
        print(if_stack, else_stack, while_stack, op_stack)
        if opc == "3":
            if_stack.append(opc)
            op_stack.append(opc)
        elif opc == "4":
            else_stack.append(opc)
            if len(else_stack) > len(if_stack):
                return False
        elif opc == "7":
            while_stack.append(opc)
            op_stack.append(opc)

        elif opc == "5":

            if not if_stack or not else_stack:
                return False

            if op_stack[-1] == "7":
                return False

            if_stack.pop()
            else_stack.pop()
            op_stack.pop()

        elif opc == "8":
            if not while_stack:
                return False

            if op_stack[-1] == "3":
                return False

            while_stack.pop()
            op_stack.pop()

    if if_stack or else_stack or while_stack:
        return False
    return True


"""
tests = [
    ["00", "3POE&CEF", "10", "4", "3", "4", "7",
     "8", "5", "5", "7POE|CEF", "10", "2", "8"],

    list(map(str, [3, 4, 5, 3, 7, 8, 4, 3, 4, 5, 5])),

    list(map(str, [7, 3, 7, 3, 4, 5, 8, 4, 3, 4, 5, 5, 8])),

    list(map(str, [7, 3, 7, 8, 4, 3, 4, 7, 8, 3, 4, 5, 5, 5, 8])),

]

for t in tests:
    print("opcl={}".format(t))
    assert checker(t)

fail_tests = [
    list(map(str, [4, 5, 8, 7])),

    list(map(str, [7, 3, 7, 3, 4, 5, 8, 4, 3, 4, 5, 5, 5, 8])),
    list(map(str, [7, 4, 3, 5, 8])),

    list(map(str, [7, 3, 4, 5, 5, 8])),
    list(map(str, [7, 3, 4, 8, 5])),



]

for t in fail_tests:
    assert not checker(t)
"""
