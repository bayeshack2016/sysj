$(document).ready(function() {
  var $countySelect = $('#county_select');
  var $monthSelect = $('#month_select');
  var $opacitySelect = $('#opacity_select');
  var $radiusSelect = $('#radius_select');
  var $map = $('#map');

  var $countyLink = $('#county_link');
  var $radiance = $('#county_radiance');
  var $frac = $('#county_fraction');
  var $pop = $('#county_pop');
  var $income = $('#county_income');
  var $pce = $('#county_pce');
  var $gdp = $('#county_gdp');

  var initial_county = 'San Francisco, California';
  // center of sf
  var initial_center = {
    lat: 37.791666369,
    lng: -122.4374995395,
  };
  var initial_zoom = 12;

  var special_counties = {
    'San Francisco, California': true,
    'Philadelphia, Pennsylvania': true,
    'New York, New York': true,
    'McKenzie, North Dakota': true,
    'Williams, North Dakota': true,
    'King, Texas': true,
    'Loving, Texas': true,
    'Austin, Texas': true,
    'San Diego, California': true,
    'Los Angeles, California': true,
    'Sumter, Florida': true,
  };

  // get list of counties, and create select menu
  function initCounties(cb) {
    $.get('/counties', function(data) {
      $countySelect.empty();

      // special counties
      data.counties.forEach(function(county) {
        if (special_counties[county]) {
          $countySelect.append(
            $('<option>').text(county).val(county)
              .attr('selected', (county.indexOf(initial_county) > -1))
          );
        }
      });

      $countySelect.append(
        $('<option>')
          .text('-------------------------------------')
          .attr('disabled', true)
      );

      // all counties
      data.counties.forEach(function(county) {
        $countySelect.append(
          $('<option>').text(county).val(county)
        );
      });

      $countySelect.change(function() {
        redrawMap();
      });

      cb();
    });
  }

  // get list of months, and create select menu
  function initMonths(cb) {
    $.get('/months', function(data) {
      $monthSelect.empty();

      data.months.forEach(function(month) {
        $monthSelect.append(
          $('<option>').text(month).val(month)
        );
      });

      $monthSelect.change(function() {
        redrawMap();
      });

      cb();
    });
  }

  // get mapping from states to state codes
  // (needs to only happen once)
  var state_code_map;
  function getStateCodeMap(cb) {
    $.get('/state_code_map', function(data) {
      state_code_map = data.state_code_map;
      cb();
    });
  }

  // cache from (county, month) pairs to a heatmap
  var heatmapCache = {};
  // gathers the data for a given county and month
  // creates a heat map using the Google maps API
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

        var minimum_radiance = d3.min(data.points, function(p) {
          return p.radiance;
        })
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
        var info = {
          heatmap: heatmap,
          bounds: data.bounds,
          radiance: radiance,
        };
        heatmapCache[key] = info;
        return cb(info);
      }
    );
  }

  // main google maps map, on top of which heat maps are overlayed
  var mainMap = new google.maps.Map($map[0], {
    zoom: initial_zoom,
    center: initial_center,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });
  var curHeatmap;

  // set the main map to contain the bounds
  function reset_zoom(bounds) {
    mainMap.fitBounds(new google.maps.LatLngBounds(
      new google.maps.LatLng(bounds.lat.min, bounds.lng.min),
      new google.maps.LatLng(bounds.lat.max, bounds.lng.max)
    ));
  }

  // set the heat map to have a certain radius
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

  // updates data for a county:
  // - tries to grab data from the server
  //     - fraction of county lit
  //     - population
  //     - gdp
  //     - income
  //     - personal consumption expenditures
  // - links to datausa.io
  function updateCounty(cb) {
    var county = $countySelect.val();
    var month = $monthSelect.val();

    var parts = county.split(',');
    var linkStr = 'http://datausa.io/profile/geo/';
    linkStr += parts[0].replace(/\s/, '-')      + '-';
    linkStr += state_code_map[parts[1].trim()] + '/';
    linkStr = linkStr.toLowerCase();
    $countyLink.attr('href', linkStr);

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

      if (data.info['frac']) {
        $frac.text(Math.round(data.info['frac'] * 100) + '%');
      } else {
        $frac.text('Unavailable');
      }

      if (data.info['pce']) {
        $pce.text('$' + data.info['pce'].toLocaleString());
      } else {
        $pce.text('Unavailable');
      }

      return cb();
    });
  }

  // redraw the map according to current selections
  function redrawMap() {
    updateCounty(function() {
      var county = $countySelect.val();
      var month = $monthSelect.val();
      getHeatmap(county, month, function(info) {
        mainMap.setCenter({
          lng: (info.bounds.lng.max + info.bounds.lng.min) / 2,
          lat: (info.bounds.lat.max + info.bounds.lat.min) / 2,
        });
        curHeatmap = info.heatmap;
        $radiance.text(info.radiance.toLocaleString());
        reset_zoom(info.bounds);
        $opacitySelect.change();
        $radiusSelect.change();
      });
    });
  }

  // initialize everything!
  initCounties(function() {
    initMonths(function() {
      getStateCodeMap(function() {
        redrawMap();
      });
    });
  });

});
