strategy3_1f = False
if mines(icoord) - mines((tx, ty)) == 0 and len(same) == len(empties1):
    print("--------------\n strategy3.1, click", icoord, (tx, ty))
    for e in empties2:
        if e not in same:
             print(e)
             click(e)
             get_map(e)
    return True