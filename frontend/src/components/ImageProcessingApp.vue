<template>
  <div class="min-h-screen p-4 flex items-center justify-center transition-all duration-500">
    <div class="w-full max-w-7xl glassmorphism rounded-xl shadow-2xl flex flex-col lg:flex-row overflow-hidden">
      <!-- Sidebar for Parameters -->
      <div v-if="!results.length"
        class="w-full lg:w-1/3 glassmorphism-light p-4 lg:p-6 border-b lg:border-b-0 lg:border-r border-white/10">
        <h2 class="text-xl font-semibold text-white mb-4">Tham số xử lý</h2>
        <form @submit.prevent="processImages" class="space-y-4">
          <!-- Kidney Threshold -->
          <div class="form-group">
            <label class="text-white/80 text-sm mb-1 block">Ngưỡng tin cậy thận</label>
            <div class="flex items-center">
              <input type="range" v-model="parameters.confidence_threshold_kidney" min="0" max="1" step="0.05"
                class="w-full accent-white/70" />
              <span class="ml-3 text-white min-w-[40px] text-right">{{ parameters.confidence_threshold_kidney }}</span>
            </div>
          </div>

          <!-- Stone Threshold -->
          <div class="form-group">
            <label class="text-white/80 text-sm mb-1 block">Ngưỡng tin cậy sỏi</label>
            <div class="flex items-center">
              <input type="range" v-model="parameters.confidence_threshold_stone" min="0" max="1" step="0.05"
                class="w-full accent-white/70" />
              <span class="ml-3 text-white min-w-[40px] text-right">{{ parameters.confidence_threshold_stone }}</span>
            </div>
          </div>

          <!-- Advanced Settings Toggle -->
          <div class="form-group">
            <button type="button" @click="showAdvanced = !showAdvanced"
              class="flex items-center justify-between w-full px-3 py-2 bg-white/10 hover:bg-white/15 rounded-lg text-white text-sm transition-all duration-300">
              <span>Cài đặt nâng cao</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform duration-300"
                :class="{ 'rotate-180': showAdvanced }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          <!-- Advanced Settings Panel -->
          <div v-if="showAdvanced" class="space-y-3 bg-white/5 p-3 rounded-lg">
            <!-- Slice Settings -->
            <div class="grid grid-cols-2 gap-3">
              <div class="form-group">
                <label class="text-white/80 text-sm mb-1 block">Chiều dọc lát cắt</label>
                <input type="number" v-model="parameters.slice_height" min="32" max="1024"
                  class="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-1 text-white focus:outline-none focus:ring-2 focus:ring-white/30" />
              </div>

              <div class="form-group">
                <label class="text-white/80 text-sm mb-1 block">Chiều ngang lát cắt</label>
                <input type="number" v-model="parameters.slice_width" min="32" max="1024"
                  class="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-1 text-white focus:outline-none focus:ring-2 focus:ring-white/30" />
              </div>
            </div>

            <!-- Overlap Settings -->
            <div class="grid grid-cols-2 gap-3">
              <div class="form-group">
                <label class="text-white/80 text-sm mb-1 block">Tỉ lệ chồng lấp dọc</label>
                <div class="flex items-center">
                  <input type="range" v-model="parameters.overlap_height_ratio" min="0" max="0.5" step="0.05"
                    class="w-full accent-white/70" />
                  <span class="ml-2 text-white min-w-[40px] text-right">{{ parameters.overlap_height_ratio }}</span>
                </div>
              </div>

              <div class="form-group">
                <label class="text-white/80 text-sm mb-1 block">T lệ chồng lấp ngang</label>
                <div class="flex items-center">
                  <input type="range" v-model="parameters.overlap_width_ratio" min="0" max="0.5" step="0.05"
                    class="w-full accent-white/70" />
                  <span class="ml-2 text-white min-w-[40px] text-right">{{ parameters.overlap_width_ratio }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <button type="submit"
            class="w-full px-6 py-3 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-all duration-300 flex items-center justify-center"
            :disabled="isProcessing || !files.length">
            <span v-if="isProcessing" class="mr-2">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
            </span>
            {{ isProcessing ? 'Đang xử lý...' : 'Phát hiện thận và sỏi' }}
          </button>
        </form>
      </div>

      <!-- Main Content Area -->
      <div :class="['w-full', results.length > 0 ? 'lg:w-full' : 'lg:w-2/3', 'flex', 'flex-col']">
        <!-- Header -->
        <div class="text-center p-4 lg:p-6 pb-0">
          <h1 class="text-2xl font-bold text-white">Công cụ hỗ trợ phát hiện sỏi thận</h1>
          <p class="text-white/80 text-sm">Tải lên ảnh và xem kết quả phân tích</p>
        </div>

        <!-- Upload Section -->
        <div v-if="!isProcessing && !results.length" class="flex-grow flex flex-col items-center justify-center p-4 lg:p-6">
          <div @dragover.prevent="dragOver = true" @dragleave.prevent="dragOver = false" @drop.prevent="handleDrop"
            class="border-2 border-dashed border-white/30 rounded-lg p-6 text-center transition-all duration-300 w-full max-w-2xl"
            :class="{ 'bg-white/10 border-white/50': dragOver }">
            <div v-if="!files.length" class="flex flex-col items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white/70 mb-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="text-white/80 mb-4">Kéo thả ảnh vào đây, hoặc</p>
              <label
                class="px-6 py-3 bg-white/20 hover:bg-white/30 text-white rounded-lg cursor-pointer transition-all duration-300">
                Chọn ảnh
                <input type="file" ref="fileInput" @change="handleFileSelect" multiple accept="image/*" class="hidden" />
              </label>
            </div>

            <!-- File Preview Grid -->
            <div v-else class="w-full">
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                <div v-for="(file, index) in files" :key="index" class="relative group">
                  <img :src="getFilePreview(file)" class="w-full h-20 object-cover rounded-lg" alt="File preview" />
                  <button @click="removeFile(index)"
                    class="absolute top-1 right-1 bg-black/50 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                      stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                  <div class="text-white/80 text-xs mt-1 truncate">{{ file.name }}</div>
                </div>
              </div>

              <div class="mt-4 flex justify-center">
                <label
                  class="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg cursor-pointer transition-all duration-300 text-sm">
                  Thêm ảnh
                  <input type="file" @change="handleFileSelect" multiple accept="image/*" class="hidden" />
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Results Section -->
        <div v-if="results.length > 0" class="flex flex-col h-full p-4 lg:p-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold text-white">Kết quả phát hiện</h2>
              <div class="flex items-center space-x-4">
                <div class="flex items-center">
                  <div class="w-3 h-3 bg-green-500 rounded-full mr-1"></div>
                  <span class="text-white/80 text-xs">Thận</span>
                </div>
                <div class="flex items-center">
                  <div class="w-3 h-3 bg-red-500 rounded-full mr-1"></div>
                  <span class="text-white/80 text-xs">Sỏi thận</span>
                </div>
              </div>
            </div>

          <!-- Carousel Navigation -->
          <div v-if="results.length > 1" class="flex justify-center mb-3">
            <button @click="prevImage" class="p-1.5 bg-white/10 hover:bg-white/20 text-white rounded-lg mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div class="text-white/80 flex items-center">
              {{ currentImageIndex + 1 }} / {{ results.length }}
            </div>
            <button @click="nextImage" class="p-1.5 bg-white/10 hover:bg-white/20 text-white rounded-lg ml-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>

          <!-- Detection Results - Improved layout -->
          <div class="flex flex-col lg:flex-row gap-4 flex-grow min-h-0">
            <!-- Left side: Overview image with all bounding boxes -->
            <div class="relative glassmorphism-light p-2 rounded-lg flex items-center justify-center lg:w-4/5 h-full ">
              <div class="relative w-full h-full flex items-center justify-center" ref="imageContainer">
                <img :src="currentResult.originalImage" class="max-w-full max-h-full object-contain rounded-lg"
                  ref="originalImage" @load="initializeCanvas" alt="Original image" />
                <canvas ref="detectionCanvas" class="absolute top-0 left-0 w-full h-full pointer-events-none"></canvas>
                <div class="absolute inset-0" @click="handleBoxClick" @dblclick="resetHighlight"></div>
              </div>
              <!-- Instructions for interaction -->
              <div class="absolute bottom-2 left-2 right-2 text-center text-white/70 text-xs bg-black/30 p-1 rounded">
                Nhấp vào vùng phát hiện để xem chi tiết. Nhấp đúp để bỏ chọn.
              </div>
            </div>

            <!-- Right side: Zoomed-in view with stone info -->
            <div class="glassmorphism-light rounded-lg flex flex-col lg:w-3/5 h-full overflow-hidden">
              <!-- Display highlighted detection info at the top -->
              <div v-if="!highlightedBox && !selectedStone"
                class="flex-grow flex items-center justify-center text-white/70 text-center p-4">
                <div>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                  </svg>
                  <p>Nhấp vào vùng phát hiện để xem chi tiết</p>
                </div>
              </div>
              <div v-else class="h-full flex flex-col">
                <!-- Header with detection info -->
                <div class="bg-white/10 p-3 flex items-start justify-between">
                  <div class="flex items-center">
                    <div class="w-4 h-4 rounded-full mr-2" :class="(highlightedBox?.category === 'kidney' || selectedStone?.category === 'kidney-stone') ?
                      (selectedStone ? 'bg-red-500' : 'bg-green-500') : 'bg-red-500'"></div>
                    <div>
                      <div class="text-white font-semibold">
                        {{ selectedStone ? 'Sỏi thận' : highlightedBox?.category === 'kidney' ? 'Thận' : 'Sỏi thận' }}
                      </div>
                      <div class="text-white/80 text-sm">Tin cậy: {{ ((selectedStone?.score || highlightedBox?.score) *
                        100).toFixed(1) }}%</div>
                    </div>
                  </div>

                  <!-- Stone count for kidney -->
                  <div v-if="highlightedBox?.category === 'kidney' && !selectedStone" class="text-right">
                    <div class="text-white/80 text-sm">Số sỏi: {{ stonesInKidney.length }}</div>
                  </div>
                </div>

                <!-- Main content area -->
                <div class="flex-grow flex">
                  <!-- Zoomed view (70% width) -->
                  <div class="relative flex-1 flex items-center justify-center bg-black/20">
                    <canvas ref="zoomedCanvas" class="max-w-full max-h-full object-contain"></canvas>
                  </div>

                  <!-- Stone info panel (30% width) -->
                  <div v-if="highlightedBox?.category === 'kidney' && stonesInKidney.length > 0"
                    class="w-[30%] bg-white/5 p-2 overflow-y-auto">
                    <div class="text-white/80 text-sm mb-2 text-center">Sỏi trong thận</div>
                    <div class="space-y-1">
                      <div v-for="(stone, index) in stonesInKidney" :key="index" @click="selectStone(stone)"
                        class="bg-white/5 p-1.5 rounded text-xs flex items-center cursor-pointer transition-colors"
                        :class="{ 'bg-white/20': selectedStone?.bbox.toString() === stone.bbox.toString() }">
                        <div class="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                        <span class="truncate">Sỏi {{ (stone.score * 100).toFixed(0) }}%</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Zoom controls at bottom -->
                <div class="bg-white/5 p-2 rounded-b-lg">
                  <div class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white/70 mr-2" viewBox="0 0 20 20"
                      fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                        clip-rule="evenodd" />
                    </svg>
                    <input type="range" v-model="zoomPadding" min="0" max="0.5" step="0.05" class="w-full accent-white/70"
                      @input="updateZoomedView" />
                    <div class="ml-2 text-white/70 text-xs w-10">{{ zoomPadding === 0 ? 'Max' : (zoomPadding *
                      2).toFixed(1)
                      + 'x' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Reset Button -->
          <div class="mt-4 flex justify-center">
            <button @click="resetAll" class="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-all duration-300 text-sm">
              Phân tích ảnh mới
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue';

// State
const fileInput = ref(null);
const dragOver = ref(false);
const files = ref([]);
const isProcessing = ref(false);
const results = ref([]);
const currentImageIndex = ref(0);
const originalImage = ref(null);
const detectionCanvas = ref(null);
const zoomedCanvas = ref(null);
const imageContainer = ref(null);
const highlightedBox = ref(null);
const selectedStone = ref(null);
const showAdvanced = ref(false);
const zoomPadding = ref(0.2);

// Parameters for processing
const parameters = reactive({
  confidence_threshold_kidney: 0.5,
  confidence_threshold_stone: 0.5,
  slice_height: 256,
  slice_width: 256,
  overlap_height_ratio: 0.25,
  overlap_width_ratio: 0.25,
});

// Computed properties
const currentResult = computed(() => {
  if (results.value.length === 0) return null;
  return results.value[currentImageIndex.value];
});

const stonesInKidney = computed(() => {
  if (!highlightedBox.value || highlightedBox.value.category !== 'kidney' || !currentResult.value) return [];

  const [kidneyX, kidneyY, kidneyWidth, kidneyHeight] = highlightedBox.value.bbox;

  return currentResult.value.detections.filter(detection => {
    if (detection.category !== 'kidney-stone') return false;

    const [stoneX, stoneY, stoneWidth, stoneHeight] = detection.bbox;

    return stoneX >= kidneyX &&
      stoneY >= kidneyY &&
      (stoneX + stoneWidth) <= (kidneyX + kidneyWidth) &&
      (stoneY + stoneHeight) <= (kidneyY + kidneyHeight);
  });
});

// Methods for file handling
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files);
  addFiles(selectedFiles);
};

const handleDrop = (event) => {
  dragOver.value = false;
  const droppedFiles = Array.from(event.dataTransfer.files).filter(file => file.type.startsWith('image/'));
  addFiles(droppedFiles);
};

const addFiles = (newFiles) => {
  const imageFiles = newFiles.filter(file => file.type.startsWith('image/'));
  files.value = [...files.value, ...imageFiles];
};

const removeFile = (index) => {
  files.value.splice(index, 1);
};

const getFilePreview = (file) => {
  return URL.createObjectURL(file);
};

// Process images
const processImages = async () => {
  if (files.value.length === 0) {
    alert('Vui lòng tải lên ít nhất một ảnh');
    return;
  }

  isProcessing.value = true;

  try {
    const formData = new FormData();

    formData.append('confidence_threshold_kidney', parameters.confidence_threshold_kidney);
    formData.append('confidence_threshold_stone', parameters.confidence_threshold_stone);
    formData.append('slice_height', parameters.slice_height);
    formData.append('slice_width', parameters.slice_width);
    formData.append('overlap_height_ratio', parameters.overlap_height_ratio);
    formData.append('overlap_width_ratio', parameters.overlap_width_ratio);

    files.value.forEach(file => {
      formData.append('images', file);
    });

    const response = await fetch('http://localhost:8000/detect', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Lỗi: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    results.value = data.results.map((result, index) => {
      const file = files.value.find(f => f.name === result.image) || files.value[index];

      let originalImageUrl;
      try {
        originalImageUrl = URL.createObjectURL(file);
      } catch (e) {
        console.error('Không thể tạo URL cho ảnh gốc:', e);
        originalImageUrl = '';
      }

      const allDetections = [
        ...result.kidneys.map(kidney => ({
          bbox: kidney.bbox,
          score: kidney.score,
          category: 'kidney',
          color: '#22c55e'
        })),
        ...result.stones.map(stone => ({
          bbox: stone.bbox,
          score: stone.score,
          category: 'kidney-stone',
          color: '#ef4444'
        }))
      ];

      return {
        originalImage: originalImageUrl,
        detections: allDetections,
        filename: result.image,
        originalSize: { width: 0, height: 0 }
      };
    });

    if (results.value.length > 0) {
      currentImageIndex.value = 0;
    } else {
      throw new Error('Không có kết quả trả về từ server');
    }

  } catch (error) {
    console.error('Chi tiết lỗi:', error);
    alert(`Lỗi: ${error.message}`);
  } finally {
    isProcessing.value = false;
  }
};

// Carousel navigation
const nextImage = () => {
  if (currentImageIndex.value < results.value.length - 1) {
    currentImageIndex.value++;
  } else {
    currentImageIndex.value = 0;
  }
};

const prevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  } else {
    currentImageIndex.value = results.value.length - 1;
  }
};

