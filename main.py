from agent import Agent


def main() -> None:
    try:
        agent = Agent()
    except Exception as exc:
        print(f"Initialization error: {exc}")
        return

    print("Custom Python Agent")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_message.lower() in ("exit", "quit"):
            break
        if not user_message:
            continue

        try:
            response = agent.run(user_message)
            print(f"\nAgent: {response}\n")
        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    main()
