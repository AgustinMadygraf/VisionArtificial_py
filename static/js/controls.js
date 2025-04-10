document.addEventListener("DOMContentLoaded", () => {
    const pixelsToUnitsInput = document.getElementById("pixelsToUnits");
    const pixelsToUnitsValue = document.getElementById("pixelsToUnitsValue");
    const applyConfigButton = document.getElementById("applyConfig");

    console.log("pixelsToUnitsInput:", pixelsToUnitsInput);
    console.log("pixelsToUnitsValue:", pixelsToUnitsValue);
    console.log("applyConfigButton:", applyConfigButton);

    if (pixelsToUnitsInput && pixelsToUnitsValue) {
        pixelsToUnitsInput.addEventListener("input", () => {
            pixelsToUnitsValue.textContent = pixelsToUnitsInput.value;
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
                    alert("Error al aplicar la configuración.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error al aplicar la configuración.");
            });
        });
    }
});