// Canvas for detections
const initializeCanvas = () => {
  if (!detectionCanvas.value || !originalImage.value || !currentResult.value) return;

  const canvas = detectionCanvas.value;
  const img = originalImage.value;

  if (currentResult.value) {
    currentResult.value.originalSize = {
      width: img.naturalWidth,
      height: img.naturalHeight
    };
  }

  canvas.width = img.clientWidth;
  canvas.height = img.clientHeight;

  drawDetections();
};

const drawDetections = (highlightIndex = -1) => {
  if (!detectionCanvas.value || !currentResult.value || !originalImage.value) return;

  const canvas = detectionCanvas.value;
  const ctx = canvas.getContext('2d');
  const detections = currentResult.value.detections;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const img = originalImage.value;
  const originalWidth = currentResult.value.originalSize.width;
  const originalHeight = currentResult.value.originalSize.height;

  const displayRatio = Math.min(
    img.clientWidth / originalWidth,
    img.clientHeight / originalHeight
  );

  const offsetX = (img.clientWidth - originalWidth * displayRatio) / 2;
  const offsetY = (img.clientHeight - originalHeight * displayRatio) / 2;

  detections.forEach((detection, index) => {
    const isHighlighted = index === highlightIndex ||
      (highlightedBox.value &&
        detection.bbox.toString() === highlightedBox.value.bbox.toString()) ||
      (selectedStone.value &&
        detection.bbox.toString() === selectedStone.value.bbox.toString());

    const [x, y, width, height] = detection.bbox;

    const scaledX = x * displayRatio + offsetX;
    const scaledY = y * displayRatio + offsetY;
    const scaledWidth = width * displayRatio;
    const scaledHeight = height * displayRatio;

    ctx.lineWidth = isHighlighted ? 3 : 2;
    ctx.strokeStyle = detection.color;

    ctx.beginPath();
    ctx.rect(scaledX, scaledY, scaledWidth, scaledHeight);
    ctx.stroke();

    if (isHighlighted) {
      ctx.fillStyle = detection.category === 'kidney'
        ? 'rgba(34, 197, 94, 0.2)'
        : 'rgba(239, 68, 68, 0.2)';
      ctx.fillRect(scaledX, scaledY, scaledWidth, scaledHeight);
    }

    const labelWidth = Math.min(100, scaledWidth);
    const labelHeight = 20;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(scaledX, scaledY - labelHeight, labelWidth, labelHeight);

    ctx.fillStyle = '#ffffff';
    ctx.font = '12px Arial';
    const labelText = detection.category === 'kidney' ? 'Thận' : 'Sỏi';
    ctx.fillText(`${labelText} ${(detection.score * 100).toFixed(0)}%`, scaledX + 5, scaledY - 5);
  });
};

