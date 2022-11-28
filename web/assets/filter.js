(function () {
  const select = document.getElementById("filter-select");

  function setfilter(code) {
    const areas = document.getElementsByClassName("filtered");
    for (let i = 0; i < areas.length; i++) {
      const classes = areas[i].classList;
      if (code === -1) {
        classes.remove("positive");
        classes.remove("negative");
      } else if (code === 0) {
        classes.add("positive");
        classes.remove("negative");
      } else {
        classes.remove("positive");
        classes.add("negative");
        if (code <= 3) {
          classes.remove("code1");
          classes.remove("code2");
          classes.remove("code3");
          classes.add("code" + code);
        }
      }
    }
  }

  function changefilter() {
    const code = +select.value;
    setfilter(code);
  }

  select.addEventListener("change", changefilter);
  changefilter();
})();
