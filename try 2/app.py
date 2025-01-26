@app.route("/process_audio", methods=["GET"])
def process_audio():
    try:
        # Update with the correct absolute path to your audio file
        file_path = "/Users/kabirkhanuja/My_drive/CS/#Hackathons/CodeFlix CodeZilla/try 2/sample.mp3"

        if not os.path.exists(file_path):
            return jsonify({"error": f"Audio file not found at {file_path}"}), 400

        
        diarization_result = diarize_audio(file_path)

        if "error" in diarization_result:
            return jsonify({"error": diarization_result["error"]}), 500

        speaker_files = []
        for idx, segment in enumerate(diarization_result.get("segments", [])):
            speaker = segment.get("label", f"unknown_speaker_{idx + 1}")
            speaker_file = os.path.join(RESULT_FOLDER, f"speaker_{speaker}_{idx + 1}.mp3")
            with open(speaker_file, "wb") as f:
                f.write(b"Dummy audio content")  # Replace this with real audio processing logic
            speaker_files.append(speaker_file)


        file_links = [f"http://127.0.0.1:5000/results/{os.path.basename(file)}" for file in speaker_files]
        return jsonify({"speakerFiles": file_links})

    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": str(e)}), 500
