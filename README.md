# 朱成轩的User Study
本次实验共有160轮。请通过`unzip data.zip`解压数据，再运行命令`pip install pillow numpy matplotlib tqdm`安装需要的依赖程序，最后运行`python user_study.py`开始实验。假如您通过GUI进行操作，请确保`user_study.py`与`PhotoWCT/`、`DSTN/`等文件夹位于同一路径下。

在每一轮中，你将在左侧两列看到1张content image和一张reference image，在右边看到6个不同的方法的结果。这些方法的目的在于将style image的摄影风格提取出来，迁移到content image中。

需要注意的是，content image的内容不应被改变。例如，如果content image是一张小狗的照片，那么狗的位置、姿势、表情不应该被改变。

而reference image的风格应该被迁移到content image中。例如，如果reference image是一张大光圈浅景深、整体色调偏暖的照片，那么content image的风格应该也具有类似的特征。

然而，reference image本身的内容不应该被迁移到content image中，例如，如果reference image展示了一辆红色的车，而content image是一辆蓝色的车，结果中仍应是一辆蓝色的车。这有一些tricky，分辨效果的好坏是需要人类的高级视觉理解才行的，需要电脑前的您来帮忙判断了。

每一轮中，你需要先判断哪个结果最好地保持了reference image的某个指定特征（如bokeh、vignetting、main color bias等），再判断哪个结果最好地完成了提取摄影特征并迁移的任务（包括了不止一个特征）。
这里将给出各个特征需要关注的地方：bokeh需要关注背景或前景的虚化效果和reference是否接近，vignetting需要关注边缘暗角效果或提亮效果，highlight则是关注高光部分的色偏，shadow对应阴影部分的色偏，contrast则是最亮与最暗之差（对比度），main color bias则是总体色调的偏移，saturation指图像的饱和度、鲜明程度，illumination则是画面整体的亮度。

实验进行中时，会在命令行中显示当前的实验进度。如果您头痛欲裂，可以在任何地方在命令行中键入`ctrl-C`停下，实验结果会自动保存，**但无法读档继续**。

实验结束后，会在本目录下生成`result`和`FOI.npy`这两个文件，请您将它们发送给我。谢谢！

朱成轩 2024年2月24日 于燕园
