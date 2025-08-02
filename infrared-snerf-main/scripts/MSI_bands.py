import os
import rasterio
import numpy as np

def process_multiband_tif(input_path, output_path):
    """
    处理多波段TIF图像，保留最后两个波段作为前两个通道，第三个通道为前两个波段的平均值
    
    参数:
    input_path (str): 输入TIF文件的路径
    output_path (str): 输出TIF文件的路径
    """
    try:
        # 打开输入图像
        with rasterio.open(input_path) as src:
            # 获取波段数量
            num_bands = src.count
            
            # 确保图像至少有两个波段
            if num_bands < 2:
                print(f"错误: {input_path} 中的波段数量少于2")
                return
            
            # 获取元数据
            meta = src.meta
            
            # 更新元数据中的波段数量为3
            meta.update(count=3)
            
            # 读取最后两个波段
            band_n_minus_1 = src.read(num_bands - 1)
            band_n = src.read(num_bands)
            
            # 计算前两个通道的平均值作为第三个通道
            band_avg = np.mean([band_n_minus_1, band_n], axis=0).astype(band_n_minus_1.dtype)
            
            # 创建输出文件
            with rasterio.open(output_path, 'w', **meta) as dst:
                # 写入三个通道
                dst.write(band_n_minus_1, 1)  # 第一个通道：原倒数第二个波段
                dst.write(band_n, 2)          # 第二个通道：原最后一个波段
                dst.write(band_avg, 3)        # 第三个通道：前两个通道的平均值
        
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
        output_file = f"{base_name}_processed{ext}"
        output_path = os.path.join(output_dir, output_file)
        
        process_multiband_tif(input_path, output_path)

if __name__ == "__main__":
    # 设置输入和输出目录
    input_directory = r"D:\one\deep_learning\data\Train_Track3-MSI-6\MSI2IR"
    output_directory = os.path.join(os.path.dirname(input_directory), "MSI2IR_processed")
    
    # 执行批量处理
    batch_process_images(input_directory, output_directory)    