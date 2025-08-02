from osgeo import gdal

def get_min_max_band_values(path):
    # 打开tif文件
    dataset = gdal.Open(path)
    if dataset is None:
        print("文件路径错误或文件无法打开")
        return
    
    # 获取波段数
    band_count = dataset.RasterCount
    for band_num in range(1, band_count + 1):
        # 读取当前波段的数据（假设数据是Int16类型，根据实际情况调整）
        band = dataset.GetRasterBand(band_num)
        data = band.ReadAsArray()
        
        # 找到最大值和最小值
        min_val = data.min()
        max_val = data.max()
        
        print(f"波段 {band_num}: 最小像素值 = {min_val}, 最大像素值 = {max_val}")
    
    dataset = None

# 替换为你的tif文件路径
path = r"D:\one\deep_learning\snerf-main\data\004MapInfo\JAX_004_007_MSI.tif"
get_min_max_band_values(path)




