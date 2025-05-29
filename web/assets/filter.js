(function () {
  const select = document.getElementById("filter-select");

  function applyfilter(code) {
    const areas = document.getElementsByClassName("filtered");
    for (let i = 0; i < areas.length; i++) {
      const classes = areas[i].classList;
      if (code === -1) {
        classes.remove("positive", "negative");
      } else if (code === 0) {
        classes.remove("negative");
        classes.add("positive");
      } else {
        classes.remove("positive", "code1", "code2", "code3", "code4");
        classes.add("negative");
        if (1 <= code && code <= 4) {
          classes.add("code" + code);
        }
      }
    }
  }

  function changefilter() {
    const code = +select.value;
    const url = new URL(location);
    if (code === -1) {
      url.searchParams.delete("filter");
    } else {
      url.searchParams.set("filter", `${code}`);
    }
    history.pushState({filter: code}, "", url);
    applyfilter(code);
  }

  function initfilter() {
    const url = new URL(location);
    const filter = url.searchParams.get("filter");
    const code = filter === null ? -1 : +filter;
    select.value = code;
    applyfilter(code);
  }

  select.addEventListener("change", changefilter);
  window.addEventListener("popstate", initfilter);
  initfilter();
})();
