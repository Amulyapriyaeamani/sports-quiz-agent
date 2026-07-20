from src.database import query_database


def main():
    results = results = query_database(
    query_text="cricket records",
    sport="Cricket",
    difficulty="Hard",
    n_results=5
)

    print("\n===== Query Results =====\n")

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        print("No documents found.")
        return

    for index, doc in enumerate(documents, start=1):
        print(f"Result {index}")
        print("--------------------")
        print("Fact:")
        print(doc)

        if metadatas:
            print("\nMetadata:")
            print(metadatas[index - 1])

        print("\n")


if __name__ == "__main__":
    main()