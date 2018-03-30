var player_classes = ['fa-play','fa-pause'];

function video_player_control(self){
  var active_classes = Array.from(self.classList);
  
  var active = null;
  active_classes.forEach(klass => (player_classes.includes(klass)) ? active = klass : false );
  
  var new_active  = null;
  player_classes.forEach(klass => klass !== active ? new_active = klass : false);
  
  self.classList.remove(active);
  self.classList.add(new_active);
}
