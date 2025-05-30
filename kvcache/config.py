"""
Configuration management for the KV Cache API layer.

This module handles reading configuration from YAML files only.
"""

import os
from typing import Dict, Any, Optional, Union
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class KVCacheConfig:
    """Configuration class for KV Cache stores that reads from YAML config files."""
    
    def __init__(self, 
                 local_hostname: str = "localhost",
                 metadata_server: str = "127.0.0.1:2379",
                 global_segment_size: int = 3200 * 1024 * 1024,  # 3200 MB
                 local_buffer_size: int = 512 * 1024 * 1024,     # 512 MB
                 protocol: str = "tcp",
                 device_name: str = "lo",
                 master_server_address: str = "127.0.0.1:50051",
                 backend: str = "mooncake",
                 log_level: str = "INFO",
                 enable_metrics: bool = False,
                 **extra_config):
        """
        Initialize configuration with default values.
        
        Args:
            local_hostname: The local hostname
            metadata_server: Address of metadata server
            global_segment_size: Size of global segments in bytes
            local_buffer_size: Size of local buffer in bytes
            protocol: Network protocol to use
            device_name: Network device name
            master_server_address: Address of master server
            backend: Backend type to use ("mooncake", "rust")
            log_level: Logging level
            enable_metrics: Whether to enable metrics collection
            **extra_config: Additional configuration parameters
        """
        self.local_hostname = local_hostname
        self.metadata_server = metadata_server
        self.global_segment_size = global_segment_size
        self.local_buffer_size = local_buffer_size
        self.protocol = protocol
        self.device_name = device_name
        self.master_server_address = master_server_address
        self.backend = backend
        self.log_level = log_level
        self.enable_metrics = enable_metrics
        
        # Store any extra configuration
        self.extra_config = extra_config
    
    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> 'KVCacheConfig':
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            KVCacheConfig instance
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ImportError: If PyYAML is not installed
            ValueError: If config file format is invalid
        """
        if not HAS_YAML:
            raise ImportError("PyYAML is required to read YAML config files. Install with: pip install PyYAML")
        
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML config file format: {e}")
        
        if not isinstance(config_data, dict):
            raise ValueError("Configuration file must contain a dictionary/object at root level")
        
        return cls.from_dict(config_data)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'KVCacheConfig':
        """
        Create configuration from a dictionary.
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            KVCacheConfig instance
        """
        # Extract known parameters
        known_params = {
            'local_hostname', 'metadata_server', 'global_segment_size',
            'local_buffer_size', 'protocol', 'device_name', 
            'master_server_address', 'backend', 'log_level', 'enable_metrics'
        }
        
        init_params = {}
        extra_config = {}
        
        for key, value in config_dict.items():
            if key in known_params:
                init_params[key] = value
            else:
                extra_config[key] = value
        
        if extra_config:
            init_params['extra_config'] = extra_config
        
        return cls(**init_params)
    
    def save_to_file(self, config_path: Union[str, Path]) -> None:
        """
        Save configuration to a YAML file.
        
        Args:
            config_path: Path to save configuration file
        """
        if not HAS_YAML:
            raise ImportError("PyYAML is required to write YAML files. Install with: pip install PyYAML")
        
        config_path = Path(config_path)
        
        config_data = {
            'local_hostname': self.local_hostname,
            'metadata_server': self.metadata_server,
            'global_segment_size': self.global_segment_size,
            'local_buffer_size': self.local_buffer_size,
            'protocol': self.protocol,
            'device_name': self.device_name,
            'master_server_address': self.master_server_address,
            'backend': self.backend,
            'log_level': self.log_level,
            'enable_metrics': self.enable_metrics,
        }
        
        # Add extra configuration
        config_data.update(self.extra_config)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)
    
    def get_backend_type(self):
        """Get BackendType enum from config."""
        from .backends import BackendType
        
        backend_map = {
            'mooncake': BackendType.MOONCAKE,
            'rust': BackendType.RUST,
        }
        
        return backend_map.get(self.backend.lower(), BackendType.MOONCAKE)
    
    def validate(self) -> None:
        """
        Validate configuration values.
        
        Raises:
            ValueError: If configuration values are invalid
        """
        if self.global_segment_size <= 0:
            raise ValueError("global_segment_size must be positive")
        
        if self.local_buffer_size <= 0:
            raise ValueError("local_buffer_size must be positive")
        
        if self.protocol not in ['tcp', 'udp', 'ib']:
            raise ValueError("protocol must be one of: tcp, udp, ib")
        
        if self.backend.lower() not in ['mooncake', 'rust']:
            raise ValueError("backend must be one of: mooncake, rust")
        
        if self.log_level.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("log_level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"KVCacheConfig(backend={self.backend}, host={self.local_hostname}, metadata={self.metadata_server})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"KVCacheConfig(backend='{self.backend}', "
                f"local_hostname='{self.local_hostname}', "
                f"metadata_server='{self.metadata_server}', "
                f"protocol='{self.protocol}')")


def load_config(config_path: Union[str, Path]) -> KVCacheConfig:
    """
    Convenience function to load configuration from YAML file.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        KVCacheConfig instance
    """
    config = KVCacheConfig.from_file(config_path)
    config.validate()
    return config


def create_default_config(output_path: Union[str, Path]) -> None:
    """
    Create a default YAML configuration file.
    
    Args:
        output_path: Path to save the default configuration
    """
    default_config = KVCacheConfig()
    default_config.save_to_file(output_path)
    print(f"Default configuration saved to: {output_path}")


# Backward compatibility with old StoreConfig
StoreConfig = KVCacheConfig 