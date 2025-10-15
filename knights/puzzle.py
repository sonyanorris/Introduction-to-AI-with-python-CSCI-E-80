from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Functions to create logical statements for any character. Can be re-used in KBs in the puzzles below.


# Function for characters who speak
def character_rules(Knight, Knave, statement):
    return And(
        # There could be only 1 knight and 1 knave
        # A character cannot be both a knight and a knave
        Biconditional(Knight, Not(Knave)),
        # If a character is a knight, then the statement is true
        Implication(Knight, statement),
        # If a character is a knave, then the statment is false
        Implication(Knave, Not(statement)),
    )


# Function for characters who do NOT speak
def silent_character_rules(Knight, Knave):
    # There could be only 1 knight and 1 knave
    # A character cannot be both a knight and a knave
    return Biconditional(Knight, Not(Knave))


# Puzzle 0
# A says "I am both a knight and a knave."
statement0 = And(AKnight, AKnave)
# Create QB
knowledge0 = And(character_rules(AKnight, AKnave, statement0))


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement1 = And(AKnave, BKnave)
# Create KB
knowledge1 = And(
    character_rules(AKnight, AKnave, statement1),
    silent_character_rules(BKnight, BKnave),
)


# Puzzle 2

# A says "We are the same kind."
statement2_A = Biconditional(AKnight, BKnight)
# B says "We are of different kinds."
statement2_B = Biconditional(AKnight, Not(BKnight))
# Create KB
knowledge2 = And(
    character_rules(AKnight, AKnave, statement2_A),
    character_rules(BKnight, BKnave, statement2_B),
)


# Puzzle 3

# A says either "I am a knight." or "I am a knave.", but you don't know which.
A_says_Knight_Knave = Or(
    character_rules(AKnight, AKnave, AKnight), character_rules(AKnight, AKnave, AKnave)
)
# B says "A said 'I am a knave'."
A_says_Knave = And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
B_says_A_says_Knave = character_rules(BKnight, BKnave, A_says_Knave)
# B says "C is a knave."
B_says_C_Knave = character_rules(BKnight, BKnave, CKnave)
# C says "A is a knight."
C_says_A_Knight = character_rules(CKnight, CKnave, AKnight)
# Create KB
knowledge3 = And(
    A_says_Knight_Knave, B_says_A_says_Knave, B_says_C_Knave, C_says_A_Knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
