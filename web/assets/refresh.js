var t = document.getElementById("auto-update");
var s = document.getElementById("auto-update-interval");
var intid = null;
t.checked = true;
s.selectedIndex = 0;

function refresh() {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "./");
  xhr.responseType = "document";
  xhr.timeout = 10000;
  xhr.onload = event => {
    if (xhr.status === 200) {
      const d = xhr.response.getElementsByClassName("items");
      if (d.length < 1) { return; }
      const div2 = d[0];
      const ndiv = document.getElementsByClassName("nothing");
      if (ndiv.length >= 1) {
        ndiv.insertAdjacentElement("beforebegin", div2);
        ndiv.remove();
      }
      let div1 = document.getElementsByClassName("items")[0];

      let hrefs = [...div1.children].map(e => e.getElementsByTagName("a")[0].href);
      let news = [];
      for (let i = 0; i < div2.children.length; i++) {
        let href = div2.children[i].getElementsByTagName("a")[0].href;
        if (!hrefs.includes(href)) {
          news.push(div2.children[i]);
        }
      }
      div1.prepend(...news);
    } else {

    }
  };
  xhr.onerror = event => {

  };
  xhr.ontimeout = event => {

  };
  xhr.send();
}

function sc(n) {
  up();
  setTimeout(sc, n * 1000, n);
}

n = 30;
setTimeout(sc, n * 1000, n);
