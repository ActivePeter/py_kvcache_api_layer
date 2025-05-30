"""
Custom exceptions for the KV Cache API layer.
"""


class KVCacheError(Exception):
    """Base exception for all KV cache related errors."""
    pass


class BackendNotFoundError(KVCacheError):
    """Raised when a requested backend is not available."""
    pass


class StoreInitializationError(KVCacheError):
    """Raised when store initialization fails."""
    pass


class KeyNotFoundError(KVCacheError):
    """Raised when a key is not found in the store."""
    pass


class InvalidOperationError(KVCacheError):
    """Raised when an invalid operation is attempted."""
    pass


class BufferError(KVCacheError):
    """Raised when there's an error with buffer operations."""
    pass


class StorageError(KVCacheError):
    """Raised when there's an error with storage operations."""
    pass 