/*
Path: static/js/main.js
*/

console.log("iniciando main.js");

document.addEventListener('DOMContentLoaded', () => {
    const videoOriginalImg = document.getElementById('video-original-img');
    const videoProcessedImg = document.getElementById('video-processed-img');

    const startOriginalBtn = document.getElementById('start-original');
    const stopOriginalBtn = document.getElementById('stop-original');
    const startProcessedBtn = document.getElementById('start-processed');
    const stopProcessedBtn = document.getElementById('stop-processed');

    // URLs de los streams
    const originalVideoUrl = '/video_original';
    const processedVideoUrl = '/video_process';

    function startStream(imgElement, url) {
        imgElement.src = `${url}?t=${new Date().getTime()}`;
        imgElement.alt = 'Cargando video...';
        imgElement.classList.remove('video-placeholder');
    }

    function stopStream(imgElement, altText) {
        imgElement.src = '';
        imgElement.alt = altText;
        imgElement.classList.add('video-placeholder');
    }

    // Event Listeners para el video original
    startOriginalBtn.addEventListener('click', () => {
        startStream(videoOriginalImg, originalVideoUrl);
    });

    stopOriginalBtn.addEventListener('click', () => {
        stopStream(videoOriginalImg, 'Video Feed Original Detenido');
    });

    // Event Listeners para el video procesado
    startProcessedBtn.addEventListener('click', () => {
        startStream(videoProcessedImg, processedVideoUrl);
    });

    stopProcessedBtn.addEventListener('click', () => {
        stopStream(videoProcessedImg, 'Video Feed Procesado Detenido');
    });

    // Manejo de errores en la carga de la imagen
    [videoOriginalImg, videoProcessedImg].forEach(img => {
        img.onerror = () => {
            console.error(`Error al cargar el stream: ${img.src}`);
            img.alt = 'Error al cargar el video. Intenta iniciar de nuevo.';
            img.classList.add('video-placeholder');
            img.src = '';
        };
    });
});