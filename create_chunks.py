import whisper
import json
import os

model = whisper.load_model("tiny.en")

Audios = os.listdir("Audio")

for audio in Audios:
    # print(audio)
    number = audio.split(".")[0]
    title = audio.split(".")[1][:-4]
    print(number, title)
        
    result = model.transcribe(audio = f"Audio/{audio}", task="transcribe", word_timestamps=True)

    chunks = []
    for segment in result["segments"]:
        chunks.append({ "number" : number ,"title" : title,  "start": segment["start"], "end": segment["end"], "text": segment["text"]})
        
    chunks_with_metadata = { "chunks" : chunks, "text": result["text"] }

    with open(f"Chunks/{audio.split('.')[0]}_chunks.json", "w") as f:
        json.dump(chunks_with_metadata, f, indent=4)