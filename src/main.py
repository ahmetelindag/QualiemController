import cv2
from core.image_processor import ImageProcessor

def resize_for_display(window_name, image, width=600):
    if image is None: return
    h, w = image.shape[:2]
    scale = width / w
    resized = cv2.resize(image, (width, int(h * scale)))
    cv2.imshow(window_name, resized)

def main():
    print("--- QualiemController: Defect Detection Test ---")
    
    processor = ImageProcessor()
    
    # Path control
    ref_path = "data/images/reference/ref.jpg"
    test_path = "data/images/test/test_01.jpg"

    try:
        # 1. Load
        print("[INFO] Loading images")
        img_ref = processor.load_image(ref_path)
        img_test = processor.load_image(test_path)

        # 2. Align
        print("[INFO] Aligning images")
        aligned_img, _ = processor.align_images(img_test, img_ref, debug=True)

        # 3. Detect Defect
        print("[INFO] Analyzing defects")
        result_img, diff_mask, count = processor.detect_defects(img_ref, aligned_img)
        
        print(f"\n ANALYSIS COMPLETE")
        print(f"❌ Defects Found: {count}")

        # 4. Show
        resize_for_display("1. Reference", img_ref)
        resize_for_display("2. Test (Aligned)", aligned_img)
        resize_for_display("3. Defect Mask (What computer sees)", diff_mask)
        resize_for_display("4. FINAL RESULT", result_img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()