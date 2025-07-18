import simpleaudio as sa
import pandas as pd
import os
from pathlib import Path

soundfont_path = "D:/Study/Ai_Music_Composer/FluidR3_GM/FluidR3_GM.sf2"  # ✅ Change to your .sf2 path
midi_folder = "D:/Study/Ai_Music_Composer/project/data/Raw/Adl-piano-midi"

# Get all MIDI files
midi_files = [str(p) for p in Path(midi_folder).rglob("*.mid")]

labels = []

for midi_path in midi_files:
    print(f"\n🎵 Now playing: {Path(midi_path).name}")
    
    # Convert MIDI to WAV using fluidsynth
    os.system(f'fluidsynth -F temp.wav "{soundfont_path}" "{midi_path}"')
    
    # Play WAV
    try:
        wave_obj = sa.WaveObject.from_wave_file("temp.wav")
        play_obj = wave_obj.play()
    except Exception as e:
        print(f"❌ Error playing file: {e}")
        continue

    # Get user label
    while True:
        mood = input("Enter mood (0=Happy, 1=Sad, 2=Angry, 3=Relaxed, q=Quit): ").strip()
        if mood in ['0', '1', '2', '3']:
            labels.append({'filepath': midi_path, 'mood': int(mood)})
            break
        elif mood == 'q':
            play_obj.stop()
            print("Labeling stopped.")
            break
        else:
            print("❗Invalid input. Try again.")
    
    play_obj.stop()
    if mood == 'q':
        break

# Save labels to CSV
df = pd.DataFrame(labels)
df.to_csv("D:/Study/Ai_Music_Composer/project/data/labeled_data.csv", index=False)
print("✅ Labeling complete. Saved to labeled_data.csv")
