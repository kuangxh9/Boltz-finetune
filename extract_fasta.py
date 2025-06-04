from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os
from argparse import ArgumentParser
import glob
from Bio.PDB import MMCIFParser, is_aa


parser = ArgumentParser()
parser.add_argument(
    "--input_dir",
    type=str,
    default="mydata/raw_cif"
)
parser.add_argument(
    "--output_fasta",
    type=str,
    default="mydata/all_seqs.fasta"
)
args = parser.parse_args()

input_dir = args.input_dir
output_fasta = args.output_fasta

aa_map = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
    # uncommon projection
    'MSE': 'M',  
    'SEC': 'U',
    'PYL': 'O',
}

parser = MMCIFParser(QUIET=True)
seq_count = 0
with open(output_fasta, "w") as out_f:
    for cif_file in glob.glob(os.path.join(input_dir, "*.cif")):
        structure_id = os.path.splitext(os.path.basename(cif_file))[0]
        structure = parser.get_structure(structure_id, cif_file)
        for model in structure:
            for chain in model:
                chain_id = chain.id if chain.id.strip() != "" else "UNK"
                sequence = []
                for residue in chain:
                    resname = residue.get_resname().strip()
                    if resname in aa_map:
                        sequence.append(aa_map[resname])
                    elif residue.id[0] == " ":
                        sequence.append('X')
                    else:
                        continue
                if sequence:
                    out_f.write(f">{structure_id}_{chain_id}\n")
                    out_f.write("".join(sequence) + "\n")
                    seq_count += 1

print(f"Extracted {seq_count} sequences to {output_fasta}")
