from src.generator import generate_quiz


def main():

    quiz = generate_quiz(
        sport="Cricket",
        difficulty="Hard"
    )

    print(f"\nSport: {quiz['sport']}")
    print(f"Difficulty: {quiz['difficulty']}")

    print("\n" + "=" * 60)

    for i, q in enumerate(quiz["questions"], start=1):

        print(f"\nQuestion {i}")
        print(q["question"])

        for key, value in q["options"].items():
            print(f"{key}. {value}")

        print(f"\nAnswer: {q['correct_answer']}")
        print(f"Explanation: {q['explanation']}")

if __name__ == "__main__":
    main()