import pandas as pd
import random
from pathlib import Path

# Get all MIDI paths
midi_files = list(Path('D:\Study\Ai_Music_Composer\project\data\Raw\Adl-piano-midi').rglob('*.mid*'))

# Sample 200 files (stratified by subfolder if needed)
sample_files = random.sample(midi_files, 200)

# Save for labeling
pd.DataFrame({'filepath': sample_files}).to_csv('D:\Study\Ai_Music_Composer\project\data\To_label.csv', index=False)
print(f"Saved {len(sample_files)} files to label in data/to_label.csv")

# Check sample distribution
df = pd.read_csv('D:\Study\Ai_Music_Composer\project\data\To_label.csv')
print(f"Sample size: {len(df)}")
print("Subfolder distribution:")
print(df['filepath'].apply(lambda x: x.split('\\')[3]).value_counts().head())