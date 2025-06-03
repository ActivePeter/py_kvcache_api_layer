#!/usr/bin/env python3
"""
Test script for the updated configuration parsing.
"""

import sys
import os
from pathlib import Path

# Add the kvcache_api_layer to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'kvcache_api_layer'))

from config import KVCacheConfig, ProtocolConfig, MooncakeSpec

def test_new_structure():
    """Test the new nested configuration structure."""
    print("=== Testing New Structure ===")
    
    # Test loading from the new structure example
    config_path = "configs/new_structure_example.yaml"
    if os.path.exists(config_path):
        config = KVCacheConfig.from_file(config_path)
        
        print(f"Local hostname: {config.local_hostname}")
        print(f"Contribute to cluster pool size: {config.contribute_to_cluster_pool_size}")
        print(f"Protocol type: {config.protocal.type}")
        print(f"RDMA device name: {config.protocal.rdma_device_name}")
        print(f"Device name: {config.device_name}")
        print(f"Log level: {config.log_level}")
        print(f"Local buffer size: {config.mooncake_spec.local_buffer_size}")
        print(f"Metadata server: {config.mooncake_spec.metadata_server}")
        print(f"Master server address: {config.mooncake_spec.master_server_address}")
        
        # Test backward compatibility properties
        print(f"Backward compat - metadata_server: {config.metadata_server}")
        print(f"Backward compat - local_buffer_size: {config.local_buffer_size}")
        print(f"Backward compat - protocol: {config.protocol}")
        
        # Test validation
        try:
            config.validate()
            print("✓ Configuration validation passed")
        except ValueError as e:
            print(f"✗ Configuration validation failed: {e}")
    else:
        print(f"Config file not found: {config_path}")

def test_old_structure():
    """Test backward compatibility with old configuration structure."""
    print("\n=== Testing Old Structure (Backward Compatibility) ===")
    
    # Test loading from the old default config
    config_path = "configs/default.yaml"
    if os.path.exists(config_path):
        config = KVCacheConfig.from_file(config_path)
        
        print(f"Local hostname: {config.local_hostname}")
        print(f"Protocol type: {config.protocal.type}")
        print(f"Device name: {config.device_name}")
        print(f"Log level: {config.log_level}")
        print(f"Local buffer size: {config.mooncake_spec.local_buffer_size}")
        print(f"Metadata server: {config.mooncake_spec.metadata_server}")
        print(f"Master server address: {config.mooncake_spec.master_server_address}")
        
        # Test validation
        try:
            config.validate()
            print("✓ Configuration validation passed")
        except ValueError as e:
            print(f"✗ Configuration validation failed: {e}")
    else:
        print(f"Config file not found: {config_path}")

def test_programmatic_creation():
    """Test creating configuration programmatically."""
    print("\n=== Testing Programmatic Creation ===")
    
    # Create config with new structure
    protocol_config = ProtocolConfig(type="ib", rdma_device_name="mlx5_0")
    mooncake_config = MooncakeSpec(
        local_buffer_size=1024 * 1024 * 1024,  # 1GB
        metadata_server="192.168.1.100:2379",
        master_server_address="192.168.1.100:50051"
    )
    
    config = KVCacheConfig(
        local_hostname="worker01",
        contribute_to_cluster_pool_size=8,
        protocal=protocol_config,
        device_name="eth0",
        log_level="DEBUG",
        mooncake_spec=mooncake_config
    )
    
    print(f"Local hostname: {config.local_hostname}")
    print(f"Contribute to cluster pool size: {config.contribute_to_cluster_pool_size}")
    print(f"Protocol type: {config.protocal.type}")
    print(f"RDMA device name: {config.protocal.rdma_device_name}")
    print(f"Device name: {config.device_name}")
    print(f"Log level: {config.log_level}")
    print(f"Local buffer size: {config.mooncake_spec.local_buffer_size}")
    
    # Test validation - this should pass
    try:
        config.validate()
        print("✓ Configuration validation passed")
    except ValueError as e:
        print(f"✗ Configuration validation failed: {e}")
    
    # Test saving with new structure
    config.save_to_file("test_new_output.yaml", use_new_structure=True)
    print("✓ Saved configuration with new structure to test_new_output.yaml")
    
    # Test saving with old structure
    config.save_to_file("test_old_output.yaml", use_new_structure=False)
    print("✓ Saved configuration with old structure to test_old_output.yaml")

def test_validation_errors():
    """Test validation error cases."""
    print("\n=== Testing Validation Errors ===")
    
    # Test invalid protocol type
    try:
        config = KVCacheConfig(protocal=ProtocolConfig(type="invalid"))
        config.validate()
        print("✗ Should have failed with invalid protocol")
    except ValueError as e:
        print(f"✓ Correctly caught invalid protocol: {e}")
    
    # Test missing RDMA device for IB protocol
    try:
        config = KVCacheConfig(protocal=ProtocolConfig(type="ib", rdma_device_name=None))
        config.validate()
        print("✗ Should have failed with missing RDMA device")
    except ValueError as e:
        print(f"✓ Correctly caught missing RDMA device: {e}")
    
    # Test invalid cluster pool size
    try:
        config = KVCacheConfig(contribute_to_cluster_pool_size=0)
        config.validate()
        print("✗ Should have failed with invalid cluster pool size")
    except ValueError as e:
        print(f"✓ Correctly caught invalid cluster pool size: {e}")

if __name__ == "__main__":
    test_new_structure()
    test_old_structure()
    test_programmatic_creation()
    test_validation_errors()
    print("\n=== All Tests Completed ===") 