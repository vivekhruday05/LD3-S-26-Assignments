# Hindi Dependency Treebank Analysis

A comprehensive linguistic analysis tool for the Hindi Dependency Treebank (HDTB) pre-release version 0.05. This project performs descriptive statistical analysis of Hindi language data including word order patterns, case markers (vibhakti), intervening distances, and POS tag distributions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Results](#analysis-results)
- [Code Documentation](#code-documentation)
- [Data Format](#data-format)

## Overview

This project analyzes the Hindi Dependency Treebank (HDTB) corpus to extract and visualize linguistic patterns in Hindi text. The analyzer processes CoNLL-formatted dependency treebank data and generates statistical reports and visualizations for various linguistic phenomena.

**Assignment Context:** Linguistic Data 3 - Descriptive Analysis of Hindi Data

## Features

- **Corpus Statistics**: Basic statistics including sentence count, token/type counts, and sentence length metrics
- **Word Order Analysis**: Identification and frequency analysis of SOV, SVO, and other word order patterns
- **Case Marker Analysis**: Distribution analysis of vibhakti (case markers) in Hindi
- **Intervening Distance**: Statistical analysis of word distances between case markers
- **POS Tag Distribution**: Part-of-speech tag frequency analysis and verb-to-noun ratios
- **Visualization**: Automatic generation of publication-quality plots for all analyses

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Required Python Packages

```bash
pip install matplotlib
```

### Setup

1. Clone or download this repository
2. Ensure the HDTB data is available at the specified path
3. Run the analysis script

```bash
git clone <repository-url>
cd Assignments/1
python3 analysis.py
```

## Usage

### Basic Usage

Run the analyzer with default settings:

```bash
python3 analysis.py
```

This will:
- Load the treebank data from the default directory
- Perform all analyses
- Generate output plots (PNG files)
- Print detailed results to stdout

### Redirecting Output

Save the analysis results to a text file:

```bash
python3 analysis.py > analysis_output.txt
```

### Customizing Data Path

Edit the `main()` function in `analysis.py` to change the data directory:

```python
def main():
    data_dir = "/path/to/your/HDTB_pre_release_version-0.05"
    analyzer = TreebankAnalyzer(data_dir)
    analyzer.generate_report()
```

## Analysis Results

### 1. Basic Corpus Statistics

| Metric | Value |
|--------|-------|
| Total Sentences | 41,399 |
| Total Word Tokens (excluding punctuation) | 603,578 |
| Total Word Types (excluding punctuation) | 21,366 |
| Average Sentence Length | 14.58 tokens |
| Minimum Sentence Length | 1 token |
| Maximum Sentence Length | 106 tokens |

**Type-Token Ratio (TTR):** 0.0354 (indicating high lexical diversity)

### 2. Word Order Patterns

| Pattern | Count | Percentage |
|---------|-------|------------|
| SVO (Subject-Verb-Object) | 7,773 | 57.81% |
| SOV (Subject-Object-Verb) | 5,214 | 38.78% |
| OSV (Object-Subject-Verb) | 442 | 3.29% |
| OVS (Object-Verb-Subject) | 12 | 0.09% |
| VSO (Verb-Subject-Object) | 5 | 0.04% |

**Key Dependency Relations:**
- Subject (k1): 28,156 instances
- Object (k2): 17,189 instances
- Main verb (main): 40,204 instances

**Discussion:** While Hindi is traditionally described as an SOV language, the corpus shows a strong preference for SVO ordering (57.81%). This might reflect the influence of written/formal register or news article style in the corpus.

### 3. Case Marker (Vibhakti) Distribution

#### Top 20 Case Markers

| Vibhakti | Count | Percentage |
|----------|-------|------------|
| 0_kA | 42,947 | 15.96% |
| 0_meM | 22,467 | 8.35% |
| yA | 22,154 | 8.24% |
| hE | 18,669 | 6.94% |
| 0_ko | 16,730 | 6.22% |
| 0_ne | 13,642 | 5.07% |
| 0_se | 11,437 | 4.25% |
| 0_para | 8,504 | 3.16% |
| yA_hE | 4,939 | 1.84% |
| kA | 4,923 | 1.83% |
| gA | 4,841 | 1.80% |
| nA_kA | 4,665 | 1.73% |
| yA1 | 4,045 | 1.50% |
| ne | 4,008 | 1.49% |
| WA | 3,968 | 1.48% |
| nA | 3,772 | 1.40% |
| kara | 3,001 | 1.12% |
| ko | 2,964 | 1.10% |
| 0_ke_lie | 2,681 | 1.00% |
| wA_hE | 2,610 | 0.97% |

**Total Case Markers Analyzed:** 269,197 instances

**Unmarked Nouns (Direct Case):**
- Count: 126,311
- Percentage: 49.00% of all nouns

**Analysis:** The genitive marker 'kA' (का) is the most frequent, followed by locative 'meM' (में). Nearly half of all nouns appear in direct/unmarked case, typical of subjects and direct objects in Hindi.

### 4. Intervening Distance Analysis

| Metric | Value |
|--------|-------|
| Average Intervening Words (Overall) | 1.29 words |
| Standard Deviation | 1.54 |
| Avg Distance (Same Markers) | 1.64 words (n=9,158) |
| Avg Distance (Different Markers) | 1.27 words (n=218,694) |

**Interpretation:** Case markers tend to appear in close proximity. Surprisingly, different case markers appear closer together than repeated instances of the same marker, suggesting varied syntactic constructions within short spans.

### 5. POS Tag Distribution

#### Major POS Categories

| POS Tag | Description | Count | Percentage |
|---------|-------------|-------|------------|
| NN | Common Noun | 170,128 | 28.19% |
| VM | Main Verb | 91,916 | 15.23% |
| PSP | Postposition | 82,327 | 13.64% |
| NNP | Proper Noun | 78,632 | 13.03% |
| PRP | Pronoun | 35,599 | 5.90% |
| JJ | Adjective | 32,981 | 5.46% |
| CC | Conjunction | 32,739 | 5.42% |

#### Verb-Noun Analysis

| Category | Count |
|----------|-------|
| Total Nouns (All types) | 257,794 |
| Total Main Verbs (VM) | 91,916 |
| **Verb-to-Noun Ratio** | **0.36** |

**Linguistic Insight:** The corpus shows a high proportion of nouns (41.22% combined), characteristic of written/formal Hindi. The verb-to-noun ratio of 0.36 indicates a noun-heavy style typical of news articles.

## Code Documentation

### Class: `TreebankAnalyzer`

The main analyzer class for processing HDTB data.

#### Constructor

```python
TreebankAnalyzer(data_dir)
```

**Parameters:**
- `data_dir` (str): Path to the HDTB data directory

**Attributes:**
- `data_dir`: Path to treebank data
- `sentences`: List of parsed sentences (each sentence is a list of token dictionaries)
- `all_tokens`: Flat list of all tokens across all sentences
- `word_types`: Set of unique word forms (types)

#### Main Methods

##### `load_data()`
Loads all CoNLL formatted data files from InterChunk and IntraChunk directories.

```python
analyzer.load_data()
```

**Processes:**
- Recursively searches for `.dat` files in wx (WX notation) subdirectories
- Parses CoNLL format files
- Populates sentence and token lists

##### `generate_report()`
Main entry point that runs all analyses and generates visualizations.

```python
analyzer.generate_report()
```

**Executes:**
1. Data loading
2. Basic statistics analysis
3. Word order pattern analysis
4. Case marker analysis
5. Intervening distance analysis
6. POS tag distribution analysis

##### `analyze_basic_statistics()`
Calculates and reports basic corpus statistics.

**Outputs:**
- Sentence count
- Token/type counts
- Average, min, max sentence lengths

##### `analyze_word_order()`
Analyzes word order patterns based on dependency relations.

**Method:**
- Identifies subjects (k1), objects (k2), and main verbs (main)
- Determines relative positions
- Classifies into patterns (SOV, SVO, OSV, etc.)

**Generates:** `plot_word_order.png`

##### `analyze_case_markers()`
Extracts and analyzes vibhakti (case marker) distribution.

**Method:**
- Parses morphological features for `vib-` tags
- Counts occurrences of each vibhakti
- Identifies unmarked nouns

**Generates:** `plot_case_markers.png`

##### `analyze_intervening_distance()`
Calculates distances between consecutive case markers.

**Method:**
- Iterates through sentences
- Measures token distance between case markers
- Separates same vs. different marker pairs

**Outputs:**
- Average distances
- Standard deviation
- Comparative statistics

##### `analyze_pos_tags()`
Analyzes Part-of-Speech tag distribution.

**Method:**
- Counts POS tags from `pos_full` field
- Calculates verb-to-noun ratios

**Generates:** `plot_pos_distribution.png`

#### Helper Methods

##### `_parse_conll_file(filepath)`
Parses a single CoNLL format file.

**Parameters:**
- `filepath`: Path to the `.dat` file

**Returns:** None (populates internal data structures)

##### `_parse_token_line(line)`
Parses a single line representing a token in CoNLL format.

**Parameters:**
- `line` (str): Tab-separated token data

**Returns:** Dictionary with token information or None if invalid/punctuation

**Token Dictionary Structure:**
```python
{
    'id': int,           # Token ID
    'word': str,         # Surface form
    'lemma': str,        # Lemma
    'pos_short': str,    # Short POS tag
    'pos_full': str,     # Full POS tag
    'morph': str,        # Morphological features
    'parent_id': int,    # Parent token ID
    'deprel': str        # Dependency relation
}
```

##### `get_case_from_morph(morph_str)`
Extracts case feature from morphological annotation.

**Parameters:**
- `morph_str` (str): Morphological features string

**Returns:** Case value or None

##### `get_vibhakti(morph_str)`
Extracts vibhakti (case marker) from morphological features.

**Parameters:**
- `morph_str` (str): Morphological features string

**Returns:** Vibhakti string or None

**Pattern:** Searches for `vib-<marker>` in the morphological string

##### `plot_frequency_distribution(data_counter, title, filename, top_n=None, xlabel, ylabel)`
Generates and saves bar chart visualizations.

**Parameters:**
- `data_counter` (Counter): Frequency data
- `title` (str): Plot title
- `filename` (str): Output filename
- `top_n` (int, optional): Limit to top N items
- `xlabel` (str): X-axis label
- `ylabel` (str): Y-axis label

**Generates:** PNG file with matplotlib bar chart

## Data Format

### CoNLL Format

The analyzer expects data in CoNLL format with the following tab-separated fields:

```
1    word    lemma    POS_short    POS_full    morph_features    parent_id    deprel
```

**Example:**
```
1    राम    राम    NNP    NNP    cat-n|gen-m|num-sg|pers-3|case-d|vib-0    2    k1
2    जाता    जा    VM    VM    cat-v|tam-yA|m-m|num-sg|per-3    0    main
3    है    है    VAUX    VAUX    cat-v|tam-hE|m-m|num-sg|per-3    2    aux
```

**Field Descriptions:**
1. **Token ID**: Unique identifier within sentence
2. **Word**: Surface form in WX notation
3. **Lemma**: Dictionary/base form
4. **POS (short)**: Coarse POS tag
5. **POS (full)**: Fine-grained POS tag
6. **Morphological Features**: Pipe-separated features (cat, gen, num, case, vib, tam, etc.)
7. **Parent ID**: ID of syntactic head (0 for root)
8. **Dependency Relation**: Type of dependency (k1, k2, main, etc.)

### Directory Structure

```
HDTB_pre_release_version-0.05/
├── InterChunk/
│   └── CoNLL/
│       └── wx/
│           ├── conversation/
│           └── news_articles_and_heritage/
│               ├── Development/
│               ├── Testing/
│               └── Training/
└── IntraChunk/
    └── CoNLL/
        └── wx/
            ├── conversation/
            └── news_articles_and_heritage/
                ├── Development/
                ├── Testing/
                └── Training/
```

## Dependencies

### Required Libraries

- **Python Standard Library:**
  - `os`: File system operations
  - `re`: Regular expression operations
  - `statistics`: Statistical calculations
  - `collections.defaultdict`: Default dictionaries
  - `collections.Counter`: Frequency counting
  - `pathlib.Path`: Path operations

- **External Libraries:**
  - `matplotlib.pyplot`: Data visualization (install via `pip install matplotlib`)

### Installation Command

```bash
pip install matplotlib
```

## Generated Visualizations

The analyzer generates three publication-quality plots:

1. **plot_word_order.png**: Bar chart of word order pattern frequencies
2. **plot_case_markers.png**: Distribution of top 20 case markers
3. **plot_pos_distribution.png**: Distribution of major POS categories

All plots include:
- Clear axis labels
- Rotated x-axis labels for readability
- Grid lines for easy value reading
- Proper titles and formatting

## Configuration

### Modifying Analysis Parameters

To analyze only specific metrics, comment out unwanted analysis calls in the `generate_report()` method:

```python
def generate_report(self):
    self.load_data()
    
    self.analyze_basic_statistics()
    # self.analyze_word_order()  # Disabled
    self.analyze_case_markers()
    # self.analyze_intervening_distance()  # Disabled
    self.analyze_pos_tags()
```

### Changing Plot Parameters

Modify the `plot_frequency_distribution()` method to customize:
- Figure size: `plt.figure(figsize=(12, 6))`
- Colors: `plt.bar(..., color='skyblue')`
- Number of top items: Pass different `top_n` parameter

## Output Files

Running the analyzer generates:

1. **analysis_output.txt**: Complete text report (if output is redirected)
2. **plot_word_order.png**: Word order visualization
3. **plot_case_markers.png**: Case marker visualization
4. **plot_pos_distribution.png**: POS tag visualization

## Error Handling

The analyzer includes error handling for:
- Missing data directories
- Malformed CoNLL files
- Invalid token lines
- Missing morphological features

Errors are caught and logged without stopping the entire analysis.

