import edge_tts

VOICES = {
    ("fa", "male"): "fa-IR-FaridNeural",
    ("fa", "female"): "fa-IR-DilaraNeural",
    ("en", "male"): "en-US-GuyNeural",
    ("en", "female"): "en-US-JennyNeural",
}


async def create_voice(text, language, gender, output_path):
    voice = VOICES.get((language, gender))

    if not voice:
        raise ValueError("Language or gender is invalid.")

    text = text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    tts = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    await tts.save(str(output_path))
