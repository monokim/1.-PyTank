import torch
import csv
import torch.utils.data as data
from torch.autograd import Variable

class TwoLayerNet():
    def __init__(self, D_in = 4, H = 5, D_out = 3):
        self.model = torch.nn.Sequential(
            torch.nn.Linear(D_in, H),
            torch.nn.ReLU(),
            torch.nn.Linear(H, D_out)
            )
        self.loss = torch.nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-2, momentum=0.9)
        
        self.data_count = 0
        self.x = []
        self.y = []
        self.num_epoch = 1000

    def train(self):
        x = torch.Tensor(self.x)
        y = torch.Tensor(self.y)
        for epoch in range(self.num_epoch):
            input = Variable(x, requires_grad=False)
            target = Variable(y, requires_grad=False)
            pred = self.model(input)
            #print(pred[0], target[0])
            loss = self.loss(pred, target)
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            if epoch % 100 == 0:
                print("[%d/%d] loss : %f" % (epoch + 1, self.num_epoch, loss.item()))


        self.save_model()
        print("train complete")

    def predict(self, x):
        #x = self.normalize(x)
        x = torch.Tensor(x)
        y_pred = self.model(x)
        return y_pred.tolist()

    def normalize(self, x):
        #normalize
        x[0] = (x[0] - 500.0) / 1400
        x[1] = (x[1] - 180.0) / 360
        x[2] = (x[2] - 180.0) / 360
        x[3] = (x[3] - 180.0) / 360
        return x


    def save_data(self, x, y):
        for data in x:
            self.x.append(data)
        for data in y:
            self.y.append(data)
        self.data_count += 1
        print(self.data_count)
        if self.data_count == 1000:
            with open('train_input.txt', 'w') as f:
                for item in self.x:
                    f.write("%s\n" % item)
            
            with open('train_output.txt', 'w') as f:
                for item in self.y:
                    f.write("%s\n" % item)
            print("txt saved")

            self.train()
            self.save_model("./PyTank_model.pt")

    def load_data(self, in_path = './train_input.txt', out_path = './train_output.txt'):
        print("load data")
        with open(in_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for data in csv_reader:
                #normalize
                data[0] = int(data[0][1:])
                data[1] = int(data[1][1:])
                data[2] = int(data[2][1:])
                data[3] = float(data[3][1:-1])
                #data[3] = (float(data[3][1:-1]) - 180.0) / 360
                #data = self.normalize(data)
                self.x.append(data)
                
        with open(out_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for data in csv_reader:
                #normalize
                data[0] = int(data[0][1:])
                data[1] = int(data[1][1:])
                data[2] = int(data[2][1:-1])
                self.y.append(data)

        print("load data complete")
        print("data example : ")
        print(self.x[0], self.y[0])

    def save_model(self, path = "./PyTank_model.pt"):
        torch.save(self.model, path)
        print(path + " saved")

    def load_model(self, path = "./PyTank_model.pt"):
        self.model = torch.load(path)
        self.model.eval()