"""
Abstract base classes for the KV Cache API layer.

This module defines the core interfaces that all backend implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Union, Optional, Any


class KVCacheStore(ABC):
    """Abstract base class for distributed KV cache stores."""
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def put(self, key: str, *values: Union[bytes, bytearray]) -> int:
        """
        Store a key-value pair with single or multiple data parts.
        
        Args:
            key: The key to store
            *values: One or more values to store as bytes
                    - If single value: calls underlying put()
                    - If multiple values: calls underlying put_parts()
            
        Returns:
            0 on success, non-zero error code on failure
        """
        pass
    
    @abstractmethod
    def get(self, key: str) -> bytes:
        """
        Retrieve a value by key.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The value as bytes, or empty bytes if key not found
        """
        pass
    
    @abstractmethod
    def get_buffer(self, key: str) -> Optional[Any]:
        """
        Get a buffer object that supports the buffer protocol for efficient access to stored data.
        
        Args:
            key: The key to retrieve
            
        Returns:
            A buffer protocol compatible object (e.g., memoryview, bytes, bytearray) or None if key not found
        """
        pass
    
    @abstractmethod
    def get_size(self, key: str) -> int:
        """
        Get the size of a stored value.
        
        Args:
            key: The key to check
            
        Returns:
            Size in bytes, or negative value if key not found
        """
        pass
    
    @abstractmethod
    def is_exist(self, key: str) -> int:
        """
        Check if a key exists in the store.
        
        Args:
            key: The key to check
            
        Returns:
            1 if key exists, 0 if not
        """
        pass
    
    @abstractmethod
    def remove(self, key: str) -> int:
        """
        Remove a key from the store.
        
        Args:
            key: The key to remove
            
        Returns:
            0 on success, non-zero error code on failure
        """
        pass
    
    @abstractmethod
    def close(self) -> int:
        """
        Close and tear down the store.
        
        Returns:
            0 on success, non-zero error code on failure
        """
        pass
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 