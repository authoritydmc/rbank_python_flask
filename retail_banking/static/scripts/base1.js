let IS_SIDE_OPENED=false;
//this is modified222
//new line
function ToggleSidebar()
{
var side=document.getElementById("my_sidebar");
var ham=document.getElementById("hamburger");
var tophead=document.getElementById("tophead");
var main_section=document.getElementById("main_section");
if (IS_SIDE_OPENED==false){
  side.style.width="300px";
  ham.innerHTML="&times";
  ham.style.fontSize="50px";
  main_section.style.marginLeft="300px";
  console.debug("opening sidebar");
}else //closing sidebar
{
  side.style.width="0";

  ham.innerHTML="&#9776;";
  ham.style.fontSize="30px";

  main_section.style.marginLeft="10px";

console.debug("closing sidebar");
}


  //toggling...

  IS_SIDE_OPENED=!IS_SIDE_OPENED;

}

/****adding all the li item an */
var li = document.getElementsByTagName("li");

for(var i = 0;i<li.length;i++){
    li[i].addEventListener("click", ToggleSidebar);
}

