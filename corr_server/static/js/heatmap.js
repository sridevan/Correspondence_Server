/////////////////////////////////////////////////////////////////////////////////////////

  (function() {
  /**
   * Decimal adjustment of a number.
   *
   * @param {String}  type  The type of adjustment.
   * @param {Number}  value The number.
   * @param {Integer} exp   The exponent (the 10 logarithm of the adjustment base).
   * @returns {Number} The adjusted value.
   */
  function decimalAdjust(type, value, exp) {
    // If the exp is undefined or zero...
    if (typeof exp === 'undefined' || +exp === 0) {
      return Math[type](value);
    }
    value = +value;
    exp = +exp;
    // If the value is not a number or the exp is not an integer...
    if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0)) {
      return NaN;
    }
    // Shift
    value = value.toString().split('e');
    value = Math[type](+(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp)));
    // Shift back
    value = value.toString().split('e');
    return +(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp));
    }

    // Decimal round
    if (!Math.round10) {
      Math.round10 = function(value, exp) {
        return decimalAdjust('round', value, exp);
      };
    }
    // Decimal floor
    if (!Math.floor10) {
      Math.floor10 = function(value, exp) {
        return decimalAdjust('floor', value, exp);
      };
    }
    // Decimal ceil
    if (!Math.ceil10) {
      Math.ceil10 = function(value, exp) {
        return decimalAdjust('ceil', value, exp);
      };
    }
  })();

  /*
  Programatically generate the gradient for the legend
  this creates an array of [pct, colour] pairs as stop
  values for legend
  */
  function linspace(start, end, n) {
        var out = [];
        var delta = (end - start) / (n - 1);

        var i = 0;
        while(i < (n - 1)) {
          out.push(start + (i * delta));
          i++;
        }

        out.push(end);
        return out;
      }

  function formatAnnotation(arr, chain, order) {
    var annotation_str =    'Order: ' + order + '\n' + '\n' +
                            'IFE: ' + chain + '\n' + '\n' +
                            'Description: ' + arr[String(chain)]['desc'] + '\n' + '\n' +
                            'Functional State: ' + arr[String(chain)]['rs'] + '\n' + '\n' +
                            'Method: ' + arr[String(chain)]['method'] + ' (' + arr[String(chain)]['res'] + ' Angstroms)' + '\n' + '\n' +
                            'PI: ' + arr[String(chain)]['PI'] + ' (' + arr[String(chain)]['pub_year'] + ')' + '\n' + '\n' +
                            'SSU Head Rotation: ' + + arr[String(chain)]['chr'] + '\n' + '\n' +
                            'Intersubunit Rotation: ' + + arr[String(chain)]['cir'] + '\n' + '\n' +
                            'tRNA Occupancy: ' + arr[String(chain)]['to'] + '\n' + '\n' +
                            'Factor bound: ' + arr[String(chain)]['fb'] + '\n' + '\n' +
                            'Ligand bound: ' + arr[String(chain)]['lb'];

    return annotation_str
  }
  // Viridis color list
  var viridisColor = ["#440154","#440256","#450457","#450559","#46075a","#46085c","#460a5d","#460b5e","#470d60","#470e61","#471063","#471164","#471365","#481467","#481668","#481769","#48186a","#481a6c","#481b6d","#481c6e","#481d6f","#481f70","#482071","#482173","#482374","#482475","#482576","#482677","#482878","#482979","#472a7a","#472c7a","#472d7b","#472e7c","#472f7d","#46307e","#46327e","#46337f","#463480","#453581","#453781","#453882","#443983","#443a83","#443b84","#433d84","#433e85","#423f85","#424086","#424186","#414287","#414487","#404588","#404688","#3f4788","#3f4889","#3e4989","#3e4a89","#3e4c8a","#3d4d8a","#3d4e8a","#3c4f8a","#3c508b","#3b518b","#3b528b","#3a538b","#3a548c","#39558c","#39568c","#38588c","#38598c","#375a8c","#375b8d","#365c8d","#365d8d","#355e8d","#355f8d","#34608d","#34618d","#33628d","#33638d","#32648e","#32658e","#31668e","#31678e","#31688e","#30698e","#306a8e","#2f6b8e","#2f6c8e","#2e6d8e","#2e6e8e","#2e6f8e","#2d708e","#2d718e","#2c718e","#2c728e","#2c738e","#2b748e","#2b758e","#2a768e","#2a778e","#2a788e","#29798e","#297a8e","#297b8e","#287c8e","#287d8e","#277e8e","#277f8e","#27808e","#26818e","#26828e","#26828e","#25838e","#25848e","#25858e","#24868e","#24878e","#23888e","#23898e","#238a8d","#228b8d","#228c8d","#228d8d","#218e8d","#218f8d","#21908d","#21918c","#20928c","#20928c","#20938c","#1f948c","#1f958b","#1f968b","#1f978b","#1f988b","#1f998a","#1f9a8a","#1e9b8a","#1e9c89","#1e9d89","#1f9e89","#1f9f88","#1fa088","#1fa188","#1fa187","#1fa287","#20a386","#20a486","#21a585","#21a685","#22a785","#22a884","#23a983","#24aa83","#25ab82","#25ac82","#26ad81","#27ad81","#28ae80","#29af7f","#2ab07f","#2cb17e","#2db27d","#2eb37c","#2fb47c","#31b57b","#32b67a","#34b679","#35b779","#37b878","#38b977","#3aba76","#3bbb75","#3dbc74","#3fbc73","#40bd72","#42be71","#44bf70","#46c06f","#48c16e","#4ac16d","#4cc26c","#4ec36b","#50c46a","#52c569","#54c568","#56c667","#58c765","#5ac864","#5cc863","#5ec962","#60ca60","#63cb5f","#65cb5e","#67cc5c","#69cd5b","#6ccd5a","#6ece58","#70cf57","#73d056","#75d054","#77d153","#7ad151","#7cd250","#7fd34e","#81d34d","#84d44b","#86d549","#89d548","#8bd646","#8ed645","#90d743","#93d741","#95d840","#98d83e","#9bd93c","#9dd93b","#a0da39","#a2da37","#a5db36","#a8db34","#aadc32","#addc30","#b0dd2f","#b2dd2d","#b5de2b","#b8de29","#bade28","#bddf26","#c0df25","#c2df23","#c5e021","#c8e020","#cae11f","#cde11d","#d0e11c","#d2e21b","#d5e21a","#d8e219","#dae319","#dde318","#dfe318","#e2e418","#e5e419","#e7e419","#eae51a","#ece51b","#efe51c","#f1e51d","#f4e61e","#f6e620","#f8e621","#fbe723","#fde725"];

  // Functional States color labels
  var stateLabel = {'4U25|1|AA': '#FF0033', '6BY1|1|BA': '#000075', '4WWW|1|XA': '#FF6600', '5JC9|1|BA': '#FF6600', '6OG7|1|3': '#339933', '5J5B|1|BA': '#FF0033', '4V52|1|AA': '#FF0033', '4WF1|1|CA': '#FF0033', '4U27|1|AA': '#FF0033', '6OGF|1|3': '#339933', '5LZD|1|a': '#3300FF', '6ENF|1|a': '#3399FF', '6H4N|1|a': '#aaffc3', '5NWY|1|0': '#8B4513', '5J8A|1|BA': '#FF0033', '6SZS|1|a': '#3399FF', '3JA1|1|SA': '#991EFF', '3JBU|1|A': '#8B4513', '5JU8|1|AA': '#8B4513', '4V9O|1|FA': '#991EFF', '5L3P|1|a': '#808000', '5J91|1|BA': '#FF0033', '4U20|1|AA': '#FF0033', '5JC9|1|AA': '#FF6600', '4V55|1|AA': '#800000', '4U26|1|CA': '#FF0033', '3JBV|1|A': '#8B4513', '5KPS|1|27': '#808000', '4V57|1|CA': '#FF0033', '5WE6|1|a': '#3300FF', '5J7L|1|BA': '#FF0033', '4U1U|1|AA': '#FF0033', '4V9C|1|AA': '#CDAD00', '6C4I|1|a': '#3399FF', '4V7T|1|CA': '#FF6600', '4V9P|1|DA': '#991EFF', '4V6C|1|AA': '#FF6600', '4V6E|1|CA': '#CDAD00', '6ORE|1|2': '#339933', '4V9D|1|AA': '#800000', '4V64|1|AA': '#FF0033', '6ORL|1|2': '#339933', '5MGP|1|a': '#3399FF', '6OSQ|1|2': '#339933', '3J9Z|1|SA': '#991EFF', '6OT3|1|2': '#339933', '5KCS|1|1a': '#bfef45', '4V4H|1|CA': '#FF0033', '4V56|1|CA': '#FF0033', '6OUO|1|2': '#339933', '4V54|1|AA': '#800000', '4WOI|1|AA': '#CDAD00', '3JCD|1|a': '#fffac8', '3JCE|1|a': '#fffac8', '5O2R|1|a': '#8B4513', '4V7S|1|AA': '#FF0033', '3J9Y|1|a': '#bfef45', '5J88|1|BA': '#FF6600', '4V4Q|1|CA': '#FF6600', '4V9O|1|DA': '#991EFF', '5MDZ|1|2': '#CDAD00', '6O9J|1|a': '#469990', '4V55|1|CA': '#800000', '6BY1|1|AA': '#000075', '6OSK|1|2': '#339933', '4V9O|1|BA': '#991EFF', '5KCR|1|1a': '#CDAD00', '4V7V|1|AA': '#FF0033', '6OFX|1|3': '#339933', '4V7T|1|AA': '#FF0033', '4V57|1|AA': '#FF0033', '3JCJ|1|g': '#469990', '4WWW|1|QA': '#FF0033', '4V5B|1|BA': '#FF6600', '4V9P|1|FA': '#991EFF', '5UYM|1|A': '#3300FF', '4V4H|1|AA': '#FF0033', '4V50|1|AA': '#CDAD00', '5U4J|1|a': '#3399FF', '5J91|1|AA': '#FF0033', '6GXM|1|a': '#339933', '4V7U|1|CA': '#FF6600', '5J88|1|AA': '#FF6600', '4YBB|1|AA': '#FF6600', '5WFK|1|a': '#3300FF', '5UYN|1|A': '#3300FF', '5UYQ|1|A': '#3300FF', '4V54|1|CA': '#800000', '5UYK|1|A': '#3300FF', '4V64|1|CA': '#FF0033', '5MDV|1|2': '#3399FF', '4V4Q|1|AA': '#FF6600', '4U1V|1|AA': '#FF0033', '5KPX|1|26': '#808000', '5WE4|1|a': '#3300FF', '5J7L|1|AA': '#FF0033', '4V56|1|AA': '#FF0033', '4V7S|1|CA': '#FF6600', '5WDT|1|a': '#3300FF', '6O9K|1|a': '#469990', '4U20|1|CA': '#FF0033', '4U26|1|AA': '#FF0033', '4V6D|1|AA': '#CDAD00', '5KPW|1|26': '#808000', '6DNC|1|A': '#339933', '5UYP|1|A': '#3300FF', '4V9D|1|BA': '#339933', '4V6D|1|CA': '#CDAD00', '4U24|1|CA': '#FF0033', '4V6C|1|CA': '#FF6600', '5J5B|1|AA': '#FF0033', '4V53|1|CA': '#FF0033', '5JTE|1|AA': '#8B4513', '5WF0|1|a': '#3300FF', '4V9P|1|HA': '#991EFF', '6OGI|1|3': '#339933', '6Q97|1|2': '#3399FF', '4V7V|1|CA': '#FF6600', '6ENU|1|a': '#3399FF', '5U9G|1|A': '#3399FF', '4V9P|1|BA': '#991EFF', '5J8A|1|AA': '#FF0033', '4U25|1|CA': '#FF0033', '4V9O|1|HA': '#991EFF', '6Q9A|1|2': '#3399FF', '6ENJ|1|a': '#3399FF', '5MDY|1|2': '#3399FF', '4V50|1|CA': '#CDAD00', '4U27|1|CA': '#FF0033', '4V52|1|CA': '#FF0033', '4WF1|1|AA': '#FF6600', '6GXN|1|a': '#339933', '4V7U|1|AA': '#FF0033', '5IT8|1|AA': '#FF6600', '5AFI|1|a': '#3300FF', '4U1V|1|CA': '#FF0033', '5IQR|1|2': '#808000', '5LZA|1|a': '#CDAD00', '4V89|1|AA': '#339933', '4V5B|1|DA': '#FF6600', '5U4I|1|a': '#3399FF', '4V85|1|AA': '#339933', '4YBB|1|BA': '#FF6600', '4U24|1|AA': '#FF0033', '5UYL|1|A': '#3300FF', '6BU8|1|A': '#CDAD00', '5NP6|1|D': '#ffd8b1', '4U1U|1|CA': '#FF0033', '4V9C|1|CA': '#800000', '4V53|1|AA': '#FF0033', '5WFS|1|a': '#3300FF', '6GXO|1|a': '#339933', '5IT8|1|BA': '#FF6600', '4V6E|1|AA': '#CDAD00', '5H5U|1|h': '#3399FF', '6NQB|1|A': '#fabebe', '5MDW|1|2': '#3399FF', '4WOI|1|DA': '#CDAD00', '5U9F|1|A': '#3399FF', '6GWT|1|a': '#339933'}
