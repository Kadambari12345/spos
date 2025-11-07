import re

# === Replace or load source lines here ===
source = """
START
MACRO
INCR &ARG1, &ARG2
ADD AREG, &AREG2
MEND
MACRO
DECR &ARG3, &ARG4
SUB AREG, &AREG3
MOVER CREG, &ARG4
MEND
INCR N1, N2
DECR N3,N4
END
""".strip().splitlines()

# Data structures
MNT = []   # list of dicts: {name, mdt_index, param_count}
MDT = []   # list of dicts: {index, text}
ALAs = {}  # macro_name -> list(formal parameters)

def parse_macro_header(header_line):
    parts = header_line.strip().split(None, 1)
    name = parts[0]
    params = []
    if len(parts) > 1:
        raw_params = parts[1]
        params = [p.strip() for p in raw_params.split(',') if p.strip()]
        params = [p if p.startswith('&') else ('&' + p) for p in params]
    return name, params

# Pass-I: build MNT, MDT, ALA
i = 0
mdt_index = 1
while i < len(source):
    line = source[i].strip()
    if not line:
        i += 1
        continue
    if line.upper() == 'MACRO':
        # header follows
        i += 1
        header = source[i].strip()
        mname, formals = parse_macro_header(header)
        ALAs[mname] = list(formals)
        MNT.append({'name': mname, 'mdt_index': mdt_index, 'param_count': len(formals)})
        # store header in MDT (optional)
        MDT.append({'index': mdt_index, 'text': f'{mname} ' + ', '.join(formals)})
        mdt_index += 1
        i += 1
        # read body until MEND
        while i < len(source):
            body_line = source[i].strip()
            if body_line.upper() == 'MEND':
                MDT.append({'index': mdt_index, 'text': 'MEND'})
                mdt_index += 1
                break
            # prepare mapping formal -> (P,n)
            mapping = {}
            for idxf, fp in enumerate(formals, start=1):
                mapping[fp] = f'(P,{idxf})'
                mapping[fp.lstrip('&')] = f'(P,{idxf})'
            # replace formals in body_line
            def replace_formals(s):
                s = re.sub(r'&([A-Za-z0-9_]+)', lambda m: mapping.get('&'+m.group(1), m.group(0)), s)
                s = re.sub(r'\b([A-Za-z0-9_]+)\b', lambda m: mapping.get(m.group(1), m.group(0)), s)
                return s
            transformed = replace_formals(body_line)
            MDT.append({'index': mdt_index, 'text': transformed})
            mdt_index += 1
            i += 1
    else:
        i += 1

# Print tables
print("MNT (Macro Name Table):")
print("{:<6} {:<10} {:<12}".format("Idx","Name","MDT_Index/Params"))
for idx, entry in enumerate(MNT, start=1):
    print("{:<6} {:<10} {:<12}".format(idx, entry['name'], f"{entry['mdt_index']}/{entry['param_count']}"))

print("\nMDT (Macro Definition Table):")
print("{:<6} {}".format("Index","Text"))
for rec in MDT:
    print("{:<6} {}".format(rec['index'], rec['text']))

print("\nALA (Argument List Arrays):")
for mname, al in ALAs.items():
    print(f"{mname}: {al}")
