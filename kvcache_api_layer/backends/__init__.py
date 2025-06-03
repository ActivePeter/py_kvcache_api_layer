"""
Backend implementations for the KV Cache API layer.
"""

from enum import Enum
from typing import Optional
from ..api import KVCacheStore
from ..exceptions import BackendNotFoundError


class BackendType(Enum):
    """Available backend types."""
    MOONCAKE = "mooncake"
    RUST = "rust"


def create_store(backend_type: BackendType, **kwargs) -> KVCacheStore:
    """
    Factory function to create a KV cache store with the specified backend.
    
    Args:
        backend_type: The type of backend to create
        **kwargs: Additional arguments to pass to the backend constructor
        
    Returns:
        A KVCacheStore instance
        
    Raises:
        BackendNotFoundError: If the requested backend is not available
    """
    if backend_type == BackendType.MOONCAKE:
        try:
            from .mooncake import MooncakeStore
            return MooncakeStore(**kwargs)
        except ImportError as e:
            raise BackendNotFoundError(f"Mooncake backend not available: {e}")
    
    elif backend_type == BackendType.RUST:
        try:
            from .rust import RustStore
            return RustStore(**kwargs)
        except ImportError as e:
            raise BackendNotFoundError(f"Rust backend not available: {e}")
    
    else:
        raise BackendNotFoundError(f"Unknown backend type: {backend_type}")


def list_available_backends() -> list[BackendType]:
    """
    List all available backends on the current system.
    
    Returns:
        List of available BackendType values
    """
    available = []
    
    # Check Mooncake
    try:
        from .mooncake import MooncakeStore
        available.append(BackendType.MOONCAKE)
    except ImportError:
        pass
    
    # Check Rust
    try:
        from .rust import RustStore
        available.append(BackendType.RUST)
    except ImportError:
        pass
    
    return available 