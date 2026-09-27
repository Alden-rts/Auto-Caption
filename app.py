from flask import Flask, render_template, request, jsonify
import os
import webbrowser

from main import transcribe_audio, generate_ass, burn_subtitles

app = Flask(__name__)

# Konfigurasi Folder Upload Statis
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

INPUT_VIDEO_PATH = os.path.join(UPLOAD_FOLDER, 'input_video.mp4')
OUTPUT_VIDEO_PATH = os.path.join(UPLOAD_FOLDER, 'output_video.mp4')
ASS_FILE = "temp_subtitles.ass"

# ==========================================
# HELPER: Konversi Waktu CapCut <-> Detik
# ==========================================
def float_to_capcut_time(seconds):
    """Mengubah detik (float) dari Whisper ke format MM:SS:cs"""
    try:
        seconds = float(seconds)
    except (ValueError, TypeError):
        seconds = 0.0
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    cs = int(round((seconds % 1) * 100))
    if cs >= 100:
        secs += 1
        cs = 0
    return f"{mins:02d}:{secs:02d}:{cs:02d}"

def capcut_time_to_float(time_str):
    """Mengubah format MM:SS:cs kembali ke detik (float) untuk ASS"""
    parts = str(time_str).strip().split(':')
    try:
        if len(parts) == 3:
            mins, secs, cs = int(parts[0]), int(parts[1]), int(parts[2])
            return (mins * 60) + secs + (cs / 100.0)
        elif len(parts) == 4:
            hrs, mins, secs, cs = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            return (hrs * 3600) + (mins * 60) + secs + (cs / 100.0)
    except ValueError:
        return 0.0
    return 0.0

# ==========================================
# ROUTES API
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({"status": "error", "message": "File video tidak ditemukan!"}), 400
            
        file = request.files['video']
        if file.filename == '':
            return jsonify({"status": "error", "message": "File kosong!"}), 400

        print(f"📥 Menerima file upload: {file.filename}")
        file.save(INPUT_VIDEO_PATH)
        return jsonify({
            "status": "success", 
            "message": "Video berhasil diupload!", 
            "video_url": f"/{INPUT_VIDEO_PATH}"
        })
    except Exception as e:
        print(f"❌ Error Upload: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_video', methods=['POST'])
def delete_video():
    try:
        for path in [INPUT_VIDEO_PATH, OUTPUT_VIDEO_PATH, ASS_FILE]:
            if os.path.exists(path):
                os.remove(path)
        print("🗑️ File temporary berhasil dibersihkan")
        return jsonify({"status": "success", "message": "Video berhasil dihapus!"})
    except Exception as e:
        print(f"❌ Error Delete: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if not os.path.exists(INPUT_VIDEO_PATH):
            return jsonify({"status": "error", "message": "Upload video dulu bro!"}), 400

        print("🎙️ Memulai ekstraksi audio...")
        words = transcribe_audio(INPUT_VIDEO_PATH)
        capcut_text = ""
        for w in words:
            start_str = float_to_capcut_time(w['start'])
            end_str = float_to_capcut_time(w['end'])
            capcut_text += f"{start_str} - {end_str}\n{w['word']}\n\n"
            
        return jsonify({"status": "success", "capcut_text": capcut_text.strip()})
    except Exception as e:
        print(f"❌ Error Transkripsi: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_captions():
    try:
        if not os.path.exists(INPUT_VIDEO_PATH):
            return jsonify({"status": "error", "message": "Video sumber tidak ditemukan!"}), 400

        data = request.json
        capcut_text = data.get('capcut_text', '')
        styles = data.get('styles', {})

        print("🔄 Membaca format CapCut dari UI...")
        words = []
        blocks = capcut_text.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                times = lines[0].split(' - ')
                if len(times) == 2:
                    start = capcut_time_to_float(times[0])
                    end = capcut_time_to_float(times[1])
                    word_text = " ".join(lines[1:]).strip()
                    if word_text:
                        words.append({'start': start, 'end': end, 'word': word_text})

        print(f"🎨 Processing ASS (Is Template: {styles.get('is_template', False)})...")
        generate_ass(words, ASS_FILE, styles)
        burn_subtitles(INPUT_VIDEO_PATH, ASS_FILE, OUTPUT_VIDEO_PATH)
        print("✅ Render Selesai!")

        return jsonify({
            "status": "success", 
            "message": "Video berhasil diproses!",
            "video_url": f"/{OUTPUT_VIDEO_PATH}"
        })
    except Exception as e:
        print(f"❌ Error Render: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
    print("==================================================")
    print("🚀 Server Lokal Siap & Membuka Browser Otomatis!")
    print("==================================================")
    webbrowser.open(url)
    app.run(debug=True, port=5000)