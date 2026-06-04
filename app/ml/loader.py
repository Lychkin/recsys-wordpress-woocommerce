import pickle
from threading import Lock

from app.core.config import settings


class ModelManager:
    """
    Singleton-менеджер модели рекомендаций.
    Загружает модель 1 раз и хранит в памяти.
    """

    _model = None
    _lock = Lock()
    _loaded = False

    @classmethod
    def load_model(cls) -> None:
        """
        Загружает модель из pickle только один раз.
        Потокобезопасно.
        """

        if cls._loaded:
            print("Model already loaded, skipping...")
            return

        with cls._lock:
            if cls._loaded:
                return

            print(f"Loading model from: {settings.hybrid_model_path}")

            with open(settings.hybrid_model_path, "rb") as f:
                cls._model = pickle.load(f)

            cls._loaded = True

            print("Model loaded successfully")

    @classmethod
    def get_model(cls):
        """
        Возвращает уже загруженную модель.
        """

        if cls._model is None:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        return cls._model

    @classmethod
    def unload_model(cls):
        """
        (опционально) очистка памяти
        """
        cls._model = None
        cls._loaded = False
