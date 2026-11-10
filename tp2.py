from collections import Counter



# 1. CHARACTER CLASSIFICATION

def is_letter(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def is_digit(c):
    return "0" <= c <= "9"



# 2. DFA FOR IDENTIFIERS
# q0 = initial state
# q1 = accepting state


def is_identifier(word):

    if word == "":
        return False

    state = "q0"

    for c in word:

        if state == "q0":

            if is_letter(c) or c == "_":
                state = "q1"
            else:
                return False

        elif state == "q1":

            if is_letter(c) or is_digit(c) or c == "_":
                state = "q1"
            else:
                return False

    return state == "q1"



# 3. DFA FOR NUMBERS
#
# q0 --digit--> q1
# q1 --digit--> q1
# q1 --dot----> q2
# q2 --digit--> q3
# q3 --digit--> q3

# q1 = INTEGER
# q3 = REAL


def recognize_number(word):

    if word == "":
        return None

    state = "q0"

    for c in word:

        if state == "q0":

            if is_digit(c):
                state = "q1"
            else:
                return None

        elif state == "q1":

            if is_digit(c):
                state = "q1"

            elif c == ".":
                state = "q2"

            else:
                return None

        elif state == "q2":

            if is_digit(c):
                state = "q3"
            else:
                return None

        elif state == "q3":

            if is_digit(c):
                state = "q3"
            else:
                return None

    if state == "q1":
        return "INTEGER"

    elif state == "q3":
        return "REAL"

    return None



# 4. DFA FOR KEYWORDS
#
# Recognizes:
# if, else, while, int, float
#
# No KEYWORDS set and no "in" operator.


def keyword_dfa(word):

    transitions = {

        # Initial state
        "q0": {
            "i": "q1",
            "e": "q4",
            "w": "q8",
            "f": "q13"
        },

        # if / int
        "q1": {
            "f": "q2",
            "n": "q3"
        },

        "q3": {
            "t": "q5"
        },

        # else
        "q4": {
            "l": "q6"
        },

        "q6": {
            "s": "q7"
        },

        "q7": {
            "e": "q9"
        },

        # while
        "q8": {
            "h": "q10"
        },

        "q10": {
            "i": "q11"
        },

        "q11": {
            "l": "q12"
        },

        "q12": {
            "e": "q14"
        },

        # float
        "q13": {
            "l": "q15"
        },

        "q15": {
            "o": "q16"
        },

        "q16": {
            "a": "q17"
        },

        "q17": {
            "t": "q18"
        }
    }

    final_states = {
        "q2",    # if
        "q5",    # int
        "q9",    # else
        "q14",   # while
        "q18"    # float
    }

    state = "q0"

    for c in word:

        if state not in transitions:
            return False

        if c not in transitions[state]:
            return False

        state = transitions[state][c]

    return state in final_states



# 5. DFA FOR INVALID IDENTIFIERS
#
# Detects identifiers starting with digits.
# Examples: 1name, 123abc, 45_value


def invalid_identifier_dfa(s, i):

    state = "q0"
    j = i

    while j < len(s):

        c = s[j]

        if state == "q0":

            if is_digit(c):
                state = "q1"
                j += 1
            else:
                return None

        elif state == "q1":

            if is_digit(c):
                state = "q1"
                j += 1

            elif is_letter(c) or c == "_":
                state = "q2"
                j += 1

            else:
                return None

        elif state == "q2":

            if is_letter(c) or is_digit(c) or c == "_":
                state = "q2"
                j += 1

            else:
                break

    if state == "q2":
        return j

    return None



# 6. DFA FOR OPERATORS
#
# + - * / < > = ! 
# == != <= >=

def operator_dfa(s, i):

    state = "q0"
    j = i

    while j < len(s):

        c = s[j]

        if state == "q0":

            if c in "+-*/":
                state = "q1"
                j += 1

            elif c in "<>":
                state = "q2"
                j += 1

            elif c == "=":
                state = "q3"
                j += 1

            elif c == "!":
                state = "q4"
                j += 1

            else:
                break

        elif state == "q2":

            if c == "=":
                state = "q5"
                j += 1
            else:
                break

        elif state == "q3":

            if c == "=":
                state = "q6"
                j += 1
            else:
                break

        elif state == "q4":

            if c == "=":
                state = "q7"
                j += 1
            else:
                break

        else:
            break

    final_states = {
        "q1",  # + - * /
        "q2",  # < >
        "q3",  # =
        "q5",  # <= >=
        "q6",  # ==
        "q7"   # !=
    }

    if state in final_states:
        return j

    return None



# 7. DFA FOR COMMENTS
#
# q0 --/--> q1
# q1 --/--> q2
# q2 --not newline--> q2
#
# q2 = accepting state


def comment_dfa(s, i):

    state = "q0"
    j = i

    while j < len(s):

        c = s[j]

        if state == "q0":

            if c == "/":
                state = "q1"
                j += 1
            else:
                return None

        elif state == "q1":

            if c == "/":
                state = "q2"
                j += 1
            else:
                return None

        elif state == "q2":

            if c != "\n":
                state = "q2"
                j += 1
            else:
                break

    if state == "q2":
        return j

    return None



# 8. DFA FOR SEPARATORS
#
# ; , ( ) { }


def separator_dfa(c):

    transitions = {
        "q0": {
            ";": "q1",
            ",": "q1",
            "(": "q1",
            ")": "q1",
            "{": "q1",
            "}": "q1"
        }
    }

    state = "q0"

    if c in transitions[state]:
        state = transitions[state][c]
        return state == "q1"

    return False



# 9. DFA FOR WHITESPACE


def whitespace_dfa(c):

    state = "q0"

    if c in (" ", "\t", "\n", "\r"):

        state = "q1"

    return state == "q1"



# 10. MAIN LEXICAL ANALYZER


def lexical_analysis(source_code):

    tokens = []
    errors = []

    i = 0
    line = 1
    column = 1

    while i < len(source_code):

        c = source_code[i]

        start_line = line
        start_column = column

        token_type = None
        end = i


        # 1 WHITESPACE


        if whitespace_dfa(c):

            end = i + 1


        # 2 COMMENTS


        elif comment_dfa(source_code, i) is not None:

            end = comment_dfa(source_code, i)

            token_type = "COMMENT"


        # 3 NUMBERS AND INVALID IDENTIFIERS
 

        elif is_digit(c):

            invalid_end = invalid_identifier_dfa(source_code, i)

            if invalid_end is not None:

                end = invalid_end
                lexeme = source_code[i:end]

                errors.append(
                    f"Lexical error: {lexeme!r} "
                    f"at line {start_line}, column {start_column}: "
                    "An identifier cannot start with a digit."
                )

            else:

                # Read digits
                j = i

                while j < len(source_code) and is_digit(source_code[j]):
                    j += 1

                # Read decimal part
                if j < len(source_code) and source_code[j] == ".":

                    j += 1

                    while j < len(source_code) and is_digit(source_code[j]):
                        j += 1

                end = j
                lexeme = source_code[i:end]

                token_type = recognize_number(lexeme)

                if token_type is None:

                    errors.append(
                        f"Lexical error: {lexeme!r} "
                        f"at line {start_line}, column {start_column}: "
                        "Invalid number format."
                    )

                elif token_type == "INTEGER":

                    if len(lexeme) > 1 and lexeme[0] == "0":

                        errors.append(
                            f"Lexical error: {lexeme!r} "
                            f"at line {start_line}, column {start_column}: "
                            "An integer cannot start with zero."
                        )

                        token_type = None

        
        # 4. IDENTIFIERS AND KEYWORDS
        

        elif is_letter(c) or c == "_":

            j = i

            while j < len(source_code):

                if (
                    is_letter(source_code[j])
                    or is_digit(source_code[j])
                    or source_code[j] == "_"
                ):
                    j += 1

                else:
                    break

            end = j
            lexeme = source_code[i:end]

            if is_identifier(lexeme):

                if keyword_dfa(lexeme):
                    token_type = "KEYWORD"

                else:
                    token_type = "IDENTIFIER"

        
        # 5. OPERATORS AND ASSIGNMENT
        

        elif operator_dfa(source_code, i) is not None:

            end = operator_dfa(source_code, i)
            lexeme = source_code[i:end]

            if lexeme == "=":
                token_type = "ASSIGNMENT"

            else:
                token_type = "OPERATOR"

        
        # 6. SEPARATORS
        

        elif separator_dfa(c):

            end = i + 1
            token_type = "SEPARATOR"

        
        # 7. INVALID CHARACTERS
        

        else:

            end = i + 1
            lexeme = source_code[i:end]

            errors.append(
                f"Lexical error: {lexeme!r} "
                f"at line {start_line}, column {start_column}: "
                "Invalid character."
            )

        
        # 8. STORE VALID TOKENS
        

        lexeme = source_code[i:end]

        if token_type is not None:

            tokens.append(
                (token_type, lexeme, start_line)
            )

        
        # 9. UPDATE LINE AND COLUMN
        

        if "\n" in lexeme:

            line += lexeme.count("\n")
            column = len(lexeme.rsplit("\n", 1)[-1]) + 1

        else:

            column += len(lexeme)

        i = end

    
    # 11. TOKEN STATISTICS


    statistics = Counter(token[0] for token in tokens)

    return tokens, errors, statistics



# 12. EXAMPLE INPUT


source = """
int x = 10;
float y = 2.5;
int _value = 25;

if x > 5
{
    while x != 0
    {
        x = x - 1;
    }
}

else
{
    x = 0;
}

int z = 01;
int 1name = 50;
int b = 0;
int c = 007;

// This is a comment
"""



# 13. RUN LEXICAL ANALYSIS


tokens, errors, statistics = lexical_analysis(source)


# Display tokens
print("TOKENS:")

for token in tokens:
    print(token)


# Display errors
print("\nLEXICAL ERRORS:")

if errors:

    for error in errors:
        print(error)

else:
    print("No lexical errors.")


# Display statistics
print("\nTOKEN STATISTICS:")

print("Total tokens:", len(tokens))

for token_type, count in sorted(statistics.items()):
    print(f"{token_type}: {count}")

print("Total errors:", len(errors))
                                                                                                                                             