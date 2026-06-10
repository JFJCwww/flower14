from ultralytics import YOLO

# 加载模型。如果本地有默认使用本地，本地没有从网上下载
model = YOLO("runs/detect/train-3/weights/best.pt")  # 使用YOLOv8n模型

# 对图片列表进行批量推理
# results = model(['./bus.jpg', './data/00001.png'])  # 返回结果对象的列表
# save=True:是否保存预测结果，模型会将检测结果（如标注了边界框的图像）保存到默认或指定的输出目录runs/detect/predict。
# imgsz=320:输入图像的尺寸
# conf=0.5:置信度阈值,过滤掉置信度低于该阈值的检测结果。值越高，检测结果越严格，漏检率可能增加；值越低，检测结果越多，误检率可能增加。
# line_width=50:边界框和标注的线条宽度
results = model.predict("", save=True, imgsz=320, conf=0.7, line_width=50)
# results = model.predict("./data/00001.png", save=True, imgsz=320, conf=0.7, line_width=50)
# 处理结果列表
for result in results:
    boxes = result.boxes  # Boes对象，用于存储边界框输出
    probs = result.probs  # Probs对象，用于存储分类概率输出
    result.show()  # 显示结果到屏幕上

    result.save(filename='result.jpg')  # 保存结果