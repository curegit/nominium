(function () {
  const queries = JSON.parse(document.getElementById("queries").textContent);
  const input = document.getElementById("query-input");
  const buttons = document.getElementById("query-buttons");

  input.addEventListener("input", () => {
    buttons.innerHTML = "";
    const query = input.value.trim();
    if (query) {
      for (const [name, f] of Object.entries(queries)) {
        const url = f(query);
        const button = document.createElement("button");
        button.textContent = name;
        button.onclick = () => {
          window.open(url, "_blank");
        };
        buttons.appendChild(button);
      }
    }
  });
})();
