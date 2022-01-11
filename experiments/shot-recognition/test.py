import spektral as spk 
from os import mkdir, path
from random import randint
import np

print('sadfsdgv')


data_dir = "data/THETIS_Skeletal_Joints/normal_oniFiles/ONI_AMATEURS/backhand/p1.txt"
new_dir = "test"


class TestDatset(Dataset):

    def __init__(self, nodes, feats, **kwargs):
        self.nodes = nodes # this is just created input?
        self.feats = feats # this is also just created input?

        super().__init__(**kwargs)

    def download(self):
        data = new_dir

        mkdir(self.path)

        for i in range(5):
            x = random.rand(self.nodes, self.feats)
            a = randint(0,2)
            y = randint(0,2)
            
            filename = path.join(self.path, f'graph_{i}')
            np.savez(filename, x=x, a=a, y=y)

    def read(self):
        # We must return a list of Graph objects
        output = []

        for i in range(5):
            data = np.load(os.path.join(self.path, f'graph_{i}.npz'))
            output.append(
                Graph(x=data['x'], a=data['a'], y=data['y'])
            )

        return output

dataset = TestDatset(3,2)
print(dataset)

print('hello')