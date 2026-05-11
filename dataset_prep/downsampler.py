import pandas as pd
import random

# NOTE
# All of the file references to /datasets directory is only applicable if ran from a local machine
# Visit /sources to see links to datasets used in this repository

def downsample_dataset(input_path: str, output_path: str, target_rows: int, 
                       description: str, random_state: int = 42):
    
    # Load dataset
    df = pd.read_csv(input_path)
    original_size = len(df)
    print(f"  Original size: {original_size:,} rows")
    
    if original_size <= target_rows:
        df.to_csv(output_path, index=False)
        return original_size
    
    # random
    df_sampled = df.sample(n=target_rows, random_state=random_state)
    
    df_sampled.to_csv(output_path, index=False)
    
    reduction_pct = (1 - target_rows / original_size) * 100
    print(f"  Downsampled to: {target_rows:,} rows ({reduction_pct:.1f}% reduction)")
    print(f"  Saved to: {output_path}")
    
    return target_rows


def main():
    config = {
        'emotion': {
            'input': 'datasets/emotions_2.csv',
            'output': 'datasets/emotions_2_downsampled.csv',
            'target_rows': 20000,
            'description': 'Emotion Dataset'
        },
        'therapy': {
            'input': 'datasets/theurapetic_sessions_3.csv',
            'output': 'datasets/theurapetic_sessions_3_downsampled.csv',
            'target_rows': 7500, 
            'description': 'Therapy Dataset'
        }
    }
    
    # Process each dataset
    results = {}
    
    for key, params in config.items():
        results[key] = downsample_dataset(
            input_path=params['input'],
            output_path=params['output'],
            target_rows=params['target_rows'],
            description=params['description']
        )


if __name__ == "__main__":
    main()