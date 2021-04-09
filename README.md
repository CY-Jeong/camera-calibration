# Calibration
Calibration chessboars with muiti-view. That is for getting geomrtric information like intrinsic, extrinsic.<br>
I did 15 multi-views.


## Sample Image
<img src='chessboards/0.png' width=700 height=300>

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
<img src='result_dir/0.png' width=200 height=150><img src='result_dir/1.png' width=200 height=150><img src='result_dir/2.png' width=200 height=150>
<img src='result_dir/3.png' width=200 height=150><img src='result_dir/4.png' width=200 height=150><img src='result_dir/5.png' width=200 height=150>
<img src='result_dir/6.png' width=200 height=150><img src='result_dir/7.png' width=200 height=150><img src='result_dir/8.png' width=200 height=150>
<img src='result_dir/9.png' width=200 height=150><img src='result_dir/10.png' width=200 height=150><img src='result_dir/11.png' width=200 height=150>
<img src='result_dir/12.png' width=200 height=150><img src='result_dir/13.png' width=200 height=150><img src='result_dir/13.png' width=200 height=150>

