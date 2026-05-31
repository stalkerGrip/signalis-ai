from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

print("Generating embedding...")

vec = model.encode("Disease scheduler optimization")

print(f"Vector size: {len(vec)}")
print("Success.")