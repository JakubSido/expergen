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

from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass
from expergen.base_classes import ExpergenModel, ExpergenModelConfig 

class Model1Config(ExpergenModelConfig):
    model_type: str = "RNN"
    activation: str = "relu"
    asdf: str = "asdf"
    
    def create_model(self):
        return Model1(self)

class Model1(ExpergenModel):
    def __init__(self, model_config: Model1Config):
        super().__init__()
        self.model_config = model_config
    
    def forward(self):
        print(f"Model1 forward with config: {self.model_config}")

class TrainingConfig(BaseModel):
    learning_rate: float = 0.001
    num_epochs: int = 100
    optimizer: str = "SGD"
    smart_feature: str = "xyz"

class ExperimentConfig(BaseModel):
    model: Model1Config = Model1Config()

    # You can use also union for variety of models
    # model: Model1Config | Model2Config | Model3Config = Model1Config()
    training: TrainingConfig = TrainingConfig()
    dropout_rate: float = 0.3

def main():
    e1 = ExperimentConfig()
    
    expergen.save_to_directory([e1], destination_dir="experiment_configs/expergen/union") 
    
    e_loaded = expergen.load_from_json("experiment_configs/expergen/union/instance_1.json", ExperimentConfig)
    model = e_loaded.model.create_model()
    
    model.forward()
    
    # Generate variations
    variations = {
        "model.activation": ["rere", "tele"],
        "training.num_epochs": [50, 100],
    }
    base_config = ExperimentConfig()
    
    varied_configs = expergen.generate_variations(base_config, variations)
    
    print(varied_configs)

if __name__ == "__main__":
    main()
```

This example demonstrates how to:
1. Define custom model configurations and models using ExpergenModelConfig and ExpergenModel
2. Create an experiment configuration using Pydantic BaseModel
3. Save and load configurations using expergen utilities
4. Generate variations of configurations
5. Create and use a model instance from a loaded configuration

Key features showcased:
- Use of Pydantic for configuration definition and validation
- Custom model creation through the `create_model` method
- Saving configurations to a directory and loading from JSON
- Generating variations of configurations based on specified parameters

For more advanced usage and customization options, please refer to the documentation.

## Features

- Use of Pydantic BaseModel for robust configuration definition and validation
- Custom model configuration and model classes with ExpergenModelConfig and ExpergenModel
- Generation of configuration variations based on specified parameter ranges
- Utilities for saving configurations to directories and loading from JSON files
- Support for creating model instances from configurations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
