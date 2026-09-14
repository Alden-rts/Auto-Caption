# ==========================================
# KONFIGURASI STYLE CAPTION (ALEX HORMOZI STYLE)
# ==========================================

INPUT_VIDEO = "video_mentah.mp4"
OUTPUT_VIDEO = "hasil_autocaption.mp4"
TEMP_AUDIO = "temp_audio.mp3"
TEMP_ASS = "temp_subs.ass"

# --- RESOLUSI VIDEO ---
# Diset 1920x1080 karena melihat video referensi lo berbentuk horizontal (Landscape).
# Kalau mau dipakai untuk Shorts/Reels, tinggal dibalik jadi WIDTH=1080 dan HEIGHT=1920
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080

# --- PENGATURAN FONT ---
FONT_NAME = "Open Sans"
FONT_SIZE = 50               # Diperkecil sedikit agar pas di layar horizontal
OUTLINE_WIDTH = 3            
MARGIN_V = 225                # Jarak subtitle dari bawah layar

# --- WARNA (.ASS BGR FORMAT) ---
# Warna untuk Style utama di header file (Format: &HAABBGGRR)
STYLE_COLOR_WHITE = "&H00FFFFFF" 
STYLE_COLOR_BLACK = "&H00000000" 

# KUNCI SUPAYA TIDAK ADA BAYANGAN:
# BackColour diset ke &H80000000 (transparan) dan Shadow diset 0
STYLE_BACK_COLOR = "&H80000000"   
SHADOW_WIDTH = 0                 # 0 berarti TANPA BAYANGAN sama sekali

# --- PENGATURAN TEKS ---
WORDS_PER_CHUNK = 1           # Jumlah kata per layar