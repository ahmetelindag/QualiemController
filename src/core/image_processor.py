import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=5000)
        
    def load_image(self, path):
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"ERROR: Image could not be found at -> {path}")
        return img

    def align_images(self, img_test, img_ref, debug=False):
        """Hizalama Fonksiyonu (Değişmedi)"""
        gray_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)
        gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)

        kp1, des1 = self.orb.detectAndCompute(gray_test, None)
        kp2, des2 = self.orb.detectAndCompute(gray_ref, None)

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        matches = matches[:int(len(matches) * 0.15)]

        if len(matches) < 4:
            return (img_test, None) if debug else img_test

        src_points = np.zeros((len(matches), 2), dtype=np.float32)
        dst_points = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            src_points[i, :] = kp1[match.queryIdx].pt
            dst_points[i, :] = kp2[match.trainIdx].pt

        h_matrix, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC)
        height, width = img_ref.shape[:2]
        aligned_img = cv2.warpPerspective(img_test, h_matrix, (width, height))

        if debug:
            return aligned_img, None
        return aligned_img

    def detect_defects(self, img_ref, img_aligned, min_area=50):
        """
        GÜNCEL MANTIK: Siyah Yol / Beyaz Zemin + Kenar Artefaktı Temizliği.
        """
        # Griye Çevir
        gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)
        gray_test = cv2.cvtColor(img_aligned, cv2.COLOR_BGR2GRAY)
        
        # Resim boyutlarını al (Kenar kontrolü için)
        img_h, img_w = gray_ref.shape[:2]
        border_margin = 10 # Kenardan kaç piksel içeriyi güvenli sayacağız?

        # Farkı Bul
        diff = cv2.absdiff(gray_ref, gray_test)
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.dilate(thresh, kernel, iterations=1)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        result_img = img_aligned.copy()
        defect_count = 0
        
        # Tasarım Rengi (Yeşil)
        box_color = (0, 255, 0) 
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            if area > min_area:
                x, y, w, h = cv2.boundingRect(cnt)

                # ---  (BORDER CHECK) ---
                # Eğer kutu resmin kenarlarına çok yakınsa, bu bir artefaktır. Atla.
                if (x < border_margin) or \
                   (y < border_margin) or \
                   (x + w > img_w - border_margin) or \
                   (y + h > img_h - border_margin):
                    continue # Bu hatayı yoksay ve bir sonrakine geç

                # Gerçek bir hata bulduk, sayacı artır
                defect_count += 1
                
                # --- RENK ANALİZİ ---
                mask_roi = np.zeros_like(gray_test)
                cv2.drawContours(mask_roi, [cnt], -1, 255, -1)
                mean_val = cv2.mean(gray_test, mask=mask_roi)[0]
                
                # --- SINIFLANDIRMA MANTIĞI ---
                # DURUM 1: BEYAZ FAZLALIK (Zemin Rengi) -> EKSİK BAKIR
                if mean_val > 150: 
                    if area < 200:
                        label = "pin-hole"
                    elif area < 600:
                        label = "mousebite"
                    else:
                        label = "open"
                        
                # DURUM 2: SİYAH FAZLALIK (Yol Rengi) -> FAZLA BAKIR
                else: 
                    if area > 350:
                        label = "short"
                    else:
                        label = "copper"
                
                # --- ÇİZİM ---
                cv2.rectangle(result_img, (x, y), (x + w, y + h), box_color, 2)
                
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                
                if y - 20 > 0:
                    text_y = y - 5
                    bg_rect = (x, y - 20, x + text_w + 4, y)
                else:
                    text_y = y + h + 15
                    bg_rect = (x, y + h, x + text_w + 4, y + h + 20)
                
                cv2.rectangle(result_img, (bg_rect[0], bg_rect[1]), (bg_rect[2], bg_rect[3]), (255, 255, 255), -1)
                cv2.rectangle(result_img, (bg_rect[0], bg_rect[1]), (bg_rect[2], bg_rect[3]), (0, 0, 0), 1)
                
                cv2.putText(result_img, label, (x + 2, text_y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        return result_img, thresh, defect_count