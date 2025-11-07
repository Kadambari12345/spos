import re

# Symbol table (index order S,1 ... S,n)
symbols = ['X', 'L1', 'NEXT', 'BACK']
sym_addr = {'X':214, 'L1':202, 'NEXT':207, 'BACK':202}

# Literal table: map index -> {lit, addr, value}
lit_index_to_entry = {
    1: {"lit":"='5'", "addr":205, "value":5},
    2: {"lit":"='2'", "addr":206, "value":2},
    3: {"lit":"='1'", "addr":210, "value":1},
    4: {"lit":"='2'", "addr":211, "value":2},
    5: {"lit":"='4'", "addr":215, "value":4},
}

# Intermediate code lines (use exactly as provided)
ic_lines = [
"(AD,01) (C,200)",
"(IS,04) 1 (L,1)",
"(IS,05) 1 (S,1)",
"(IS,04) 2(L,2)",
"(AD,03) (S,2)+3",
"(AD,05)",
"(L,1)",
"(L,2)",
"(IS,01) 1 (L,3)",
"(IS, 02) 2 (L,4)",
"(IS,07) 1(S,4)",
"(AD,05)",
"(L,3)",
"(L,4)",
"(AD,04) (S,2)",
"(IS,03) 3 (L,5)",
"(IS,00)",
"(DL,02) (C,1)",
"(AD,02)",
]

def parse_tuple(tok):
    m = re.match(r'\(([^,]+),\s*([^\)]+)\)', tok)
    if not m:
        return None
    return (m.group(1).strip(), m.group(2).strip())

machine_lines = []
LC = None
i = 0
while i < len(ic_lines):
    line = ic_lines[i].strip()
    parts = re.findall(r'\([^\)]+\)|\S+', line)
    first = parse_tuple(parts[0])
    if first is None:
        i += 1
        continue
    tag, val = first
    tag = tag.strip()

    if tag == 'AD':
        code = val
        if code == '01':  # START
            if len(parts) > 1:
                c = parse_tuple(parts[1])
                if c and c[0] == 'C':
                    LC = int(c[1])
            i += 1
            continue
        if code == '03':  # ORIGIN (S,n)+k
            expr = parts[1].replace(' ', '')
            m = re.match(r'\(S,(\d+)\)\+(\d+)', expr)
            if m:
                sidx = int(m.group(1)); offset = int(m.group(2))
                sym_name = symbols[sidx-1]
                LC = sym_addr[sym_name] + offset
            else:
                m2 = re.match(r'\(S,(\d+)\)', expr)
                if m2:
                    sidx = int(m2.group(1))
                    LC = sym_addr[symbols[sidx-1]]
            i += 1
            continue
        if code == '05':  # LTORG - literal pool marker
            i += 1
            continue
        if code == '04':  # EQU -- no machine code emission in pass2 here
            i += 1
            continue
        if code == '02':  # END
            break
        i += 1
        continue

    if tag == 'IS':
        opcode = int(val)
        reg = None; mem = None
        for p in parts[1:]:
            p = p.strip()
            if re.match(r'^\d+$', p):
                if reg is None:
                    reg = int(p)
            elif p.startswith('('):
                tup = parse_tuple(p)
                if tup:
                    if tup[0] == 'L':
                        lidx = int(tup[1]); mem = lit_index_to_entry[lidx]['addr']
                    elif tup[0] == 'S':
                        sidx = int(tup[1]); mem = sym_addr[symbols[sidx-1]]
                    elif tup[0] == 'C':
                        mem = int(tup[1])
        if LC is None:
            LC = 0
        machine_lines.append((LC, f"{opcode:02d} { (reg if reg is not None else 0) } { (mem if mem is not None else 0) }"))
        LC += 1
        i += 1
        continue

    if tag == 'L':
        lidx = int(val)
        entry = lit_index_to_entry[lidx]
        lit_address = entry['addr']; lit_value = entry['value']
        machine_lines.append((lit_address, f"DC {lit_value}"))
        if LC is None:
            LC = lit_address + 1
        else:
            LC = max(LC, lit_address + 1)
        i += 1
        continue

    if tag == 'DL':
        # DL,02 (C,x) -> DC x
        if len(parts) > 1:
            c = parse_tuple(parts[1])
            if c and c[0] == 'C':
                const_val = int(c[1])
                if LC is None:
                    LC = 0
                machine_lines.append((LC, f"DC {const_val}"))
                LC += 1
        i += 1
        continue

    i += 1

machine_lines_sorted = sorted(machine_lines, key=lambda x: x[0])
for addr, text in machine_lines_sorted:
    print(f"{addr:03d} : {text}")

# Optionally save to a file:
with open('machine_code.txt', 'w') as f:
    for addr, text in machine_lines_sorted:
        f.write(f"{addr:03d} : {text}\n")
