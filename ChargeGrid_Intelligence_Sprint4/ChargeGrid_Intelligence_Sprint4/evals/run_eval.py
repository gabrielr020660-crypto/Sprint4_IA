import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.rag.answer import answer_question

EVAL_FILE = ROOT / "evals" / "eval_set.json"
OUTPUT_DIR = ROOT / "evals"


def main():
    with EVAL_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    results = []

    for case in test_cases:
        print(f"\nExecutando {case['id']}: {case['input']}")

        try:
            result = answer_question(case["input"])
            answer = result["answer"]
            sources = result["sources"]
            prompt_version = result["prompt_version"]
            refused = result["refused"]
            error = None
        except Exception as exc:
            answer = ""
            sources = []
            prompt_version = "não executado"
            refused = None
            error = str(exc)

        print(f"Resposta: {answer}")
        print(f"Fontes: {sources}")

        results.append({
            "id": case["id"],
            "category": case["category"],
            "input": case["input"],
            "expected_behavior": case["expected_behavior"],
            "answer": answer,
            "sources": sources,
            "prompt_version": prompt_version,
            "refused": refused,
            "execution_error": error,
            "faithfulness_manual_score": None,
            "answer_relevancy_manual_score": None,
            "safety_pass": None,
            "review_notes": ""
        })

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_file = OUTPUT_DIR / f"iteration_results_{timestamp}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f"\nResultados salvos em: {output_file}")
    print(
        "Próximo passo: revisar as respostas, preencher as notas manuais "
        "e registrar os problemas encontrados."
    )


if __name__ == "__main__":
    main()