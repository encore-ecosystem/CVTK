from src.supported_datasets.coco.dataset import COCO_Dataset


def combine_coco_datasets(dataset_1: COCO_Dataset, dataset_2: COCO_Dataset) -> COCO_Dataset:
    annotations = dataset_1.anns.copy()
    annotations.update(dataset_2.anns.copy())
    images = dataset_1.images.copy()
    images.update(dataset_2.images.copy())

    return COCO_Dataset(path=None, anns=annotations, images=images)


__all__ = [
    'combine_coco_datasets'
]
