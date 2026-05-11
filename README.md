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
