import tifffile
import cv2

input_path = r"D:\one\deep_learning\snerf-main\result\文档\JAX_068_df1_06.tif"
output_path = r"D:\one\deep_learning\snerf-main\result\文档\JAX_068_df1_06_df8.tif"

# 读取 TIFF（支持多页、多通道、高 bit 深）
img = tifffile.imread(input_path)

# 降采样
downsample_factor = 8
h, w = img.shape[:2]
downsampled_img = cv2.resize(img, (w // downsample_factor, h // downsample_factor), interpolation=cv2.INTER_AREA)

# 保存
tifffile.imwrite(output_path, downsampled_img)

print(f"tifffile 降采样完成，结果已保存至: {output_path}")