const drawZoomedView = () => {
  if (!zoomedCanvas.value || !originalImage.value || !(highlightedBox.value || selectedStone.value) || !currentResult.value) return;

  const canvas = zoomedCanvas.value;
  const ctx = canvas.getContext('2d');
  const img = originalImage.value;

  // Sử dụng bbox của sỏi nếu có, ngược lại dùng bbox của thận
  const targetBox = selectedStone.value || highlightedBox.value;
  const [x, y, width, height] = targetBox.bbox;
  const padding = Math.min(width, height) * zoomPadding.value;

  const paddedX = Math.max(0, x - padding);
  const paddedY = Math.max(0, y - padding);
  const paddedWidth = Math.min(currentResult.value.originalSize.width - paddedX, width + padding * 2);
  const paddedHeight = Math.min(currentResult.value.originalSize.height - paddedY, height + padding * 2);

  const containerWidth = canvas.parentElement.clientWidth;
  const containerHeight = canvas.parentElement.clientHeight;

  const aspectRatio = paddedWidth / paddedHeight;
  let canvasWidth, canvasHeight;

  if (containerWidth / aspectRatio <= containerHeight) {
    canvasWidth = containerWidth;
    canvasHeight = containerWidth / aspectRatio;
  } else {
    canvasHeight = containerHeight;
    canvasWidth = containerHeight * aspectRatio;
  }

  canvas.width = canvasWidth;
  canvas.height = canvasHeight;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.drawImage(
    img,
    paddedX, paddedY, paddedWidth, paddedHeight,
    0, 0, canvas.width, canvas.height
  );

  const boxX = (x - paddedX) * (canvas.width / paddedWidth);
  const boxY = (y - paddedY) * (canvas.height / paddedHeight);
  const boxWidth = width * (canvas.width / paddedWidth);
  const boxHeight = height * (canvas.height / paddedHeight);

  ctx.lineWidth = 3;
  ctx.strokeStyle = targetBox.color;
  ctx.beginPath();
  ctx.rect(boxX, boxY, boxWidth, boxHeight);
  ctx.stroke();

  ctx.fillStyle = targetBox.category === 'kidney'
    ? 'rgba(34, 197, 94, 0.2)'
    : 'rgba(239, 68, 68, 0.2)';
  ctx.fillRect(boxX, boxY, boxWidth, boxHeight);

  const labelText = targetBox.category === 'kidney' ? 'Thận' : 'Sỏi thận';
  const labelWidth = Math.min(150, boxWidth);
  const labelHeight = 24;

  ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
  ctx.fillRect(boxX, boxY - labelHeight, labelWidth, labelHeight);

  ctx.fillStyle = '#ffffff';
  ctx.font = '14px Arial';
  ctx.fillText(
    `${labelText} ${(targetBox.score * 100).toFixed(1)}%`,
    boxX + 5,
    boxY - 6
  );

  // Nếu đang zoom vào thận, vẽ tất cả sỏi trong đó
  if (highlightedBox.value?.category === 'kidney' && !selectedStone.value) {
    stonesInKidney.value.forEach(stone => {
      const [stoneX, stoneY, stoneWidth, stoneHeight] = stone.bbox;

      const stoneBoxX = (stoneX - paddedX) * (canvas.width / paddedWidth);
      const stoneBoxY = (stoneY - paddedY) * (canvas.height / paddedHeight);
      const stoneBoxWidth = stoneWidth * (canvas.width / paddedWidth);
      const stoneBoxHeight = stoneHeight * (canvas.height / paddedHeight);

      // Draw red border for kidney stones
      ctx.lineWidth = 3;
      ctx.strokeStyle = '#ef4444';
      ctx.beginPath();
      ctx.rect(stoneBoxX, stoneBoxY, stoneBoxWidth, stoneBoxHeight);
      ctx.stroke();

      // Fill with semi-transparent red
      ctx.fillStyle = 'rgba(239, 68, 68, 0.3)';
      ctx.fillRect(stoneBoxX, stoneBoxY, stoneBoxWidth, stoneBoxHeight);

      const stoneLabelWidth = Math.min(100, stoneBoxWidth);
      const stoneLabelHeight = 20;

      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      ctx.fillRect(stoneBoxX, stoneBoxY - stoneLabelHeight, stoneLabelWidth, stoneLabelHeight);

      ctx.fillStyle = '#ffffff';
      ctx.font = '12px Arial';
      ctx.fillText(
        `Sỏi ${(stone.score * 100).toFixed(0)}%`,
        stoneBoxX + 5,
        stoneBoxY - 5
      );
    });
  }
};

