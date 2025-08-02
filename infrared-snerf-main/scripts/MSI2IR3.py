import os
from osgeo import gdal
import numpy as np

def process_multiband_tif(input_path, output_path):
    """
    处理多波段TIF图像，保留最后两个波段作为前两个通道，第三个通道为0
    
    参数:
    input_path (str): 输入TIF文件的路径
    output_path (str): 输出TIF文件的路径
    """
    try:
        # 打开输入图像
        gdal_dataset = gdal.Open(input_path)
        if gdal_dataset is None:
            print(f"无法打开文件: {input_path}")
            return

        # 获取波段数量
        num_bands = gdal_dataset.RasterCount
        print(num_bands)
        
        # 确保图像至少有两个波段
        if num_bands < 2:
            print(f"错误: {input_path} 中的波段数量少于2")
            del gdal_dataset  # 释放资源
            return
        cols=gdal_dataset.RasterXSize
        rows=gdal_dataset.RasterYSize
        
        # 读取最后一个和倒数第二个波段的数据
        band_1 = gdal_dataset.GetRasterBand(num_bands).ReadAsArray()
        band_2 = gdal_dataset.GetRasterBand(num_bands-1).ReadAsArray()

        # 第三个通道赋值0/取倒数第3个波段的数据
        band_3 = gdal_dataset.GetRasterBand(num_bands).ReadAsArray()
        # band_avg = np.zeros_like(band_n)
        
        # 准备创建输出文件的参数
        driver = gdal.GetDriverByName('GTiff')
        output_dataset = driver.Create(output_path,cols,rows,3,gdal.GDT_Float32)

        # 设置地理变换和投影信息
        output_dataset.SetGeoTransform(gdal_dataset.GetGeoTransform())
        output_dataset.SetProjection(gdal_dataset.GetProjection())

        # 写入数据到输出文件的三个波段中
        # 波段索引从1开始
        output_dataset.GetRasterBand(1).WriteArray(band_1)
        output_dataset.GetRasterBand(2).WriteArray(band_2)
        output_dataset.GetRasterBand(3).WriteArray(band_3)

        # 释放资源
        gdal_dataset=None
        output_dataset=None

        print(f"成功处理: {input_path} -> {output_path}")

    except Exception as e:
        print(f"处理文件 {input_path} 时出错: {str(e)}")

def batch_process_images(input_dir, output_dir):
    """
    批量处理目录中的所有多波段.tif图像
    
    参数:
    input_dir (str): 输入目录路径
    output_dir (str): 输出目录路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有TIF文件
    tif_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.tif')]
    
    if not tif_files:
        print(f"错误: 在 {input_dir} 中未找到TIF文件")
        return
    
    # 处理每个TIF文件
    for tif_file in tif_files:
        input_path = os.path.join(input_dir, tif_file)
        # 构建输出文件名，添加后缀以标识处理后的文件
        base_name, ext = os.path.splitext(tif_file)
        output_file = f"{base_name}{ext}"
        output_path = os.path.join(output_dir, output_file)
        # print(input_path,output_path)
        process_multiband_tif(input_path, output_path)

if __name__ == "__main__":
    # 设置输入和输出目录
    # input_directory = r"D:\WorkSpace\lixue\snerf-main\data\068MapInfo"
    # output_directory = os.path.join(os.path.dirname(input_directory), "068_Ir_111")

    input_directory = r"D:\WorkSpace\weinan\068\output"
    output_directory = os.path.join(os.path.dirname(input_directory), "068_Ir_121")
    
    # 执行批量处理
    batch_process_images(input_directory, output_directory)


