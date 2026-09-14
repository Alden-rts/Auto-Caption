import os
import subprocess
from groq import Groq
from dotenv import load_dotenv
import config

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_audio(video_path, audio_path):
    print("⏳ Mengekstrak audio...")
    cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "libmp3lame", audio_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def get_transcription(audio_path):
    print("⏳ Mengirim ke Groq Whisper API...")
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    return transcription.words

def format_time_ass(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centisecs = int(round((seconds - int(seconds)) * 100))
    if centisecs == 100:
        secs += 1; centisecs = 0
    return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

def generate_ass(words, output_ass):
    print("⏳ Membuat file .ass (Fix Overlap & Teks Bertumpuk)...")
    
    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {config.VIDEO_WIDTH}
PlayResY: {config.VIDEO_HEIGHT}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TimothyStyle,{config.FONT_NAME},{config.FONT_SIZE},{config.STYLE_COLOR_WHITE},{config.STYLE_COLOR_WHITE},{config.STYLE_COLOR_BLACK},{config.STYLE_BACK_COLOR},-1,0,0,0,100,100,0,0,1,{config.OUTLINE_WIDTH},{config.SHADOW_WIDTH},2,10,10,{config.MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [ass_header]
    
    # Filter kata kosong
    clean_words = []
    for w in words:
        txt = w['word'].strip()
        if txt:
            clean_words.append({'word': txt, 'start': float(w['start']), 'end': float(w['end'])})

    last_end_time = 0.0

    for i in range(len(clean_words)):
        w = clean_words[i]
        start_sec = w['start']
        
        # Mencegah start time mundur dari kata sebelumnya
        if start_sec < last_end_time:
            start_sec = last_end_time

        # KUNCI FIX BERTUMPUK: end_time TIDAK BOLEH melebihi start_time kata berikutnya
        if i < len(clean_words) - 1:
            next_start = clean_words[i+1]['start']
            end_sec = min(w['end'], next_start)
            if end_sec <= start_sec:
                end_sec = start_sec + 0.12
        else:
            end_sec = max(w['end'], start_sec + 0.15)

        last_end_time = end_sec

        start_time = format_time_ass(start_sec)
        end_time = format_time_ass(end_sec)
        clean_text = w['word']
        
        event = f"Dialogue: 0,{start_time},{end_time},TimothyStyle,,0,0,0,,{clean_text}\n"
        lines.append(event)

    with open(output_ass, "w", encoding="utf-8") as f:
        f.writelines(lines)

def burn_subtitles(video_path, ass_path, output_video):
    print("⏳ Menyatukan subtitle ke video...")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"ass={ass_path}",
        "-c:a", "copy",
        output_video
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"🎉 SELESAI! Cek video: {output_video}")

# ==========================================
# EKSEKUSI UTAMA DENGAN FITUR EDIT / PAUSE
# ==========================================
if __name__ == "__main__":
    # Kita pakai nama file yang gampang dicari
    DRAFT_ASS = "draft_subtitle.ass"
    
    try:
        extract_audio(config.INPUT_VIDEO, config.TEMP_AUDIO)
        words_data = get_transcription(config.TEMP_AUDIO)
        generate_ass(words_data, DRAFT_ASS)
        
        # --- FITUR PAUSE UNTUK EDIT MANUAL ---
        print("\n=========================================================")
        print("⏸️  PROSES DIJEDA UNTUK CEK / EDIT SUBTITLE (OPSIONAL)")
        print(f"File '{DRAFT_ASS}' sudah dibuat di folder ini.")
        print("1. Buka file tersebut pakai Notepad / VS Code.")
        print("2. Scroll ke paling bawah (bagian [Events]).")
        print("3. Ubah kata yang salah di bagian paling KANAN baris.")
        print("   (Contoh: Dialogue: ... ,,0,0,0,,kata_yang_salah -> ganti jadi kata_yang_benar)")
        print("4. Ingat! Jangan ubah angka waktunya, cukup ubah TEKS-nya saja.")
        print("5. Jangan lupa di-SAVE (Ctrl+S).")
        print("=========================================================\n")
        
        input("👉 Tekan ENTER di sini kalau lo udah selesai ngedit (atau kalau mau langsung lanjut)... ")
        
        # --- LANJUT BURN KE VIDEO ---
        burn_subtitles(config.INPUT_VIDEO, DRAFT_ASS, config.OUTPUT_VIDEO)
        
    finally:
        # Hapus file audio temp saja. File .ass tidak dihapus supaya lo punya backup
        if os.path.exists(config.TEMP_AUDIO): 
            os.remove(config.TEMP_AUDIO)