const updateZoomedView = () => {
  if (highlightedBox.value || selectedStone.value) {
    drawZoomedView();
  }
};

const selectStone = (stone) => {
  selectedStone.value = stone;
  // Tìm bbox thận chứa sỏi này
  const containingKidney = currentResult.value.detections.find(detection => {
    if (detection.category !== 'kidney') return false;

    const [kidneyX, kidneyY, kidneyWidth, kidneyHeight] = detection.bbox;
    const [stoneX, stoneY, stoneWidth, stoneHeight] = stone.bbox;

    return stoneX >= kidneyX &&
      stoneY >= kidneyY &&
      (stoneX + stoneWidth) <= (kidneyX + kidneyWidth) &&
      (stoneY + stoneHeight) <= (kidneyY + kidneyHeight);
  });

  if (containingKidney) {
    highlightedBox.value = containingKidney;
    setTimeout(() => {
      drawZoomedView();
    }, 0);
  }
};

const handleBoxClick = (event) => {
  if (!detectionCanvas.value || !currentResult.value || !originalImage.value) return;

  const img = originalImage.value;
  const rect = img.getBoundingClientRect();

  const originalWidth = currentResult.value.originalSize.width;
  const originalHeight = currentResult.value.originalSize.height;

  const displayRatio = Math.min(
    img.clientWidth / originalWidth,
    img.clientHeight / originalHeight
  );

  const offsetX = (img.clientWidth - originalWidth * displayRatio) / 2;
  const offsetY = (img.clientHeight - originalHeight * displayRatio) / 2;

  const clickX = event.clientX - rect.left;
  const clickY = event.clientY - rect.top;

  const detections = currentResult.value.detections;
  let clickedIndex = -1;
  let clickedStone = null;

  // u tiên kiểm tra sỏi trước
  for (let i = 0; i < detections.length; i++) {
    const detection = detections[i];
    if (detection.category !== 'kidney-stone') continue;

    const [x, y, width, height] = detection.bbox;

    const scaledX = x * displayRatio + offsetX;
    const scaledY = y * displayRatio + offsetY;
    const scaledWidth = width * displayRatio;
    const scaledHeight = height * displayRatio;

    if (clickX >= scaledX && clickX <= scaledX + scaledWidth &&
      clickY >= scaledY && clickY <= scaledY + scaledHeight) {
      clickedStone = detection;
      break;
    }
  }

  // Nếu không click vào sỏi, kiểm tra thận
  if (!clickedStone) {
    for (let i = 0; i < detections.length; i++) {
      const detection = detections[i];
      const [x, y, width, height] = detection.bbox;

      const scaledX = x * displayRatio + offsetX;
      const scaledY = y * displayRatio + offsetY;
      const scaledWidth = width * displayRatio;
      const scaledHeight = height * displayRatio;

      if (clickX >= scaledX && clickX <= scaledX + scaledWidth &&
        clickY >= scaledY && clickY <= scaledY + scaledHeight) {
        clickedIndex = i;
        highlightedBox.value = detection;
        selectedStone.value = null;
        break;
      }
    }
  } else {
    // Nếu click vào sỏi, tìm thận chứa nó
    selectedStone.value = clickedStone;
    const containingKidney = detections.find(detection => {
      if (detection.category !== 'kidney') return false;

      const [kidneyX, kidneyY, kidneyWidth, kidneyHeight] = detection.bbox;
      const [stoneX, stoneY, stoneWidth, stoneHeight] = clickedStone.bbox;

      return stoneX >= kidneyX &&
        stoneY >= kidneyY &&
        (stoneX + stoneWidth) <= (kidneyX + kidneyWidth) &&
        (stoneY + stoneHeight) <= (kidneyY + kidneyHeight);
    });

    if (containingKidney) {
      highlightedBox.value = containingKidney;
    }
  }

  drawDetections(clickedIndex);

  if (highlightedBox.value || selectedStone.value) {
    drawZoomedView();
  }
};

