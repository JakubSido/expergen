# ExperGen

ExperGen is a Python package for creating and manipulating experiment configurations for machine learning tasks. It provides tools for generating random configurations based on custom schemas, with flexible output options.

## Installation

You can install ExperGen using pip:

```bash
pip install expergen
```

## Usage Example

Here's an example of how to use ExperGen for generating machine learning experiment configurations:

```python
from dataclasses import dataclass
from expergen import create_dataclass, generate_variations, save_to_json_files
import numpy as np

from dataclasses import dataclass, field

@dataclass
class MLExperimentConfig:
    model_type: str = "CNN"
    learning_rate: float = 0.001
    batch_size: int = 64
    num_epochs: int = 100
    optimizer: str = "Adam"
    dropout_rate: float = 0.3
    hidden_layers: list = field(default_factory=lambda: [64, 32])

# Define custom probability distributions
learning_rate_dist = lambda: np.random.loguniform(1e-5, 1e-2)
dropout_rate_dist = lambda: np.random.uniform(0.1, 0.5)

# Generate random configurations
base_config = MLExperimentConfig()

# Or override some defaults:
# base_config = MLExperimentConfig(
#     learning_rate=learning_rate_dist(),
#     dropout_rate=dropout_rate_dist(),
#     batch_size=32
# )

# Generate variations
variations = {
    "model_type": ["CNN", "RNN", "Transformer"],
    "batch_size": [32, 64, 128],
    "num_epochs": range(50, 201, 50),
    "optimizer": ["Adam", "SGD", "RMSprop"],
    "hidden_layers": [[64, 32], [128, 64], [256, 128, 64]]
}
varied_configs = generate_variations(base_config, variations)

# Save the generated configurations to JSON files
save_to_json_files(
    varied_configs,
    directory="ml_experiments",
    filename_prefix="exp_config",
    filename_template="{prefix}_{index:03d}.json"
)
```

This example generates multiple machine learning experiment configurations with various hyperparameters and model architectures, and saves them as JSON files in the "ml_experiments" directory.

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