//////////////////////////////////////////////////////////////////////////////////////

  // get the unique values of the ife's in an ordered list
  var lookup = {};
  var items = data;
  var ife_nr = [];

  for (var item, i = 0; item = items[i++];) {
      var name = item.ife1;

      if (!(name in lookup)) {
        lookup[name] = 1;
        ife_nr.push(name);
      }
  }

  // Calculate the size of heatmap array
  ife_nr_size = ife_nr.length;

  // Set the dimensions of the canvas
  var margin = {top: 0, right: 10, bottom: 70, left: 90},
    width = 400,
    height = 400,
    gridSize = Math.round10((width / ife_nr_size), -1),
    legendElementWidth = gridSize * ife_nr_size,
    new_width = gridSize * ife_nr_size;
    if (new_width > width) {
      width = new_width;
      height = new_width;
    }

      // the unary operator (+) converts a numeric string into a number
      data.forEach(function(d) {
        ife1 = d.ife1;
        ife1_index = +d.ife1_index;
        ife2 = d.ife2;
        ife2_index = +d.ife2_index;
        discrepancy = +d.discrepancy;
      });

      var domainMax = d3.max(data, function(d) {return +d.discrepancy;});
      var domainMin = d3.min(data, function(d) {return +d.discrepancy;});


      var colorScale = d3.scaleLinear()
          .domain(linspace(domainMin, domainMax, viridisColor.length))
          .range(viridisColor)

      // Set the svg container
      var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // Create the paired elements
      var heatMap = svg.selectAll(".ife2_index")
        .data(data, function(d) { return d.ife1_index+':'+d.ife2_index; });

      // Draw the grids to make the heatmap
      heatMap.enter().append("rect")
        .attr("x", function(d) { return d.ife2_index * gridSize; })
        .attr("y", function(d) { return d.ife1_index * gridSize; })
        .attr("class", "bordered")
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("fill", function(d) {
          if ((d.ife1 != d.ife2) && (d.discrepancy == null)) {
              return "#C0C0C0";
          } else if (d.ife1 == d.ife2) {
              var label = stateLabel[d.ife1];
              return label;
          } else {
              return colorScale(d.discrepancy);
            }
        })
        .on("click", function(d) {
          
          var row = d.ife1_index;
          var column = d.ife2_index;

          // superimpose instances above diagonal
          if (row < column) {
              for (i = 1; i < ife_nr_size; i++) {
               $.jmolTools.models[i].hideAll();
              }

              for (i = row; i <= column; i++) {
               $('#' + i).jmolShow();
              }
          
          // display diagonal instance
          } else if (row == column) {
              for (i = 1; i < ife_nr_size; i++) {
               $.jmolTools.models[i].hideAll();
              }

              $('#' + row).jmolShow();
          
          // sumperimpose instances below diagonal
          } else if (row > column) {
              for (i = 1; i < ife_nr_size; i++) {
               $.jmolTools.models[i].hideAll();
              }

              $('#' + row).jmolShow();
              $('#' + column).jmolShow();
          }
        })
        .append("title")
        .text(function(d) {
          var formatDecimal = d3.format(",.4f")
          if (d.ife1 == d.ife2) {
            var row = d.ife1_index + 1;
            var label = stateLabel[d.ife1]
            var annotation = formatAnnotation(annotationEc, d.ife1, row)
            return annotation
            // return d.ife1 + ':' + d.ife2 + ' = ' + formatDecimal(d.discrepancy);
          } else if ((d.ife1 != d.ife2) && (d.discrepancy == null)) {
              return 'No discrepancy value is computed between ' + d.ife1 + ' and ' + d.ife2;
          } else {
              return d.ife1 + ':' + d.ife2 + ' = ' + formatDecimal(d.discrepancy);
          }
        });

      heatMap.exit().remove();

      // append gradient bar
      var defs = svg.append('defs')
      //.attr("transform", "translate(" + (width) + "," + (height+50) + ")");

      //Append a linearGradient element to the defs and give it a unique id
      var linearGradient = defs.append("linearGradient")
        .attr("id", "linear-gradient");

      //Horizontal gradient
      linearGradient
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "0%");

      // programatically generate the gradient for the legend
      // this creates an array of [pct, colour] pairs as stop
      // values for legend
      // Adapted from: https://gist.github.com/starcalibre/6cccfa843ed254aa0a0d
      var pct = linspace(0, 100, viridisColor.length).map(function(d) {
        return Math.round(d) + '%';
      });

      var colourPct = d3.zip(pct, viridisColor);

      colourPct.forEach(function(d) {
        linearGradient.append('stop')
          .attr('offset', d[0])
          .attr('stop-color', d[1])
          .attr('stop-opacity', 1);
      });

      //Draw the rectangle and fill with gradient
      svg.append("rect")
        .attr('x1', 0)
        .attr('y1', height)
        .attr("width", width)
        .attr("height", 15)
        .attr("transform", "translate(" + 0 + "," + (height + 5) + ")")
        .style("fill", "url(#linear-gradient)");

      var legendScale = d3.scaleLinear()
          .domain([domainMin, domainMax])
          .range([0, width])

      // create an axis for the legend
      var legendAxis = d3.axisBottom()
        .scale(legendScale)
        .ticks(5)
        .tickFormat(d3.format(".2f"));

      svg.append("g")
        .attr("class", "legend axis")
        //.attr("height", 80)
        .text('Discrepancy')
        .attr("transform", "translate(" + 0 + "," + (height + 17) + ")")
        .call(legendAxis);

      function updateColoring () {
          var color = null;
          console.log('Hello world');
      }

