SH = 0
LA = 1
RA = 2


def has_head(node, arcs):
    return any(d == node for (_, d, _) in arcs)


def transition(trans, stack, buffer, arcs):
    """Apply one arc-standard transition.

    Representation matches the starter code conventions:
    - stack[0] is top
    - buffer[0] is next
    """
    action, label = trans
    if action == SH:
        if not buffer:
            return stack, buffer, arcs
        stack.insert(0, buffer.pop(0))
        return stack, buffer, arcs

    if action == LA:
        # Add (s1 -> s0) and pop s0
        if len(stack) < 2:
            return stack, buffer, arcs
        s0 = stack[0]
        s1 = stack[1]
        arcs.append((s1, s0, label))
        stack.pop(0)
        return stack, buffer, arcs

    if action == RA:
        # Add (s0 -> s1) and pop s1 (i.e., remove the second item)
        if len(stack) < 2:
            return stack, buffer, arcs
        s0 = stack[0]
        s1 = stack[1]
        arcs.append((s0, s1, label))
        stack.pop(1)
        return stack, buffer, arcs

    raise ValueError(f"Unknown transition action: {action}")


def oracle(stack, buffer, gold_heads, gold_labels, arcs):
    """Static oracle for arc-standard.

    Standard condition: if stack has (s1, s0) on top, we can:
    - LEFT-ARC when gold_head[s0] == s1 and all gold dependents of s0 are already attached.
    - RIGHT-ARC when gold_head[s1] == s0 and all gold dependents of s1 are already attached.
    Else SHIFT.
    """
    if len(stack) < 2:
        return (SH, "_")
    s0 = stack[0]
    s1 = stack[1]

    # Helper: does x have any gold dependents not yet attached (still in stack/buffer)?
    def has_unprocessed_gold_dependents(x):
        remaining = set(stack[1:]) | set(buffer)
        return any(gold_heads[k] == x for k in remaining)

    if s0 != 0 and gold_heads[s0] == s1 and not has_unprocessed_gold_dependents(s0):
        return (LA, gold_labels[s0])

    if s1 != 0 and gold_heads[s1] == s0 and not has_unprocessed_gold_dependents(s1):
        return (RA, gold_labels[s1])

    if buffer:
        return (SH, "_")

    # Buffer empty but no oracle condition matched (typically non-projective / inconsistent).
    # Fall back to a deterministic action to guarantee termination.
    if s1 != 0 and not has_head(s1, arcs):
        return (RA, gold_labels[s1])
    if s0 != 0 and not has_head(s0, arcs):
        return (LA, gold_labels[s0])
    return (RA, "dep")
