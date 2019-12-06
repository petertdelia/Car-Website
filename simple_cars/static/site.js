var button = document.getElementById("hello");
button.addEventListener("click",function(e){
 
    console.log(e);
},true);
var box = document.getElementById("box");
box.addEventListener("click",function(e){
   
    console.log(e);
},true);


function changeAction(sortselect,sortform) {

	// var sort_select = document.getElementById(sortselect);
	// var selected_opt = sort_select.options[sort_select.selectedIndex].value;

	// var sort_form = document.getElementById(sortform).action;
	// var form_action = sort_form + selected_opt;

	// document.getElementById(sortform).action = form_action
	form = document.getElementById(sortform)
	form.submit()
}

function setSelectedIndex(s, i) {

	s.options[i-1].selected = true;

	return;
}

setSelectedIndex(document.getElementById("sort-select"),5);

