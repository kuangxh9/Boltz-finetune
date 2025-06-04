import hashlib
import shutil
from pathlib import Path
from Bio import SeqIO
from argparse import ArgumentParser

parser = ArgumentParser(description="Rename .a3m files by SHA256 hash of sequences.")
parser.add_argument("--msa_dir", type=str, default="mydata/raw_msa", help="Directory containing original .a3m files")
parser.add_argument("--fasta", type=str, default="mydata/all_seqs.fasta", help="FASTA file containing sequences")
parser.add_argument("--output_dir", type=str, default="mydata/hash_raw_msa", help="Output directory for renamed .a3m files")
args = parser.parse_args()

msa_dir = Path(args.msa_dir)
fasta_path = Path(args.fasta)
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

# Copy original .a3m files to output_dir
for msa_file in msa_dir.glob("*.a3m"):
    shutil.copy(msa_file, output_dir / msa_file.name)

print(f"[INFO] Copied {len(list(msa_dir.glob('*.a3m')))} files to {output_dir}")

# Rename based on hash
renamed_count = 0
for record in SeqIO.parse(fasta_path, "fasta"):
    seq = str(record.seq).replace("-", "").upper()
    hashname = hashlib.sha256(seq.encode()).hexdigest()
    original_id = record.id  # e.g., "8q6f_A"

    # Match original .a3m file
    matched_files = list(output_dir.glob(f"{original_id}*.a3m"))
    if not matched_files:
        print(f"[WARN] No MSA file matched for {original_id}")
        continue

    src_file = matched_files[0]
    dst_file = output_dir / f"{hashname}.a3m"

    if dst_file.exists():
        print(f"[WARN] Target file {dst_file} already exists. Skipping and removing duplicate {src_file.name}")
        src_file.unlink()
        continue

    src_file.rename(dst_file)
    renamed_count += 1
    print(f"[OK] Renamed {src_file.name} → {dst_file.name}")

print(f"[DONE] Total renamed: {renamed_count}")
