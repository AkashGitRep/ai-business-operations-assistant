
with open("knowledge/refund_policy.txt", "r", encoding="utf-8") as file:
    content = file.read()

chunks = [
    chunk.strip()
    for chunk in content.split("\n\n")
    if chunk.strip()
]

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ---")
    print(chunk)
