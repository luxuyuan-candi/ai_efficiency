<template>
  <div class="container">
    <!-- 上传区域 -->
    <div
      class="upload-area"
      :class="{ active: dragActive }"
      @click="triggerInput"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
    >
      <!-- 隐藏文件选择框 -->
      <input
        ref="inputRef"
        type="file"
        style="display:none"
        @change="(e) => handleFiles(e.target.files)"
      />

      <!-- 图片按钮 -->
      <img src="/upload-icon.png" alt="选择文件" class="upload-icon" />
      <p class="upload-text">点击或拖拽文件上传</p>
      <p v-if="file" class="file-name">已选择: {{ file.name }}</p>
    </div>

    <!-- 上传进度 -->
    <div class="progress-container">
      <div class="progress-label">上传进度：{{ uploadProgress }}%</div>
      <div class="progress-bar">
        <div class="progress-fill upload-fill" :style="{ width: uploadProgress + '%' }"></div>
      </div>
    </div>

    <!-- 处理进度 -->
    <div class="progress-container">
      <div class="progress-label">处理进度：{{ processProgress }}%</div>
      <div class="progress-bar">
        <div class="progress-fill process-fill" :style="{ width: processProgress + '%' }"></div>
      </div>
    </div>

    <!-- 上传按钮 -->
    <button
      :disabled="!file"
      @click="uploadFile"
      class="upload-button"
    >
      {{ file ? '开始上传' : '请选择文件' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";

const dragActive = ref(false);
const file = ref(null);
const uploadProgress = ref(0);
const processProgress = ref(0);
const inputRef = ref(null);

const uploadUrl = "http://170.106.150.85:5001/upload";

function handleFiles(files) {
  if (!files || files.length === 0) return;
  file.value = files[0];
  uploadProgress.value = 0;
  processProgress.value = 0;

  // 重置 input 以便连续选择同一个文件
  if (inputRef.value) inputRef.value.value = "";
}

function onDragOver() { dragActive.value = true; }
function onDragLeave() { dragActive.value = false; }
function onDrop(e) {
  dragActive.value = false;
  if (e.dataTransfer?.files?.length) handleFiles(e.dataTransfer.files);
}
function triggerInput() {
  inputRef.value?.click();
}

function getFilenameFromCD(cd) {
  if (!cd) return null;
  const fnMatch = cd.match(/filename\*=(?:UTF-8'')?([^;\n]+)/i);
  if (fnMatch && fnMatch[1]) return decodeURIComponent(fnMatch[1].replace(/"/g, ""));
  const fnMatch2 = cd.match(/filename=(?:(?:")?)([^";\n]+)(?:")?/i);
  if (fnMatch2 && fnMatch2[1]) return fnMatch2[1];
  return null;
}

function uploadFile() {
  if (!file.value) return;
  uploadProgress.value = 0;
  processProgress.value = 0;

  const form = new FormData();
  form.append("file", file.value);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", uploadUrl, true);
  xhr.responseType = "blob";

  xhr.upload.onprogress = (ev) => {
    if (ev.lengthComputable) uploadProgress.value = Math.round((ev.loaded / ev.total) * 100);
  };
  xhr.onloadstart = () => processProgress.value = 0;
  xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      const cd = xhr.getResponseHeader("Content-Disposition");
      const filename = getFilenameFromCD(cd) || `response-${file.value.name}`;
      const url = window.URL.createObjectURL(xhr.response);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      processProgress.value = 100;
    }
  };
  xhr.send(form);
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
  gap: 24px;
  font-family: Arial, sans-serif;
}

.upload-area {
  width: 288px;
  height: 192px;
  border: 2px dashed #ccc;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}
.upload-area.active {
  border-color: #1e90ff;
  background-color: #e6f0ff;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.upload-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 8px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}
.upload-icon:hover {
  opacity: 1;
}

.upload-text {
  font-size: 14px;
  color: #666;
}

.file-name {
  font-size: 12px;
  color: #1e90ff;
  margin-top: 4px;
}

.progress-container {
  width: 288px;
}

.progress-label {
  font-size: 14px;
  color: #444;
  margin-bottom: 4px;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background-color: #eee;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.upload-fill {
  background-color: #1e90ff;
}

.process-fill {
  background-color: #28a745;
}

.upload-button {
  padding: 8px 24px;
  background-color: #1e90ff;
  color: #fff;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.upload-button:hover:not(:disabled) {
  background-color: #1565c0;
}
.upload-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>

