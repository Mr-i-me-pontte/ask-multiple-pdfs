if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='PDF Chat Lambda')
    parser.add_argument('--initialize', action='store_true', help='Initialize the conversation with PDFs')
    parser.add_argument('--question', type=str, help='User question for the conversation')
    parser.add_argument('--pdfs', nargs='+', type=str, help='List of PDF files to process')

    args = parser.parse_args()

    if args.initialize:
        # Initialize the conversation with PDFs
        conversation_handler = ConversationHandler()
        message = conversation_handler.initialize_conversation(args.pdfs)
        print(message)

    elif args.question:
        # Handle user question
        conversation_handler = ConversationHandler()
        chat_history = conversation_handler.handle_user_input(args.question)
        for message in chat_history:
            print(message)

    else:
        print("Invalid command. Use '--initialize' to process PDFs or '--question' to ask a question.")
