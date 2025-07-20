import pretty_midi
import simpleaudio as sa
import tempfile
import threading
import os
import csv
from pathlib import Path
import soundfile as sf

output_file = "project/data/manually_labeled_midi.csv"
fieldnames = ["file_path", "mood"]

# Load already labeled files to skip
labeled_files = set()
if Path(output_file).exists():
    with open(output_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            labeled_files.add(row["file_path"])

# Function to convert MIDI to WAV
def midi_to_wav(midi_path, wav_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        audio_data = midi_data.synthesize()
        sf.write(wav_path, audio_data, samplerate=22050)
        return True
    except Exception as e:
        print(f"Error converting {midi_path}: {e}")
        return False

# Function to play audio and return the playback object
def play_audio(wav_path):
    try:
        wave_obj = sa.WaveObject.from_wave_file(wav_path)
        return wave_obj.play()
    except Exception as e:
        print(f"Playback error: {e}")
        return None

# Prepare CSV file
if not Path(output_file).exists():
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

midi_folder = "project/data/archive"

# Start manual labeling
for i, midi_file in enumerate(Path(midi_folder).rglob("*.mid"), 1):
    midi_file_str = str(midi_file)

    if midi_file_str in labeled_files:
        print(f"Skipping already labeled file {i}: {midi_file_str}")
        continue

    print(f"\nNow playing file {i}: {midi_file_str}")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        success = midi_to_wav(midi_file_str, temp_wav.name)
        if not success:
            continue

        # Play audio
        playback = play_audio(temp_wav.name)

        # Take input during playback
        mood = input("Enter mood (happy/sad/angry/relaxed): ").strip().lower()

        # Stop audio immediately if still playing
        if playback is not None and playback.is_playing():
            playback.stop()

        # Save to CSV
        with open(output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({"file_path": midi_file_str, "mood": mood})
            labeled_files.add(midi_file_str)  # update set to avoid relabeling

        # Delete the temporary file
        os.remove(temp_wav.name)
