import os
import glob
from collections import defaultdict, Counter
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def parse_conll(filepath):
    distances = []
    deprels = Counter()
    feats_counts = {'gen': Counter(), 'num': Counter(), 'case': Counter()}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            cols = line.strip().split('\t')
            if len(cols) != 10:
                continue
            
            try:
                id_val = int(cols[0])
                head_val = int(cols[6])
            except ValueError:
                continue
            
            deprel = cols[7]
            feats_str = cols[5]
            
            if head_val > 0:
                dist = abs(id_val - head_val)
                distances.append(dist)
            
            deprels[deprel] += 1
            
            if feats_str and feats_str != '_':
                feats_list = feats_str.split('|')
                for feat in feats_list:
                    if '-' in feat:
                        k, v = feat.split('-', 1)
                        if k in feats_counts and v and v != '_':
                            feats_counts[k][v] += 1

    return distances, deprels, feats_counts

def process():
    telugu_file = '/home/vivek/python/LD3/Assignments/3/telugu_treebank-master/iiit_hcu_intra_chunk_v1.conll'
    hindi_files = glob.glob('/home/vivek/python/LD3/Assignments/3/HDTB_pre_release_version-0.05/IntraChunk/CoNLL/utf/**/*.dat', recursive=True)
    
    print("Parsing Telugu...")
    tel_dist, tel_deprel, tel_feats = parse_conll(telugu_file)
    
    print("Parsing Hindi...")
    hin_dist = []
    hin_deprel = Counter()
    hin_feats = {'gen': Counter(), 'num': Counter(), 'case': Counter()}
    for hf in hindi_files:
        d, r, f = parse_conll(hf)
        hin_dist.extend(d)
        hin_deprel.update(r)
        for k in hin_feats:
            hin_feats[k].update(f[k])
            
    with open('part1_output.txt', 'w', encoding='utf-8') as out:
        out.write("==== PART 1: Python Data Analysis ====\n\n")
        
        # 1. Dependency Distances
        out.write("1. Dependency Distances\n")
        out.write(f"Telugu: Mean = {np.mean(tel_dist):.4f}, Median = {np.median(tel_dist)}\n")
        out.write(f"Hindi: Mean = {np.mean(hin_dist):.4f}, Median = {np.median(hin_dist)}\n\n")
        
        plt.figure(figsize=(10, 5))
        plt.hist(tel_dist, bins=range(0, 30), alpha=0.5, label='Telugu', color='blue', density=True)
        plt.hist(hin_dist, bins=range(0, 30), alpha=0.5, label='Hindi', color='green', density=True)
        plt.xlabel("Dependency Distance")
        plt.ylabel("Density")
        plt.legend()
        plt.title("Dependency Distance Distribution")
        plt.savefig('/home/vivek/python/LD3/Assignments/3/dep_dist_hist.png')
        plt.close()
        
        # 2. Dependency relations
        out.write("2. Top 10 Dependency Relations\n")
        out.write("Telugu:\n")
        for k, v in tel_deprel.most_common(10):
            out.write(f"  {k}: {v}\n")
        out.write("Hindi:\n")
        for k, v in hin_deprel.most_common(10):
            out.write(f"  {k}: {v}\n")
        out.write("\n")
        
        # 4. Significance Testing
        t_stat, p_val = stats.ttest_ind(tel_dist, hin_dist, equal_var=False)
        out.write(f"4. Significance Testing on Dependency Distances\n")
        out.write(f"T-statistic = {t_stat:.4f}, P-value = {p_val:.4e}\n\n")
        
        # 5. Morphological Feats
        out.write("5. Morphological Features Summary\n")
        for feat in ['gen', 'num', 'case']:
            out.write(f"Feature: {feat.capitalize()}\n")
            out.write("Telugu Top:\n")
            for k, v in tel_feats[feat].most_common():
                out.write(f"  {k}: {v}\n")
            out.write("Hindi Top:\n")
            for k, v in hin_feats[feat].most_common():
                out.write(f"  {k}: {v}\n")
            out.write("\n")

if __name__ == '__main__':
    process()
