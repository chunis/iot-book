
let map;
let first_zoom = true;
let node_id = 1;
let markerLayer;
let infoWindow;
const port = 3454;

function initMap() {
  var center = new TMap.LatLng(36.984120, 110.307484);
  map = new TMap.Map(document.getElementById('container'), {
    center: center,
    zoom: 5,
    pitch: 0,
    rotation: 0
  });
}

// Create WebSocket connection.
//const socket = new WebSocket(`ws://192.168.1.202:${port}`);
const socket = new WebSocket('ws://localhost:3454');

// Connection opened; do nothing.
socket.addEventListener('open', (event) => { });

// Listen for messages
socket.addEventListener('message', processMessage);


let icons_path = 'icons/';
function floor_to_icon_name(which_floor) {
  let name = '';
  let floor = parseInt(which_floor);

  if(floor == '')
    //name = icons_path + 'ERR.ico';
    name = icons_path + 'LTM5.ico';
  else if(floor > 39)
    name = icons_path + 'BGT39.ico';
  else if(floor < -5)
    name = icons_path + 'LTM5.ico';
  else if(floor < 0)
    name = `${icons_path}FM${Math.abs(floor)}.ico`;
  else
    name = `${icons_path}F${floor}.ico`;

  return name;
}

function style_from_node_name(node_name) {
  return {
    "myStyle": new TMap.MarkerStyle({
      "width": 32,
      "height": 32,
      "src": node_name,
      "anchor": { x: 32, y: 32 }
    })};
}

function processMessage(event) {
  console.log('Message from server ', event.data);
  let json_str = JSON.parse(event.data);
  let name = json_str.name;
  let lat = json_str.lat;
  let lon = json_str.lon;
  let deveui = json_str.name.split(' ')[0];
  let time = json_str.time;
  let which_floor = json_str.which_floor.split('(')[0];
  let node_name = floor_to_icon_name(which_floor);

  if(first_zoom){
    console.log("1st time. node name:", node_name);
    map.setCenter(new TMap.LatLng(lat, lon));
    map.setZoom(13);
    first_zoom = false;

    let map_styles = style_from_node_name(node_name);
    console.log(map_styles.myStyle.src);

    markerLayer = new TMap.MultiMarker({
      map: map,
      styles: map_styles,
      geometries:
      [
        {
          "id": node_id,
          "styleId": 'myStyle',
          "position": new TMap.LatLng(lat, lon),
          "properties": {
              "node": deveui,
              "time": time,
              "which_floor": which_floor ? which_floor : "(unknown)"
          }
        }
      ]
    });

    infoWindow = new TMap.InfoWindow({
      map: map,
      position: new TMap.LatLng(39.984104,116.307503),
      offset: { x: -16, y: -32 }
    });
    infoWindow.close();
    markerLayer.on("click", function (evt) {
        infoWindow.open();
        infoWindow.setPosition(evt.geometry.position);
        infoWindow.setContent(`#${evt.geometry.id}: (${evt.geometry.properties.node})<br>
          time: ${evt.geometry.properties.time}<br>
          latitude/longitude: ${evt.geometry.position.toString()}<br>
          @floor: ${evt.geometry.properties.which_floor}`);
        //console.log(evt);
    });
  } else {
    console.log("2nd time. node name:", node_name);
    infoWindow.close();
    markerLayer.remove(node_id);
    node_id++;

    let newStyle = style_from_node_name(node_name);
    markerLayer.setStyles({"myStyle": newStyle["myStyle"]});
    markerLayer.updateGeometries(
    [
      {
        "id": node_id,
        "styleId": 'myStyle',
        "position": new TMap.LatLng(lat, lon),
        "properties": {
          "node": deveui,
          "time": time,
          "which_floor": which_floor ? which_floor : "(unknown)"
        }
      }
    ]);
  }

}
