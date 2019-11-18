var button = document.getElementById("hello");
button.addEventListener("click",function(e){
 
    console.log(e);
},true);
var box = document.getElementById("box");
box.addEventListener("click",function(e){
   
    console.log(e);
},true);


function changeAction() {

	var sort_select = document.getElementById('sort-select');
	var selected_opt = sort_select.options[sort_select.selectedIndex].value;

	var sort_form = document.getElementById('sort-form').action;
	var form_action = sort_form + selected_opt;

	document.getElementById('sort-form').action = form_action
	form = document.getElementById('sort-form')
	form.submit()
}

function setSelectedIndex(s, i) {

	s.options[i-1].selected = true;

	return;
}

setSelectedIndex(document.getElementById("sort-select"),5);

