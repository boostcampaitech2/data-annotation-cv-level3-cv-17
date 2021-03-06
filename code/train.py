import os
import os.path as osp
import time
import math
from datetime import timedelta
from argparse import ArgumentParser
import random

import torch
from torch import cuda
from torch.utils.data import DataLoader
from torch.optim import lr_scheduler
from tqdm import tqdm

import wandb

from east_dataset import EASTDataset
from dataset import SceneTextDataset
from model import EAST

def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # np.random.seed(seed)
    random.seed(seed)

def parse_args():
    parser = ArgumentParser()

    # Conventional args
    parser.add_argument('--data_dir', type=str,
                        default=os.environ.get('SM_CHANNEL_TRAIN', '../../input/data/annotation/'))
    parser.add_argument('--model_dir', type=str, default=os.environ.get('SM_MODEL_DIR',
                                                                        'trained_models'))

    parser.add_argument('--device', default='cuda' if cuda.is_available() else 'cpu')
    parser.add_argument('--num_workers', type=int, default=4)

    parser.add_argument('--image_size', type=int, default=1024)
    parser.add_argument('--input_size', type=int, default=512)
    parser.add_argument('--batch_size', type=int, default=12)
    parser.add_argument('--learning_rate', type=float, default=1e-3)
    parser.add_argument('--max_epoch', type=int, default=200)
    parser.add_argument('--save_interval', type=int, default=5)

    parser.add_argument('--seed', type=int, default=2222, help='random seed (default: 2222)')
    parser.add_argument('--name', type=str, default="helloworld")
    parser.add_argument('--annotation', type=str, default="annotation", help='check file path (default: annotation')

    args = parser.parse_args()

    if args.input_size % 32 != 0:
        raise ValueError('`input_size` must be a multiple of 32')

    return args


def do_training(data_dir, model_dir, device, image_size, input_size, num_workers, batch_size,
                learning_rate, max_epoch, save_interval, seed, name, annotation):

    seed_everything(seed)
    wandb.init(project="text-detection", entity="visual_cv17", name=name)

    dataset = SceneTextDataset(data_dir, split=annotation, image_size=image_size, crop_size=input_size)
    dataset = EASTDataset(dataset)
    num_batches = math.ceil(len(dataset) / batch_size)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = EAST()
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = lr_scheduler.MultiStepLR(optimizer, milestones=[max_epoch // 2], gamma=0.1)

    wandb.watch(model) ## custom
    model.train()

    best_loss = 9999
    for epoch in range(max_epoch):
        epoch_loss, epoch_start = 0, time.time()
        cls_loss, angle_loss, iou_loss = 0, 0, 0
        with tqdm(total=num_batches) as pbar:
            for img, gt_score_map, gt_geo_map, roi_mask in train_loader:
                pbar.set_description('[Epoch {}]'.format(epoch + 1))

                loss, extra_info = model.train_step(img, gt_score_map, gt_geo_map, roi_mask)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                loss_val = loss.item()
                epoch_loss += loss_val
                cls_loss += extra_info['cls_loss']
                angle_loss += extra_info['angle_loss']
                iou_loss += extra_info['iou_loss']

                pbar.update(1)
                val_dict = {
                    'Cls loss': extra_info['cls_loss'], 'Angle loss': extra_info['angle_loss'],
                    'IoU loss': extra_info['iou_loss']
                }

                pbar.set_postfix(val_dict)

        scheduler.step()

        mean_loss = epoch_loss / num_batches
        print('Mean loss: {:.4f} | Elapsed time: {}'.format(
            mean_loss, timedelta(seconds=time.time() - epoch_start)))

        if best_loss > mean_loss:
            if not osp.exists(model_dir):
                os.makedirs(model_dir)
            ckpt_fpath = osp.join(model_dir, 'best_model.pth')
            torch.save(model.state_dict(), ckpt_fpath)

        if (epoch + 1) % save_interval == 0:
            if not osp.exists(model_dir):
                os.makedirs(model_dir)

            ckpt_fpath = osp.join(model_dir, 'latest.pth')
            torch.save(model.state_dict(), ckpt_fpath)

        ## custom
        wandb.log({
            "train/Mean_loss" : mean_loss,
            "train/Cls_loss": cls_loss / num_batches,
            "train/Angle_loss" : angle_loss / num_batches,
            "train/IoU_loss" : iou_loss / num_batches,
            })
        ##


def main(args):
    do_training(**args.__dict__)


if __name__ == '__main__':
    args = parse_args()
    main(args)
