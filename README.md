# Fla-task-2

# Finite Automata for Real-Time Input Validation

## CLA-2 - Task 2

### Project Overview
This project demonstrates the use of Finite Automata for real-time input validation using Python.

It implements DFA, NFA, subset construction, product construction and DFA minimisation.

## Applications

### 1. PIN Validation
- Validates a 4-digit PIN.
- Rejects invalid characters.
- Checks PIN length.

### 2. Card Lock Validation
- Tracks consecutive incorrect PIN attempts.
- Locks the card after three consecutive wrong attempts.
- Correct PIN resets the wrong-attempt counter before locking.

### 3. Password Validation
- Minimum length: 8 characters.
- Maximum length: 12 characters.
- Requires uppercase letters.
- Requires lowercase letters.
- Requires at least one digit.
- Rejects whitespace.

### 4. Email Validation
- Uses Non-Deterministic Finite Automata.
- Converts NFA into DFA using subset construction.
- Minimises the resulting DFA.

## Technologies Used
- Python 3
- Regular Expressions
- GitHub

## Automata Concepts
- Deterministic Finite Automata (DFA)
- Non-Deterministic Finite Automata (NFA)
- Subset Construction
- Product Construction
- DFA Minimisation
- State Transitions

## Project Files
- `fa_validators.py` - Main implementation.
- `tests.py` - Automated test cases.

## How to Run

Run PIN validation:

```bash
python fa_validators.py pin 4821
```

Run card lock validation:

```bash
python fa_validators.py lock WWC
```

Run password validation:

```bash
python fa_validators.py password Srm2026abc
```

Run email validation:

```bash
python fa_validators.py email a@b.co
```

Run automated tests:

```bash
python tests.py
```

## Conclusion
This project demonstrates how finite automata can be applied to real-time input validation through state transitions, acceptance conditions and automata operations.
