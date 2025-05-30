"""
Python KV Cache API Layer

A unified interface for key-value caching with support for multiple backends
including Mooncake and Rust implementations.
"""

from .api import KVCacheStore
from .backends import BackendType, create_store, list_available_backends
from .config import KVCacheConfig, load_config, create_default_config
from .exceptions import (
    KVCacheError, 
    BackendNotFoundError, 
    StoreInitializationError,
    KeyNotFoundError,
    InvalidOperationError,
    BufferError,
    StorageError
)
from .utils import (
    get_client,
    get_client_with_config,
    detect_best_backend,
    create_store_with_auto_backend,
    create_store_from_config,
    StoreConfig  # Backward compatibility
)

__version__ = "0.1.0"
__all__ = [
    # Core API
    "KVCacheStore",
    
    # Backend management
    "BackendType",
    "create_store",
    "list_available_backends",
    
    # Configuration
    "KVCacheConfig",
    "load_config",
    "create_default_config",
    
    # Exceptions
    "KVCacheError",
    "BackendNotFoundError",
    "StoreInitializationError",
    "KeyNotFoundError",
    "InvalidOperationError",
    "BufferError",
    "StorageError",
    
    # Utilities
    "get_client",
    "get_client_with_config",
    "detect_best_backend",
    "create_store_with_auto_backend",
    "create_store_from_config",
    "StoreConfig",  # Backward compatibility
] 