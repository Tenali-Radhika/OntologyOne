with open(r'c:\Users\radhi\Downloads\Ontology One\streamlit_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if '"""' in l:
        print(f"Line {i}: {repr(l)}")
