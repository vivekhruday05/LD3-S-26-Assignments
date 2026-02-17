import sys

SH = 0; RE = 1; RA = 2; LA = 3;

# Default to arc-eager so importing this module works.
import arc_eager as _default_sys
system_transition = _default_sys.transition
system_oracle = _default_sys.oracle
system_name = "arc-eager"

labels = ["nsubj", "csubj", "nsubjpass", "csubjpass", "dobj", "iobj", "ccomp", "xcomp", "nmod", "advcl", "advmod", "neg", "aux", "auxpass", "cop", "mark", "discourse", "vocative", "expl", "nummod", "acl", "amod", "appos", "det", "case", "compound", "mwe", "goeswith", "name", "foreign", "conj", "cc", "punct", "list", "parataxis", "remnant", "dislocated", "reparandum", "root", "dep", "nmod:npmod", "nmod:tmod", "nmod:poss", "acl:relcl", "cc:preconj", "compound:prt"]

def read_sentences():
    sentence = []
    sentences = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            sentences.append(sentence)
            sentence = []
        elif line[0] != "#":
            token = line.split("\t")
            sentence.append(token)
    return(sentences)

def attach_orphans(arcs, n):
    attached = []
    for (h, d, l) in arcs:
        attached.append(d)
    for i in range(1, n):
        if not i in attached:
            arcs.append((0, i, "root"))

def print_tab(arcs, words, tags):
    hs = {}
    ls = {}
    for (h, d, l) in arcs:
        hs[d] = h
        ls[d] = l
    for i in range(1, len(words)):
        print("\t".join([words[i], tags[i], str(hs[i]), ls[i]]))
    print()
        
def print_tree(root, arcs, words, indent):
    if root == 0:
        print(" ".join(words[1:]))
    children = [(root, i, l) for i in range(len(words)) for l in labels if (root, i, l) in arcs]
    for (h, d, l) in sorted(children):
        print(indent + l + "(" + words[h] + "_" + str(h) + ", " + words[d] + "_" + str(d) + ")")
        print_tree(d, arcs, words, indent + "  ")

def transition(trans, stack, buffer, arcs):
    # Backwards-compatible wrapper around the selected transition system.
    return system_transition(trans, stack, buffer, arcs)

def oracle(stack, buffer, heads, labels, arcs):
    # Backwards-compatible wrapper around the selected oracle.
    return system_oracle(stack, buffer, heads, labels, arcs)

def parse(sentence):
    sentence.insert(0, ("root", "_", "0", "_"))
    words = [sentence[i][0] for i in range(len(sentence))]
    tags = [sentence[i][1] for i in range(len(sentence))]
    heads = [int(sentence[i][2]) for i in range(len(sentence))]
    labels = [sentence[i][3] for i in range(len(sentence))]
    stack = [0]
    buffer = [x for x in range(1, len(words))]
    arcs = []

    max_steps = 10 * (len(words) + 1) ** 2
    steps = 0
    if system_name == "arc-standard":
        while (buffer or len(stack) > 1) and steps < max_steps:
            trans = system_oracle(stack, buffer, heads, labels, arcs)
            prev = (tuple(stack), tuple(buffer), len(arcs))
            stack, buffer, arcs = system_transition(trans, stack, buffer, arcs)
            if (tuple(stack), tuple(buffer), len(arcs)) == prev:
                break
            steps += 1
    else:
        while buffer and steps < max_steps:
            trans = system_oracle(stack, buffer, heads, labels, arcs)
            prev = (tuple(stack), tuple(buffer), len(arcs))
            stack, buffer, arcs = system_transition(trans, stack, buffer, arcs)
            if (tuple(stack), tuple(buffer), len(arcs)) == prev:
                break
            steps += 1
    attach_orphans(arcs, len(words))
    if tab_format:
        print_tab(arcs, words, tags)
    else:
        print_tree(0, arcs, words, "")

if __name__ == "__main__":
    # CLI (keeps assignment-required usage working):
    #   python3 oracle.py < example.tab
    #   python3 oracle.py tab < example.tab
    # Extra credit:
    #   python3 oracle.py tab arc-standard < example.tab
    args = set(sys.argv[1:])
    tab_format = "tab" in args

    system_name = "arc-standard" if ("arc-standard" in args or "arc_standard" in args) else "arc-eager"

    if system_name == "arc-standard":
        import arc_standard as _sys
        system_transition = _sys.transition
        system_oracle = _sys.oracle
    else:
        import arc_eager as _sys
        system_transition = _sys.transition
        system_oracle = _sys.oracle

    for sentence in read_sentences():
        parse(sentence)
