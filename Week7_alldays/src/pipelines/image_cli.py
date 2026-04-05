from retriever.image_search import ImageSearch
from generator.caption_generator import CaptionGenerator
from generator.image_answer import ImageAnswerGenerator
from utils.chart_detector import detect_chart_type
from utils.logger import log_info
import pytesseract
import cv2
import os


# 🔥 OCR CLEANER (FIXED)
def clean_ocr(text):
    words = text.split()

    clean = []
    for w in words:
        if any(c.isalpha() for c in w) and len(w) > 2:
            clean.append(w)

    return " ".join(clean[:40])  # limit


# 🔥 OCR EXTRACTION (IMPROVED)
def extract_text(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    thresh = cv2.resize(thresh, None, fx=2, fy=2)

    config = r'--oem 3 --psm 11'

    text = pytesseract.image_to_string(thresh, config=config)

    return text.strip()


# 🔥 CAPTION IMPROVER (IMPORTANT)
def improve_caption(caption):
    caption = caption.lower()

    if "bar" in caption:
        return "Bar chart showing comparison across categories"
    elif "pie" in caption:
        return "Pie chart showing distribution of categories"
    elif "graph" in caption or "plot" in caption:
        return "Graph showing trend or relationship"
    else:
        return caption


def main():
    search = ImageSearch()
    cap = CaptionGenerator()
    ans = ImageAnswerGenerator()

    print("IMAGE RAG SYSTEM (SMART FINAL)")

    while True:
        print("\n1. Text→Image\n2. Image→Image\n3. Image→Text\n4. Exit")
        c = input("Choice: ")

        # -------- TEXT → IMAGE --------
        if c == "1":
            q = input("Query: ")
            log_info(f"[QUERY] {q}")

            res = search.search_by_text(q)

            for i, r in enumerate(res, 1):
                image_path = os.path.join("src/data/raw/images", r["file"])

                caption, _ = cap.generate(image_path, r["ocr"])
                caption = improve_caption(caption)

                print(f"\nRESULT {i}")
                print("-" * 40)
                print("File:", r["file"])
                print("Caption:", caption)

        # -------- IMAGE → IMAGE --------
        elif c == "2":
            p = input("Path: ")
            log_info(f"[IMAGE SEARCH] {p}")

            res = search.search_by_image(p)

            for i, r in enumerate(res, 1):
                image_path = os.path.join("src/data/raw/images", r["file"])

                caption, _ = cap.generate(image_path, r["ocr"])
                caption = improve_caption(caption)

                print(f"\nRESULT {i}")
                print("-" * 40)
                print("File:", r["file"])
                print("Caption:", caption)

        # -------- IMAGE → TEXT --------
        elif c == "3":
            p = input("Path: ")

            # STEP 1: caption
            caption, _ = cap.generate(p, "")
            caption = improve_caption(caption)

            # STEP 2: OCR
            raw_text = extract_text(p)
            ocr_text = clean_ocr(raw_text)

            # STEP 3: chart type
            chart_type = detect_chart_type(p, caption)

            # STEP 4: LLM
            answer = ans.generate(caption, ocr_text, chart_type)

            print("\nEXPLANATION")
            print("-" * 40)
            print(answer)

        elif c == "4":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()