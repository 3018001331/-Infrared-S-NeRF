from osgeo import gdal
import numpy as np
import os

def process_image(input_path, output_path):
    # 打开输入图像
    dataset = gdal.Open(input_path, gdal.GA_ReadOnly)
    if dataset is None:
        print(f"无法打开图像: {input_path}")
        return
    
    # 获取图像的宽度、高度和波段数
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    bands = dataset.RasterCount
    
    # 确保图像有3个通道
    if bands != 3:
        print(f"图像通道数不符合要求，需要3通道，实际为{bands}通道")
        return
    
    # 获取数据类型
    band1 = dataset.GetRasterBand(1)
    gdal_datatype = band1.DataType
    numpy_datatype = gdal.GetDataTypeName(gdal_datatype)
    
    # 确定输出数据类型
    if numpy_datatype in ['Byte', 'UInt16', 'Int16', 'UInt32', 'Int32']:
        is_integer = True
        output_datatype = gdal.GDT_Float32  # 转换为浮点型以保留小数
    else:
        is_integer = False
        output_datatype = gdal_datatype
    
    # 读取三个通道的数据
    r_band = dataset.GetRasterBand(1).ReadAsArray()  # R通道
    g_band = dataset.GetRasterBand(2).ReadAsArray()  # G通道
    b_band = dataset.GetRasterBand(3).ReadAsArray()  # B通道
    
    # 如果是整数类型，转换为浮点数
    if is_integer:
        r_band = r_band.astype(np.float32)
    
    # 创建新的G、B通道，全部设为0，保持相同数据类型
    new_g_band = np.zeros_like(g_band, dtype=r_band.dtype)
    new_b_band = np.zeros_like(b_band, dtype=r_band.dtype)
    
    # 创建输出图像
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(
        output_path, width, height, 3, output_datatype
    )
    
    # 设置地理参考信息和投影信息
    output_dataset.SetGeoTransform(dataset.GetGeoTransform())
    output_dataset.SetProjection(dataset.GetProjection())
    
    # 写入三个通道的数据
    output_dataset.GetRasterBand(1).WriteArray(r_band)  # R通道保持不变
    output_dataset.GetRasterBand(2).WriteArray(new_g_band)  # G通道全部为0
    output_dataset.GetRasterBand(3).WriteArray(new_b_band)  # B通道全部为0
    
    # 关闭数据集，确保数据写入磁盘
    output_dataset = None
    dataset = None
    
    print(f"图像处理完成，输出路径: {output_path}")

def process_folder(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 构建完整的文件路径
        input_path = os.path.join(input_folder, filename)
        
        # 跳过子文件夹，只处理文件
        if not os.path.isfile(input_path):
            continue
        
        # 检查文件扩展名，只处理常见的图像格式
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.tif', '.tiff']:
            print(f"跳过非tif文件: {filename}")
            continue
        
        # 构建输出文件路径
        output_filename = f"{os.path.splitext(filename)[0]}_R_only.tif"
        output_path = os.path.join(output_folder, output_filename)
        
        # 处理图像
        print(f"正在处理: {filename}")
        process_image(input_path, output_path)

# 使用示例
input_folder_path = r"D:\one\deep_learning\snerf-main\data\0681"  # 替换为你的输入文件夹路径
output_folder_path = r"D:\one\deep_learning\snerf-main\data\0681"  # 替换为你的输出文件夹路径
process_folder(input_folder_path, output_folder_path)    