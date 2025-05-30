"""
Utility functions for the KV Cache API layer.
"""

from typing import Optional
from .backends import BackendType
from .exceptions import StoreInitializationError
from .config import KVCacheConfig


def get_client_with_config(store, config: KVCacheConfig) -> None:
    """
    Initialize and setup a store client with the given configuration.
    
    Args:
        store: The KVCacheStore instance to setup
        config: Configuration object
        
    Raises:
        StoreInitializationError: If setup fails
    """
    retcode = store.setup(
        config.local_hostname,
        config.metadata_server,
        config.global_segment_size,
        config.local_buffer_size,
        config.protocol,
        config.device_name,
        config.master_server_address
    )
    
    if retcode != 0:
        raise StoreInitializationError(f"Failed to setup store client. Return code: {retcode}")


def get_client(store, 
               local_hostname: Optional[str] = None,
               metadata_server: Optional[str] = None,
               global_segment_size: int = 3200 * 1024 * 1024,
               local_buffer_size: int = 512 * 1024 * 1024,
               protocol: str = "tcp",
               device_name: Optional[str] = None,
               master_server_address: Optional[str] = None) -> None:
    """
    Initialize and setup a store client (backwards compatible with original interface).
    
    Args:
        store: The KVCacheStore instance to setup
        local_hostname: The local hostname
        metadata_server: Address of metadata server
        global_segment_size: Size of global segments in bytes
        local_buffer_size: Size of local buffer in bytes
        protocol: Network protocol to use
        device_name: Network device name
        master_server_address: Address of master server
        
    Raises:
        StoreInitializationError: If setup fails
    """
    config = KVCacheConfig(
        local_hostname=local_hostname or "localhost",
        metadata_server=metadata_server or "127.0.0.1:2379",
        global_segment_size=global_segment_size,
        local_buffer_size=local_buffer_size,
        protocol=protocol,
        device_name=device_name or "lo",
        master_server_address=master_server_address or "127.0.0.1:50051"
    )
    get_client_with_config(store, config)


def detect_best_backend() -> BackendType:
    """
    Automatically detect the best available backend.
    
    Returns:
        The best available backend type
        
    Raises:
        RuntimeError: If no backends are available
    """
    from .backends import list_available_backends
    
    available = list_available_backends()
    
    if not available:
        raise RuntimeError("No KV cache backends are available")
    
    # Prefer Mooncake if available, otherwise use the first available
    if BackendType.MOONCAKE in available:
        return BackendType.MOONCAKE
    
    return available[0]


def create_store_with_auto_backend(**kwargs):
    """
    Create a store with automatically detected backend.
    
    Args:
        **kwargs: Arguments to pass to the backend constructor
        
    Returns:
        A KVCacheStore instance with the best available backend
    """
    from .backends import create_store
    
    backend_type = detect_best_backend()
    return create_store(backend_type, **kwargs)


def create_store_from_config(config: KVCacheConfig):
    """
    Create a store from configuration and setup it.
    
    Args:
        config: KVCacheConfig instance
        
    Returns:
        Configured and setup KVCacheStore instance
        
    Raises:
        StoreInitializationError: If setup fails
    """
    from .backends import create_store
    
    backend_type = config.get_backend_type()
    store = create_store(backend_type)
    get_client_with_config(store, config)
    return store


# Backward compatibility
StoreConfig = KVCacheConfig 