import logging

from dvmp.sc import SmartContract

class Function:
    def __init__(self, name, compute_cost, storage_cost, parameters: dict):
        self.sc = SmartContract.get_instance()
        self.name = name
        self.compute_cost = compute_cost
        self.storage_cost = storage_cost
        self.parameters = parameters

    def __str__(self):
        return self.name.upper()
    
    def _computeGasStorageCost(self):
        raise NotImplementedError
    
    def __call__(self, **kwargs):
        # Check if the argument provided in kwargs are identical to the parameters of the function
        for key, value in kwargs.items():
            if key not in self.parameters.keys():
                raise Exception(f"Invalid argument [{key}] provided to function {self.name}")
            
            if self.parameters[key]["type"] == "Any":
                continue
            
            # Check the parameters, since we are parsing the arguments as strings we need to convert them to the correct type
            if self.parameters[key]["type"] == "int":
                try:
                    kwargs[key] = int(value)
                except:
                    raise Exception(f"Invalid type [str] for argument [{key}] provided to function [{self.name}], expected [int]")
            
        print(f'interpreting: {self.name}({kwargs})') # This is the line that is printed
        value = self._exec(**kwargs)
        self.sc.gasCompute.append(self.compute_cost)
        self.sc.gasStorage.append(self._computeGasStorageCost())
        return value
