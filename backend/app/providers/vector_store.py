from abc import ABC, abstractmethod
from pathlib import Path

import faiss
import numpy as np


class VectorStore(ABC):
    @abstractmethod
    def add(self, item_id: int, vector: np.ndarray) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, vector: np.ndarray, k: int = 3) -> list[tuple[int, float]]:
        raise NotImplementedError


class FaissVectorStore(VectorStore):
    def __init__(self, dimension: int, index_path: str) -> None:
        self.dimension = dimension
        self.index_path = Path(index_path)
        self.ids: list[int] = []
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            ids_path = self.index_path.with_suffix(".ids.npy")
            self.ids = np.load(ids_path).tolist() if ids_path.exists() else []
        else:
            self.index = faiss.IndexFlatIP(dimension)

    def add(self, item_id: int, vector: np.ndarray) -> None:
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        faiss.normalize_L2(vector)
        self.index.add(vector.astype("float32"))
        self.ids.append(item_id)
        self._persist()

    def search(self, vector: np.ndarray, k: int = 3) -> list[tuple[int, float]]:
        if self.index.ntotal == 0:
            return []
        query = vector.reshape(1, -1).astype("float32")
        faiss.normalize_L2(query)
        scores, indices = self.index.search(query, min(k, self.index.ntotal))
        results: list[tuple[int, float]] = []
        for idx, score in zip(indices[0], scores[0], strict=True):
            if idx == -1:
                continue
            results.append((self.ids[idx], float(score)))
        return results

    def _persist(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        np.save(self.index_path.with_suffix(".ids.npy"), np.array(self.ids, dtype=int))
