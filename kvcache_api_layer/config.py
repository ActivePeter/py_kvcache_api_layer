"""
Configuration management for the KV Cache API layer.

This module handles reading configuration from YAML files only.
"""

import os
from typing import Dict, Any, Optional, Union
from pathlib import Path
import yaml

# 重新设计参数
# local_hostname: 
# contribute_to_cluster_pool_size:
# protocal:
#   type:
#   rdma_device_name:
# log_level:
# mooncake_spec:
#   local_buffer_size:
#   metadata_server:
#   master_server_address:

class ProtocolConfig:
    """Configuration for network protocol settings."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize protocol configuration from dictionary.
        
        Args:
            config_dict: Protocol configuration dictionary
        """
        self.type = config_dict['type']
        self.rdma_device_name = config_dict.get('rdma_device_name')
        
        # Validate configuration
        if self.type not in ['tcp', 'rdma']:
            raise ValueError("protocol type must be one of: tcp, udp, ib")
        
        if self.type == 'rdma' and not self.rdma_device_name:
            raise ValueError("rdma_device_name is required when protocol type is 'ib'")


class MooncakeSpec:
    """Configuration for Mooncake backend specifications."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize Mooncake specifications from dictionary.
        
        Args:
            config_dict: Mooncake configuration dictionary
        """
        self.local_buffer_size = config_dict['local_buffer_size']
        self.metadata_server = config_dict['metadata_server']
        self.master_server_address = config_dict['master_server_address']
        
        # Validate configuration
        if self.local_buffer_size <= 0:
            raise ValueError("local_buffer_size must be positive")


class KVCacheConfig:
    """Configuration class for KV Cache stores that reads from YAML config files."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize configuration from dictionary.
        
        Args:
            config_dict: Configuration dictionary (required)
        """
        # Extract known parameters (new structure)
        new_structure_params = {
            'local_hostname', 'contribute_to_cluster_pool_size', 'protocal',
            'log_level', 'mooncake_spec'
        }
        
        # Extract backward compatibility parameters
        backward_compat_params = {
            'metadata_server', 'global_segment_size', 'local_buffer_size',
            'protocol', 'master_server_address', 'backend', 'enable_metrics'
        }
        
        all_known_params = new_structure_params | backward_compat_params
        
        # Extract values and store extra config
        extra_config = {}
        for key, value in config_dict.items():
            if key not in all_known_params:
                extra_config[key] = value
        
        # Set basic attributes
        self.local_hostname = config_dict['local_hostname']
        self.contribute_to_cluster_pool_size = config_dict['contribute_to_cluster_pool_size']
        self.log_level = config_dict['log_level']
        
        if self.log_level.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("log_level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        
        if self.contribute_to_cluster_pool_size <= 0:
            raise ValueError("contribute_to_cluster_pool_size must be positive")
        
        # Handle protocol configuration (new nested structure)
        # Validation happens in ProtocolConfig constructor
        self.protocal = ProtocolConfig(config_dict['protocal'])
        
        specs=[
            'mooncake_spec',
        ]

        # Handle mooncake_spec configuration (new nested structure)
        # Validation happens in MooncakeSpec constructor
        if specs[0] in config_dict:
            self.mooncake_spec = MooncakeSpec(config_dict['mooncake_spec'])
        else:
            raise ValueError(f"at least one of the following is required: {specs}")
        
        # Store any extra configuration
        self.extra_config = extra_config
