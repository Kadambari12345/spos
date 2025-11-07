import re
import sys
from pathlib import Path

# ---------- Sample program (will be used if input.asm not found) ----------
sample_program = """START 200

MOVER AREG, ='5'
MOVEM AREG, X
L1 MOVER BREG, ='2'
ORIGIN L1+3
LTORG

NEXT ADD AREG, ='1'
SUB BREG, ='2'
BC LT, BACK
LTORG
BACK EQU L1

ORIGIN NEXT+5
MULT CREG, ='4'
STOP
X DS 1
END
"""

# ---------- Opcode tables (simple numeric codes used in IC) ----------
# You may adjust numeric opcodes to match your course convention.
OPCODE = {
    # Imperative Statements (IS)
    "STOP": ("IS", 0),
    "ADD":  ("IS", 1),
    "SUB":  ("IS", 2),
    "MULT": ("IS", 3),
    "MOVER":("IS", 4),
    "MOVEM":("IS", 5),
    "BC":   ("IS", 6),
    "DIV":  ("IS", 7),

    # Assembler Directives (AD)
    "START": ("AD", 1),
    "END":   ("AD", 2),
    "ORIGIN":("AD", 3),
    "EQU":   ("AD", 4),
    "LTORG": ("AD", 5),

    # Declarative (DL)
    "DS": ("DL", 1),
    "DC": ("DL", 2),
}

# Registers mapping (for convenience)
REG = {"AREG":1, "BREG":2, "CREG":3, "DREG":4}

# ---------- Data structures ----------
SYMTAB = {}        # symbol -> {'address': int or None, 'defined': bool}
LITTAB = []        # list of {'lit': "='5'", 'value': 5, 'address': None, 'pool':pool_index}
POOLTAB = []       # list of indices (start index into LITTAB) for each literal pool
INTERMEDIATE = []  # list of (LC or None, tokens_list) tokens_list is representation of IC

# ---------- Helpers ----------
def is_literal(tok):
    return tok.startswith("=")

def parse_literal(tok):
    # parse forms: ='5' or =5
    m = re.match(r"=\s*'(\d+)'\s*$", tok)
    if m:
        return int(m.group(1))
    m2 = re.match(r"=\s*(\d+)\s*$", tok)
    if m2:
        return int(m2.group(1))
    return tok  # fallback

def add_literal(tok):
    # if already present return index (1-based)
    for idx, entry in enumerate(LITTAB, start=1):
        if entry['lit'] == tok:
            return idx
    value = parse_literal(tok)
    pool_idx = len(POOLTAB)-1 if POOLTAB else 0
    LITTAB.append({'lit':tok, 'value':value, 'address':None, 'pool':pool_idx})
    return len(LITTAB)

def add_symbol(sym, addr=None):
    if sym in SYMTAB:
        if addr is not None:
            SYMTAB[sym]['address'] = addr
            SYMTAB[sym]['defined'] = True
    else:
        SYMTAB[sym] = {'address': addr, 'defined': addr is not None}

def evaluate_expression(expr):
    # handles forms: SYMBOL +/- number OR numeric constant OR SYMBOL
    expr = expr.strip()
    # numeric?
    if re.fullmatch(r'\d+', expr):
        return int(expr)
    # SYMBOL+num or SYMBOL-num
    m = re.match(r'^([A-Za-z_]\w*)\s*([\+\-])\s*(\d+)$', expr)
    if m:
        sym = m.group(1)
        op = m.group(2)
        num = int(m.group(3))
        if sym not in SYMTAB or SYMTAB[sym]['address'] is None:
            raise Exception(f"Undefined symbol in expression: {sym}")
        base = SYMTAB[sym]['address']
        return base + num if op == '+' else base - num
    # plain symbol
    if re.fullmatch(r'[A-Za-z_]\w*', expr):
        if expr in SYMTAB and SYMTAB[expr]['address'] is not None:
            return SYMTAB[expr]['address']
        else:
            raise Exception(f"Undefined symbol in expression: {expr}")
    raise Exception(f"Cannot evaluate expression: {expr}")

def flush_literal_pool(LC):
    """Assign addresses to all literals in the current pool starting at LC.
       Returns new LC after allocation."""
    if not POOLTAB:
        POOLTAB.append(0)
    start = POOLTAB[-1]
    for i in range(start, len(LITTAB)):
        if LITTAB[i]['address'] is None:
            LITTAB[i]['address'] = LC
            LC += 1
    # start a new pool for subsequent literals
    POOLTAB.append(len(LITTAB))
    return LC

