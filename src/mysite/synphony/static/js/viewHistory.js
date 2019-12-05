// View history page content change when pressing different buttons
function viewStudio() {
    document.getElementById("studio").style.visibility = "visible";
    document.getElementById("comment").style.visibility = "hidden";
    document.getElementById("music").style.visibility = "hidden";
  }

  function viewComment() {
    document.getElementById("studio").style.visibility = "hidden";
    document.getElementById("comment").style.visibility = "visible";
    document.getElementById("music").style.visibility = "hidden";
  }

  function viewMusic() {
    document.getElementById("studio").style.visibility = "hidden";
    document.getElementById("comment").style.visibility = "hidden";
    document.getElementById("music").style.visibility = "visible";
  }
