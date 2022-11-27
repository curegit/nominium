(function () {
  const select = document.getElementById("filter-select");

  function setfilter(code) {
    const items = document.getElementsByClassName("item");
    for (let i = 0; i < items.length; i++) {
      const classes = items[i].classList;
      if (code === -1) {
        classes.remove("filtered");
      } else {
        if (classes.contains("notify" + code)) {
          classes.remove("filtered");
        } else {
          classes.add("filtered");
        }
      }
    }
  }

  function changefilter() {
    const code = +select.value;
    setfilter(code);
  }

  select.addEventListener("change", changefilter);
})();
