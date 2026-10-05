import streamlit as st
from recommender import load_resources, create_recommendations


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Competitive Exam Resource Recommender",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎯 AI-Based Competitive Exam Resource Recommendation System")

st.subheader("🤖 Find the Right Study Resources for Your Exam")

st.write(
    "Select your exam, subject, preparation level and resource type. "
    "The AI will recommend suitable study resources based on your preferences."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

resources = load_resources()


# --------------------------------------------------
# USER SELECTIONS
# --------------------------------------------------

st.header("📝 Choose Your Preparation Requirements")


# --------------------------------------------------
# EXAM
# --------------------------------------------------

exams = ["Select Exam"] + sorted(
    resources["exam"].dropna().unique().tolist()
)

selected_exam = st.selectbox(
    "🎯 1. Which exam are you preparing for?",
    exams
)


# --------------------------------------------------
# SUBJECT
# --------------------------------------------------

if selected_exam != "Select Exam":

    subject_values = sorted(
        resources.loc[
            resources["exam"] == selected_exam,
            "subject"
        ].dropna().unique().tolist()
    )

    subjects = ["All Subjects"] + subject_values

else:

    subjects = ["Select Subject"]


selected_subject = st.selectbox(
    "📚 2. Which subject do you want to study?",
    subjects
)


# --------------------------------------------------
# PREPARATION LEVEL
# --------------------------------------------------

levels = ["Select Level"] + sorted(
    resources["level"].dropna().unique().tolist()
)

selected_level = st.selectbox(
    "📊 3. What is your preparation level?",
    levels
)


# --------------------------------------------------
# RESOURCE TYPE
# --------------------------------------------------

resource_types = ["Select Resource Type"] + sorted(
    resources["resource_type"].dropna().unique().tolist()
)

selected_type = st.selectbox(
    "📖 4. What type of study resource do you want?",
    resource_types
)


# --------------------------------------------------
# RECOMMENDATION BUTTON
# --------------------------------------------------

st.divider()

if st.button(
    "✨ Get AI Recommendations",
    type="primary"
):

    # --------------------------------------------------
    # CHECK USER INPUT
    # --------------------------------------------------

    if (
        selected_exam == "Select Exam"
        or selected_subject == "Select Subject"
        or selected_level == "Select Level"
        or selected_type == "Select Resource Type"
    ):

        st.warning(
            "⚠️ Please select all four options before getting recommendations."
        )

    else:

        # --------------------------------------------------
        # ALL SUBJECTS
        # --------------------------------------------------

        if selected_subject == "All Subjects":

            exam_resources = resources[
                resources["exam"] == selected_exam
            ].copy()

            # Only selected resource type
            exam_resources = exam_resources[
                exam_resources["resource_type"] == selected_type
            ]

            recommendations = []

            # Find all subjects available for the selected exam
            subjects_for_exam = sorted(
                exam_resources["subject"].dropna().unique().tolist()
            )

            # Get the best resource from each subject
            for subject in subjects_for_exam:

                subject_recommendations = create_recommendations(
                    resources=resources,
                    selected_exam=selected_exam,
                    selected_subject=subject,
                    selected_level=selected_level,
                    selected_type=selected_type,
                    number_of_recommendations=1
                )

                if subject_recommendations:
                    recommendations.extend(
                        subject_recommendations
                    )

            # Rank the best resources
            recommendations.sort(
                key=lambda item: item["score"],
                reverse=True
            )

            # Keep maximum 5 recommendations
            recommendations = recommendations[:5]


        # --------------------------------------------------
        # SPECIFIC SUBJECT
        # --------------------------------------------------

        else:

            recommendations = create_recommendations(
                resources=resources,
                selected_exam=selected_exam,
                selected_subject=selected_subject,
                selected_level=selected_level,
                selected_type=selected_type,
                number_of_recommendations=5
            )


        # --------------------------------------------------
        # DISPLAY SELECTED PREFERENCES
        # --------------------------------------------------

        st.success(
            "🎉 Your preparation requirements have been analyzed!"
        )

        st.header("📋 Your Selected Preferences")

        st.write(
            f"**🎯 Exam:** {selected_exam}"
        )

        st.write(
            f"**📚 Subject:** {selected_subject}"
        )

        st.write(
            f"**📊 Preparation Level:** {selected_level}"
        )

        st.write(
            f"**📖 Resource Type:** {selected_type}"
        )


        # --------------------------------------------------
        # DISPLAY RECOMMENDATIONS
        # --------------------------------------------------

        st.divider()

        st.header("🤖 AI-Powered Recommendations")

        st.write(
            "The recommendations are ranked using "
            "TF-IDF, Cosine Similarity and your selected preferences."
        )


        # --------------------------------------------------
        # NO RESULTS
        # --------------------------------------------------

        if not recommendations:

            st.warning(
                "⚠️ No suitable resources were found for these selections."
            )


        # --------------------------------------------------
        # SHOW RESULTS
        # --------------------------------------------------

        else:

            for number, resource in enumerate(
                recommendations,
                start=1
            ):

                st.subheader(
                    f"{number}. 📘 {resource['title']}"
                )

                st.write(
                    f"**🎯 Exam:** {resource['exam']}"
                )

                st.write(
                    f"**📚 Subject:** {resource['subject']}"
                )

                st.write(
                    f"**📖 Resource Type:** {resource['resource_type']}"
                )

                st.write(
                    f"**📊 Level:** {resource['level']}"
                )

                st.write(
                    f"🤖 **AI Match Score:** {resource['score']}%"
                )

                st.write(
                    f"💡 **Why recommended:** {resource['reason']}"
                )

                st.divider()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "AI-Based Competitive Exam Resource Recommendation System | "
    "TF-IDF + Cosine Similarity"
)