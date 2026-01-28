import argparse
import sys
import os

MARKER_LIBRARY = {
    "AmpR_gene": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAACTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTT", 
    "KanR_gene": "ATGAGCCATATTCAACGGGAAACGTCTTGCTCTAGGCCGCGATTAAATTCCAACATGGATGCTGATTTATATGGGTATAAATGGGCTCGCGATAATGTCGGGCAATCAGGTGCGACAATCTATCGATTGTATGGGAAGCCCGATGCGCCAGAGTTGTTTCTGAAACATGGCAAAGGTAGCGTTGCCAATGATGTTACAGATGAGATGGTCAGACTAAACTGGCTGACGGAATTTATGCCTCTTCCGACCATCAAGCATTTTATCCGTACTCCTGATGATGCATGGTTACTCACCACTGCGATCCCCGGGAAAACAGCATTCCAGGTATTAGAAGAATATCCTGATTCAGGTGAAAATATTGTTGATGCGCTGGCAGTGTTCCTGCGCCGGTTGCATTCGATTCCTGTTTGTAATTGTCCTTTTAACAGCGATCGCGTATTTCGTCTCGCTCAGGCGCAATCACGAATGAATAACGGTTTGGTTGATGCGAGTGATTTTGATGACGAGCGTAATGGCTGGCCTGTTGAACAAGTCTGGAAAGAAATGCATAACTTTTGCCATTCCACAGATTTCGTCTCACTGGCGCAAATGGAGGATGCTAGAAATCTCTATGACGTATACAGCGCAATGTCTATTATGACAGGTGTTGTTTGGCGATCTGTGGCTTCTGGCACTGAGAAAGCTT",
    "CmR_gene": "ATGGAGAAAAAAATCACTGGATATACCACCGTTGATATATCCCAATGGCATCGTAAAGAACATTTTGAGGCATTTCAGTCAGTTGCTCAATGTACCTATAACCAGACCGTTCAGCTGGATATTACGGCCTTTTTAAAGACCGTAAAGAAAAATAAGCACAAGTTTTATCCGGCCTTTATTCACATTCTTGCCCGCCTGATGAATGCTCATCCGGAATTCCGTATGGCAATGAAAGACGGTGAGCTGGTGATATGGGATAGTGTTCACCCTTGTTACACCGTTTTCCATGAGCAAACTGAAACGTTTTCATCGCTCTGGAGTGAATACCACGACGATTTCCGGCAGTTTCTACACATATATTCGCAAGATGTGGCGTGTTACGGTGAAAACCTGGCCTATTTCCCTAAAGGGTTTATTGAGAATATGTTTTTCGTCTCAGCCAATCCCTGGGTGAGTTTCACCAGTTTTGATTTAAACGTGGCCAATATGGACAACTTCTTCGCCCCCGTTTTCACCATGGGCAAATATTATACGCAAGGCGACAAGGTGCTGATGCCGCTGGCGATTCAGGTTCATCATGCCGTCTGTGATGGCTTCCATGTCGGCAGAATGCTTAATGAATTACAACAGTACTGCGATGAGTGGCAGGGCGGGGCGTAA",
    "TetR_gene": "ATGTCTAGATTAGATAAAAGTAAAGTGATTAACAGCGCATTAGAGCTGCTTAATGAGGTCGGAATCGAAGGTTTAACAACCCGTAAACTCGCCCAGAAGCTAGGTGTAGAGCAGCCTACATTGTATTGGCATGTAAAAAATAAGCGGGCTTTGCTCGACGCCTTAGCCATTGAGATGTTAGATAGGCACCATACTCACTTTTGCCCTTTAGAAGGGGAAAGCTGGCAAGATTTTTTACGTAATAACGCTAAAAGTTTTAGATGTGCTTTACTAAGTCATCGCGATGGAGCAAAAGTACATTTAGGTACACGGCCTACAGAAAAACAGTATGAAACTCTCGAAAATCAATTAGCCTTTTTATGCCAACAAGGTTTTTCACTAGAGAATGCATTATATGCACTCAGCGCTGTGGGGCATTTTACTTTAGGTTGCGTATTGGAAGATCAAGAGCATCAAGTCGCTAAAGAAGAAAGGGAAACACCTACTACTGATAGTATGCCGCCATTATTACGACAAGCTATCGAATTATTTGATCACCAAGGTGCAGAGCCAGCCTTCTTATTCGGCCTTGAATTGATCATATGCGGATTAGAAAAACAACTTAAATGTGAAAGTGGGTCTTAA",
    "SpecR_gene": "ATGCGAGATATGGTCAAAAGGACGGGCCTTGGCATCCGTGAACAAGGGGAGCTTCAGCGTGTCTATGATGCGTGGCAGGTCCGATAGAGCGCCACAATTTCACTCAAAAGCGCCTTGGTATCAAACAAATTCTTAAAACTGAAAGTGCCTTTGTCGCCAATCGTGGTACTATGCTTCGATCTGGATATGATTTTGTTGCTGGTTATCGTGCAACTAACTGACGGCATCGAGGTCAGGATGGTTGTCGGCGCAGTAACGGACTGTCGAATGGTCGTTACGTATCCTCGTTTCTCGCATGGGGCGCAGATGATTCATAAACTTCCTGACGAGCTCATCACGCGCTGGGGCCAGTAT", 
    
    "lacZ_alpha": "ATGACCATGATTACGCCAAGCTTGCATGCCTGCAGGTCGACTCTAGAGGATCCCCGGGTACCGAGCTCGAATTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCCTGATGCGGTATTTTCTCCTTACGCATCTGTGCGGTATTTCACACCGCATATGGTGCACTCTCAGTACAATCTGCTCTGATGCCGCATAGTTAAGCCAGCCCCGACACCCGCCAACACCCGCTGACGCGCCCTGACGGGCTTGTCTGCTCCCGGCATCCGCTTACAGACAAGCTGTGACCGTCTCCGGGAGCTGCATGTGTCAGAGGTTTTCACCGTCATCACCGAAACGCGCGAGACGAAAGGGCCTCGTGATACGCCTATTTTTATAGGTTAATGTCATGATAATAATGGTTTCTTAGACGTCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATGAGACAATAACCCTGATAAATGCTTCAATAATATTGAAAAAGGAAGAGT", 
    "GFP": "ATGGGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCCAATTCTTGTTGAATTAGATGGTGATGTTAATGGGCACAAATTTTCTGTCAGTGGAGAGGGTGAAGGTGATGCAACATACGGAAAACTTACCCTTAAATTTATTTGCACTACTGGAAAACTACCTGTTCCATGGCCAACACTTGTCACTACTTTCTCTTATGGTGTTCAATGCTTTTCCCGTTATCCGGATCATATGAAACGGCATGACTTTTTCAAGAGTGCCATGCCCGAAGGTTATGTACAGGAACGCACTATATCTTTCAAAGATGACGGGAACTACAAGACGCGTGCTGAAGTCAAGTTTGAAGGTGATACCCTTGTTAATCGTATCGAGTTAAAAGGTATTGATTTTAAAGAAGATGGAAACATTCTCGGACACAAATTGGAATACAACTATAACTCACACAATGTATACATCACGGCAGACAAACAAAAGAATGGAATCAAAGCTAACTTCAAAATTCGCCACAACATTGAAGATGGATCCGTTCAACTAGCAGACCATTATCAACAAAATACTCCAATTGGCGATGGCCCTGTCCTTTTACCAGACAACCATTACCTGTCGACACAATCTGCCCTTTCGAAAGATCCCAACGAAAAGCGTGACCACATGGTCCTTCTTGAGTTTGTAACTGCTGCTGGGATTACACATGGCATGGATGAGCTCTACAAATAA",
    "mCherry": "ATGGTGAGCAAGGGCGAGGAGGATAACATGGCCATCATCAAGGAGTTCATGCGCTTCAAGGTGCACATGGAGGGCTCCGTGAACGGCCACGAGTTCGAGATCGAGGGCGAGGGCGAGGGCCGCCCCTACGAGGGCACCCAGACCGCCAAGCTGAAGGTGACCAAGGGTGGCCCCCTGCCCTTCGCCTGGGACATCCTGTCCCCTCAGTTCATGTACGGCTCCAAGGCCTACGTGAAGCACCCCGCCGACATCCCCGACTACTTGAAGCTGTCCTTCCCCGAGGGCTTCAAGTGGGAGCGCGTGATGAACTTCGAGGACGGCGGCGTGGTGACCGTGACCCAGGACTCCTCCCTGCAGGACGGCGAGTTCATCTACAAGGTGAAGCTGCGCGGCACCAACTTCCCCTCCGACGGCCCCGTAATGCAGAAGAAGACCATGGGCTGGGAGGCCTCCTCCGAGCGGATGTACCCCGAGGACGGCGCCCTGAAGGGCGAGATCAAGCAGAGGCTGAAGCTGAAGGACGGCGGCCACTACGACGCTGAGGTCAAGACCACCTACAAGGCCAAGAAGCCCGTGCAGCTGCCCGGCGCCTACAACGTCAACATCAAGTTGGACATCACCTCCCACAACGAGGACTACACCATCGTGGAACAGTACGAACGCGCCGAGGGCCGCCACTCCACCGGCGGCATGGACGAGCTGTACAAGTAA",
    
    "ori_pMB1": "TTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTTCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAAAACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTTCTTTCCTGCGTTATCCCCTGATTCTGTGGATAACCGTATTACCGCCTTTGAGTGAGCTGATACCGCTCGCCGCAGCCGAACGACCGAGCGCAGCGAGTCAGTGAGCGAGGAAGCGGAAG",
}

