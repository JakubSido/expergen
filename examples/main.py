import expergen
import pydantic.dataclasses 
from dataclasses import dataclass, field

@pydantic.dataclasses.dataclass
class ModelConfig:
    model_type: str = "CNN"
    hidden_layers: list = field(default_factory=lambda: [64, 32])

@dataclass
class BaseTrainingConfig:
    learning_rate: float = 0.001
    batch_size: int = 64
    num_epochs: int = 100
    optimizer: str = "Adam"

@pydantic.dataclasses.dataclass
class TrainingConfig(BaseTrainingConfig):
    learning_rate: float = 0.001
    num_epochs: int = 100
    optimizer: str = "SGD"
    smart_feature: str = "xyz"
    
@pydantic.dataclasses.dataclass
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
