var dragsource = null;

function dragstart(event) {
  event.preventDefault();
  event.stopPropagation();
  event.dataTransfer.effectAllowed = "move";
  dragsource = event.currentTarget;
  const children = dragsource.parentElement.children;
  for (let i = 0, above = true; i < children.length; i++) {
    if (children[i] === dragsource) {
      above = false;
      dragsource.classList.remove("above", "below");
    } else {
      if (above) {
        dragsource.classList.add("above");
        dragsource.classList.remove("below");
      } else {
        dragsource.classList.add("below");
        dragsource.classList.remove("above");
      }
    }
  }
}

function dragend(event) {
  const children = event.currentTarget.parentElement.children;
  for (let i = 0; i < children.length; i++) {
    children[i].classList.remove("over");
  }
}

function dragover(event) {
  event.preventDefault();
  event.stopPropagation();
  event.dataTransfer.dropEffect = "move";
  event.currentTarget.classList.add("over");
}

function dragleave(event) {
  event.currentTarget.classList.remove("over");
}

function drop(event) {
  event.preventDefault();
  event.stopPropagation();
  const target = event.currentTarget;
  const parent = target.parentElement;
  const children = [...parent.children];
  target.classList.remove("over");
  for (let i = 0; i < children.length; i++) {
    if (children[i] !== dragsource) {
      if (children[i] === target) {
        if (children[i].classList.contains("above")) {
          parent.appendChild(dragsource);
          parent.appendChild(children[i]);
        } else if (children[i].classList.contains("below")) {
          parent.appendChild(children[i]);
          parent.appendChild(dragsource);
        }
      } else {
        parent.appendChild(children[i]);
      }
    }
  }
}