def load_fasta(filename):
    seq = []
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                seq.append(line.strip().upper())
    return "".join(seq)

def load_markers_info(filename):
    markers_db = {}
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found.")
        return markers_db
        
    with open(filename, 'r') as f:
        for line in f:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                category = parts[1].strip()
                name_cell = parts[2].strip()
                recognition_cell = parts[3].strip()
                
                name_key = name_cell.split('(')[0].strip()
                if "Restriction enzyme" in category and "Recognizes" in recognition_cell:
                    site = recognition_cell.replace("Recognizes", "").split(',')[0].strip()
                    site = ''.join(filter(str.isalpha, site))
                    markers_db[name_key] = site.upper()
    return markers_db

def load_design(filename):
    design_elements = []
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        sys.exit(1)
        
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('*') or line.startswith('**'):
                continue
            if ',' in line:
                name, desc = line.split(',', 1)
                design_elements.append((name.strip(), desc.strip()))
    return design_elements

def find_ori_and_enrichment(sequence, k=8, window_size=5000, step=500):
    n = len(sequence)
    if n < window_size:
        window_size = n // 2
        step = max(1, n // 20)

    cumulative_skew = 0
    min_skew = float('inf')
    ori_coord = 0
    
    for i in range(0, n - window_size + 1, step):
        window = sequence[i : i + window_size]
        mid_point = i + (window_size // 2)
        
        g = window.count('G')
        c = window.count('C')
        if (g + c) > 0:
            skew = (g - c) / (g + c)
        else:
            skew = 0
            
        cumulative_skew += skew
        if cumulative_skew < min_skew:
            min_skew = cumulative_skew
            ori_coord = mid_point
            
    return ori_coord

def extract_ori_region(sequence, center, length=800):
    start = max(0, center - length // 2)
    end = min(len(sequence), center + length // 2)
    return sequence[start:end]

def construct_plasmid(input_seq, design_file, markers_db, output_file):
    
    print("Finding ORI in input sequence...")
    # 1. FIND ORI using GC Skew Logic
    ori_center = find_ori_and_enrichment(input_seq, k=8, window_size=100, step=10) # Smaller window for plasmid
    print(f"ORI Center detected at bp: {ori_center}")
    
    ori_seq = extract_ori_region(input_seq, ori_center, length=800)
    print(f"Extracted ORI sequence (length {len(ori_seq)} bp)")

    # 2. Parse Design
    design_elements = load_design(design_file)
    final_sequence = ""
    
    # 3. Assemble based on Design File Order
    
    for name, val in design_elements:
        feature_added = False
        
        # Check for ORI specific request
        if "ori" in name.lower() or "replication" in val.lower():
            final_sequence += ori_seq
            print(f"Added Extracted ORI for feature: {name}")
            feature_added = True
            
        # Check explicit Marker Library
        elif name in MARKER_LIBRARY:
            final_sequence += MARKER_LIBRARY[name]
            print(f"Added Feature from Library: {name}")
            feature_added = True
            
        # Check Restriction Sites
        elif val in markers_db:
            final_sequence += markers_db[val]
            print(f"Added Restriction Site: {val} ({markers_db[val]})")
            feature_added = True
            
        # Check Fuzzy Matches for Markers
        elif not feature_added:
            if "Amp" in val: final_sequence += MARKER_LIBRARY["AmpR_gene"]; feature_added=True; print(f"Added AmpR for {name}")
            elif "Kan" in val: final_sequence += MARKER_LIBRARY["KanR_gene"]; feature_added=True; print(f"Added KanR for {name}")
            elif "Chl" in val or "CmR" in name: final_sequence += MARKER_LIBRARY["CmR_gene"]; feature_added=True; print(f"Added CmR for {name}")
            elif "Tet" in val: final_sequence += MARKER_LIBRARY["TetR_gene"]; feature_added=True; print(f"Added TetR for {name}")
            elif "Spec" in val: final_sequence += MARKER_LIBRARY["SpecR_gene"]; feature_added=True; print(f"Added SpecR for {name}")
            elif "lacZ" in name or "Blue" in val: final_sequence += MARKER_LIBRARY["lacZ_alpha"]; feature_added=True; print(f"Added lacZ for {name}")
            elif "GFP" in name: final_sequence += MARKER_LIBRARY["GFP"]; feature_added=True; print(f"Added GFP for {name}")
            elif "Cherry" in name: final_sequence += MARKER_LIBRARY["mCherry"]; feature_added=True; print(f"Added mCherry for {name}")
        
        # Check Fuzzy Matches for Sites
        if not feature_added:
            # Try to look up the Value directly in markers_db (e.g. if name was arbitrary but val was 'BamHI')
            clean_val = val.split('_')[0]
            if clean_val in markers_db:
                final_sequence += markers_db[clean_val]
                print(f"Added Restriction Site via value lookup: {clean_val}")
                feature_added = True
        
        if not feature_added:
            print(f"Warning: Could not identify or find sequence for '{name}: {val}'. Skipping.")

    # 4. Write Output
    with open(output_file, 'w') as f:
        f.write(">Designed_Plasmid\n")
        for i in range(0, len(final_sequence), 70):
            f.write(final_sequence[i:i+70] + "\n")
    
    print(f"Success! Plasmid constructed. Total Length: {len(final_sequence)} bp.")
    print(f"Output saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Design a plasmid from input parts.")
    parser.add_argument("--input", required=True, help="Input DNA sequence (unknown organism)")
    parser.add_argument("--design", required=True, help="Design file")
    parser.add_argument("--markers", required=True, help="Markers info file")
    parser.add_argument("--output", required=True, help="Output FASTA file")
    
    args = parser.parse_args()
    
    input_seq = load_fasta(args.input)
    markers_db = load_markers_info(args.markers)
    
    construct_plasmid(input_seq, args.design, markers_db, args.output)

if __name__ == "__main__":
    main()
