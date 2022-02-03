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
    parser.add_argument('-p', "--printargs", action="store_true", help="Print the entered arguments")

    args = parser.parse_args()

    if args.printargs:
        print('processing the following arguments:\n', args)

    correct = [None if elem == '_' else elem for elem in args.correct]

    misplaced_arguments = parse_misplaced_character_inputs(args.misplaced)

    return args.incorrect, misplaced_arguments, correct, args.ranked, args.all


def parse_misplaced_character_inputs(misplaced_argument):
    """
    example input from command line: __r__,___ac
    this input would be used to show that two guesses had misplaced characters. The first guess has a misplaced
    character at index 2, with a value of r. The second guess has two misplaced characters at indexes 3 and 4, with
    values a and c respectively. Notice that the guesses are separated by commas.
    Example: convert from ['_','_','r','_','_','_',',','_','_','_','_','a','c'] to ['__r__','___ac']
    """
    return "".join(misplaced_argument).split(',') if len(misplaced_argument) > 0 else []
