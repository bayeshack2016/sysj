$(document).ready(function() {
  var $countySelect = $('#county_select');
  var $monthSelect = $('#month_select');
  var $opacitySelect = $('#opacity_select');
  var $radiusSelect = $('#radius_select');
  var $map = $('#map');
  var $countyStats = $('#county_stats');
  var $countyStatsNone = $('#county_stats_none');

  var $radiance = $('#county_radiance');
  var $pop = $('#county_pop');
  var $income = $('#county_income');
  var $pce = $('#county_pce');
  var $gdp = $('#county_gdp');

  var initial_county = 'San Francisco';
  // center of sf
  var initial_center = {
    lat: 37.791666369,
    lng: -122.4374995395,
  };
  var initial_zoom = 12;


  function getCounties(cb) {
    $.get('/counties', function(data) {
      $countySelect.empty();
      data.counties.forEach(function(county) {
        $countySelect.append(
          $('<option>')
            .text(county)
            .val(county)
            .attr('selected', (county.indexOf(initial_county) > -1))
        );
      });
      cb();
    });
  }

  function getMonths(cb) {
    $.get('/months', function(data) {
      $monthSelect.empty();
      data.months.forEach(function(month) {
        $monthSelect.append(
          $('<option>').text(month).val(month)
        );
      });
      cb();
    });
  }

  var heatmapCache = {};
  function getHeatmap(county, month, cb) {
    var key = county + '::' + month;
    if (curHeatmap) {
      curHeatmap.setMap(null);
    }
    if (heatmapCache[key]) {
      var info = heatmapCache[key];
      info.heatmap.setMap(mainMap);
      return cb(info);
    }
    $.get(
      '/viirs_data',
      {county: county, month: month},
      function(data) {

        var minimum_radiance = Math.min.apply(0,
          data.points.map(function(x) { return x.radiance; })
        );
        var min_threshold = minimum_radiance + 5;

        var total_radiance = 0;
        var dataPoints = data.points.map(function(x) {
          total_radiance += x.radiance;
          return {
            location: new google.maps.LatLng(x.lat, x.lng),
            weight: Math.max(x.radiance - min_threshold, 0),
          };
        });

        var radiance = total_radiance / data.points.length;

        var heatmap = new google.maps.visualization.HeatmapLayer({
          data: dataPoints,
          map: mainMap
        });
        var center = {
          lng: (data.bounds.lng.min + data.bounds.lng.max) / 2,
          lat: (data.bounds.lat.min + data.bounds.lat.max) / 2,
        };
        var info = {
          heatmap: heatmap,
          center: center,
          radiance: radiance,
        };
        heatmapCache[key] = info;
        return cb(info);
      }
    );
  }

  var mainMap = new google.maps.Map($map[0], {
    zoom: initial_zoom,
    center: initial_center,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });
  var curHeatmap;

  function reset_radius() {
    var radius =
        0.005 * $radiusSelect.val() *
        Math.pow(2, mainMap.getZoom());
    curHeatmap && curHeatmap.set('radius', radius);
  }

  mainMap.addListener('zoom_changed', reset_radius);
  $radiusSelect.on('input change', reset_radius);

  $opacitySelect.on('input change', function() {
    curHeatmap && curHeatmap.set('opacity', $opacitySelect.val());
  });

  function initMap() {
    var county = $countySelect.val();
    var month = $monthSelect.val();
    $.get('/county_info', {county: county, month: month}, function(data) {

      if (data.info['pop']) {
        $pop.text(data.info['pop'].toLocaleString());
      } else {
        $pop.text('Unavailable');
      }

      if (data.info['gdp']) {
        $gdp.text('$' + data.info['gdp'].toLocaleString());
      } else {
        $gdp.text('Unavailable');
      }

      if (data.info['income']) {
        $income.text('$' + data.info['income'].toLocaleString());
      } else {
        $income.text('Unavailable');
      }

      if (data.info['pce']) {
        $pce.text('$' + data.info['pce'].toLocaleString());
      } else {
        $pce.text('Unavailable');
      }

      if (data.info) {
        $countyStats.removeClass('hidden');
        $countyStatsNone.addClass('hidden');
      } else {
        $countyStats.addClass('hidden');
        $countyStatsNone.removeClass('hidden');
      }

      getHeatmap(county, month, function(info) {
        mainMap.setCenter(info.center);
        curHeatmap = info.heatmap;
        $radiance.text(info.radiance.toLocaleString());
        $opacitySelect.change();
        $radiusSelect.change();
      });
    });
  }


  getCounties(function() {
    getMonths(function() {
      initMap();
    });
  });

  $countySelect.change(function() {
    initMap();
  });

  $monthSelect.change(function() {
    initMap();
  });
});
