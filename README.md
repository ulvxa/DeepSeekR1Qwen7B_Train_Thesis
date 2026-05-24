# Wellness Assistant — Fine-Tuning

Bachelor's thesis: *Evaluation and Implementation of a Generative AI-Based Wellness Assistant*
Ulvi Aliyev

---

## Notebooks

- `Thesis.ipynb` — main training notebook (dual-mode: subset / full dataset)
- `Inference(Output model test).ipynb` — all testing: qualitative, BLEU/ROUGE, hallucination, base model comparison

## Dataset pipeline

`dataset_prep/` — builds the unified instruction-tuning dataset from 4 source files

- `main.py` — generates Alpaca-format instruction pairs
- `downsampler.py` — stratified downsampling for emotion and therapy datasets
- `train.jsonl` / `val.jsonl` — final split used for training

## Results

- `5k_subset_training/` — subset test run (5k samples, 1 epoch)
- `full_training/` — full dataset run (195k samples, 3 epochs, 14h10m)

Each contains `logs/`, `testing/output.txt`, and `output_model/`.

## Repo Structure

```bash
Train/
├── Thesis.ipynb
├── Inference(Output model test).ipynb
├── dataset_prep/
│   ├── main.py
│   ├── downsampler.py
│   ├── cut_csv.py
│   ├── train.jsonl
│   ├── val.jsonl
│   ├── train_sample.json
│   ├── val_sample.json
│   ├── output.txt
│   ├── requirements.txt
│   └── sources/
│       ├── med_1_link.txt
│       ├── emotions_2_link.txt
│       ├── theurapetic_sessions_3_link.txt
│       └── nutritionalData_4_link.txt
├── 5k_subset_training/
│   ├── subset_train_5k.json
│   ├── subset_val_500.json
│   ├── logs/
│   ├── testing/
│   │   ├── output.txt
│   │   ├── test_cases.json
│   │   └── NOTE.txt
│   └── output_model/
│       └── google_drive_link.txt
├── full_training/
│   ├── logs/
│   ├── testing/
│   │   └── output.txt
│   └── output_model_full/
│       └── google_drive_link.txt
```

## Note
Assistance of Artificial Intelligence was used strictly to beautify output logs for better representation.