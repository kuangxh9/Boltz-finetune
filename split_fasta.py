from Bio import SeqIO
import os
from argparse import ArgumentParser

parser = ArgumentParser(description="Dump new ligand files to Boltz CCD library.")
parser.add_argument(
    "--input_fasta",
    type=str,
    default="mydata/all_seqs.fasta"
)
parser.add_argument(
    "--output_dir",
    type=str,
    default="mydata/split_fasta"
)
args = parser.parse_args()

input_fasta = "mydata/all_seqs.fasta"
output_dir = "mydata/split_fasta"

os.makedirs(output_dir, exist_ok=True)

for record in SeqIO.parse(input_fasta, "fasta"):
    seq_id = record.id
    with open(os.path.join(output_dir, f"{seq_id}.fasta"), "w") as f:
        SeqIO.write(record, f, "fasta")

print("Done: split all_seqs.fasta into individual FASTA files.")
