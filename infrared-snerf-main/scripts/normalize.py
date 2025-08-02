import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, ogr


def normalizetif(input_path, output_path):
    print("当前打开的文件为：",input_path)
    # 打开输入的TIF文件
    dataset = gdal.Open(input_path)
    if dataset is None:
        print(f"无法打开文件：{input_path}")
        return

    # 获取波段数
    band_count = dataset.RasterCount
    if band_count != 3:
        print(f"跳过非三通道的文件：{input_path}")
        return

    # 创建输出数据集，与输入相同的地理变换和投影
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(
        output_path,
        dataset.RasterXSize,
        dataset.RasterYSize,
        band_count,
        gdal.GDT_Float32  # 使用浮点数存储归一化后的值
    )

    # 复制地理变换信息
    output_dataset.SetGeoTransform(dataset.GetGeoTransform())
    output_dataset.SetProjection(dataset.GetProjection())

    # 遍历每个波段进行归一化
    for band_index in range(1, 2):  # 波段索引从1开始
        band = dataset.GetRasterBand(band_index)
        data = band.ReadAsArray()

        # 找到最小值和最大值来进行归一化
        min_val = data.min()
        max_val = data.max()
        
        # 使用布尔索引进行归一化
        CUT_NUM_1=max_val
        if max_val>1500:
           CUT_NUM_1 = 1500.0

        mask = data >= CUT_NUM_1
        
        normalized_data = np.zeros_like(data, dtype=np.float32)
        normalized_data[mask] = 1.0
        normalized_data[~mask] = data[~mask].astype(np.float32) / CUT_NUM_1

        # if (max_val - min_val) == 0:
        #     normalized_data = data / max_val # 或者保持原值，这里假设max_val不为零
        # else:
        #     normalized_data = (data - min_val) / (max_val - min_val)

        output_band = output_dataset.GetRasterBand(band_index)
        output_band.WriteArray(normalized_data) # 归一化到[0,1]

    print("数据归一化完成")
    for band_index in range(2, 3):  # 波段索引从2开始
        band = dataset.GetRasterBand(band_index)
        data = band.ReadAsArray()
        
        min_val = data.min()
        max_val = data.max()
        CUT_NUM_2=max_val
        if max_val>1500:
           CUT_NUM_2 = 1500.0
        # 使用布尔索引进行归一化
        mask = data >= CUT_NUM_2
        normalized_data = np.zeros_like(data, dtype=np.float32)
        normalized_data[mask] = 1.0
        normalized_data[~mask] = data[~mask].astype(np.float32) / CUT_NUM_2

        output_band = output_dataset.GetRasterBand(band_index)
        output_band.WriteArray(normalized_data) # 归一化到[0,1]
    for band_index in range(3, 4):  
        band = dataset.GetRasterBand(band_index)
        data = band.ReadAsArray()
        
        min_val = data.min()
        max_val = data.max()
        CUT_NUM_3=max_val
        if max_val>1500:
           CUT_NUM_3 = 1500.0
        # 使用布尔索引进行归一化
        mask = data >= CUT_NUM_3
        normalized_data = np.zeros_like(data, dtype=np.float32)
        normalized_data[mask] = 1.0
        normalized_data[~mask] = data[~mask].astype(np.float32) / CUT_NUM_3

        output_band = output_dataset.GetRasterBand(band_index)
        output_band.WriteArray(normalized_data) # 归一化到[0,1]


def batch_normalize(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.tif'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            normalizetif(input_path, output_path)

if __name__ == "__main__":
    # input_directory = r"D:\WorkSpace\lixue\snerf-main\data\068_Ir_121"
    # output_directory = os.path.join(input_directory, "068_01")
    
    input_directory = R"D:\WorkSpace\lixue\snerf-main\data\068_Ir_111"
    output_directory = os.path.join(input_directory, "068_01")
    batch_normalize(input_directory, output_directory)