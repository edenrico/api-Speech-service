import pyaudio
import wave
import whisper
import threading


def record_audio(filename, stop_event):
    chunk = 1024  
    format = pyaudio.paInt16  
    channels = 1
    rate = 44100  # 

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Gravando...")

    frames = []

    while not stop_event.is_set():
        data = stream.read(chunk)
        frames.append(data)

    print("Gravação concluída")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def transcribe_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print("Transcrição: {}".format(result["text"]))


def main():
    stop_event = threading.Event()
    filename = "chamada.wav"

   
    recording_thread = threading.Thread(target=record_audio, args=(filename, stop_event))
    recording_thread.start()

    
    input("Pressione Enter para parar a gravação...")

    
    stop_event.set()
    recording_thread.join()

    
    transcribe_audio(filename)

if __name__ == "__main__":
    main()
