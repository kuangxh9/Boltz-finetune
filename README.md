# Boltz-Finetune

Fine-tune [Boltz](https://github.com/jwohlwend/boltz) on your own protein dataset – from raw structures to a retrained model.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick-Start](#quick-start)
3. [Step-by-Step Guide](#step-by-step-guide)
   3.1 [Environment setup](#31-environment-setup)
   3.2 [Download Boltz caches](#32-download-boltz-caches)
   3.3 [Data layout](#33-data-layout)
   3.4 [Extract FASTA sequences](#34-extract-fasta-sequences)
   3.5 [Create sequence clusters](#35-create-sequence-clusters)
   3.6 [Install LocalColabFold & databases](#36-install-localcolabfold--databases)
   3.7 [Generate MSAs](#37-generate-msas)
   3.8 [Hash-rename MSAs](#38-hash-rename-msas)
4. [Next Steps](#next-steps)
5. [Troubleshooting](#troubleshooting)
6. [License](#license)

---

## Prerequisites

| Name        | Version      | Notes                            |
| ----------- | ------------ | -------------------------------- |
| **Python**  | 3.10         | Tested with 3.10.x               |
| **Conda**   | ≥ 23.x       | Miniconda or Anaconda            |
| **mmseqs2** | current      | Sequence clustering & MSA search |
| **Redis**   | ≥ 7.0        | Boltz feature store              |
| **GPU**     | ≥ 12 GB VRAM | Training / inference             |

> **Tip** To keep the repo light, only essential scripts live here; advanced utilities are linked where relevant.

---

## Quick-Start

```bash
# 1 Create and activate an environment
conda create -n boltz_finetune python=3.10
conda activate boltz_finetune

# 2 Install Boltz from source
git clone https://github.com/jwohlwend/boltz.git
cd boltz && pip install -e .

# 3 Install external tools (follow upstream docs)
# mmseqs2 -> https://github.com/soedinglab/mmseqs2#installation
# Redis    -> https://redis.io/docs/latest/operate/oss_and_stack/install/

# 4 Clone this finetune repo next to Boltz and follow Step-by-Step Guide
```

---

## Step-by-Step Guide

### 3.1 Environment setup

Already covered in **Quick-Start**. Activate `boltz_finetune` before every session.

### 3.2 Download Boltz caches

```bash
mkdir -p boltz_cache && cd boltz_cache
wget https://boltz1.s3.us-east-2.amazonaws.com/boltz1_ptm.pt
wget https://boltz1.s3.us-east-2.amazonaws.com/ccd.pkl
cd ..
```

### 3.3 Data layout

```
mydata/
├── raw_cif/
│   ├── 1abc.cif
│   └── 2xyz.cif
└── ...
```

### 3.4 Extract FASTA sequences

```bash
python scripts/process/extract_fasta.py \
  --input_dir mydata/raw_cif \
  --output_fasta mydata/all_seqs.fasta
```

### 3.5 Create sequence clusters

```bash
# Download PDB reference sequences
wget https://files.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt.gz
gunzip pdb_seqres.txt.gz

# Cluster
python cluster.py \
  --ccd boltz_cache/ccd.pkl \
  --sequences pdb_seqres.txt \
  --mmseqs /path/to/mmseqs \
  --outdir clustering/
```

### 3.6 Install LocalColabFold & databases

LocalColabFold lets you run MSA searches offline.

```bash
# Install (Linux)
wget https://raw.githubusercontent.com/YoshitakaMo/localcolabfold/main/install_colabbatch_linux.sh
bash install_colabbatch_linux.sh
```

> **Database size** Full UniRef 30 + environment/PDB templates ≈ 2 TB.
> If you only need UniRef 30, stop the script after `uniref30_2302.tar.gz` downloads.

Build the index (optional but faster):

```bash
tar xf uniref30_2302.tar.gz
mmseqs tsv2exprofiledb uniref30_2302 uniref30_2302_db
mmseqs createindex uniref30_2302_db tmp_uniref30 --remove-tmp-files 1
```

Add LocalColabFold to `$PATH`:

```bash
export PATH="/abs/path/to/localcolabfold/colabfold-conda/bin:$PATH"
```

### 3.7 Generate MSAs

```bash
colabfold_search \
  --db-load-mode 2 \
  --threads 16 \
  --use-env 0 \
  mydata/all_seqs.fasta \
  ./colabfold_db \
  mydata/raw_msa
```

### 3.8 Hash-rename MSAs

```bash
python rename_msa_by_hash.py \
  --msa_dir mydata/raw_msa \
  --fasta mydata/all_seqs.fasta \
  --output_dir mydata/hash_raw_msa
```

---

## Next Steps

1. 
