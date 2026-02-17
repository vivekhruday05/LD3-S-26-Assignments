SH = 0
RE = 1
RA = 2
LA = 3


def has_head(node, arcs):
    return any(d == node for (_, d, _) in arcs)


def transition(trans, stack, buffer, arcs):
    """Apply one arc-eager transition.

    Configuration representation follows the assignment/starter code:
    - stack: list[int] where stack[0] is TOP
    - buffer: list[int] where buffer[0] is NEXT
    - arcs: list[tuple[int,int,str]]
    """
    action, label = trans
    if action == SH:
        if not buffer:
            return stack, buffer, arcs
        stack.insert(0, buffer.pop(0))
        return stack, buffer, arcs

    if action == RE:
        if stack:
            stack.pop(0)
        return stack, buffer, arcs

    if action == RA:
        if not stack or not buffer:
            return stack, buffer, arcs
        head = stack[0]
        dep = buffer[0]
        arcs.append((head, dep, label))
        stack.insert(0, buffer.pop(0))
        return stack, buffer, arcs

    if action == LA:
        if not stack or not buffer:
            return stack, buffer, arcs
        dep = stack[0]
        head = buffer[0]
        arcs.append((head, dep, label))
        stack.pop(0)
        return stack, buffer, arcs

    raise ValueError(f"Unknown transition action: {action}")


def oracle(stack, buffer, gold_heads, gold_labels, arcs):
    """Static oracle for arc-eager (Goldberg & Nivre, 2012; Algorithm 1).

    Returns a (action, label) pair where label is '_' for SH/RE.
    """
    if not buffer:
        return (RE, "_")
    if not stack:
        return (SH, "_")

    i = stack[0]  # TOP
    j = buffer[0]  # NEXT

    # LEFT-ARC if NEXT is the gold head of TOP.
    if i != 0 and gold_heads[i] == j and not has_head(i, arcs):
        return (LA, gold_labels[i])

    # RIGHT-ARC if TOP is the gold head of NEXT.
    if gold_heads[j] == i and not has_head(j, arcs):
        return (RA, gold_labels[j])

    # REDUCE if TOP already has a head, and TOP has no remaining gold dependents in buffer.
    if i != 0 and has_head(i, arcs):
        if all(gold_heads[k] != i for k in buffer):
            return (RE, "_")

    return (SH, "_")
