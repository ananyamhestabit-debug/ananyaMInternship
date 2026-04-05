from generator.llm_client import LLMClient


class ImageAnswerGenerator:
    def __init__(self):
        self.llm = LLMClient()

    def generate(self, caption, ocr_text, chart_type):

        if not ocr_text or len(ocr_text.strip()) < 5:
            prompt = f"""
You are analyzing a {chart_type}.

Caption: {caption}

Explain clearly what this chart shows in 2 lines.
"""
        else:
            prompt = f"""
You are analyzing a {chart_type}.

Caption: {caption}
Text: {ocr_text}

Explain main idea and trend in 2 lines.
"""

        return self.llm.generate(prompt)