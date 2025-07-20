# # Step 0: Imports and Setup
# import os
# import pandas as pd
# import numpy as np
# import librosa
# import joblib
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score

# # Step 1: Load Labeled Data from CSV
# labeled_df = pd.read_csv("D:/Study/Ai_Music_Composer/2/piano_dataset_with_target.csv")
# X = labeled_df.drop("target", axis=1)
# y = labeled_df["target"]

# # Step 2: Train Mood Classifier (Random Forest)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Save the model for later use
# joblib.dump(model, "mood_classifier.pkl")

# # Evaluate
# preds = model.predict(X_test)
# print("Accuracy:", accuracy_score(y_test, preds))

# # Step 3: Define Feature Extraction for New MIDI Files
# import pretty_midi

# def extract_features_from_midi(midi_path):
#     try:
#         # Convert to audio
#         midi_data = pretty_midi.PrettyMIDI(midi_path)
#         audio = midi_data.synthesize()

#         # Extract MFCCs and Chroma
#         sr = 22050
#         mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
#         chroma = librosa.feature.chroma_stft(y=audio, sr=sr)

#         # Aggregate
#         mfccs_mean = np.mean(mfccs, axis=1)
#         chroma_mean = np.mean(chroma, axis=1)

#         return np.concatenate([mfccs_mean, chroma_mean])
#     except Exception as e:
#         print("Error with file", midi_path, ":", e)
#         return None

# # Step 4: Auto-label MIDI files with predicted mood
# from pathlib import Path

# midi_root_folder = "D:/Study/Ai_Music_Composer/archive"  # Set your path here
# output_csv = []
# classifier = joblib.load("mood_classifier.pkl")

# for midi_path in Path(midi_root_folder).rglob("*.mid"):
#     features = extract_features_from_midi(str(midi_path))
#     if features is not None and len(features) == 25:
#         predicted_mood = int(classifier.predict([features])[0])
#         output_csv.append([str(midi_path), predicted_mood] + list(features))

# # Step 5: Save Auto-Labeled MIDI Metadata
# columns = ["filepath", "predicted_mood"] + [f"f{i}" for i in range(25)]
# auto_df = pd.DataFrame(output_csv, columns=columns)
# auto_df.to_csv("auto_labeled_midi.csv", index=False)
# print("Saved labeled MIDI data to auto_labeled_midi.csv")


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load dataset with 30 features
df = pd.read_csv('D:/Study/Ai_Music_Composer/2/piano_dataset_with_target.csv')
# Convert mood labels to integers
label_map = {'happy': 0, 'sad': 1, 'angry': 2, 'relaxed': 3}
df['target'] = df['target'].map(label_map)

# Drop file path and separate features/labels
X = df.drop(['target'], axis=1)
y = df['target']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, 'mood_classifier.pkl')

### Step 2: Extract 30 Features (25 Tonal + 5 Metadata)

import librosa
import pretty_midi
import numpy as np
from pathlib import Path

def extract_features_from_midi(midi_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        audio = midi_data.synthesize()

        if len(audio) < 22050:
            return None

        # Tonal Features
        mfcc = librosa.feature.mfcc(y=audio, sr=22050, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=audio, sr=22050)
        mfcc_mean = mfcc.mean(axis=1)
        chroma_mean = chroma.mean(axis=1)

        # Metadata Features
        duration = midi_data.get_end_time()
        tempo = midi_data.estimate_tempo()
        num_notes = sum(len(i.notes) for i in midi_data.instruments)
        num_instruments = len(midi_data.instruments)
        avg_pitch = np.mean([note.pitch for inst in midi_data.instruments for note in inst.notes]) if num_notes > 0 else 0

        # Combine
        features = list(mfcc_mean) + list(chroma_mean) + [duration, tempo, num_notes, num_instruments, avg_pitch]

        if len(features) != 30:
            return None

        return features
    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

# Load model
classifier = joblib.load('mood_classifier.pkl')

# Prepare output
output_rows = []

# Recursively go through nested folders
for midi_file in Path("D:/Study/Ai_Music_Composer/archive").rglob("*.mid"):
    features = extract_features_from_midi(str(midi_file))
    if features:
        mood = int(classifier.predict([features])[0])
        output_rows.append([str(midi_file), mood] + features)

# Save CSV
columns = ['file_path', 'predicted_mood'] + [f'feat_{i+1}' for i in range(30)]
predicted_df = pd.DataFrame(output_rows, columns=columns)
predicted_df.to_csv("auto_labeled_midi.csv", index=False)

print("✅ Auto-labelling complete. File saved as auto_labeled_midi.csv.")