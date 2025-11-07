# Pass-II of Two-Pass Macro Processor

# Macro Definition Table (MDT)
MDT = [
    "INCR &ARG1, &ARG2",
    "MOVER AREG, &ARG1",
    "ADD AREG, &ARG2",
    "MEND",
    "DECR &ARG3, &ARG4",
    "MOVER AREG, &ARG3",
    "SUB AREG, &ARG4",
    "MEND"
]

# Macro Name Table (MNT) - macro name : MDT start index
MNT = {
    "INCR": 0,
    "DECR": 4
}

# Argument List Array (ALA)
ALA = {
    "INCR": ["&ARG1", "&ARG2"],
    "DECR": ["&ARG3", "&ARG4"]
}

# Intermediate Code (main program)
intermediate_code = [
    "START",
    "INCR N1, N2",
    "DECR N3, N4",
    "END"
]

print("\n===== PASS II MACRO PROCESSOR =====\n")
print("Expanded Code:\n")

output = []

for line in intermediate_code:
    parts = line.strip().split()
    if len(parts) == 0:
        continue

    mnemonic = parts[0]

    # If it's a macro call
    if mnemonic in MNT:
        start_index = MNT[mnemonic]
        args = parts[1].split(",") if len(parts) > 1 else []

        # Create mapping from &ARG to actual parameters
        arg_map = {}
        for formal, actual in zip(ALA[mnemonic], args):
            arg_map[formal] = actual.strip()

        # Expand macro lines from MDT
        i = start_index + 1
        while MDT[i] != "MEND":
            expanded_line = MDT[i]
            for formal, actual in arg_map.items():
                expanded_line = expanded_line.replace(formal, actual)
            output.append(expanded_line)
            i += 1
    else:
        output.append(line)

# Print final output
for line in output:
    print(line)
