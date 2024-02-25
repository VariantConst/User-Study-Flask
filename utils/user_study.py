# Create a table of images from directories.
order = ['Content', 'Style', 'PhotoWCT', 'WCT2', 'ASTMAN', 'StyTR2', 'DSTN', 'Dreamstyler', 'pro']
record_number = {k:0 for k in order[2:]}
record_attr = {k:[0 for _ in range(8)] for k in order[2:]}
pro_filename = []
# pro_filename_part = ['' for _ in range(8)]
selected_name = "Content" # default
is_ready = False
tar_resolution = 384
import multiprocessing
total_num = 24
import matplotlib.style as mplstyle
mplstyle.use('fast')
suffix = ['', '', '', '', '', '', '_cfg_9.00*']
import os
from tqdm import tqdm
import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import gridspec
import matplotlib.transforms as mtrans
from glob import glob
from PIL import Image
from matplotlib.backend_bases import MouseButton

# Create a list to store the recorded numbers
recorded_numbers = []
style_list = sorted(os.listdir(order[-1]))
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



filename_comb_cache = dict()

for name in style_list:
    filename_comb_cache[name] = list(zip(*[sorted(glob(os.path.join(order[j_+2],name)+'/*'+suffix[j_])) for j_ in range(len(order)-2)]))
N = sum([len(filename_comb_cache[name]) for name in style_list])
segment = np.cumsum([len(filename_comb_cache[name]) for name in style_list])
chosen = np.random.choice(N, total_num, replace=False)
chosen_style = np.digitize(chosen, segment)
chosen_content = chosen - np.insert(segment, 0, 0)[chosen_style]
pro_filename = np.zeros(N)
#### Entering loop ####
attributes = ['bokeh','vignetting', 'highlight color', 'shadow color', 'contrast', 'color bias','saturation','exposure']
pid = np.arange(N//8).repeat(8)
file_data = np.zeros((N, len(order), 384, 384, 3), dtype=np.uint8)

def process_data(*args, **kwargs):
    cr_chosen, cr_style, cr_content = args[0]
    # cr_chosen, cr_style, cr_content = kwargs['cr_chosen'], kwargs['cr_style'], kwargs['cr_content']
    vec = np.zeros((len(order), 384, 384, 3), dtype=np.uint8)
    style_name = style_list[cr_style]
    filename_comb = filename_comb_cache[style_name][cr_content]
    filename = filename_comb[0].replace('\\','/').split('/')[-1]
    vec[0] = np.array(resize_crop(Image.open(glob(os.path.join(order[1], style_name)+'/*')[0]).convert('RGB'), tar_resolution))
    vec[1] =  np.array(resize_crop(Image.open(os.path.join(order[0], filename)).convert('RGB'), tar_resolution))
    vec[2:] = np.array([np.array(resize_crop(Image.open(os.path.join(filename_comb[j].replace('\\','/'))).convert('RGB'), tar_resolution)) for j in range(len(order)-2)])
    return vec

pool = multiprocessing.Pool(processes=32)

for i,vec in enumerate(tqdm(pool.imap(process_data, list(zip(chosen, chosen_style, chosen_content))), total=len(chosen))):
    file_data[i] = vec
pool.close()
pool.join()

def on_click(event):
    global selected_name
    if event.inaxes is not None and is_ready and event.button is MouseButton.LEFT:
        selected_name = event.inaxes.name
#### Preparing ####
fig, ax = plt.subplots(2, 5, figsize=(18, 8))
plt.connect('button_press_event', on_click)
for i,(cr_chosen, cr_style, cr_content, cr_pid) in tqdm(enumerate(zip(chosen, chosen_style, chosen_content, pid)), total=total_num):
    style_name = style_list[cr_style]
    filename_comb = filename_comb_cache[style_name][cr_content]
    order_perm = np.random.permutation(len(order)-2)
    filename = filename_comb[0].replace('\\','/').split('/')[-1]
    # plt.title(filename)
    ax[0][0].imshow(file_data[i,0])
    ax[0][0].set_title('Reference')
    ax[0][0].axis('off')
    ax[1][0].imshow(file_data[i,1])
    ax[1][0].set_title('Content')
    ax[1][0].axis('off')

    for index,j in enumerate(order_perm):
        filename = filename_comb[j].replace('\\','/')
        # img = Image.open(os.path.join(filename))
        # Display the image in the corresponding subplot
        tar = ax[(index+2)%2][(index+2)//2]
        tar.imshow(file_data[i,j+2])
        tar.axis('off')
        tar.name = filename.split('/')[-3]
    tar = ax[-1][-1]
    tar.axis('off')
    tar.set_visible(False)
    
    fig.suptitle(rf"Please select the one with the closest **{attributes[cr_pid]}** to the reference image.", fontsize=24)
    fig.tight_layout()
    fig.show()
    is_ready = True
    while(is_ready):
        pts = np.asarray(plt.ginput(1, timeout=-1))
        record_attr[selected_name][cr_pid] += 1
        if selected_name in order[2:]:
            is_ready = False
    is_ready = True
    fig.suptitle(f"Please select the one that best preserves the contents while transferring the photographic concepts)", fontsize=22)
    while(is_ready):
        pts = np.asarray(plt.ginput(1, timeout=-1))
        if selected_name in order[2:]:
            is_ready = False
        if selected_name == 'pro':
            pro_filename[cr_chosen] = 1
        else:
            pro_filename[cr_chosen] = -1
    record_number[selected_name] += 1
    # if (i % 10 == 0):
    with open('result', 'w') as f:
        f.writelines(str(record_number)+'\n')
        f.writelines(str(record_attr))
    np.save('FOI.npy',np.array(pro_filename))
    if i % 2 == 1:
        plt.close()
        fig, ax = plt.subplots(2, 5, figsize=(18, 8))
        plt.connect('button_press_event', on_click)

print("=========================\nPlease send the following to ZCX:\nresult\nFOI.npy\n(=========================\nWe appreciate your help!!")
# print(np.load('FOI.npy'))

# Show the row of images
# plt.show()