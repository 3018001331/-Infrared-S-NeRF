import os
import rasterio
from rasterio.windows import Window

def select_last_two_bands(input_path, output_path):
    """
    选择多波段TIF图像的最后两个波段并保存为新的TIF文件
    
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
            
            # 更新元数据中的波段数量
            meta.update(count=2)
            
            # 创建输出文件
            with rasterio.open(output_path, 'w', **meta) as dst:
                # 读取并写入最后两个波段
                for i in range(2):
                    # 波段索引从1开始，所以最后两个波段是 num_bands-1 和 num_bands
                    src_band_idx = num_bands - 1 + i
                    dst.write(src.read(src_band_idx), i + 1)
        
        print(f"成功处理: {input_path} -> {output_path}")
        
    except Exception as e:
        print(f"处理文件 {input_path} 时出错: {str(e)}")

def batch_process_images(input_dir, output_dir):
    """
    批量处理目录中的所有MSI.tif图像
    
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
        output_file = f"{base_name}_last2bands{ext}"
        output_path = os.path.join(output_dir, output_file)
        
        select_last_two_bands(input_path, output_path)

if __name__ == "__main__":
    # 设置输入和输出目录
    input_directory = r"D:\one\deep_learning\data\Train_Track3-MSI-6\MSI2IR"
    output_directory = os.path.join(os.path.dirname(input_directory), "MSI2IR2")
    
    # 执行批量处理
    batch_process_images(input_directory, output_directory)    