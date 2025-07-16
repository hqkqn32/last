import cv2

# 📷 Kamera yakalayıcı
cap = cv2.VideoCapture(0)  # veya '/dev/video0'

# 🎥 Kaydedilecek boyutlar
target_width = 640
target_height = 480

# 🔧 Genişlik/yükseklik ayarla
cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)

# ✅ Dosyaya yazıcı (output.mp4)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 formatı için
out_file = cv2.VideoWriter('output.mp4', fourcc, 30, (target_width, target_height))

# ✅ UDP yayını için GStreamer VideoWriter
gst_out = cv2.VideoWriter(
    'appsrc ! videoconvert ! video/x-raw,format=I420 ! '
    'x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! '
    'rtph264pay config-interval=1 pt=96 ! '
    'udpsink host=10.94.167.27 port=5005',
    cv2.CAP_GSTREAMER,
    0,  # fourcc
    30,
    (target_width, target_height)
)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

if not out_file.isOpened():
    print("Dosya kaydedici başlatılamadı!")

if not gst_out.isOpened():
    print("UDP GStreamer çıkışı başlatılamadı!")

print("Kayıt ve UDP yayın başlatıldı. Çıkmak için 'q'ya bas.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı.")
        break

    # Görüntüyü hem kaydet hem UDP ile gönder
    out_file.write(frame)
    gst_out.write(frame)

    cv2.imshow('Kamera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out_file.release()
gst_out.release()
cv2.destroyAllWindows()
