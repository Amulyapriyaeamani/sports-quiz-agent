from src.search import get_live_news_context


def main():

    context = get_live_news_context(
        "Cricket"
    )

    print("\n===== LIVE SPORTS NEWS =====\n")
    print(context)


if __name__ == "__main__":
    main()