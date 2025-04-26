from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
from typing import List

# Khởi tạo FastAPI app
app = FastAPI()

# Thêm middleware CORS để cho phép frontend truy cập API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đường dẫn đến các mô hình (có thể thay bằng biến môi trường)
KIDNEY_MODEL_PATH = ".\models\kidney_detect.pt"
STONE_MODEL_PATH = ".\models\kidney_stone_detect_SF.pt"

# Tải mô hình khi khởi động ứng dụng
try:
    kidney_model = AutoDetectionModel.from_pretrained(
        model_type='yolov8',
        model_path=KIDNEY_MODEL_PATH,
        confidence_threshold=0.5,  # Giá trị mặc định, sẽ được cập nhật theo yêu cầu
    )
    stone_model = AutoDetectionModel.from_pretrained(
        model_type='yolov8',
        model_path=STONE_MODEL_PATH,
        confidence_threshold=0.25,  # Giá trị mặc định, sẽ được cập nhật theo yêu cầu
    )
except Exception as e:
    raise RuntimeError(f"Không thể tải mô hình: {str(e)}")

@app.post("/detect")
async def detect(
    images: List[UploadFile] = Form(...),
    confidence_threshold_kidney: float = Form(...),
    confidence_threshold_stone: float = Form(...),
    slice_height: int = Form(default=256),
    slice_width: int = Form(default=256),
    overlap_height_ratio: float = Form(default=0.25),
    overlap_width_ratio: float = Form(default=0.25),
):
    """
    Endpoint để phát hiện vùng thận và sỏi thận trong ảnh.

    Args:
        images: Danh sách các file ảnh được upload.
        confidence_threshold_kidney: Ngưỡng tin cậy cho phát hiện thận.
        confidence_threshold_stone: Ngưỡng tin cậy cho phát hiện sỏi thận.
        slice_height: Chiều cao lát cắt cho SAHI.
        slice_width: Chiều rộng lát cắt cho SAHI.
        overlap_height_ratio: Tỷ lệ chồng lấp chiều cao.
        overlap_width_ratio: Tỷ lệ chồng lấp chiều rộng.

    Returns:
        JSONResponse chứa kết quả phát hiện cho từng ảnh.
    """
    # Cập nhật ngưỡng tin cậy cho các mô hình
    kidney_model.confidence_threshold = confidence_threshold_kidney
    stone_model.confidence_threshold = confidence_threshold_stone

    results = []

    # Xử lý từng ảnh
    for image_file in images:
        try:
            # Đọc dữ liệu ảnh từ UploadFile
            contents = await image_file.read()
            nparr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f"Không thể đọc ảnh: {image_file.filename}")

            # Giai đoạn 1: Phát hiện vùng thận trên toàn ảnh
            kidney_prediction = get_sliced_prediction(
                image,
                kidney_model,
                slice_height=640,  # Kích thước cố định cho phát hiện thận trên ảnh lớn
                slice_width=640,
                overlap_height_ratio=0.25,
                overlap_width_ratio=0.25,
                perform_standard_pred=True,
                postprocess_type="NMS",
            )

            kidney_detections = []
            stone_detections = []

            # Xử lý từng vùng thận được phát hiện
            for kidney_pred in kidney_prediction.object_prediction_list:
                if kidney_pred.category.name.lower() != 'kidney':
                    continue

                # Tạo bounding box cho thận [x_min, y_min, width, height]
                kidney_bbox = [
                    kidney_pred.bbox.minx,
                    kidney_pred.bbox.miny,
                    kidney_pred.bbox.maxx - kidney_pred.bbox.minx,
                    kidney_pred.bbox.maxy - kidney_pred.bbox.miny,
                ]
                kidney_detections.append({
                    "bbox": kidney_bbox,
                    "score": kidney_pred.score.value
                })

                # Trích xuất vùng thận với padding
                padding = 10 
                x_min, y_min, width, height = map(int, kidney_bbox)
                img_height, img_width = image.shape[:2]
                x_min_padded = max(0, x_min - padding)
                y_min_padded = max(0, y_min - padding)
                x_max_padded = min(img_width, x_min + width + padding)
                y_max_padded = min(img_height, y_min + height + padding)
                kidney_region = image[y_min_padded:y_max_padded, x_min_padded:x_max_padded]

                # Giai đoạn 2: Phát hiện sỏi thận trên vùng thận
                stone_prediction = get_sliced_prediction(
                    kidney_region,
                    stone_model,
                    slice_height=slice_height,
                    slice_width=slice_width,
                    overlap_height_ratio=overlap_height_ratio,
                    overlap_width_ratio=overlap_width_ratio,
                    perform_standard_pred=True,
                    postprocess_type="NMS"
                )

                # Điều chỉnh tọa độ sỏi về ảnh gốc
                for stone_pred in stone_prediction.object_prediction_list:
                    stone_bbox = [
                        stone_pred.bbox.minx + x_min_padded,
                        stone_pred.bbox.miny + y_min_padded,
                        stone_pred.bbox.maxx - stone_pred.bbox.minx,
                        stone_pred.bbox.maxy - stone_pred.bbox.miny,
                    ]
                    stone_detections.append({
                        "bbox": stone_bbox,
                        "score": stone_pred.score.value
                    })

            # Thêm kết quả cho ảnh hiện tại
            results.append({
                "image": image_file.filename,
                "kidneys": kidney_detections,
                "stones": stone_detections
            })

        except Exception as e:
            # Ghi log lỗi nếu cần và bỏ qua ảnh này
            print(f"Lỗi xử lý ảnh {image_file.filename}: {str(e)}")
            continue

    # Trả về kết quả
    return JSONResponse(content={"results": results})

# Chạy ứng dụng với Uvicorn (nếu chạy trực tiếp)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)