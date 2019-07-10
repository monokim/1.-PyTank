import torch

class TwoLayerNet():
    def __init__(self, D_in, H, D_out):
        self.model = torch.nn.Sequential(
            torch.nn.Linear(D_in, H),
            torch.nn.ReLU(),
            torch.nn.Linear(H, D_out)
            )
        self.loss_fn = torch.nn.MSELoss(size_average = False)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4)
        self.running_loss = 0.0

        self.data_count = 0
        self.x = []
        self.y = []

    def train(self, x, y):
        #print(y)
        x = torch.FloatTensor(x)
        y = torch.FloatTensor(y)
        for i in range(500):
            y_pred = self.model(x)
            loss = self.loss_fn(y_pred, y)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        
        self.running_loss = loss.item()
        print("running_loss " + str(self.running_loss))


    def predict(self, x):
        x = torch.FloatTensor(x)
        y_pred = self.model(x)
        y_pred = y_pred.tolist()
        #print(y_pred)
        return y_pred

    def evaluation(self, x, y):
        x = torch.FloatTensor(x)
        y_pred = self.model(x)
        y_pred = y_pred.tolist()
        count = 0
        for i in range(len(y)):
            if y[i] == y_pred[i]:
                count += 1

    def save_data(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.data_count += 1
        if self.data_count == 5000:
            self.train(x, y)
            self.save("./PyTank_model_5000.pt")

    def save(self, path = "./PyTank_model.pt"):
        torch.save(self.model, path)
        print(path + " saved")

    def load(self, path):
        self.model = torch.load(path)
        self.model.eval()
