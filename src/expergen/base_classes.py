import abc

import pydantic


class ExpergenModel(abc.ABC):
    @abc.abstractmethod
    def forward(self):
        pass

class ExpergenModelConfig(pydantic.BaseModel):
    @abc.abstractmethod 
    def create_model(self) -> ExpergenModel:
        pass
    