// Función para cargar el stream de video en un elemento <video>
function loadVideoStream(videoElementId, streamUrl) {
    const videoElement = document.getElementById(videoElementId);
    if (videoElement) {
        videoElement.src = streamUrl;
        videoElement.onerror = () => {
            console.error(`Error al cargar el stream desde ${streamUrl}`);
        };
    } else {
        console.error(`Elemento de video con ID ${videoElementId} no encontrado.`);
    }
}

// Cargar los streams en los elementos de video
loadVideoStream('videoOriginal', '/video_original');
loadVideoStream('videoProcesado', '/video_process');

// Funciones JavaScript para la aplicación