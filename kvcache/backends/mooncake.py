"""
Mooncake backend implementation for the KV Cache API layer.

This module provides a wrapper around the original MooncakeDistributedStore
to conform to the unified KV Cache API.
"""

from typing import Union, Optional, Any
from ..api import KVCacheStore
from ..exceptions import StoreInitializationError, StorageError

try:
    from mooncake.store import MooncakeDistributedStore
except ImportError:
    MooncakeDistributedStore = None


class MooncakeStore(KVCacheStore):
    """Mooncake implementation of the KV Cache Store interface."""
    
    def __init__(self):
        """Initialize the Mooncake store wrapper."""
        if MooncakeDistributedStore is None:
            raise ImportError("MooncakeDistributedStore is not available")
        
        self._store = MooncakeDistributedStore()
        self._initialized = False
    
    def setup(self, 
              local_hostname: str,
              metadata_server: str, 
              global_segment_size: int,
              local_buffer_size: int,
              protocol: str = "tcp",
              device_name: str = "lo",
              master_server_address: Optional[str] = None) -> int:
        """
        Initialize and setup the distributed store.
        
        Args:
            local_hostname: The local hostname
            metadata_server: Address of the metadata server
            global_segment_size: Size of global segments in bytes
            local_buffer_size: Size of local buffer in bytes  
            protocol: Network protocol to use (tcp, udp, etc.)
            device_name: Network device name
            master_server_address: Address of the master server
            
        Returns:
            0 on success, non-zero error code on failure
        """
        try:
            retcode = self._store.setup(
                local_hostname,
                metadata_server,
                global_segment_size,
                local_buffer_size,
                protocol,
                device_name,
                master_server_address
            )
            
            if retcode == 0:
                self._initialized = True
            
            return retcode
            
        except Exception as e:
            raise StoreInitializationError(f"Failed to setup Mooncake store: {e}")
    
    def put(self, key: str, *values: Union[bytes, bytearray]) -> int:
        """
        Store a key-value pair with single or multiple data parts.
        
        Args:
            key: The key to store
            *values: One or more values to store as bytes
            
        Returns:
            0 on success, non-zero error code on failure
        """
        if not self._initialized:
            raise StorageError("Store not initialized. Call setup() first.")
        
        if not values:
            raise ValueError("At least one value must be provided")
        
        try:
            if len(values) == 1:
                # Single value: use regular put
                return self._store.put(key, values[0])
            else:
                # Multiple values: use put_parts if available, otherwise concatenate
                if hasattr(self._store, 'put_parts'):
                    return self._store.put_parts(key, *values)
                else:
                    # Fallback: concatenate and use regular put
                    combined_data = b''.join(values)
                    return self._store.put(key, combined_data)
        except Exception as e:
            raise StorageError(f"Failed to put key '{key}': {e}")
    
    def get(self, key: str) -> bytes:
        """
        Retrieve a value by key.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value as bytes, or empty bytes if key not found
        """
        if not self._initialized:
            raise StorageError("Store not initialized. Call setup() first.")
        
        try:
            return self._store.get(key)
        except Exception as e:
            raise StorageError(f"Failed to get key '{key}': {e}")
    
    def get_buffer(self, key: str) -> Optional[Any]:
        """
        Get a buffer object that supports the buffer protocol for efficient access to stored data.
        
        Args:
            key: The key to retrieve
            
        Returns:
            A buffer protocol compatible object or None if key not found
        """
        if not self._initialized:
            raise StorageError("Store not initialized. Call setup() first.")
        
        try:
            # Return the raw Mooncake buffer which should support buffer protocol
            return self._store.get_buffer(key)
        except Exception as e:
            raise StorageError(f"Failed to get buffer for key '{key}': {e}")
    
    def get_size(self, key: str) -> int:
        """
        Get the size of a stored value.
        
        Args:
            key: The key to check
            
        Returns:
            Size in bytes, or negative value if key not found
        """
        if not self._initialized:
            raise StorageError("Store not initialized. Call setup() first.")
        
        try:
            return self._store.get_size(key)
        except Exception as e:
            raise StorageError(f"Failed to get size for key '{key}': {e}")
    
    def is_exist(self, key: str) -> int:
        """
        Check if a key exists in the store.
        
        Args:
            key: The key to check
            
        Returns:
            1 if key exists, 0 if not
        """
        if not self._initialized:
            raise StorageError("Store not initialized. Call setup() first.")
        
        try:
            return self._store.is_exist(key)
        except Exception as e:
            raise StorageError(f"Failed to check existence of key '{key}': {e}")
    
    def remove(self, key: str) -> int:
        """
        Remove a key from the store.
        
        Args:
            key: The key to remove
            
        Returns:
            0 on success, non-zero error code on failure
        """
        if not self._initialized:
            raise StorageError("Store not initialized. Call setup() first.")
        
        try:
            return self._store.remove(key)
        except Exception as e:
            raise StorageError(f"Failed to remove key '{key}': {e}")
    
    def close(self) -> int:
        """
        Close and tear down the store.
        
        Returns:
            0 on success, non-zero error code on failure
        """
        if not self._initialized:
            return 0
        
        try:
            retcode = self._store.close()
            if retcode == 0:
                self._initialized = False
            return retcode
        except Exception as e:
            raise StorageError(f"Failed to close store: {e}")
    
    @property
    def native_store(self):
        """Access to the underlying Mooncake store for advanced usage."""
        return self._store 