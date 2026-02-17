import os
import sys
import glob

def convert_dat_to_tab(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Walk recursively or just list files in the dir? 
        # The structure is .../Development/*.dat
        # I'll just use glob
        files = glob.glob(os.path.join(input_dir, '*.dat'))
        files.sort() # Ensure deterministic order (optional but good practice)
        
        for filepath in files:
            with open(filepath, 'r', encoding='utf-8') as infile:
                for line in infile:
                    line = line.strip()
                    if not line:
                        outfile.write('\n')
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) >= 8:
                        # Extract relevant columns
                        # Index (1-based) is parts[0]
                        word = parts[1]
                        pos = parts[4] # Using Coarse POS (5th column)
                        head = parts[6]
                        deprel = parts[7]
                        
                        # Write to tab format: WORD<TAB>POS<TAB>HEAD<TAB>DEPREL
                        outfile.write(f"{word}\t{pos}\t{head}\t{deprel}\n")
                    else:
                        # Handle cases where line might be malformed or different
                        pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 convert_hindi_to_tab.py <input_dir> <output_file>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    convert_dat_to_tab(input_dir, output_file)
