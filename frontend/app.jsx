import React, { useState, useRef } from "react";

export default function FileUploader() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [processProgress, setProcessProgress] = useState(0);
  const inputRef = useRef(null);

  const uploadUrl = "http://170.106.150.85:5001/upload";

  function handleFiles(files) {
    if (!files || files.length === 0) return;
    setFile(files[0]);
    setUploadProgress(0);
    setProcessProgress(0);
  }

  function onDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  }
  function onDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  }
  function onDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer?.files?.length) handleFiles(e.dataTransfer.files);
  }
  function triggerInput() {
    inputRef.current?.click();
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
    if (!file) return;
    setUploadProgress(0);
    setProcessProgress(0);
    const form = new FormData();
    form.append("file", file);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", uploadUrl, true);
    xhr.responseType = "blob";
    xhr.upload.onprogress = (ev) => {
      if (ev.lengthComputable) setUploadProgress(Math.round((ev.loaded / ev.total) * 100));
    };
    xhr.onloadstart = () => setProcessProgress(0);
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        const cd = xhr.getResponseHeader("Content-Disposition");
        const filename = getFilenameFromCD(cd) || `response-${file.name}`;
        const url = window.URL.createObjectURL(xhr.response);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        setProcessProgress(100);
      }
    };
    xhr.send(form);
  }

  return (
    <div className="flex flex-col items-center mt-10 space-y-6">
      <div
        className={`w-64 h-48 border-2 rounded-md flex items-center justify-center cursor-pointer overflow-hidden transition ${
          dragActive ? "border-blue-500 bg-blue-50" : "border-gray-400"
        }`}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={triggerInput}
      >
        <input ref={inputRef} type="file" className="hidden" onChange={(e) => handleFiles(e.target.files)} />
      </div>

      <button
        onClick={uploadFile}
        disabled={!file}
        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {file ? `上传 ${file.name}` : "选择文件后上传"}
      </button>

      <div className="text-gray-700">上传进度：{uploadProgress}%</div>
      <div className="text-gray-700">处理进度：{processProgress}%</div>
    </div>
  );
}
