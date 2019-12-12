questions = [
    "On a scale of 1 to 10, what is your favorite color?",
    "On a scale of 1 to 10, how friendly are you with kittens?",
    "Do you enjoy hikes (Y/N)?)",
    "Do you like video games (Y/N)?",
    ["Do you like airplanes or boats? (Please answer 'planes', 'boats', 'neither' or 'both')",
        "planes",
        "boats",
        "neither",
        "both"],
    "Are you a quality human being (Y/N)?",
]

def question_scale(n):
    while True:
        try:
            answer = float(input(questions[n] + "  "))
            if answer > 5:
                print("Good answer.")
                return 3
            if answer <= 5:
                print("You ought to be ashamed.")
                return -2
        except:
            print("Answer not valid. Please try again.")

def question_bool(n):
    while True:
        #try:
            answer = str(input(questions[n] + "  "))
            if (answer == "Y" or answer == "y"):
                print("Good.")
                return 2
            if (answer == "N" or answer == "n"):
                print("That is not exceptionally cash money of you.")
                return -2
            else:
                raise ValueError
        #except:
            print("That is not Y or N. Fool.")


print(question_bool(3))