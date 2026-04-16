from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.ai_engine.nlp_preprocessor import clean_text


@dataclass
class RecommendationCandidate:
    movie_id: int
    score: float


class MockRecommender:
    def __init__(self) -> None:
        self._movies = [
            {
                "id": 1,
                "title": "Interstellar",
                "overview": "Space travel wormhole future science family survival",
                "genres": "Sci-Fi Drama Adventure",
            },
            {
                "id": 2,
                "title": "The Martian",
                "overview": "Astronaut survives alone on Mars with science and humor",
                "genres": "Sci-Fi Adventure",
            },
            {
                "id": 3,
                "title": "Inception",
                "overview": "Dream layers espionage mind-bending heist thriller",
                "genres": "Sci-Fi Thriller",
            },
            {
                "id": 4,
                "title": "Gravity",
                "overview": "Two astronauts struggle to survive in space after disaster",
                "genres": "Sci-Fi Drama",
            },
        ]
        corpus = [
            clean_text(f"{movie['overview']} {movie['genres']}")
            for movie in self._movies
        ]
        self._vectorizer = TfidfVectorizer()
        self._matrix = self._vectorizer.fit_transform(corpus)

    def recommend(self, movie_id: int, top_k: int = 3) -> list[RecommendationCandidate]:
        movie_index = next(
            (index for index, movie in enumerate(self._movies) if movie["id"] == movie_id),
            None,
        )
        if movie_index is None:
            return []

        scores = cosine_similarity(self._matrix[movie_index], self._matrix).flatten()
        ranked = sorted(
            [
                RecommendationCandidate(
                    movie_id=self._movies[index]["id"],
                    score=float(score),
                )
                for index, score in enumerate(scores)
                if self._movies[index]["id"] != movie_id
            ],
            key=lambda item: item.score,
            reverse=True,
        )
        return ranked[:top_k]
