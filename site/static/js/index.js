
function initMap() {
  var county = $countySelect.val();
  console.log('initializing county', county);
  $.get('/viirs_data', {county: county}, function(data) {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 13,
      center: {lat: 37.775, lng: -122.434},
      mapTypeId: google.maps.MapTypeId.SATELLITE
    });

    var dataPoints = data.points.map(function(x) {
      return new google.maps.LatLng(x.lat, x.lng);
    });

    var heatmap = new google.maps.visualization.HeatmapLayer({
      data: dataPoints,
      map: map
    });

    function toggleHeatmap() {
      heatmap.setMap(heatmap.getMap() ? null : map);
    }

    function changeGradient() {
      var gradient = [
        'rgba(0, 255, 255, 0)',
        'rgba(0, 255, 255, 1)',
        'rgba(0, 191, 255, 1)',
        'rgba(0, 127, 255, 1)',
        'rgba(0, 63, 255, 1)',
        'rgba(0, 0, 255, 1)',
        'rgba(0, 0, 223, 1)',
        'rgba(0, 0, 191, 1)',
        'rgba(0, 0, 159, 1)',
        'rgba(0, 0, 127, 1)',
        'rgba(63, 0, 91, 1)',
        'rgba(127, 0, 63, 1)',
        'rgba(191, 0, 31, 1)',
        'rgba(255, 0, 0, 1)'
      ];
      heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
    }

    function changeRadius() {
      heatmap.set('radius', heatmap.get('radius') ? null : 20);
    }

    function changeOpacity() {
      heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
    }
  });
}

$(document).ready(function() {
  $countySelect = $('#county_select');

  $.get('/counties', function(data) {
    $countySelect.empty();
    data.counties.forEach(function(county) {
      $countySelect.append(
        $('<option>').text(county).val(county)
      );
    });
    initMap();
  });

  $countySelect.change(function() {
    initMap();
  });
});
