import librosa
import numpy as np

def detect_beats(audio_file, bpm, time_signature, song_duration, volume_threshold):
    # Step 1: Analyze the audio file to detect beats
    y, sr = librosa.load(audio_file)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, bpm=bpm, units='time')

    # Step 2: Calculate time interval between beats
    beat_interval =  (60 / bpm )

    # Step 3: Determine volume threshold
    volume_threshold = volume_threshold  # You can adjust this threshold based on your needs

    # Step 4: Iterate through beats and check volume
    num_beats = int(np.ceil(song_duration / beat_interval))
    beat_list = []
    beat_idx = 0

    for i in range(num_beats):
        if beat_idx < len(beats) and beats[beat_idx] < (i + 1) * beat_interval:
            # Check the volume of the beat
            beat_volume = np.max(np.abs(y[int(beats[beat_idx] * sr):int((beats[beat_idx] + 0.1) * sr)]))
            print(beat_volume)
            if beat_volume >= volume_threshold:
                beat_list.append(1)
            else:
                beat_list.append(0)
            beat_idx += 1
        else:
            beat_list.append(0)
    
    print(beat_list)
    print(len(beat_list))
    return beat_list