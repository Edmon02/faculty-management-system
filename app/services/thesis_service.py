# app/services/thesis_service.py
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.student import Student
from app.models.thesis import Thesis


class ThesisService:
    @staticmethod
    def find_similar_thesis(thesis_title: str, similarity_threshold: float = 0.5) -> List[Dict]:
        """
        Find students with thesis similar to the given title.

        Args:
            thesis_title: The thesis title to compare against
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of student data with similar thesis
        """
        # Get all thesis data
        thesis_data = Thesis.query.all()

        # Armenian stop words to filter out
        stop_words = set(
            [
                "այդ",
                "այլ",
                "այն",
                "այս",
                "դու",
                "դուք",
                "եմ",
                "են",
                "ենք",
                "ես",
                "եք",
                "է",
                "էի",
                "էին",
                "էինք",
                "էիր",
                "էիք",
                "էր",
                "ըստ",
                "թ",
                "ի",
                "ին",
                "իսկ",
                "իր",
                "կամ",
                "համար",
                "հետ",
                "հետո",
                "մենք",
                "մեջ",
                "մի",
                "ն",
                "նա",
                "նաև",
                "նրա",
                "նրանք",
                "որ",
                "որը",
                "որոնք",
                "որպես",
                "ու",
                "ում",
                "պիտի",
                "վրա",
                "և",
            ]
        )

        # Preprocess thesis topics and input title
        preprocessed_topics = [" ".join([word for word in thesis.thesis_title.split() if word.lower() not in stop_words]) for thesis in thesis_data]

        preprocessed_large_text = " ".join([word for word in thesis_title.split() if word.lower() not in stop_words])

        # Create TF-IDF vectors and calculate similarity
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_large_text] + preprocessed_topics)
        cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])

        # Find students with similar thesis
        similar_students_ids = [thesis_data[i].student_id for i, score in enumerate(cosine_similarities[0]) if score > similarity_threshold]

        # Get student data
        if similar_students_ids:
            students = Student.query.filter(Student.id.in_(similar_students_ids)).all()

            # Convert to dictionaries and add thesis data
            result = []
            thesis_mapping = {thesis.student_id: thesis.thesis_title for thesis in thesis_data}

            for student in students:
                student_dict = student.to_dict()
                student_id = student.id
                thesis_title = thesis_mapping.get(student_id)

                if thesis_title:
                    student_dict["thesis"] = thesis_title

                result.append(student_dict)

            return result

        return []
