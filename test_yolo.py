from ultralytics import YOLO

import os

model = YOLO("yolov8n.pt")  # 加载预训练模型（建议用于训练）

if __name__ == '__main__':
    path = os.getcwd() + "/dataset/mydata.yaml"
    # 单GPU训练
    model.train(data=path, epochs=3, imgsz=640)  # 训练模型
    # 也可以直接传入相对路径，如果无法传入相对路径就获取绝对路径，如上所示
    # model.train(data="./dataset/mydata.yaml", epochs=3, imgsz=640)
    # 多GPU训练，device指向gpu。两个GPU比给GPU提升大约百分之六七十
    # results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device=[0, 1])
    metrics = model.val()  # 在验证集上评估模型性能
    success = model.export(format="onnx")  # 将模型导出为 ONNX 格式
    results = model("dataset/test/images/00004.png")  # 对图像进行预测

    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        result.show()  # display to screen