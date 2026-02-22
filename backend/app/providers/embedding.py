from abc import ABC, abstractmethod

import numpy as np


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        raise NotImplementedError


class DeterministicHashEmbeddingProvider(EmbeddingProvider):
    """Simple deterministic embedding for local/offline development."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension

    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dimension, dtype="float32")
        for index, char in enumerate(text.encode("utf-8")):
            vector[index % self.dimension] += (char % 31) / 31.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector
