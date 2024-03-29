from torch.utils.data import Dataset
from torchvision.datasets import MNIST
from torchvision.transforms import Compose, Lambda, ToTensor
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

def load_data(dataclass, dataset, batch_size = 1500, download = False):
    dataset_train = dataclass(
        "data",
        dataset,
        train=True,
        download= download,
    )
    dataset_val = dataclass(
        "data",
        dataset,
        train=False,
        download= download,
    )
    
    dataloader_train = DataLoader(
        dataset_train, batch_size= batch_size, shuffle=True
    )
    dataloader_val = DataLoader(
        dataset_val, batch_size= batch_size, shuffle=True
    )

    return dataloader_train, dataloader_val

class UnraveledDataset(Dataset):
    """Unraveled Image dataset.

    Feature images are automatically flattened.

    Parameters
    ----------
    root : str
        Directory where the actual data is located (or downloaded to).

    train : bool
        If True the training set is returned. Otherwise
        the validation set is returned.

    data: Image dataset from datasets


    """

    def __init__(self, root, data, train= True, download= False):
        transform = Compose(
            [
                ToTensor(),
                Lambda(lambda x: x.ravel()),
            ]
        )

        self.unraveled_dataset = data(
            root,
            train=train,
            download=download,
            transform=transform,
        )

    def __len__(self):
        """Get the length of the dataset."""
        return len(self.unraveled_dataset)

    def __getitem__(self, ix):
        """Get a selected sample.

        Parameters
        ----------
        ix : int
            Index of the sample to get.

        Returns
        -------
        x : torch.Tensor
            Flattened feature tensor of shape `(784,)`.

        y : torch.Tensor
            Scalar representing the ground truth label. Number between 0 and 9.
        """
        return self.unraveled_dataset[ix]