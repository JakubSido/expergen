# ExperGen

ExperGen is a Python package for creating and manipulating experiment configurations for machine learning tasks. It provides tools for generating random configurations based on custom schemas, with flexible output options.

## Installation

You can install ExperGen using pip:

```bash
pip install expergen
```

## Usage Example

Here's an example of how to use ExperGen for generating, saving, and loading machine learning experiment configurations:

```python
import expergen
from dataclasses import dataclass, field

@dataclass
class ModelConfig:
    model_type: str = "CNN"
    hidden_layers: list = field(default_factory=lambda: [64, 32])

@dataclass
class TrainingConfig:
    learning_rate: float = 0.001
    batch_size: int = 64
    num_epochs: int = 100
    optimizer: str = "Adam"

@dataclass
class ExperimentConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    dropout_rate: float = 0.3
    
def main():
    # Generate variations
    variations = {
        "model.hidden_layers": [[64, 32], [256, 128, 64]],
        "training.num_epochs": [50, 100],
    }

    base_config = ExperimentConfig()
    
    varied_configs = expergen.generate_variations(base_config, variations)
        
    # Save the generated configurations to JSON files
    expergen.save_to_json_files(
        varied_configs,
        destination_dir="experiment_configs/expergen/basic",
    )
    
    # Load a single configuration
    single_config = expergen.load_from_json(
        filepath="experiment_configs/expergen/basic/instance_1.json",
        dataclass_type=ExperimentConfig,
    )
    print("Single loaded configuration:")
    print(single_config)
    
    # Load all configurations from the directory
    all_configs = expergen.load_from_directory(
        directory="experiment_configs/expergen/basic",
        dataclass_type=ExperimentConfig,
    )
    print(f"\nLoaded {len(all_configs)} configurations from directory:")
    for i, config in enumerate(all_configs, 1):
        print(f"Configuration {i}:")
        print(config)
        print()

if __name__ == "__main__":
    main()
```

This example demonstrates how to:
1. Define nested dataclasses for structured experiment configurations
2. Generate variations of configurations
3. Save configurations to JSON files
4. Load a single configuration from a JSON file
5. Load all configurations from a directory

You can run this script to see the generated and loaded configurations.

For more advanced usage and customization options, please refer to the documentation.

## Features

- Use of standard Python dataclasses for experiment configuration definition
- Random configuration generation based on dataclass fields
- Support for custom probability distributions for numeric parameters
- Generation of configuration variations based on specified parameter ranges
- Custom directory for saving generated JSON configuration files
- Custom filename prefix and template for generated configuration files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
