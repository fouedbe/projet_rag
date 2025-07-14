from transformers import pipeline
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

def generate_answer(question: str, context_chunks: List[str], top_k: int = 3) -> str:
    try:
        # إعداد ال pipeline
        qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
        logging.info("✅ QA pipeline loaded successfully.")

        # قائمة للإجابات المحتملة
        answers = []

        for i, chunk in enumerate(context_chunks):
            if not chunk.strip():
                continue  # نتجاوز الشظايا الفارغة

            result = qa_pipeline(question=question, context=chunk)
            answer_text = result.get("answer", "").strip()
            score = result.get("score", 0)

            if answer_text:
                answers.append({
                    "answer": answer_text,
                    "score": score,
                    "chunk_index": i
                })

        # ترتيب الإجابات حسب الـ score
        sorted_answers = sorted(answers, key=lambda x: x["score"], reverse=True)

        if not sorted_answers:
            return "🤖 ما لقيتش إجابة واضحة في النص."

        # ترجع أقوى إجابة أو أكثر من إجابة حسب top_k
        top_answers = sorted_answers[:top_k]
        if top_k == 1:
            return top_answers[0]["answer"]
        else:
            return "\n".join([f"- {a['answer']} (score={a['score']:.2f})" for a in top_answers])

    except Exception as e:
        logging.error(f"🚨 Error during question answering: {e}")
        return "⚠️ صار مشكل أثناء توليد الإجابة."
