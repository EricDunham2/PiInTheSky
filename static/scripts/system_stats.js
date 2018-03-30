function update_system_values() {
            $.ajax({
		url: '/system_stats',
                type:'GET',
                success: function(result) {
		    console.log(result)
		    data = JSON.parse(result)
                    $("#temp").text(data.temp)
                    $("#memory").text(data.memory)
                    $("#disk").text(data.space)
                    $("#unet").text(data.uspeed)
                    $("#dnet").text(data.dspeed)
                    $("#mbuffer").text(data.mbuffer)
                    $("#rbuffer").text(data.rbuffer)
                    $("#ismotion").text(data.is_motion)
		    //$("#dnet").show()
                }
	     });
}


function update_script_values() {
            $.ajax({
                url: '/script_stats',
                type:'GET',
                success: function(result) {
                    data = JSON.parse(result)
                    $("#mbuffer").text(data.mbuffer)
                    $("#rbuffer").text(data.rbuffer)
                    $("#ismotion").text(data.motion)
                }
             });
}





setInterval(function() {console.log('Stats'); update_system_values();},3000);


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/*async function demo() {
  console.log('Taking a break...');
  await sleep(2000);
  console.log('Two second later');
}*/

