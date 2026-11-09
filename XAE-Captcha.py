# =====================================================================
#  XAE-Captcha (Year 2050)

#  Someone claims to be a registered person. The system runs a small
#  TEST for each of five verification layers, turns each test result
#  into a score (0-100), combines the scores into one trust score, and
#  decides: APPROVED, EXTRA CHECK, or REJECTED.

#  The code is split into 6 SEGMENTS: (Do not add your code here, this is the introduction, do it below.)
#    Segment 1: Setup - settings and registered identities
#    Segment 2: Input helpers - asking questions safely
#    Segment 3: The five verification tests
#    Segment 4: Calculating the trust score
#    Segment 5: Making the decision
#    Segment 6: Main program and final report

#  DEMO ACCOUNTS (answers for your presentation):
#    username: Aina   PIN: 482913   habits: morning / phone / Kuala Lumpur
#                     vouchers: Zack, Nova, Alex
#                     in-person registration: 2048, North Office

#    username: Alex   PIN: 123456   habits: night / laptop / Penang
#                     vouchers: Aina, Neo, Zack
#                     in-person registration: 2049, South Office
#
#  Tip: for the biometric test, type the code after about 1-8 seconds.
# =====================================================================

import random  # to create a fresh random code for the liveness test
import time  # to measure how long a person takes to respond

# Segment 1: Setup - settings and registered identities

APP_NAME = "XAE-Captcha"  # text (string)
YEAR = 2050  # whole number (integer)
MAX_PIN_ATTEMPTS = 3  # whole number (integer)
MIN_CREDENTIAL = 30  # whole number (integer)
BORDERLINE_MARGIN = 10.0  # decimal (float)
SHOW_BARS = True  # True/False (boolean)

# Create LAYERS, a list of tuples: (layer name, weight, short description)
# The weights must add up to 1.0 (0.35 + 0.25 + 0.15 + 0.15 + 0.10 = 1.0)
LAYERS = [
    ("Credential", 0.35, "PIN verification"),
    ("Biometric", 0.25, "Speed and code reaction"),
    ("Behavior", 0.15, "Usual habits & patterns"),
    ("Vouching", 0.15, "Trusted network check"),
    ("In-person anchor", 0.10, "Physical registration data"),
]

# 3. Create REGISTRY, a list of tuples (one per registered person)
# Format: (username, pin, usual time, usual device, usual city, list of vouchers, in-person year, in-person office)
REGISTRY = [
    ("aina", "482913", "morning", "phone", "kuala lumpur", ["zack", "nova", "alex"], 2048, "north office"),
    ("alex", "123456", "night", "laptop", "penang", ["aina", "neo", "zack"], 2049, "south office")
]

# 4. Create three lists that line up by position for risk levels
RISK_LEVELS = ["low", "medium", "high"]
RISK_EXAMPLES = ["Social media posts", "Opening a bank account", "Transferring property"]
RISK_THRESHOLDS = [50, 70, 90]

# Segment 2: Input helpers - asking questions safely

# function 1: asking for non-empty text
def ask_text(prompt):
    while True:
        answer = input(prompt).strip()  # strip() to remove spaces
        if answer != "":
            return answer
        else:
            print("Error: Input cannot be empty.")


# function 2: asking for whole number
def ask_whole_num(prompt, low, high):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit():
            number = int(answer)
            if low <= number <= high:
                return number
            else:
                print("Error: Number is outside the range.")
        else:
            print("Error: Please enter a whole number.")


# function 3: asking for risk level
def ask_risk_level():
    print("\nSelect Risk Level: ")
    for i in range(len(RISK_LEVELS)):
        print(f" {i + 1}.{RISK_LEVELS[i].capitalize()} risk - {RISK_EXAMPLES[i]}")
    choice = ask_whole_num(f"\nEnter your risk level (1, 2, 3): ", 1, 3) - 1
    return choice


# function 4: ask for YES or NO
def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().upper()
        if answer == "YES":
            return answer
        elif answer == "NO":
            return answer
        else:
            print("Error: Invalid input (Yes or No).")


# function 5: find registered person
def find_person(username):
    for record in REGISTRY:  # REGISTRY depends on segment 1
        if record[0] == username:
            return record
    return None


# Segment 3: The five verification tests

# Each tests asks questions, checks the answers and then returns a tuple:
# (Score ranging 0 - 100, short note explaining the result)

def show_result(score, note):
    # Print the result of one test.
    print(f"  --> Score: {score}/100  ({note})")


