/*
Path: static/js/main.js
*/

console.log("iniciando main.js");

class VideoStreamManager {
    constructor(imgElement, startButton, stopButton, streamUrl, placeholderText) {
        this.imgElement = imgElement;
        this.startButton = startButton;
        this.stopButton = stopButton;
        this.streamUrl = streamUrl;
        this.placeholderText = placeholderText;

        this.initEventListeners();
    }

    initEventListeners() {
        this.startButton.addEventListener('click', () => this.startStream());
        this.stopButton.addEventListener('click', () => this.stopStream());

        this.imgElement.onerror = () => {
            console.error(`Error al cargar el stream: ${this.imgElement.src}`);
            this.imgElement.alt = 'Error al cargar el video. Intenta iniciar de nuevo.';
            this.imgElement.classList.add('video-placeholder');
            this.imgElement.src = '';
        };
    }

    startStream() {
        this.imgElement.src = `${this.streamUrl}?t=${new Date().getTime()}`;
        this.imgElement.alt = 'Cargando video...';
        this.imgElement.classList.remove('video-placeholder');
    }

    stopStream() {
        this.imgElement.src = '';
        this.imgElement.alt = this.placeholderText;
        this.imgElement.classList.add('video-placeholder');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const videoOriginalManager = new VideoStreamManager(
        document.getElementById('video-original-img'),
        document.getElementById('start-original'),
        document.getElementById('stop-original'),
        '/video_original',
        'Video Feed Original Detenido'
    );

    const videoProcessedManager = new VideoStreamManager(
        document.getElementById('video-processed-img'),
        document.getElementById('start-processed'),
        document.getElementById('stop-processed'),
        '/video_process',
        'Video Feed Procesado Detenido'
    );
});