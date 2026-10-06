with open(r'c:\Users\radhi\Downloads\Ontology One\streamlit_app.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        l_lower = line.lower()
        for w in ['judge', 'pitch']:
            if w in l_lower:
                safe_line = line.strip().encode('ascii', 'replace').decode('ascii')
                print(f"{i}: {safe_line[:80]}")