def credential_test(pin):
    # TEST 1: Enter the PIN. Fewer attempts = higher score.
    print("\n[TEST 1: CREDENTIAL] Enter your secret PIN.")
    points_by_attempt = [100, 70, 40]  # a list: score for attempt 1, 2, 3
    score = 0
    note = f"PIN failed {MAX_PIN_ATTEMPTS} times."
    for attempt in range(MAX_PIN_ATTEMPTS):
        guess = input(f"  PIN (Attempt {attempt + 1} of {MAX_PIN_ATTEMPTS}): ").strip()
        if guess == pin:
            score = points_by_attempt[attempt]
            note = f"PIN correct on attempt {attempt + 1}."
            break
    show_result(score, note)
    return score, note


def biometric_test():
    # TEST 2: Type a fresh code. Real people respond in a human time.
    print("\n[TEST 2: BIOMETRIC] A live person must react to a fresh code.")
    code = f"{random.randint(0, 9999):04d}"
    input("  Press Enter when you are ready...")
    start = time.time()  # starts the stopwatch
    print(f"  >>>  {code}  <<<")
    answer = input("  Type the code you see: ").strip()
    seconds = round(time.time() - start, 1)  # Calculates the time by (end time - start time)

    if answer != code:
        score, note = 0, "Wrong code."
    elif seconds < 0.5:
        score, note = 20, f"Answered in {seconds}s: too fast, realistically impossible, most definitely AI."
    elif seconds <= 6:
        score, note = 100, f"Correct in {seconds}s: a normal human response, but still could be AI."
    else:
        score, note = 60, f"Correct but slow ({seconds}s): weaker proof of human presence, likely to be AI."
    show_result(score, note)
    return score, note


def behavior_test(usual_time, usual_device, usual_city):
    # TEST 3: Quiz about the person's usual habits.
    print("\n[TEST 3: BEHAVIOR] Answer questions about your usual habits.")
    questions = [
        "When do you usually log in? (morning/afternoon/evening): ",
        "Which device do you usually use? (phone/laptop/tablet): ",
        "Which city do you usually log in from?: ",
    ]
    correct_answers = [usual_time, usual_device, usual_city]
    correct = 0
    for i in range(len(questions)):
        answer = input("  " + questions[i]).strip().lower()
        if answer == correct_answers[i]:
            correct += 1
    score = round(correct / len(questions) * 100)
    note = f"{correct} of {len(questions)} habits matched."
    show_result(score, note)
    return score, note


def vouching_test(username, contacts):
    # TEST 4: Name up to 3 people who can vouch for you.
    print("\n[TEST 4: VOUCHING] Name up to 3 verified people who can vouch for you.")
    print("  (Press Enter on an empty line to stop early.)")
    vouchers = []
    while len(vouchers) < 3:
        name = input(f"  Voucher {len(vouchers) + 1}: ").strip().lower()
        if name == "":
            break
        elif name == username:
            print("  You cannot vouch for yourself.")
        elif name in vouchers:
            print("  You already named that person.")
        else:
            vouchers.append(name)

    confirmed = 0
    for name in vouchers:
        if name in contacts:  # is the name in the registered list?
            confirmed += 1
            print(f"  {name.capitalize()} confirmed.")
        else:
            print(f"  {name.capitalize()} does not know this account.")
    score = round(confirmed / 3 * 100)
    note = f"{confirmed} of 3 vouchers confirmed."
    show_result(score, note)
    return score, note


def anchor_test(anchor_year, anchor_office):
    # TEST 5: Details of the one-time in-person registration.
    print("\n[TEST 5: IN-PERSON ANCHOR] Recall your in-person registration.")
    year_answer = ask_whole_num("  Which year did you register in person? ", 2000, YEAR)
    office_answer = ask_text("  Which office did you visit? ").lower()

    points = 0
    difference = abs(year_answer - anchor_year)  # abs() ignores minus signs
    if difference == 0:
        points += 50
        year_note = "Year matched"
    elif difference == 1:
        points += 25
        year_note = "Year off by 1"
    else:
        year_note = "Wrong year"

    if office_answer == anchor_office:
        points += 50
        office_note = "Office matched"
    else:
        office_note = "Wrong office"

    note = f"{year_note}, {office_note}."
    show_result(points, note)
    return points, note


def run_all_tests(record):
    # Run the five tests in order. Return two lists: scores and notes.
    username, pin, usual_time, usual_device, usual_city, contacts, a_year, a_office = record

    results = [credential_test(pin), biometric_test(), behavior_test(usual_time, usual_device, usual_city),
               vouching_test(username, contacts), anchor_test(a_year, a_office)]

    scores = []
    notes = []
    for result in results:
        scores.append(result[0])
        notes.append(result[1])
    return scores, notes


# Segment 4: Calculating the trust score

# the reason why scores,points & digits flagged/warned because its name the same as inputs
# but ig it's fine ,cuz it just serves as placeholders,doesn't interfere with the code
# also need to wait for LAYERS[], scores[], points and digit
# before this can work so ye
# the functions:trust scores, average, points, combinations

