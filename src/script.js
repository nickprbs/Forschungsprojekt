const embed = vegaEmbed;

const specUrl = "https://vega.github.io/vega-lite/examples/interactive_global_development.vl.json";


embed("#vis", specUrl).then((result) => {
  const view = result.view;

  
  fetch("./gapminder.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load local Gapminder dataset");
      }
      return response.json();
    })
    .then((gapminderData) => {
      view.data("source_0", gapminderData).run();

      console.log("Visualization loaded with local data!");

      // Gamepad functionality
      window.addEventListener("gamepadconnected", (event) => {
        console.log("Gamepad connected:", event.gamepad);

        let currentYear = 2000;

        function updateYear(delta) {
          currentYear += delta;
          currentYear = Math.max(1950, Math.min(2005, currentYear)); 
        
          // Update the year signal and force the slider to update
          view.signal("year", currentYear).run();
        
          // Manually simulate the slider update (trigger a re-render of the slider)
          const sliderElement = document.querySelector(".vega-bind input"); 
          if (sliderElement) {
            sliderElement.value = currentYear; // Update the slider's visual value
            sliderElement.dispatchEvent(new Event("input")); // Trigger an "input" event to make it respond
          }
        
          console.log("Year updated to:", currentYear);
        }
        

        // Poll gamepad inputs
        function pollGamepad(gamepadIndex) {
          function poll() {
            const gamepad = navigator.getGamepads()[gamepadIndex];
            if (gamepad) {
              if (gamepad.buttons[4].pressed) updateYear(-1); // L1: Decrease year
              if (gamepad.buttons[5].pressed) updateYear(1);  // R1: Increase year
            }
            requestAnimationFrame(poll);
          }
          poll();
        }

        pollGamepad(event.gamepad.index);
      });
    })
    .catch((error) => {
      console.error("Error loading local dataset:", error);
    });
});