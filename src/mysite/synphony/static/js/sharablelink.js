// Deals with sharable link
function copySharableLink() {
  /* Get the text field */
  var copyText = document.getElementById("sharablelink");
  var oldText = copyText.value;
  copyText.value = window.location.protocol + '//' + window.location.host  + "/" + window.location.pathname.split("/")[1] + "/" + copyText.value;

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /*For mobile devices*/

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);

  copyText.value = oldText;
}


function openStudio(){
   var url = $("#sharablelink").val();
   if ((!url.startsWith("https://")) && (!url.startsWith("http://"))){
    url = "https://" + url;
   }
   console.log(url);
   window.open(url);
}
