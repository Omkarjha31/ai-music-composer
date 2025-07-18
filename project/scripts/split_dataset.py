import pandas as pd
import os
from pretty_midi import PrettyMIDI
from sklearn.model_selection import train_test_split

midi_dir = 'D:/Study/Ai_Music_Composer/project/data/Raw/Adl-piano-midi'
midi_files = [os.path.join(root, f) for root, _, files in os.walk(midi_dir) for f in files if f.endswith('.mid')]

valid_files = []
tempos = []

# ✅ Read MIDI safely
for f in midi_files:
    try:
        pm = PrettyMIDI(f)
        tempo = pm.estimate_tempo()
        valid_files.append(f)
        tempos.append(tempo)
    except Exception as e:
        print(f"❌ Skipping {f} due to error: {e}")

# ✅ Check if enough valid files
if len(valid_files) < 4:
    raise ValueError("Not enough valid MIDI files for stratification.")

tempo_bins = pd.qcut(tempos, q=4, labels=False)

# ✅ Stratified split
train_files, test_files = train_test_split(valid_files, test_size=0.2, stratify=tempo_bins)
val_files, test_files = train_test_split(test_files, test_size=0.5, stratify=tempo_bins[:len(test_files)])

# ✅ Save train files
pd.DataFrame({'file': train_files}).to_csv('D:/Study/Ai_Music_Composer/project/data/Train_files.csv', index=False)
