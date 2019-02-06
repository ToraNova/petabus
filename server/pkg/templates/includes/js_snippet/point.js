var namespace = '/geopoint'
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace); //persistent
socket.on('connect', function() {
    console.log("pointdisp_test connected...")
});

setInterval(timercallback, 5000);
var pointArray = new Array();
socket.on('point_data', function(msg) {
  msg.points.forEach(function proc(element, index){
    var test = findPoint(element,pointArray); //find the element in the array
    if( test != -1 ){
      //element already in
      //console.log("Point edited on map",element) //DEBUGGING USE ONLY
      pointArray[test][0] = element;
      pointArray[test][1].setLatLng([element.lati,element.long]);
    }else{
      //console.log("Point added to map",element) //DEBUGGING USE ONLY
      pointArray.push([element,L.marker([element.lati,element.long]).addTo(mmap)
        .bindPopup("<b>{0}</b><br/>{1}".format(element.route,element.id))])
    }
  });
});

String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

function findPoint(point,array){
  //checks if a point element is in the point array by comparing
  //the ID
  var out = -1;
  array.forEach(function proc(element, index){
    if(element[0].id == point.id){
      out = index;
      return;
    }
  });
  return out;
}

function timercallback() {
  socket.emit('update');
}
