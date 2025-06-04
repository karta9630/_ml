import cv2
import re
import pytesseract
from PIL import Image
import numpy as np
from mss import mss
from ultralytics import YOLO


my_dict = []
counter = 1 
# 設定 Tesseract 路徑
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 載入 YOLO 模型
model = YOLO("best_license_plate_model.pt")

# 設定螢幕截圖參數
sct = mss()
monitor = {
    "top": 0,       # 截圖起始位置 (y 軸)
    "left": 1300,      # 截圖起始位置 (x 軸)
    "width": 600,     # 截圖寬度
    "height": 1800     # 截圖高度
}
def detect_and_display():
    while True:
        # 截取螢幕
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)

        # OpenCV 顏色順序是 BGR，需要轉成 RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        # 進行物件偵測
        results = model.predict(source=img_rgb, conf=0.5, verbose=False)

        # 取得檢測框的座標
        for result in results[0].boxes:
            # 獲取每個物件的邊界框 (x1, y1, x2, y2)
            x1, y1, x2, y2 = result.xyxy[0].int().tolist()
            cropped_img = img_rgb[y1:y2, x1:x2]
            resized_img = cv2.resize(cropped_img, (1000, 250), interpolation=cv2.INTER_CUBIC)
            gray_img = cv2.cvtColor(resized_img,cv2.COLOR_RGB2GRAY)
            kernel = np.ones((3,3),np.uint8)
            open_img = cv2.morphologyEx(gray_img,cv2.MORPH_OPEN,kernel)
            sim_inv = cv2.threshold(open_img,100,255,cv2.THRESH_BINARY_INV)[1]
            mblur = cv2.medianBlur(sim_inv,3)
            
            cv2.imshow("Cropped Image", mblur)
            # 使用 Pillow 轉換為圖片格式進行 OCR
            pil_img = Image.fromarray(mblur)
            text = pytesseract.image_to_string(pil_img, lang="eng")
            out=add_dict(text)
            
            img_rgb = cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img_rgb, out, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 顯示包含檢測框的圖像
        cv2.imshow("YOLOv8 Detection", img_rgb)
        
        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


def add_dict(text):
    out = re.sub(r'[^A-Z0-9-]', '', text)
    if re.match(r'^[A-Z].*[A-Z0-9]$', out):  
        my_dict.append(out)
        find = my_dict.count(out)
        print(out)
        if find >2:
            return out
        else :
            return " "

if __name__ == "__main__":

     detect_and_display()
