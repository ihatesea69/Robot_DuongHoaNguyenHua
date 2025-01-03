import time
import cv2
import random
import threading
from ffpyplayer.player import MediaPlayer
from playsound import playsound
import numpy as np

# Hàm hiển thị mắt với âm thanh đồng bộ
def display_eye(video_path):
    # Khởi tạo VideoCapture
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Không thể mở video:", video_path)
        return

    # Sử dụng ffpyplayer để phát âm thanh từ video
    player = MediaPlayer(video_path)

    loop_count = 0
    loop_max = 10

    # Lấy kích thước video
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(video_height)

    # Kích thước khung hình nền (màu đen)
    screen_width, screen_height = 1920, 1200  # Đặt độ phân giải màn hình
    background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)  # Khung màu đen

    # Tạo cửa sổ hiển thị video
    window_name = "ROBOT"
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Cho phép thay đổi kích thước cửa sổ
    # cv2.resizeWindow(window_name, screen_width, screen_height)  # Cửa sổ có thể thay đổi kích thước để phù hợp với độ phân giải

    while loop_count < loop_max:
        ret, frame = cap.read()  # Đọc từng frame của video
        if not ret:  # Nếu video kết thúc
            loop_count = loop_count + 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Quay lại frame đầu tiên
            continue

        # Lấy audio stream và đồng bộ hóa với video
        audio_frame, val = player.get_frame()
        if val == 'eof':  # Kiểm tra nếu âm thanh đã hết
            player = MediaPlayer(video_path)  # Tạo lại player nếu âm thanh kết thúc
        if audio_frame is not None:
            pass  # Âm thanh được phát tự động bởi ffpyplayer

        # Đặt video vào giữa nền đen
        start_x = (screen_width - video_width) // 2
        start_y = (screen_height - video_height) // 2
        end_x = start_x + video_width
        end_y = start_y + video_height

        # Xóa nền cũ và chèn video vào giữa
        background[:, :] = 0  # Đặt lại nền đen
        background[start_y:end_y, start_x:end_x] = frame

        # Hiển thị video với nền đen
        cv2.imshow(window_name, background)

        # Thoát nếu người dùng nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Người dùng đã nhấn 'q', thoát chương trình.")
            break

    # Giải phóng tài nguyên
    cap.release()
    # cv2.destroyAllWindows()

# Hàm phát âm thanh chúc mừng năm mới 
def play_greeting_audio(): 
    greeting_sounds = ['VN', 'EN', 'CHINA', 'FR', 'JP', 'KR', 'RUS']
    for i in greeting_sounds:
        audio_path = 'resouces/sound_greeting/HPNewYear_' + i +'.mp3'
        try:
            playsound(audio_path)
            time.sleep(1)
        except Exception as e:
            print("Lỗi khi phát âm thanh:", e)

# Hàm phát âm thanh
def play_audio(audio_path): 
    try:
        playsound(audio_path)
    except Exception as e:
        print("Lỗi khi phát âm thanh:", e)

def display_eye_with_audio(video_path):
    # Tạo thread để phát âm thanh chào hỏi
    greeting_thread = threading.Thread(target=play_greeting_audio)
    
    # Bắt đầu các thread
    greeting_thread.start()
    
    # Phát video
    display_eye(video_path)
    
    # Đợi các thread kết thúc
    greeting_thread.join()


# Định nghĩa các hàm gesture
def gesture_happy():
    return "Hành động: Vẫy tay vui vẻ!"

def gesture_roll():
    return "Hành động: Xoay tròn mắt!"

def gesture_heart():
    return "Hành động: Tạo hình trái tim bằng tay!"

def gesture_blink():
    return "Hành động: Chớp mắt liên tục!"


# Tạo danh sách trạng thái cảm xúc
def create_emotion_dict(eye, gesture):
    return {
        "eye": eye,
        "gesture": gesture
    }

happy = create_emotion_dict("resouces/happy/happy.mp4", gesture_happy)
roll = create_emotion_dict("resouces/roll/roll.mp4", gesture_roll)
heart = create_emotion_dict("resouces/heart/heart.mp4", gesture_heart)
blink = create_emotion_dict("resouces/blink/blink.mp4", gesture_blink)

def main():
    emotions = [happy, roll, heart, blink]

    while True:
        selected_emotion = random.choice(emotions)
        print(selected_emotion)
        display_eye_with_audio(selected_emotion["eye"]) 

if __name__ == "__main__":
    main()



