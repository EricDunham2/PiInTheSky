const user = 'root@System:~$&nbsp;';

function terminal_submit(self) {
  var submitted_value = self.value;
  var output_value = user + self.value;
  if (submitted_value === 'clear') {
     var output_div = document.getElementsByClassName('terminal-output')[0];
     var children  = Array.from(output_div.children);
     children.forEach(child => {
         child.remove()
     })
     self.value = '';
     return;
  }
  exec(submitted_value)
  output(output_value)

  self.value = '';
}

document.getElementById("term-in")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
       terminal_submit(document.getElementById("term-in"));
    }
});

function createElement(type,attrsMap,html,parent) {
  var el = document.createElement(type);
  var attributes = Object.keys(attrsMap);
  
  attributes.forEach(attr => {
     el.setAttribute(attr,attrsMap[attr]);
  });
  
  el.innerHTML = html;
  
  parent.appendChild(el);
  return el;
}


function output(data) {
  var results  = data.split('\n')
  var output_div = document.getElementsByClassName('terminal-output')[0];

  results.forEach(res => {
      o_type = 'div'
      o_attrMap = {
        'class':'terminal-output-text'
      }
      o_html  = res

      createElement(o_type,o_attrMap,o_html,output_div)
  })

  //var terminal_output = document.createElement('div');
  //terminal_output.classList.add('terminal-output-text');

  //terminal_output.innerHTML = data;
  //output_div.appendChild(terminal_output);
  output_div.scrollTop = output_div.scrollHeight;
  self.value = ''; 
}

function exec(json) {
json  = '{"cmd":"' + json +'"}' 
$.ajax({
    type : "POST",
    url : "/exe",
    data: json,
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
        output(result)
    }
});
}
