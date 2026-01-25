#!/usr/bin/env python3
"""
Hindi Dependency Treebank Analysis
Linguistic Data 3 - Assignment on Descriptive Analysis of Hindi Data
"""

import os
import re
import statistics
from collections import defaultdict, Counter
from pathlib import Path
import matplotlib.pyplot as plt

class TreebankAnalyzer:
    """Analyzer for Hindi Dependency Treebank (HDTB) in CoNLL format"""
    
    def __init__(self, data_dir):
        """Initialize analyzer with path to treebank data"""
        self.data_dir = data_dir
        self.sentences = []
        self.all_tokens = []
        self.word_types = set()
        
    def load_data(self):
        """Load all CoNLL formatted data files"""
        print("Loading treebank data...")
        
        # Use InterChunk CoNLL wx format
        data_paths = [
            Path(self.data_dir) / "InterChunk" / "CoNLL" / "wx",
            Path(self.data_dir) / "IntraChunk" / "CoNLL" / "wx"
        ]
        
        for data_path in data_paths:
            if not data_path.exists():
                continue
                
            # Find all .dat files
            for dat_file in data_path.rglob("*.dat"):
                try:
                    self._parse_conll_file(dat_file)
                except Exception as e:
                    print(f"Error processing {dat_file}: {e}")
        
        print(f"Loaded {len(self.sentences)} sentences")
        print(f"Total tokens: {len(self.all_tokens)}")
        print()
    
    def _parse_conll_file(self, filepath):
        """Parse a single CoNLL formatted file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            current_sentence = []
            
            for line in f:
                line = line.strip()
                
                if not line:
                    # Empty line marks end of sentence
                    if current_sentence:
                        self.sentences.append(current_sentence)
                        current_sentence = []
                else:
                    # Parse token line
                    try:
                        token = self._parse_token_line(line)
                        if token:
                            current_sentence.append(token)
                            self.all_tokens.append(token)
                    except:
                        pass
            # Handle last sentence if file doesn't end with newline
            if current_sentence:
                self.sentences.append(current_sentence)
    
    def _parse_token_line(self, line):
        """Parse a single token line from CoNLL format"""
        parts = line.split('\t')
        
        if len(parts) < 8:
            return None
        
        try:
            token_id = int(parts[0])
        except ValueError:
            return None

        word = parts[1]
        lemma = parts[2]
        pos_short = parts[3]
        pos_full = parts[4]
        morph = parts[5]
        parent_id = int(parts[6]) if parts[6] != '_' else 0
        deprel = parts[7]
        
        # Skip punctuation for analysis
        if pos_short == 'SYM' or pos_full == 'SYM':  
            return None
        
        token = {
            'id': token_id,
            'word': word,
            'lemma': lemma,
            'pos_short': pos_short,
            'pos_full': pos_full,
            'morph': morph,
            'parent_id': parent_id,
            'deprel': deprel
        }
        
        # Track word types
        self.word_types.add(word)
        
        return token
    
    def get_case_from_morph(self, morph_str):
        """Extract case feature (State) from morphological features"""
        if not morph_str or morph_str == '_':
            return None
        
        match = re.search(r'case-([^|]+)', morph_str)
        if match:
            case = match.group(1)
            if case == 'd':
                return 'unmarked' # Direct case state
            return case # Oblique, Ergative, etc.
        return None
    
    def get_vibhakti(self, morph_str):
        """Extract vibhakti (case marker suffix) from morphological features"""
        if not morph_str or morph_str == '_':
            return None
        
        match = re.search(r'vib-([^|]+)', morph_str)
        if match:
            vib = match.group(1)
            # '0' usually denotes a null marker or part of a complex marker like 0_ne
            # We treat '0' as NO visible marker
            if vib == '0': 
                return None
            return vib
        return None

    def plot_frequency_distribution(self, data_counter, title, filename, top_n=None, xlabel="Category", ylabel="Frequency"):
        """Helper to generate and save bar charts"""
        if not data_counter:
            return

        # Prepare data
        if top_n:
            common = data_counter.most_common(top_n)
            title = f"{title} (Top {top_n})"
        else:
            common = data_counter.most_common()
            
        labels = [x[0] for x in common]
        values = [x[1] for x in common]
        
        plt.figure(figsize=(12, 6))
        plt.bar(labels, values, color='skyblue', edgecolor='black')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        print(f"Saving plot to {filename}...")
        plt.savefig(filename)
        plt.close()
    
    def analyze_basic_statistics(self):
        """1. Basic Corpus Statistics"""
        print("=" * 60)
        print("1. BASIC CORPUS STATISTICS")
        print("=" * 60)
        
        total_sentences = len(self.sentences)
        total_tokens = len(self.all_tokens)
        word_types = len(self.word_types)
        
        print(f"(a) Total number of sentences: {total_sentences}")
        print(f"(b) Total number of word tokens (excluding punctuation): {total_tokens}")
        print(f"(c) Total number of word types (excluding punctuation): {word_types}")
        
        if total_sentences > 0:
            avg_length = total_tokens / total_sentences
            print(f"(d) Average sentence length: {avg_length:.2f} tokens")
        
        sentence_lengths = [len(sent) for sent in self.sentences]
        if sentence_lengths:
            print(f"(e) Minimum sentence length: {min(sentence_lengths)} tokens")
            print(f"    Maximum sentence length: {max(sentence_lengths)} tokens")
        print()

    def analyze_word_order(self):
        """2. Word Order Patterns Analysis (Dependency-aware, Hindi-safe)"""
        print("=" * 60)
        print("2. WORD ORDER PATTERNS")
        print("=" * 60)

        subject_count = 0
        object_count = 0
        main_verb_count = 0
        word_order_patterns = Counter()

        for sentence in self.sentences:
            # build index map for linear order
            idx_map = {tok['id']: i for i, tok in enumerate(sentence)}

            # identify main verb (predicate head)
            verb = next((t for t in sentence if t['deprel'] == 'main'), None)
            if not verb:
                continue

            main_verb_count += 1

            # collect auxiliaries attached to main verb
            verb_positions = [idx_map[verb['id']]]
            for tok in sentence:
                if tok['parent_id'] == verb['id'] and tok['pos_short'].startswith('V'):
                    verb_positions.append(idx_map[tok['id']])

            # take the RIGHTMOST verb element (surface verb position)
            verb_pos = max(verb_positions)

            # find subject and object linked to the verb
            subj = next((t for t in sentence if t['deprel'] == 'k1' and t['parent_id'] == verb['id']), None)
            obj  = next((t for t in sentence if t['deprel'] == 'k2' and t['parent_id'] == verb['id']), None)

            if subj:
                subject_count += 1
            if obj:
                object_count += 1

            # only count clean S–O–V sentences
            if subj and obj:
                s_pos = idx_map[subj['id']]
                o_pos = idx_map[obj['id']]

                order = sorted(
                    [('S', s_pos), ('O', o_pos), ('V', verb_pos)],
                    key=lambda x: x[1]
                )
                pattern = ''.join(x[0] for x in order)
                word_order_patterns[pattern] += 1

        # reporting
        print(f"(a) Frequencies of key dependency relations:")
        print(f"    Subject (k1): {subject_count}")
        print(f"    Object (k2): {object_count}")
        print(f"    Main verb (main): {main_verb_count}")

        print(f"\n(b) Word order patterns found:")
        total = sum(word_order_patterns.values())
        for pat, cnt in word_order_patterns.most_common():
            print(f"    {pat}: {cnt} ({(cnt/total)*100:.2f}%)")

        print(f"\n(c) Discussion:")
        if word_order_patterns:
            top = word_order_patterns.most_common(1)[0]
            print(f"    Dominant pattern: {top[0]} ({top[1]} occurrences)")
            if 'SOV' in word_order_patterns:
                print(
                    f"    SOV frequency: {word_order_patterns['SOV']} "
                    f"({(word_order_patterns['SOV']/total)*100:.2f}%)"
                )

        # plot
        self.plot_frequency_distribution(
            word_order_patterns,
            "Word Order Patterns",
            "plot_word_order.png",
            xlabel="Pattern"
        )
    def analyze_case_markers(self):
        """3. Case Marker and Vibhakti Analysis"""
        print("=" * 60)
        print("3. CASE MARKER AND VIBHAKTI ANALYSIS")
        print("=" * 60)
        
        vibhakti_distribution = Counter()
        unmarked_noun_count = 0
        total_nouns = 0
        
        for token in self.all_tokens:
            pos = token['pos_full']
            morph = token['morph']
            
            # Collect Vibhakti stats (The actual Markers)
            vib = self.get_vibhakti(morph)
            if vib:
                vibhakti_distribution[vib] += 1
            
            # Count Unmarked Nouns
            # Nouns usually include NN, NNP, NNC, NNPC
            if pos.startswith('NN'): 
                total_nouns += 1
                case = self.get_case_from_morph(morph)
                
                # Definition of Unmarked: 
                # 1. Has 'case-d' (Direct State) OR
                # 2. Has no explicit Vibhakti marker
                is_unmarked = False
                if case == 'unmarked':
                    is_unmarked = True
                elif vib is None:
                    is_unmarked = True
                
                if is_unmarked:
                    unmarked_noun_count += 1
        
        print(f"(a) All Case Markers (Vibhaktis):")
        total_vib = sum(vibhakti_distribution.values())
        
        # PRINT ALL (No Limit)
        for v, c in vibhakti_distribution.most_common():
             print(f"    {v}: {c} ({(c/total_vib)*100:.2f}%)")
             
        print(f"\n(b) Unmarked Nouns (No case marker/Direct case):")
        print(f"    Count: {unmarked_noun_count}")
        if total_nouns > 0:
            print(f"    Percentage of total nouns: {(unmarked_noun_count/total_nouns)*100:.2f}%")
        print()

        # Save Plot (Top 20 for readability)
        self.plot_frequency_distribution(
            vibhakti_distribution, 
            "Case Marker Distribution", 
            "plot_case_markers.png", 
            top_n=20, # Plot only top 20 to keep chart readable
            xlabel="Vibhakti Marker"
        )

    def analyze_intervening_distance(self):
        """4. Intervening Distance Analysis"""
        print("=" * 60)
        print("4. INTERVENING DISTANCE ANALYSIS")
        print("=" * 60)
        
        distances = []
        same_marker = []
        diff_marker = []
        
        for sentence in self.sentences:
            # Find all tokens with an explicit Case Marker (Vibhakti)
            marked_tokens = []
            for idx, token in enumerate(sentence):
                vib = self.get_vibhakti(token['morph'])
                if vib: # Only consider tokens that actually HAVE a marker
                    marked_tokens.append({'idx': idx, 'marker': vib})
            
            if len(marked_tokens) < 2:
                continue
                
            for i in range(len(marked_tokens) - 1):
                # Distance calculation excludes punctuation (already excluded from list)
                # Distance = IndexB - IndexA - 1
                dist = marked_tokens[i+1]['idx'] - marked_tokens[i]['idx'] - 1
                if dist < 0: dist = 0
                
                distances.append(dist)
                
                # Check if markers are same or different strings
                if marked_tokens[i]['marker'] == marked_tokens[i+1]['marker']:
                    same_marker.append(dist)
                else:
                    diff_marker.append(dist)
        
        if distances:
            avg_dist = sum(distances)/len(distances)
            stdev_dist = statistics.stdev(distances) if len(distances) > 1 else 0.0
            
            print(f"(a) Average intervening words between case markers: {avg_dist:.2f}")
            print(f"    Standard Deviation: {stdev_dist:.2f}")
            
            avg_same = sum(same_marker)/len(same_marker) if same_marker else 0
            avg_diff = sum(diff_marker)/len(diff_marker) if diff_marker else 0
            
            print(f"\n(b) Avg distance for SAME markers: {avg_same:.2f} (n={len(same_marker)})")
            print(f"    Avg distance for DIFFERENT markers: {avg_diff:.2f} (n={len(diff_marker)})")
            
            print(f"\n(c) Discussion:")
            if avg_same < avg_diff:
                print("    Same markers appear closer together.")
            else:
                print("    Different markers appear closer together.")

    def analyze_pos_tags(self):
        """5. POS Tag Distribution"""
        print("=" * 60)
        print("5. POS TAG DISTRIBUTION")
        print("=" * 60)
        
        # Count only fine-grained POS tags
        # To avoid double counting, we use exact matches or strict categorization [Task 5 Critical Fix]
        pos_counts = Counter(token['pos_full'] for token in self.all_tokens)
        total = len(self.all_tokens)
        
        # Define categories strictly to avoid overlapping matches
        categories = {
            'NN (Common Noun)': lambda x: x == 'NN' or x.startswith('NN:'),
            'NNP (Proper Noun)': lambda x: x.startswith('NNP'), # Includes NNPC
            'VM (Main Verb)': lambda x: x.startswith('VM'),
            'JJ (Adjective)': lambda x: x.startswith('JJ'),
            'PRP (Pronoun)': lambda x: x.startswith('PRP'),
            'PSP (Postposition)': lambda x: x.startswith('PSP'),
            'CC (Conjunction)': lambda x: x.startswith('CC'),
        }
        
        category_counts = Counter()
        print("(a) Major POS Categories:")
        for cat_name, matcher in categories.items():
            count = sum(c for tag, c in pos_counts.items() if matcher(tag))
            print(f"    {cat_name}: {count} ({(count/total)*100:.2f}%)")
            category_counts[cat_name] = count
            
        # Verb to Noun Ratio
        # Nouns = All Noun types (NN, NNP, NNC, etc.)
        noun_count = sum(c for tag, c in pos_counts.items() if tag.startswith('NN'))
        verb_count = sum(c for tag, c in pos_counts.items() if tag.startswith('VM'))
        
        print(f"\n(b) Proportion of Verbs vs Nouns:")
        print(f"    Total Nouns (All types): {noun_count}")
        print(f"    Total Main Verbs (VM): {verb_count}")
        if noun_count > 0:
            print(f"    Verb-to-Noun Ratio: {verb_count/noun_count:.2f}")

        # Save Plot
        self.plot_frequency_distribution(
            category_counts, 
            "Major POS Category Distribution", 
            "plot_pos_distribution.png", 
            xlabel="POS Category"
        )

    def generate_report(self):
        self.load_data()
        self.analyze_basic_statistics()
        self.analyze_word_order()
        self.analyze_case_markers()
        self.analyze_intervening_distance()
        self.analyze_pos_tags()


def main():
    # Update this path if necessary
    data_dir = "/home/vivek/python/LD3/Assignments/1/HDTB_pre_release_version-0.05"
    analyzer = TreebankAnalyzer(data_dir)
    analyzer.generate_report()

if __name__ == "__main__":
    main()