import argparse


def read_command_line_args():
    parser = argparse.ArgumentParser(description="Parse wordle characters.")
    parser.add_argument('-i', "--incorrect", type=list, default=[],
                        help="List of incorrect chars that are not in the Wordle word."
                             "(default: [])")

    parser.add_argument('-m', "--misplaced", type=list, default=[],
                        help="List of misplaced chars that are in the wordle word, but the location is unknown."
                             "(default: [])")

    parser.add_argument('-c', "--correct", type=list, default=[None, None, None, None, None],
                        help="A list of chars whose location/index in the tuple is also the correct location/index of "
                             "the char in the Wordle word. (default: [None, None, None, None, None])")

    parser.add_argument('-r', "--ranked", action="store_true",
                        help="Print the most common characters in each position, ranked.")
    parser.add_argument('-a', "--all", action="store_true", help="Print all 5-letter words.")

    args = parser.parse_args()

    print('processing the following arguments:\n', args)

    correct = [None if elem == '_' else elem for elem in args.correct]

    return args.incorrect, args.misplaced, correct, args.ranked, args.all
