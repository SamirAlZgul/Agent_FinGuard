# rag_knowledge_base.py
import os
import uuid
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# создаем класс для управления RAG-системой
# сначала документы надо загрузить, потом создать из них эмбеддинги и искать по ним

class FinancialRAG:
    def __init__(self, persist_directory: str="./chroma_db"):
        self.persist_directory=persist_directory

        #Надо откуда-то взять модель эмбеддингов
        logger.info("🔄 Загрузка модели эмбеддингов...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        logger.info("✅ Модель эмбеддингов загружена")

        # далее надо инициализировать векторное хранилище документов
        self.vectorstore=None
        self._init_vectorstore()

        # далее надо инициализировать сплиттер для разбивки документов на части
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=100, length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def _init_vectorstore(self):
        """Инициализирует или загружает существующую векторную БД"""
        try:
            self.vectorstore=Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings)
            # Проверяем есть ли в ней документы
            if self.vectorstore._collection.count() > 0:
                logger.info(f"✅ Загружена существующая БД с {self.vectorstore._collection.count()} чанками")
            else:
                logger.info("🔄 База данных пуста, готова к загрузке документов")
        except Exception as e:
            logger.warning(f"⚠️ Не удалось загрузить существующую БД: {e}. Создаем новую.")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

    def load_documents_from_folder(self, folder_path: str) -> int:
        """
        Загружает все PDF и TXT файлы из папки в векторную БД.
        Возвращает количество загруженных чанков.
        """
        if not os.path.exists(folder_path):
            logger.error(f"❌ Папка {folder_path} не найдена")
            return 0

        all_chunks = []  # <-- собираем ВСЕ чанки

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                if filename.endswith('.pdf'):
                    logger.info(f"📄 Загрузка PDF: {filename}")
                    loader = PyPDFLoader(file_path)
                    documents = loader.load()
                elif filename.endswith('.txt'):
                    logger.info(f"📄 Загрузка TXT: {filename}")
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents = loader.load()
                else:
                    continue

                # Добавляем метаданные (источник)
                for doc in documents:
                    doc.metadata["source"] = filename

                # Разбиваем на чанки
                chunks = self.text_splitter.split_documents(documents)
                all_chunks.extend(chunks)  # <-- добавляем в общий список
                logger.info(f"   → {len(chunks)} чанков создано из {filename}")

            except Exception as e:
                logger.error(f"❌ Ошибка при загрузке {filename}: {e}")

        # Добавляем ВСЕ чанки одной операцией ПОСЛЕ цикла
        if all_chunks:
            uuids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in all_chunks]
            self.vectorstore.add_documents(documents=all_chunks, ids=uuids)
            logger.info(f"✅ Загружено ВСЕГО {len(all_chunks)} чанков в БД")
            return len(all_chunks)
        else:
            logger.warning("⚠️ Не найдено документов для загрузки")
            return 0

    def search(self, query: str, k: int = 4) -> List[str]:
        """
        Поиск релевантных чанков по запросу.
        Возвращает список текстов чанков.
        """
        try:
            logger.info(f"🔍 Поиск: '{query}'")

            # Поиск по векторной БД
            results = self.vectorstore.similarity_search_with_score(query, k=k)

            # Форматируем результаты для агента
            contexts = []
            for doc, score in results:
                # score - это расстояние (чем меньше, тем лучше)
                # Для ChromDB это расстояние L2, поэтому нормализуем его
                relevance = 1 / (1 + score)  # Превращаем расстояние в оценку релевантности

                context = f"""
                [Источник: {doc.metadata.get('source', 'Unknown')}]
                [Релевантность: {relevance:.2f}]
                {doc.page_content}
                """
                contexts.append(context)
                logger.info(
                    f"   → Найден чанк из {doc.metadata.get('source', 'Unknown')} (релевантность: {relevance:.2f})")

            return contexts
        except Exception as e:
            logger.error(f"❌ Ошибка при поиске: {e}")
            return []

    def get_stats(self) -> dict:
        """Возвращает статистику базы знаний"""
        try:
            count = self.vectorstore._collection.count()
            return {
                "total_chunks": count,
                "persist_directory": self.persist_directory,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
            }
        except:
            return {"error": "База данных не инициализирована"}


# Создаем глобальный экземпляр для использования в инструментах
rag_db = FinancialRAG()