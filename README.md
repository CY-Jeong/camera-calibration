# Calibration
Calibration chessboars with muiti-view. That is for getting geomrtric information like intrinsic, extrinsic.<br>
I did 15 multi-views.


## Sample Image
<img src='chessboards/0.jpg' width=200 height=150><img src='chessboards/1.jpg' width=200 height=150><img src='chessboards/2.jpg' width=200 height=150><img src='chessboards/3.jpg' width=200 height=150><img src='chessboards/4.jpg' width=200 height=150> <img src='chessboards/5.jpg' width=200 height=150><img src='chessboards/6.jpg' width=200 height=150><img src='chessboards/7.jpg' width=200 height=150><img src='chessboards/8.jpg' width=200 height=150><img src='chessboards/9.jpg' width=200 height=150> <img src='chessboards/10.jpg' width=200 height=150><img src='chessboards/11.jpg' width=200 height=150><img src='chessboards/12.jpg' width=200 height=150><img src='chessboards/13.jpg' width=200 height=150><img src='chessboards/14.jpg' width=200 height=150>

## installation
```bash
git clone https://github.com/CY-Jeong/anomaly-detection-mvtec.git
cd anomaly-detection-mvtec## Usage
```
- Pip users, ```pip install -r requirements.txt```
- Conta users, ```conda env create -f environment.yml```

## Usage
First prepair chessboards images or videos with multi view in chessboards folder.
In config file, you can modify input dir, result dir, mode(image, video) and view number and 3d points.
After finishing all,
```bash
python calibration.py
```

# Results
<img src='result_dir/0.png' width=200 height=150><img src='result_dir/1.png' width=200 height=150><img src='result_dir/2.png' width=200 height=150><img src='result_dir/3.png' width=200 height=150><img src='result_dir/4.png' width=200 height=150> <img src='result_dir/5.png' width=200 height=150><img src='result_dir/6.png' width=200 height=150><img src='result_dir/7.png' width=200 height=150><img src='result_dir/8.png' width=200 height=150><img src='result_dir/9.png' width=200 height=150> <img src='result_dir/10.png' width=200 height=150><img src='result_dir/11.png' width=200 height=150><img src='result_dir/12.png' width=200 height=150><img src='result_dir/13.png' width=200 height=150><img src='result_dir/14.png' width=200 height=150>

You can see some connection lines between points.
