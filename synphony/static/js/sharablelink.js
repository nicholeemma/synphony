
function copySharableLink() {
  /* Get the text field */
  var copyText = document.getElementById("sharablelink");
  copyText.value = window.location.host  + "/" + window.location.pathname.split("/")[1] + "/" + copyText.value;

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /*For mobile devices*/

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
}


function openStudio(){
   var url = $("#sharablelink").val();
   console.log(url);
   window.open(url);
}
