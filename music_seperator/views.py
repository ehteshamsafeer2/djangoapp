import os
import zipfile
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SongUploadForm
from django.http import HttpResponse
from django.shortcuts import render
from pydub import AudioSegment
import shutil
import random
import numpy as np
#import noisereduce as nr

def separate_instruments(request):
    num_variations = 20
    min_duration=100
    root_zip = []
    var_file = []
    print("Called")
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        print("checking form valid", form)
        if form.is_valid():
            song = form.save()
            original_audio = AudioSegment.from_file(song.audio_file.path)
            output_folder = os.path.join('media', 'output')
            # Process the song using Spleeter
   #         separator = Separator('spleeter:2stems')
    #        separator.separate_to_file(song.audio_file.path, output_folder)
            
            for i in range(num_variations):
                pitch_shift = random.uniform(-9, 7)   # Adjust speed by 80% to 120%
                varied_audio = original_audio.set_frame_rate(int(original_audio.frame_rate * 2 ** (pitch_shift)))
            #    varied_audio = apply_random_effects(original_audio)
                if len(varied_audio) < min_duration:
                    continue
                output_file = f"{output_folder}/variation_{i}.wav"
                varied_audio.export(output_file, format="wav")
            #extract_segments(file_list)
            # Create a zip file containing the separated instrument tracks
            zip_file_path = os.path.join("media", "output", "melody.zip")   
            with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for stem_name in os.listdir(output_folder):
                    if stem_name[-4:] == '.wav':
                        zipf.write(f'media/output/{stem_name}')

            # Provide the zip file as a download response
            # Empty the output_folder
            response = HttpResponse(open(zip_file_path, 'rb'))
            response['Content-Type'] = 'zip'
            response['Content-Disposition'] = 'attachment; filename="melody_generated.zip"'
            path = output_folder
            print(var_file)
            print(212)
            print(root_zip)
            for file_name in os.listdir(path):
     #           print(file_name)
    # construct full file pat
                file = path +'/'+ file_name
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    shutil.rmtree(file)

            return response

    else:
        form = SongUploadForm()
    return render(request, 'index.html', {'form': form})


def apply_random_effects(audio):
    # Apply filtering effects raondomly
    if random.choice([True, False]):
        filter_type = random.choice(["low-pass", "high-pass", "band-pass"])
        cutoff_frequency = random.randint(100, 5000)  # Adjust as needed
        if filter_type == "low-pass":
            audio = audio.low_pass_filter(cutoff_frequency)
        elif filter_type == "high-pass":
            audio = audio.high_pass_filter(cutoff_frequency)
        elif filter_type == "band-pass":
            band_width = random.randint(100, 1000)  # Adjust as needed
            audio = audio.low_pass_filter(cutoff_frequency + band_width).high_pass_filter(cutoff_frequency)

    # Apply modulation effects randomly (chorus or tremolo)
    if random.choice([True, False]):
        if random.choice(["chorus", "tremolo"]) == "chorus":
            num_voices = random.randint(2, 4)  # Number of chorus voices  # Adjust as needed
            delay_range = random.uniform(10, 50)  # Adjust as needed
            chorus_sound = AudioSegment.silent(duration=len(audio))
            for _ in range(num_voices):
                pitched_sound = audio
                delay_time = random.uniform(0, delay_range)
                delayed_sound = pitched_sound + AudioSegment.silent(duration=delay_time)
                chorus_sound += delayed_sound
            audio = chorus_sound

        elif random.choice(["chorus", "tremolo"]) == "tremolo":
            modulation_frequency = random.uniform(1, 5)  # Adjust as needed
            modulation_depth = random.uniform(0.2, 0.8)  # Adjust as needed
            duration_ms = len(audio)
            time_points = [i / 1000.0 for i in range(duration_ms)]  # Time points in seconds
            modulation_waveform = [1.0 + modulation_depth * (1 + np.sin(2 * np.pi * modulation_frequency * t)) for t in time_points]
            audio = audio * modulation_waveform

    # Apply reverb effect randomly
    if random.choice([True, False]):
        reverb = random.choice([50, 100, 150])  # Adjust reverb duration as needed
        audio = audio.apply_gain(reverb)

    return audio