# ---------- Parser & Pass-I main ----------
def tokenize_line(line):
    # remove comments (if any) after ';' and compact spaces
    line = line.split(';',1)[0].strip()
    # replace commas with spaces so tokens separated easily
    # keep literals intact (they contain = and quotes)
    # naive split: we will split on whitespace but keep tokens like "AREG," cleaned
    tokens = re.split(r'\s+|,', line)
    tokens = [t for t in tokens if t != '']
    return tokens

def pass1(lines):
    LC = 0
    # initialize first pool index
    POOLTAB.clear()
    POOLTAB.append(0)

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip('\n')
        line = raw.strip()
        i += 1
        if not line:
            continue

        tokens = tokenize_line(line)
        if not tokens:
            continue

        # detect label: if first token is not opcode/directive and next token is opcode OR first token ends with ':'
        first = tokens[0].upper()
        label = None
        idx = 0

        # If token ends with ':' treat as label (remove colon)
        if tokens[0].endswith(':'):
            label = tokens[0][:-1]
            add_symbol(label, LC)
            idx = 1
        else:
            # if first token is not a known opcode or register or directive, treat as label
            if first not in OPCODE and first not in REG and not is_literal(first):
                # Could be label, but ensure there's an opcode afterwards
                if len(tokens) > 1 and tokens[1].upper() in OPCODE:
                    label = tokens[0]
                    add_symbol(label, LC)
                    idx = 1

        if idx >= len(tokens):
            continue
        op = tokens[idx].upper()
        idx += 1

        # START
        if op == "START":
            operand = tokens[idx] if idx < len(tokens) else "0"
            start_addr = int(operand)
            LC = start_addr
            INTERMEDIATE.append((None, [("AD", OPCODE["START"][1]), ("C", start_addr)]))
            continue

        # ORIGIN
        if op == "ORIGIN":
            expr = tokens[idx]
            new_lc = evaluate_expression(expr)
            INTERMEDIATE.append((None, [("AD", OPCODE["ORIGIN"][1]), ("C", new_lc)]))
            LC = new_lc
            continue

        # EQU -> label EQU expr
        if op == "EQU":
            expr = tokens[idx]
            val = evaluate_expression(expr) if not expr.isdigit() else int(expr)
            if label:
                add_symbol(label, val)
                INTERMEDIATE.append((None, [("AD", OPCODE["EQU"][1]), ("C", val)]))
            else:
                raise Exception("EQU used without label")
            continue

        # LTORG -> flush literals now
        if op == "LTORG":
            INTERMEDIATE.append((None, [("AD", OPCODE["LTORG"][1])]))
            LC = flush_literal_pool(LC)
            continue

        # END
        if op == "END":
            INTERMEDIATE.append((None, [("AD", OPCODE["END"][1])]))
            LC = flush_literal_pool(LC)
            break

        # Declarative (DS / DC)
        if op == "DS" or op == "DC":
            # operand is size or const
            operand = tokens[idx] if idx < len(tokens) else "1"
            if op == "DS":
                size = int(operand)
                INTERMEDIATE.append((LC, [("DL", OPCODE["DS"][1]), ("C", size)]))
                LC += size
            else:  # DC
                val = int(operand)
                INTERMEDIATE.append((LC, [("DL", OPCODE["DC"][1]), ("C", val)]))
                LC += 1
            continue

        # Imperative statements (IS)
        if op in OPCODE and OPCODE[op][0] == "IS":
            op_class, op_code = OPCODE[op]
            tokens_out = [("IS", op_code)]

            # parse operands remaining: could be register, symbol, literal, or condition
            # typical forms: MOVER AREG, ='5'  OR BC LT, BACK  (BC has condition and symbol)
            if idx < len(tokens):
                a1 = tokens[idx].upper(); idx += 1
                if a1 in REG:
                    tokens_out.append(("REG", REG[a1]))
                else:
                    # assume condition or symbol
                    tokens_out.append(("COND", a1))
            if idx < len(tokens):
                a2 = tokens[idx]
                # literal?
                if is_literal(a2):
                    lit_idx = add_literal(a2)
                    tokens_out.append(("L", lit_idx))
                else:
                    # symbol
                    sym = a2
                    add_symbol(sym, None)
                    # find sym index? We'll keep symbolic reference as (S,sym)
                    tokens_out.append(("S", sym))
            INTERMEDIATE.append((LC, tokens_out))
            LC += 1
            continue

        # If control reaches here, unknown token - record as-is
        INTERMEDIATE.append((LC, [("??", op)]))
        LC += 1

    # End pass
    return

