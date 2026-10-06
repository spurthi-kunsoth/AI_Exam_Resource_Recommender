import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_resources():

    resources = pd.read_csv("resources.csv")

    # Clean text columns
    text_columns = [
        "title",
        "exam",
        "subject",
        "resource_type",
        "level",
        "description"
    ]

    for column in text_columns:
        resources[column] = (
            resources[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Create searchable text
    resources["combined"] = (
        resources["title"] + " "
        + resources["exam"] + " "
        + resources["subject"] + " "
        + resources["resource_type"] + " "
        + resources["level"] + " "
        + resources["description"]
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

    # --------------------------------------------------
    # 1. FILTER BY EXAM
    # --------------------------------------------------

    filtered = resources[
        resources["exam"].str.lower()
        == selected_exam.strip().lower()
    ].copy()

    # --------------------------------------------------
    # 2. FILTER BY RESOURCE TYPE
    # --------------------------------------------------

    filtered = filtered[
        filtered["resource_type"].str.lower()
        == selected_type.strip().lower()
    ].copy()

    # --------------------------------------------------
    # 3. FILTER BY SUBJECT
    # --------------------------------------------------

    if selected_subject != "All Subjects":

        filtered = filtered[
            filtered["subject"].str.lower()
            == selected_subject.strip().lower()
        ].copy()

    # --------------------------------------------------
    # 4. IF NOTHING FOUND
    # --------------------------------------------------

    if filtered.empty:
        return []

    # --------------------------------------------------
    # 5. CREATE USER QUERY
    # --------------------------------------------------

    query = (
        selected_exam + " "
        + selected_subject + " "
        + selected_level + " "
        + selected_type
    )

    # --------------------------------------------------
    # 6. TF-IDF
    # --------------------------------------------------

    documents = filtered["combined"].tolist()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents + [query]
    )

    # --------------------------------------------------
    # 7. COSINE SIMILARITY
    # --------------------------------------------------

    similarity_scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    ).flatten()

    recommendations = []

    # --------------------------------------------------
    # 8. CALCULATE RECOMMENDATION SCORE
    # --------------------------------------------------

    for index, similarity in enumerate(similarity_scores):

        resource = filtered.iloc[index]

        score = similarity * 70

        # Level preference
        if (
            resource["level"].lower()
            == selected_level.strip().lower()
        ):
            score += 20

        # Title relevance
        title_words = set(
            resource["title"].lower().split()
        )

        query_words = set(
            query.lower().split()
        )

        common_words = title_words.intersection(
            query_words
        )

        score += min(
            len(common_words) * 2,
            10
        )

        score = min(score, 100)

        # --------------------------------------------------
        # 9. CREATE MEANINGFUL REASON
        # --------------------------------------------------

        reasons = []

        # Subject reason
        if selected_subject != "All Subjects":
            reasons.append(
                f"specifically focused on {resource['subject']}"
            )

        # Resource type reason
        if resource["resource_type"].lower() == "book":
            reasons.append(
                "is a book suitable for concept preparation"
            )

        elif resource["resource_type"].lower() == "practice":
            reasons.append(
                "provides topic-wise practice questions"
            )

        elif resource["resource_type"].lower() == "previous papers":
            reasons.append(
                "contains previous-year exam questions"
            )

        elif resource["resource_type"].lower() == "mock test":
            reasons.append(
                "provides exam-style mock tests"
            )

        # Level reason
        if (
            resource["level"].lower()
            == selected_level.strip().lower()
        ):
            reasons.append(
                f"matches your {selected_level.lower()} preparation level"
            )

        # Description-based reason
        description = resource["description"].lower()

        if "algorithms" in description:
            reasons.append(
                "covers algorithms and problem-solving concepts"
            )

        elif "operating systems" in description:
            reasons.append(
                "covers operating-system concepts"
            )

        elif "network" in description:
            reasons.append(
                "covers computer networking concepts"
            )

        elif "database" in description:
            reasons.append(
                "covers database concepts"
            )

        elif "grammar" in description:
            reasons.append(
                "covers English grammar and language skills"
            )

        elif "vocabulary" in description:
            reasons.append(
                "helps build vocabulary and language skills"
            )

        elif "arithmetic" in description:
            reasons.append(
                "covers important quantitative aptitude concepts"
            )

        elif "reasoning" in description:
            reasons.append(
                "develops logical and analytical reasoning"
            )

        elif "environment" in description:
            reasons.append(
                "covers important environment and ecology concepts"
            )

        elif "constitution" in description:
            reasons.append(
                "covers Indian constitutional and polity concepts"
            )

        elif "history" in description:
            reasons.append(
                "covers important historical concepts and events"
            )

        elif "geography" in description:
            reasons.append(
                "covers important geography concepts"
            )

        elif "banking" in description:
            reasons.append(
                "covers banking and financial awareness"
            )

        # Fallback
        if not reasons:
            reasons.append(
                "matches your selected preparation requirements"
            )

        recommendations.append({

            "title": resource["title"],

            "exam": resource["exam"],

            "subject": resource["subject"],

            "resource_type": resource["resource_type"],

            "level": resource["level"],

            "score": round(score, 2),

            "reason": ", ".join(reasons)

        })

    # --------------------------------------------------
    # 10. SORT BEST RECOMMENDATIONS FIRST
    # --------------------------------------------------

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # --------------------------------------------------
    # 11. RETURN TOP RESULTS
    # --------------------------------------------------

    return recommendations[
        :number_of_recommendations
    ]