const resetHighlight = () => {
  highlightedBox.value = null;
  selectedStone.value = null;
  drawDetections();
};

const resetAll = () => {
  files.value = [];
  results.value = [];
  currentImageIndex.value = 0;
  highlightedBox.value = null;
  selectedStone.value = null;
};

// Watchers
watch([highlightedBox, selectedStone], () => {
  if (highlightedBox.value || selectedStone.value) {
    setTimeout(() => {
      drawZoomedView();
    }, 0);
  }
});

watch(currentImageIndex, () => {
  highlightedBox.value = null;
  selectedStone.value = null;
  setTimeout(() => {
    initializeCanvas();
  }, 0);
});

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('resize', () => {
    initializeCanvas();
    if (highlightedBox.value || selectedStone.value) {
      drawZoomedView();
    }
  });
});

onUnmounted(() => {
  window.removeEventListener('resize', initializeCanvas);
});
</script>

<style>
/* Glassmorphism effect */
.glassmorphism {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.glassmorphism-light {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Custom gradient background */
.custom-gradient {
    /* background-color:#000000; */
    background-color:#99f5ff;
    background-image:
    radial-gradient(at 55% 42%, hsla(149,88%,7%,1) 0px, transparent 50%),
    radial-gradient(at 28% 45%, hsla(189,96%,7%,1) 0px, transparent 50%),
    radial-gradient(at 77% 6%, hsla(227,73%,7%,1) 0px, transparent 50%),
    radial-gradient(at 83% 71%, hsla(129,77%,7%,1) 0px, transparent 50%),
    radial-gradient(at 31% 88%, hsla(216,71%,7%,1) 0px, transparent 50%),
    radial-gradient(at 40% 16%, hsla(30,72%,7%,1) 0px, transparent 50%),
    radial-gradient(at 3% 80%, hsla(175,67%,7%,1) 0px, transparent 50%);
}

/* Custom scrollbar */
/* n scrollbar nhưng vẫn cho phép scroll */
html {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE và Edge */
}

html::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

/* Đảm bảo các phần tử có overflow vẫn hoạt động */
body {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

body::-webkit-scrollbar {
  display: none;
}

/* Layout improvements */
.h-full {
  height: 100%;
}

.max-h-full {
  max-height: 100%;
}

.flex-grow {
  flex-grow: 1;
}

.min-h-0 {
  min-height: 0;
}

/* Result container styling */
.result-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.image-container {
  flex: 1;
  min-height: 0;
  position: relative;
}

/* Stone list styling */
.stone-list {
  max-height: 120px;
  overflow-y: auto;
}

.stone-item {
  transition: all 0.2s ease;
}

.stone-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Main content area */
.main-content {
  display: flex;
  flex-direction: column;
  height: 80vh;
}

.results-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.detection-results {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.image-viewer {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.zoomed-view-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
</style>
