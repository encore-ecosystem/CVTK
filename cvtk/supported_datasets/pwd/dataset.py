from torch.utils.data import Dataset
from abc import abstractmethod, ABCMeta
from pathlib import Path
from tqdm import tqdm

import torch
import random


class PairwiseDataset(Dataset, metaclass=ABCMeta):
    def __init__(self):
        self._objects2samples = {}
        self._is_checked = False

        self._objects_names = None
        self._len = 0
    
    def check(self):
        self._len = 0
        for obj in self._objects2samples.keys():
            n = len(self._objects2samples[obj])
            if n <= 1:
                raise ValueError(f"Object {obj} should have more at least two faces")
            self._len += n * (n - 1) // 2  # permutations
        self._objects_names = list(self._objects2samples.keys())
        self._is_checked = True

    def add_object_sample(self, obj: str, sample):
        self._objects2samples[obj] = self._objects2samples.get(obj, []) + [sample]
        self._is_checked = False

    @classmethod
    @abstractmethod
    def write_sample(cls, obj, obj_path: Path, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load_sample(cls, obj_path: Path, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def load(cls, dataset_path: Path, *args, **kwargs):
        assert dataset_path.is_dir(), 'Dataset path should be a directory'

        result = cls()

        for object_path in tqdm(dataset_path.glob("*"), desc="loading dataset"):
            object_name = object_path.stem
            for sample_path in object_path.glob("*"):
                if sample_path.is_file():
                    result.add_object_sample(object_name, result.load_sample(obj_path=sample_path, **kwargs))
                else:
                    print(f"[WARN]: {sample_path} is not file")
        result.check()
        return result

    def write(self, dataset_path: Path):
        dataset_path.mkdir(parents=True, exist_ok=True)
        for object_name in self.objects2samples.keys():
            object_path = dataset_path / object_name
            object_path.mkdir(exist_ok=True)
            for object_sample in self.objects2samples[object_name]:
                self.write_sample(object_path / object_sample)

    def get_bootstrap(self, num_of_samples: int, batch_size: int = 32):
        assert batch_size % 2 == 0 and batch_size > 1
        assert self._is_checked is True

        if self._len < num_of_samples:
            print(f'[WARNING]: {num_of_samples} is too big: {num_of_samples}/{self._len}')
    
        half_batch_size = batch_size // 2
    
        def bootstrap():
            for _ in range(num_of_samples):
                batch_objs, batch_sampes = [], []
                for f in (self._get_sim_pair, self._get_dif_pair):
                    for _ in range(half_batch_size // 2):
                        obj, sample = f()
                        batch_objs.append(obj)
                        batch_sampes.append(sample)
                yield batch_objs, torch.cat(batch_sampes, dim = 0)
        return bootstrap()

    def __iter__(self):
        return iter(self._objects2samples.items())

    def _get_sim_pair(self) -> tuple[tuple[str, str], torch.Tensor]:
        obj = random.choice(self._objects_names)
        sample_1, sample_2 = random.choices(self._objects2samples[obj], k=2)
        return (obj, obj), torch.cat((sample_1.unsqueeze(0), sample_2.unsqueeze(0)), dim=0)

    def _get_dif_pair(self) -> tuple[tuple[str, str], torch.Tensor]:
        obj_1, obj_2 = random.choices(self._objects_names, k=2)
        sample_1, sample_2 = random.choice(self._objects2samples[obj_1]), random.choice(self._objects2samples[obj_2])
        return (obj_1, obj_2), torch.cat((sample_1.unsqueeze(0), sample_2.unsqueeze(0)), dim=0)

    def __len__(self):
        return len(self._objects_names)


__all__ = [
    'PairwiseDataset',
]
