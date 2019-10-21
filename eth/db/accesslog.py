from contextlib import contextmanager
import logging
from typing import (
    Iterator,
    Set,
)

from eth.abc import (
    AtomicDatabaseAPI,
)
from eth.db.atomic import (
    AtomicDBWriteBatch,
    BaseAtomicDB,
)

class KeyAccessLoggerDB(BaseAtomicDB):
    logger = logging.getLogger("eth.db.KeyAccessLoggerDB")

    keys_read: Set[bytes]

    def __init__(self, wrapped_db: AtomicDatabaseAPI) -> None:
        self.wrapped_db = wrapped_db
        self.keys_read = set()

    def __getitem__(self, key: bytes) -> bytes:
        self.keys_read.add(key)
        return self.wrapped_db.__getitem__(key)

    def __setitem__(self, key: bytes, value: bytes) -> None:
        self.wrapped_db[key] = value

    def __delitem__(self, key: bytes) -> None:
        del self.wrapped_db[key]

    def _exists(self, key: bytes) -> bool:
        return key in self.wrapped_db

    @contextmanager
    def atomic_batch(self) -> Iterator[AtomicDBWriteBatch]:
        with self.wrapped_db.atomic_batch() as readable_batch:
            yield readable_batch