def calculate_trust_score(scores):
    trust = 0
    for i in range(len(scores)):
        multiply = scores[i] * LAYERS[i][1]
        trust += multiply
    return round(trust, 1)


def calculate_simple_average(scores):
    return round(sum(scores) / len(scores), 1)


def make_bar(points):
    num_blocks = int(points // 10)
    leftover_blocks = points % 10
    bar = num_blocks * '#'
    if leftover_blocks >= 5:
        bar += '+'
    return bar


def pin_combinations(digits):
    return 10 ** digits

# Segment 5: Making the decision

def make_decision(scores, trust_score, risk_index):
    # Decide APPROVED, EXTRA CHECK or REJECTED. Returns a tuple: (decision, reason)
    # Order matters here: the first check that matches wins.
    needed = RISK_THRESHOLDS[risk_index]  # score needed for the chosen risk level
    credential_score = scores[0]  # Credential is the first layer in LAYERS

    if credential_score < MIN_CREDENTIAL:
        decision = "REJECTED"
        reason = f"Credential score {credential_score} is below the minimum of {MIN_CREDENTIAL} (hard rule)."
    elif trust_score >= needed:
        decision = "APPROVED"
        reason = f"Trust score {trust_score} meets the {RISK_LEVELS[risk_index]}-risk threshold of {needed}."
    elif trust_score >= needed - BORDERLINE_MARGIN:
        decision = "EXTRA CHECK"
        reason = f"Trust score {trust_score} is within {BORDERLINE_MARGIN} points below the threshold of {needed}."
    else:
        decision = "REJECTED"
        reason = f"Trust score {trust_score} is too far below the threshold of {needed}."
    return decision, reason


def find_weakest_layer(scores):
    # Find the layer with the lowest score. Returns a tuple: (layer name, score)
    weakest = 0  # start by assuming the first layer is the weakest
    for i in range(len(scores)):
        if scores[i] < scores[weakest]:  # found a lower score, remember its position
            weakest = i
    return LAYERS[weakest][0], scores[weakest]


# Segment 6
def check_one_person(history):
    username = ask_text("\nClaimed username: ").lower()
    risk_index = ask_risk_level()
    risk_level = RISK_LEVELS[risk_index]
    record = find_person(username)

    if record is None:
        print(f"REJECTED: username '{username.upper()}' is not registered.")
        history.append((username, risk_level, None, "REJECTED"))
        return

    print(f"\nIdentity found. Starting the 5 verification tests for {username.upper()}.")

    scores, notes = run_all_tests(record)
    trust_score = calculate_trust_score(scores)
    average_score = calculate_simple_average(scores)
    decision, reason = make_decision(scores, trust_score, risk_index)
    weakest_layer, weakest_score = find_weakest_layer(scores)

    print()
    print(f"=" * 48)
    print("             VERIFICATION REPORT             ")
    print(f"=" * 48)
    for i, (layer_name, _, _) in enumerate(LAYERS):
        bar = make_bar(scores[i]) if SHOW_BARS else ""
        print(f"{layer_name:18} {scores[i]:3}/100  {bar:10} {notes[i]}")
    print(f"\nTrust score: {trust_score}/100")
    print(f"Simple average: {average_score}/100")
    print(f"Weakest layer: {weakest_layer} ({weakest_score}/100)")
    print(f"\n[DECISION]: {decision} - {reason}")
    history.append((username, risk_level, trust_score, decision))


def show_summary(history):
    print()
    print(f"=" * 58)
    print(f"*"*20, "SESSION SUMMARY", "*"*21)
    print(f"=" * 58)
    print(f"\n{'Username':<16} {'Risk':<10} {'Trust score':<12} Decision")
    print("-" * 58)
    approved = 0
    rejected = 0
    extra = 0
    for username, risk_level, trust_score, decision in history:
        score_text = "N/A" if trust_score is None else f"{trust_score}/100"
        print(f"{username.upper():<16} {risk_level:<10} {score_text:<12} {decision}")
        if decision == 'APPROVED':
            approved += 1
        elif decision == 'EXTRA CHECK':
            extra += 1
        else:
            rejected += 1
    print("-" * 58)
    print(
        f"Approved: {approved} | Extra check: {extra} | Rejected: {rejected}")


def main():
    print(f"=" * 48)
    print(f"*** {APP_NAME} Identity Verification ({YEAR}) ***")
    print(f"=" * 48)
    history = []
    while True:
        check_one_person(history)
        if ask_yes_no("\nCheck another person? (Yes/No) ") == "NO":
            break
    show_summary(history)
    print(f'\nThank you for using {APP_NAME}.')


main()
