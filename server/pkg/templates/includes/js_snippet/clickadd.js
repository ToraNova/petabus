var popup = L.popup();
function onMapClick(e) {
  popup
    .setLatLng(e.latlng)
    .setContent("Adding point " + e.latlng.toString())
    .openOn(mmap);
    var json_send = {
      "lati":e.latlng.lat.toString(),
      "long":e.latlng.lng.toString()
    }
    socket.emit('pointAdd',json_send)
}
mmap.on('click', onMapClick);
