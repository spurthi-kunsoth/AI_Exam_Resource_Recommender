import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_resources():

    resources = pd.read_csv("resources.csv")

    resources["combined"] = (
        resources["title"].fillna("").astype(str)
        + " "
        + resources["exam"].fillna("").astype(str)
        + " "
        + resources["subject"].fillna("").astype(str)
        + " "
        + resources["resource_type"].fillna("").astype(str)
        + " "
        + resources["level"].fillna("").astype(str)
        + " "
        + resources["description"].fillna("").astype(str)
    )

    return resources


def create_recommendations(
    resources,
    selected_exam,
    selected_subject,
    selected_level,
    selected_type,
    number_of_recommendations=5
):

    # ==================================================
    # 1. FILTER BY EXAM
    # ==================================================

    filtered = resources[
        resources["exam"].str.strip().str.lower()
        == selected_exam.strip().lower()
    ].copy()


    # ==================================================
    # 2. FILTER BY RESOURCE TYPE
    # ==================================================

    filtered = filtered[
        filtered["resource_type"].str.strip().str.lower()
        == selected_type.strip().lower()
    ].copy()


    # ==================================================
    # 3. FILTER BY SUBJECT
    # ==================================================

    if selected_subject != "All Subjects":

        filtered = filtered[
            filtered["subject"].str.strip().str.lower()
            == selected_subject.strip().lower()
        ].copy()


    # ==================================================
    # 4. IF NOTHING MATCHES
    # ==================================================

    if filtered.empty:
        return []


    # ==================================================
    # 5. CREATE SEARCH QUERY
    # ==================================================

    query = (
        selected_exam + " "
        + selected_subject + " "
        + selected_level + " "
        + selected_type
    )


    # ==================================================
    # 6. TF-IDF
    # ==================================================

    documents = filtered["combined"].tolist()

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents + [query]
    )


    # ==================================================
    # 7. COSINE SIMILARITY
    # ==================================================

    similarity_scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    ).flatten()


    recommendations = []


    # ==================================================
    # 8. CALCULATE SCORE
    # ==================================================

    for index, similarity in enumerate(
        similarity_scores
    ):

        resource = filtered.iloc[index]

        # Start with AI similarity
        score = similarity * 100

        # Preparation level match
        if (
            resource["level"].strip().lower()
            == selected_level.strip().lower()
        ):
            score += 20


        # Keep score between 0 and 100
        score = min(score, 100)


        # ==================================================
        # 9. EXPLANATION
        # ==================================================

        reasons = [
            "same exam",
            "same resource type"
        ]


        if selected_subject != "All Subjects":
            reasons.append("same subject")


        if (
            resource["level"].strip().lower()
            == selected_level.strip().lower()
        ):
            reasons.append("same preparation level")


        reasons.append("similar study content")


        recommendations.append({

            "title": resource["title"],

            "exam": resource["exam"],

            "subject": resource["subject"],

            "resource_type": resource["resource_type"],

            "level": resource["level"],

            "score": round(score, 2),

            "reason": ", ".join(reasons)

        })


    # ==================================================
    # 10. SORT
    # ==================================================

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    # ==================================================
    # 11. RETURN TOP RESULTS
    # ==================================================

    return recommendations[
        :number_of_recommendations
    ]