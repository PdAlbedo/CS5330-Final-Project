"""
Project the images into embedding space
"""
import cv2
import torch
import numpy as np
from torch.utils.data import DataLoader
import model_build

torch.manual_seed(888)

def ssd(a, b):
    d = np.sum((a - b) ** 2)
    return d


def nn(results, targets, a):
    min_dis = float('inf')
    file_name = None
    for i in range(len(results)):
        d = ssd(a.detach().numpy(), results[i].detach().numpy())
        print("%.2f" % d, end = " ")
        if d < min_dis:
            min_dis = d
            file_name = targets[i]

    return file_name


def build_embedding_space(model, dataloader):
    model.eval()
    results = []
    targets = []
    b = 0
    for data, target in dataloader:
        output = model(data)
        print("\nBatch %d:" % b)
        print("Input batch size: ", end = "")
        print(data.shape)
        print("Apply the model with 50-node dense layer to the data, "
              "we have the returned output with the shape of: ", end = "")
        print(output.shape)
        b += 1

        for i in range(len(output)):
            results.append(output[i])
            targets.append(target[i])
    print("\nShape of the output nodes from the model: ", end = "")
    print(torch.stack(results).shape)

    return results, targets


def main():
    model_build.generate_csv('image', 'image_info.csv')
    model_build.generate_csv('test', 'test_info.csv')

    network = model_build.MyNetwork()
    network.eval()

    cele_faces = model_build.CustomizedDataset(annotations_file = '../data/image_info.csv',
                                               img_dir = '../data/image')
    cele_faces_loader = DataLoader(dataset = cele_faces,
                                   batch_size = 100,
                                   shuffle = False,
                                   num_workers = 4)

    test_face = model_build.CustomizedDataset(annotations_file = '../data/test_info.csv',
                                              img_dir = '../data/test')
    test_face_loader = DataLoader(dataset = test_face,
                                  batch_size = 100,
                                  shuffle = False,
                                  num_workers = 4)

    results, targets = build_embedding_space(network, cele_faces_loader)
    results_t, targets_t = build_embedding_space(network, test_face_loader)

    # print(type(results_t[0].detach().numpy()))
    # print(type(results[0].detach().numpy()))
    print('\n')
    print('\n')
    img = cv2.imread(nn(results, targets, results_t[0]))
    cv2.imshow('tmp', img)
    cv2.waitKey()


if __name__ == '__main__':
    main()
