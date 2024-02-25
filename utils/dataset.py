import os
from glob import glob
import numpy as np
from PIL import Image
import random

def resize_crop(image: Image.Image, resolution: int):
    width, height = image.size
    min_w_h = min(width, height)
    left = (width - min_w_h) // 2
    top = (height - min_w_h) // 2
    right = left + min_w_h
    bottom = top + min_w_h
    image = image.crop((left, top, right, bottom))
    image = image.resize((resolution, resolution))
    return image
    

class dat():
    def __init__(self, upload_folder, total_num=160):
        self.total_num = total_num
        self.order = ['Content', 'Style', 'PhotoWCT', 'WCT2', 'ASTMAN', 
                      'StyTR2', 'DSTN', 'Dreamstyler', 'pro']
        self.suffix = ['', '', '', '', '', '', '_cfg_9.00*']
        self.upload_folder = upload_folder
        self.style_list = sorted(os.listdir(
            os.path.join(upload_folder, 'PhotoWCT')))[10:]
        self.filename_comb_cache = dict()
        for name in self.style_list:
            self.filename_comb_cache[name] = list(
                zip(*[sorted(
                    glob(os.path.join(upload_folder, self.order[j_+2],name)
                         +'/*'+self.suffix[j_])
                ) for j_ in range(len(self.order)-2)]))
        N = sum([len(self.filename_comb_cache[name]) for name in self.style_list])
        self.pid2concept = ["Bokeh", "Vignetting", "Highlight", "Shadow", 
                            "Contrast", "Main color bias", "Saturation", "Exposure"]
        self.pid = np.arange(8).repeat(self.total_num//8)
        segment = np.cumsum([len(self.filename_comb_cache[name]) 
                             for name in self.style_list])
        self.chosen = np.random.choice(N, total_num, replace=False)
        self.chosen_style = np.digitize(self.chosen, segment)
        self.chosen_content = self.chosen - np.insert(segment, 0, 0)[self.chosen_style]

    def __getitem__(self, index):
        cr_chosen = self.chosen[index]
        cr_style = self.chosen_style[index]
        cr_content = self.chosen_content[index]
        cr_pid = self.pid[index]
        filename_url = list(self.filename_comb_cache
                            [self.style_list[cr_style]][cr_content])
        filename = filename_url[0].replace('\\','/').split('/')[-1]
        random.shuffle(filename_url)
        filename_url.insert(0, os.path.join(
            self.upload_folder, self.order[0], filename))
        filename_url.insert(0, glob(os.path.join(
            self.upload_folder, self.order[1], self.style_list[cr_style])+'/*')[0])
        # cr_chosen shall be saved.
        return filename_url, self.pid2concept[cr_pid], int(cr_chosen)
    
    def __len__(self):
        return self.total_num