# ---------- Utility to pretty-print and save results ----------
def print_and_save():
    out_folder = Path.cwd()
    # IC save
    with open(out_folder / "IC.txt", "w") as f:
        f.write("LC\tIntermediate\n")
        for lc, parts in INTERMEDIATE:
            lc_str = "" if lc is None else str(lc)
            parts_str = []
            for p in parts:
                if p[0] in ("IS","AD","DL"):
                    parts_str.append(f"({p[0]},{p[1]})")
                elif p[0] == "C":
                    parts_str.append(f"(C,{p[1]})")
                elif p[0] == "REG":
                    parts_str.append(f"(REG,{p[1]})")
                elif p[0] == "L":
                    parts_str.append(f"(L,{p[1]})")
                elif p[0] == "S":
                    parts_str.append(f"(S,{p[1]})")
                elif p[0] == "COND":
                    parts_str.append(f"(COND,{p[1]})")
                else:
                    parts_str.append(str(p))
            line = f"{lc_str}\t{' '.join(parts_str)}\n"
            f.write(line)

    # SYMTAB
    with open(out_folder / "SYMTAB.txt", "w") as f:
        f.write("Symbol\tAddress\tDefined\n")
        for sym, info in SYMTAB.items():
            f.write(f"{sym}\t{info['address']}\t{info['defined']}\n")

    # LITTAB
    with open(out_folder / "LITTAB.txt", "w") as f:
        f.write("Index\tLiteral\tValue\tAddress\tPool\n")
        for idx, lit in enumerate(LITTAB, start=1):
            f.write(f"{idx}\t{lit['lit']}\t{lit['value']}\t{lit['address']}\t{lit['pool']}\n")

    # POOLTAB
    with open(out_folder / "POOLTAB.txt", "w") as f:
        f.write("PoolIndex\tLITTABStartIndex\n")
        for idx, start in enumerate(POOLTAB):
            f.write(f"{idx}\t{start}\n")

    # Also print to console
    print("\n=== Intermediate Code (IC.txt) ===")
    for lc, parts in INTERMEDIATE:
        lc_str = "" if lc is None else str(lc)
        parts_str = []
        for p in parts:
            if p[0] in ("IS","AD","DL"):
                parts_str.append(f"({p[0]},{p[1]})")
            elif p[0] == "C":
                parts_str.append(f"(C,{p[1]})")
            elif p[0] == "REG":
                parts_str.append(f"(REG,{p[1]})")
            elif p[0] == "L":
                parts_str.append(f"(L,{p[1]})")
            elif p[0] == "S":
                parts_str.append(f"(S,{p[1]})")
            elif p[0] == "COND":
                parts_str.append(f"(COND,{p[1]})")
            else:
                parts_str.append(str(p))
        print(f"{lc_str:4} -> {' '.join(parts_str)}")

    print("\n=== SYMTAB (SYMTAB.txt) ===")
    for sym, info in SYMTAB.items():
        print(f"{sym}\t{info['address']}\t{info['defined']}")

    print("\n=== LITTAB (LITTAB.txt) ===")
    for idx, lit in enumerate(LITTAB, start=1):
        print(f"{idx}\t{lit['lit']}\t{lit['value']}\t{lit['address']}\t{lit['pool']}")

    print("\n=== POOLTAB (POOLTAB.txt) ===")
    for idx, start in enumerate(POOLTAB):
        print(f"{idx}\t{start}")

# ---------- Entry point ----------
def main():
    inp = Path("input.asm")
    if inp.exists():
        lines = inp.read_text().splitlines()
    else:
        lines = sample_program.splitlines()

    pass1(lines)
    print_and_save()
    print("\nFiles written: IC.txt, SYMTAB.txt, LITTAB.txt, POOLTAB.txt in folder:", Path.cwd())

if __name__ == "__main__":
    main()

