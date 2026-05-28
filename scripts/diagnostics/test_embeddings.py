from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")

print("Generating embedding...")

vec = model.encode("Disease scheduler optimization")

print(f"Vector size: {len(vec)}")
print("Success.")