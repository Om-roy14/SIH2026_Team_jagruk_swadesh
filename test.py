import json
from Rag_agent import ask_rag

def main():
    while True:
        question = input("Enter your question (or type 'exit' to quit): ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            break
        result = ask_rag(question)
        print("\nJSON RESPONSE:")
        print(json.dumps(result, indent=4, ensure_ascii=False, default=str))
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()