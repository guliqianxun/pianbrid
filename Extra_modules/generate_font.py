from midiutil import MIDIFile
import subprocess
import os

def create_signal_midi_file(filename, note, duration=1.0):
    """
    为单个音符创建MIDI文件。
    
    :param filename: 输出的MIDI文件名
    :param note: MIDI音符编号
    :param duration: 音符持续时间（默认1.0秒）
    """
    midi_file = MIDIFile(1)
    track = 0
    time = 0
    
    midi_file.addTrackName(track, time, f"Note {note}")
    midi_file.addTempo(track, time, 120)

    channel = 0
    volume = 100
    
    midi_file.addNote(track, channel, note, time, duration, volume)

    with open(filename, 'wb') as file:
        midi_file.writeFile(file)

def synthesize_midi_to_audio(midi_filename, soundfont_path, output_filename='output.wav', sample_rate='44100'):
    """
    使用FluidSynth将MIDI文件合成音频文件。
    
    :param midi_filename: 输入的MIDI文件名
    :param soundfont_path: 声音字库文件的路径
    :param output_filename: 输出的音频文件名（默认'output.wav'）
    :param sample_rate: 采样率（默认44100）
    """
    command = [
        'fluidsynth',
        '-ni',
        soundfont_path,
        midi_filename,
        '-F', output_filename,  # 指定输出文件名和格式
        '-r', sample_rate  # 设置采样率
    ]

    subprocess.run(command, check=True)
    print(f"MIDI file has been processed and audio has been saved to '{output_filename}'")

def midi_number_to_note(note_number):
    """
    将 MIDI 音符编号转换为音符名称。
    
    :param note_number: MIDI 音符编号
    :return: 音符名称（例如 'C4', 'D4' 等）
    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note_names[note_number % 12]
    octave = note_number // 12 - 1
    return f"{note_name}{octave}"

def main():
    # 定义音符映射
    note_mapping = {
        'a': ('C4', 60),
        's': ('D4', 62),
        'd': ('E4', 64),
        'f': ('F4', 65),
        'j': ('G4', 67),
        'k': ('A4', 69),
        'l': ('B4', 71),
        ';': ('C5', 72)
    }

    # 创建输出目录
    output_dir = "./assets/sounds/piano_notes"
    os.makedirs(output_dir, exist_ok=True)

    # 定义声音字库文件的路径
    soundfont_path = './assets/sounds/Emperador Classic Concert Grand Piano.sf3'

    # 为每个音符创建MIDI和WAV文件
    for key, (note_name, midi_note) in note_mapping.items():
        midi_filename = os.path.join(output_dir, f"{note_name}.mid")
        wav_filename = os.path.join(output_dir, f"{note_name}.wav")
        
        create_signal_midi_file(midi_filename, midi_note)
        synthesize_midi_to_audio(midi_filename, soundfont_path, wav_filename)

    print("All notes have been processed. WAV files are available in the 'piano_notes' directory.")

    # 创建音符到WAV文件的映射
    wav_mapping = {key: f"{output_dir}/{note_name}.wav" for key, (note_name, _) in note_mapping.items()}
    print("WAV file mapping:")
    print(wav_mapping)

if __name__ == "__main__":
    main()