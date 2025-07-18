#to check all the valid and non valid instruments
import os
from collections import Counter
import pretty_midi

def check_piano_instruments(root_folder):
    """Analyze instrument distribution across nested folders"""
    # piano_programs = range(8)
    piano_programs = {
    0: 'Acoustic Grand Piano',
    1: 'Bright Acoustic Piano',
    2: 'Electric Grand Piano',
    3: 'Honky-tonk Piano',
    4: 'Electric Piano 1',  # Rhodes
    5: 'Electric Piano 2',  # Chorused
    6: 'Harpsichord',
    7: 'Clavinet'
    }  
    # Programs 0-7 (piano family)
    results = {
        'total_files': 0,
        'valid_piano': 0,
        'invalid_files': 0,
        'instrument_dist': Counter()
    }

    for root, _, files in os.walk(root_folder):
        for file in files:
            if not file.lower().endswith(('.mid', '.midi')):
                continue

            results['total_files'] += 1
            filepath = os.path.join(root, file)

            try:
                pm = pretty_midi.PrettyMIDI(filepath)
                instruments = [i.program for i in pm.instruments]

                if not instruments:
                    results['invalid_files'] += 1
                    continue

                if all(program in piano_programs for program in instruments):
                    results['valid_piano'] += 1
                else:
                    for program in instruments:
                        name = pretty_midi.program_to_instrument_name(program)
                        results['instrument_dist'][name] += 1

            except Exception as e:
                results['invalid_files'] += 1
                continue

    return results
            
# Usage
analysis = check_piano_instruments('D:\Study\Ai_Music_Composer\project\data\Raw\Adl-piano-midi')
print(f"Total files: {analysis['total_files']}")
print(f"Valid piano-only: {analysis['valid_piano']} ({analysis['valid_piano']/analysis['total_files']:.1%})")
print(f"Non-piano instruments found:")
for instr, count in analysis['instrument_dist'].most_common():
    print(f"- {instr}: {count}")