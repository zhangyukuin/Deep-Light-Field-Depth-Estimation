import torch
import torch.nn.functional as F
from torch.autograd import Variable
import os, argparse
from model.decoder import Depth_Net
from functions import imsave
import dataset_loader

parser = argparse.ArgumentParser()
parser.add_argument('--test_root', type=str, default='D:\dataset\our_transform\change/test', help='testing size')
parser.add_argument('--testsize', type=int, default=256, help='testing size')
opt = parser.parse_args()

model = Depth_Net()
model.load_state_dict(torch.load('D:\mycode\our_method\jxx_2.26\cpd_rfb+gru_change\checkpoint/54_w.pth'))

model.cuda()
model.eval()

save_rgb = './result_our_54/rgb/'
if not os.path.exists(save_rgb):
    os.makedirs(save_rgb)
test_loader = dataset_loader.getTestingData(opt.test_root, 1)

with torch.no_grad():
    for id, (sample_batched, img_name,img_size) in enumerate(test_loader):
        data, depth, focal = sample_batched['image'], sample_batched['depth'], sample_batched['focal']
        image = Variable(data).cuda()
        focal = Variable(focal).cuda()
        focal = torch.cat(torch.chunk(focal, 12, dim=1), dim=0)
        focal = focal.view(12, 3, 256, 256)
        out = model(image,focal)
        pred = F.interpolate(out,[img_size[1],img_size[0]],mode = 'bilinear')
        pred = pred.view(img_size[1],img_size[0]).cpu().data
        imsave(os.path.join(save_rgb, img_name[0] + '.png'), pred)
