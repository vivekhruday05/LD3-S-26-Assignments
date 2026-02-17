import argparse


def read_sentences(path):
    sentences = []
    sentence = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                sentence = []
            elif line[0] != "#":
                sentence.append(line.split("\t"))
    if sentence:
        sentences.append(sentence)
    return sentences


def attach_orphans(arcs, n):
    attached = {d for (_, d, _) in arcs}
    for i in range(1, n):
        if i not in attached:
            arcs.append((0, i, "root"))


def arcs_to_heads_labels(arcs, n):
    heads = [0] * n
    labels = ["_"] * n
    for h, d, l in arcs:
        if 0 <= d < n:
            heads[d] = h
            labels[d] = l
    return heads, labels


def parse_with_oracle(sentence, system_name):
    sentence = [("root", "_", "0", "_")] + [tuple(tok) for tok in sentence]
    words = [sentence[i][0] for i in range(len(sentence))]
    tags = [sentence[i][1] for i in range(len(sentence))]
    gold_heads = [int(sentence[i][2]) for i in range(len(sentence))]
    gold_labels = [sentence[i][3] for i in range(len(sentence))]

    if system_name == "arc-standard":
        import arc_standard as sysmod
    else:
        import arc_eager as sysmod

    stack = [0]
    buffer = [i for i in range(1, len(words))]
    arcs = []

    # Safety bound to avoid infinite loops on unexpected data.
    max_steps = 10 * (len(words) + 1) ** 2
    steps = 0
    if system_name == "arc-standard":
        while (buffer or len(stack) > 1) and steps < max_steps:
            trans = sysmod.oracle(stack, buffer, gold_heads, gold_labels, arcs)
            prev = (tuple(stack), tuple(buffer), len(arcs))
            stack, buffer, arcs = sysmod.transition(trans, stack, buffer, arcs)
            if (tuple(stack), tuple(buffer), len(arcs)) == prev:
                break
            steps += 1
    else:
        while buffer and steps < max_steps:
            trans = sysmod.oracle(stack, buffer, gold_heads, gold_labels, arcs)
            prev = (tuple(stack), tuple(buffer), len(arcs))
            stack, buffer, arcs = sysmod.transition(trans, stack, buffer, arcs)
            if (tuple(stack), tuple(buffer), len(arcs)) == prev:
                break
            steps += 1

    attach_orphans(arcs, len(words))
    pred_heads, pred_labels = arcs_to_heads_labels(arcs, len(words))

    return {
        "words": words,
        "tags": tags,
        "gold_heads": gold_heads,
        "gold_labels": gold_labels,
        "pred_heads": pred_heads,
        "pred_labels": pred_labels,
    }


def main():
    ap = argparse.ArgumentParser(description="Evaluate oracle-derived trees vs gold (.tab format).")
    ap.add_argument("tab_file", help="Path to a .tab file (blank-line separated sentences).")
    ap.add_argument("--system", choices=["arc-eager", "arc-standard"], default="arc-eager")
    ap.add_argument("--show", type=int, default=5, help="Show up to N example mismatches.")
    args = ap.parse_args()

    sentences = read_sentences(args.tab_file)
    total = 0
    uas_ok = 0
    las_ok = 0
    shown = 0

    for sent in sentences:
        parsed = parse_with_oracle(sent, args.system)
        words = parsed["words"]
        gold_h = parsed["gold_heads"]
        gold_l = parsed["gold_labels"]
        pred_h = parsed["pred_heads"]
        pred_l = parsed["pred_labels"]

        for i in range(1, len(words)):
            total += 1
            if pred_h[i] == gold_h[i]:
                uas_ok += 1
                if pred_l[i] == gold_l[i]:
                    las_ok += 1
            elif shown < args.show:
                shown += 1
                print("Mismatch:")
                print("  sent:", " ".join(words[1:]))
                print(f"  token: {i}\t{words[i]}")
                print(f"  gold:  head={gold_h[i]} label={gold_l[i]}")
                print(f"  pred:  head={pred_h[i]} label={pred_l[i]}")
                print()

    uas = (uas_ok / total) if total else 0.0
    las = (las_ok / total) if total else 0.0
    print(f"System: {args.system}")
    print(f"Tokens: {total}")
    print(f"UAS: {uas:.4f} ({uas_ok}/{total})")
    print(f"LAS: {las:.4f} ({las_ok}/{total})")


if __name__ == "__main__":
    main()
