import expergen

from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass
from expergen.base_classes import ExpergenModel, ExpergenModelConfig 

class Model1Config(ExpergenModelConfig):
    model_type: str = "RNN"
    activation: str = "relu"
    bar :str = "foo"
    
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
    training: TrainingConfig = TrainingConfig()
    dropout_rate: float = 0.3

    
def main():
    e1 = ExperimentConfig()
    
    expergen.save_to_directory([e1], destination_dir="experiment_configs/expergen/union") 
    
    e_loaded = expergen.load_from_json("experiment_configs/expergen/union/instance_1.json",ExperimentConfig)
    model = e_loaded.model.create_model()
    
    model.forward()
    
    # Generate variations
    variations = {
        "model.activation": ["relu", "tanh"],
        "training.num_epochs": [50, 100],
    }
    base_config = ExperimentConfig()
    
    varied_configs = expergen.generate_variations(base_config, variations)
    
    print(varied_configs)
    
    expergen.save_to_directory(varied_configs, destination_dir="experiment_configs/expergen/variations")
        
    # save_to_directory() 
    # load_from_json()
    # load_from_directory()
    
    

if __name__ == "__main__":
    main()
