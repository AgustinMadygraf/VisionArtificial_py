document.addEventListener("DOMContentLoaded", () => {
    const pixelsToUnitsInput = document.getElementById("pixelsToUnits");
    const pixelsToUnitsValue = document.getElementById("pixelsToUnitsValue");
    const applyConfigButton = document.getElementById("applyConfig");

    if (pixelsToUnitsInput && pixelsToUnitsValue) {
        pixelsToUnitsInput.addEventListener("input", () => {
            pixelsToUnitsValue.textContent = pixelsToUnitsInput.value;
        });

        // Fetch initial value from the server
        fetch("/config/PIXELS_TO_UNITS")
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Failed to fetch initial configuration.");
                }
            })
            .then(data => {
                if (data && data.PIXELS_TO_UNITS !== undefined) {
                    pixelsToUnitsInput.value = data.PIXELS_TO_UNITS;
                    pixelsToUnitsValue.textContent = data.PIXELS_TO_UNITS;
                }
            })
            .catch(error => {
                console.error("Error fetching initial configuration:", error);
            });
    }

    if (applyConfigButton) {
        applyConfigButton.addEventListener("click", () => {
            const config = {
                PIXELS_TO_UNITS: parseInt(pixelsToUnitsInput.value, 10)
            };

            fetch("/config", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(config)
            })
            .then(response => {
                if (response.ok) {
                    alert("Configuración aplicada correctamente.");
                } else {
                    return response.json().then(err => {
                        throw new Error(err.error || "Error desconocido.");
                    });
                }
            })
            .catch(error => {
                console.error("Error al aplicar la configuración:", error);
                alert(`Error al aplicar la configuración: ${error.message}`);
            });
        });
    }
});
