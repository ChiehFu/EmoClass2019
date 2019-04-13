from torch.utils.data import Dataset
import numpy as np
from PIL import Image

class FER2013(Dataset):
    """FER2013 dataset."""
    def __init__(self, data, transform=None):
        """
        Args:
            data (tuple): A tuple of (images, labels).
            transform (callable, optional): Optional transform to be applied
                on an image.
        """
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data = self.data[index]
        image = Image.open(data[0])
        label = data[1]
        if self.transform is not None:
            image = self.transform(image)
        return image, label
