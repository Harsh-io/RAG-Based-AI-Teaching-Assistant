import whisper
import json

model = whisper.load_model("tiny.en")
result = model.transcribe(audio = "Audio/2_Video.mp3", task="transcribe", word_timestamps=True)

# print(result["text"])
# print(result["segments"])
#print(result)

# with open("sample.json", "w") as f:
#     json.dump(result, f, indent=4) 


chunk = []
for segment in result["segments"]:
    chunk.append({"start": segment["start"], "end": segment["end"], "text": segment["text"]})

    # print(json.dumps(chunk, indent=4))
    # print(chunk)

    with open("chunks.json", "w") as f:
        json.dump(chunk, f, indent=4)

