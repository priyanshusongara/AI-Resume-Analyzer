from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection(name="skills")


def store_skills(skills, doc_type):
    docs = []
    ids = []

    for i, skill in enumerate(skills):
        docs.append(f"{doc_type}: {skill}")
        ids.append(f"{doc_type}_{i}")

    embeddings = model.encode(docs).tolist()

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids
    )


def compute_similarity(resume_skills, job_skills):
    if not resume_skills or not job_skills:
        return 0.0

    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)

    emb1 = model.encode([resume_text])[0]
    emb2 = model.encode([job_text])[0]

    from sklearn.metrics.pairwise import cosine_similarity
    score = cosine_similarity([emb1], [emb2])[0][0]

    return float(score)