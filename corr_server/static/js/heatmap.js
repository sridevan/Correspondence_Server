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

  var authorLabel = {'4U25|1|AA': '#FF0033', '6BY1|1|BA': '#800000', '4WWW|1|XA': '#808000', '5JC9|1|BA': '#3300FF', '6OG7|1|3': '#FF6600', '5AFI|1|a': '#469990', '4V52|1|AA': '#FF0033', '4WF1|1|CA': '#991EFF', '4V89|1|AA': '#800000', '6OGF|1|3': '#FF6600', '5LZD|1|a': '#469990', '6ENF|1|a': '#3399FF', '6H4N|1|a': '#3399FF', '5NWY|1|0': '#FFFFFF', '5J8A|1|BA': '#3300FF', '6ORE|1|2': '#339933', '4V5B|1|BA': '#fabebe', '3JA1|1|SA': '#339933', '3JBU|1|A': '#f032e6', '5JU8|1|AA': '#3399FF', '4V9O|1|FA': '#FF0033', '5L3P|1|a': '#3399FF', '5J91|1|BA': '#3300FF', '4U20|1|AA': '#FF0033', '4V55|1|AA': '#FF0033', '4U26|1|CA': '#FF0033', '3JBV|1|A': '#f032e6', '5KPS|1|27': '#FF6600', '4V57|1|CA': '#FF0033', '5J7L|1|BA': '#3300FF', '4U1U|1|AA': '#FF0033', '4V9C|1|AA': '#991EFF', '6C4I|1|a': '#ffd8b1', '4V7T|1|CA': '#FF0033', '4V9P|1|DA': '#FF0033', '4V6C|1|AA': '#FF0033', '4V6E|1|CA': '#FF0033', '5J91|1|AA': '#3300FF', '4V9D|1|AA': '#FF0033', '4V64|1|AA': '#8B4513', '6ORL|1|2': '#339933', '5MGP|1|a': '#3399FF', '6OSQ|1|2': '#339933', '3J9Z|1|SA': '#339933', '6OT3|1|2': '#339933', '5KCS|1|1a': '#3399FF', '4V4H|1|CA': '#000075', '4V56|1|CA': '#FF0033', '6OUO|1|2': '#339933', '4V54|1|AA': '#FF0033', '4WOI|1|AA': '#991EFF', '3JCD|1|a': '#bfef45', '3JCE|1|a': '#bfef45', '5O2R|1|a': '#808000', '4V7S|1|AA': '#FF0033', '3J9Y|1|a': '#3399FF', '5J88|1|BA': '#3300FF', '4V4Q|1|CA': '#FF0033', '4V9O|1|DA': '#FF0033', '5MDZ|1|2': '#CDAD00', '6O9J|1|a': '#339933', '4V55|1|CA': '#FF0033', '6BY1|1|AA': '#800000', '6OSK|1|2': '#339933', '6ENU|1|a': '#3399FF', '5MDV|1|2': '#CDAD00', '5KCR|1|1a': '#3399FF', '5J88|1|AA': '#3300FF', '6OFX|1|3': '#FF6600', '4V7T|1|AA': '#FF0033', '4V57|1|AA': '#FF0033', '5NP6|1|D': '#000000', '4WWW|1|QA': '#808000', '6SZS|1|a': '#A9A9A9', '4V9P|1|FA': '#FF0033', '5UYM|1|A': '#FF6600', '5KPX|1|26': '#FF6600', '4V50|1|AA': '#8B4513', '4U27|1|AA': '#FF0033', '5WE6|1|a': '#339933', '6GXM|1|a': '#3399FF', '5J7L|1|AA': '#3300FF', '4V7V|1|AA': '#FF0033', '4YBB|1|AA': '#FF0033', '5WFK|1|a': '#339933', '5UYN|1|A': '#FF6600', '5UYQ|1|A': '#FF6600', '4V54|1|CA': '#FF0033', '5UYK|1|A': '#FF6600', '4V64|1|CA': '#8B4513', '4V9O|1|BA': '#FF0033', '4V4Q|1|AA': '#FF0033', '4U1V|1|AA': '#FF0033', '4V4H|1|AA': '#000075', '5WE4|1|a': '#339933', '4V7U|1|CA': '#FF0033', '4V56|1|AA': '#FF0033', '4V7S|1|CA': '#FF0033', '5WDT|1|a': '#339933', '6O9K|1|a': '#339933', '4U20|1|CA': '#FF0033', '4U26|1|AA': '#FF0033', '4V6D|1|AA': '#FF0033', '6DNC|1|A': '#FF6600', '5UYP|1|A': '#FF6600', '4V9D|1|BA': '#FF0033', '4V6D|1|CA': '#FF0033', '4U24|1|CA': '#FF0033', '5IT8|1|BA': '#3300FF', '5J5B|1|AA': '#3300FF', '4V53|1|CA': '#FF0033', '5JTE|1|AA': '#3399FF', '5WF0|1|a': '#339933', '4V9P|1|HA': '#FF0033', '6OGI|1|3': '#FF6600', '6Q97|1|2': '#CDAD00', '4V7V|1|CA': '#FF0033', '5WFS|1|a': '#339933', '5U9G|1|A': '#FF6600', '4V9P|1|BA': '#FF0033', '5H5U|1|h': '#fffac8', '4U25|1|CA': '#FF0033', '4V6C|1|CA': '#FF0033', '4V9O|1|HA': '#FF0033', '6Q9A|1|2': '#CDAD00', '6ENJ|1|a': '#3399FF', '5MDY|1|2': '#CDAD00', '4V50|1|CA': '#8B4513', '4U27|1|CA': '#FF0033', '4V52|1|CA': '#FF0033', '4WF1|1|AA': '#991EFF', '4V7U|1|AA': '#FF0033', '5IT8|1|AA': '#3300FF', '5J5B|1|BA': '#3300FF', '4U1V|1|CA': '#FF0033', '5IQR|1|2': '#CDAD00', '5LZA|1|a': '#469990', '5JC9|1|AA': '#3300FF', '4V5B|1|DA': '#fabebe', '5U4I|1|a': '#ffd8b1', '4V85|1|AA': '#800000', '4YBB|1|BA': '#FF0033', '4U24|1|AA': '#FF0033', '5UYL|1|A': '#FF6600', '6BU8|1|A': '#FF6600', '3JCJ|1|g': '#fffac8', '4U1U|1|CA': '#FF0033', '4V9C|1|CA': '#991EFF', '4V53|1|AA': '#FF0033', '5KPW|1|26': '#FF6600', '6GXO|1|a': '#3399FF', '6GXN|1|a': '#3399FF', '4V6E|1|AA': '#FF0033', '5J8A|1|AA': '#3300FF', '6NQB|1|A': '#aaffc3', '5MDW|1|2': '#CDAD00', '4WOI|1|DA': '#991EFF', '5U9F|1|A': '#FF6600', '6GWT|1|a': '#3399FF'}

  var plasmaColor = ["#0d0887","#110889","#17078b","#1b078d","#20068f","#240691","#2a0693","#300596","#340597","#3a049a","#3d049b","#43049e","#4903a0","#4b03a1","#5003a2","#5303a2","#5803a3","#5c03a3","#6103a4","#6603a5","#6903a5","#6e03a6","#7103a6","#7603a7","#7b03a8","#7d03a8","#8106a6","#8408a5","#880ba4","#8a0da2","#8e10a1","#93139f","#95149e","#99179c","#9c199b","#a01c99","#a41f98","#a72197","#a92395","#ac2693","#af2990","#b32d8d","#b52f8b","#b83388","#bb3587","#be3984","#c13b82","#c43f7f","#c8427c","#ca457a","#cc4778","#cd4976","#d04d74","#d25071","#d4536f","#d6566d","#d8596b","#da5c68","#dc5e67","#df6264","#e16561","#e36860","#e56b5d","#e66c5c","#e87059","#e97556","#eb7755","#ed7b52","#ee7e50","#f0824d","#f2864a","#f38948","#f58d46","#f69044","#f89441","#f89540","#f99a3e","#f99e3c","#f9a13a","#faa638","#faa936","#fbad34","#fbb131","#fbb430","#fcb92d","#fcbc2c","#fdc02a","#fdc328","#fcc728","#fbcc27","#fad026","#f9d526","#f8d925","#f7de25","#f5e324","#f4e723","#f3ec23","#f2f022","#f1f521","#f0f921"];

  var headRotation = {'4U25|1|AA': 11.1, '6BY1|1|BA': 1.1, '4WWW|1|XA': 8.4, '5JC9|1|BA': 7.8, '6OG7|1|3': 1.9, '5AFI|1|a': 0.2, '4V52|1|AA': 7.7, '4WF1|1|CA': 7.1, '4V89|1|AA': 15.0, '6OGF|1|3': 2.1, '5LZD|1|a': 0.4, '6ENF|1|a': 2.0, '6H4N|1|a': 1.7, '5NWY|1|0': 2.1, '5J8A|1|BA': 8.1, '6ORE|1|2': 2.2, '4V5B|1|BA': 6.5, '3JA1|1|SA': 5.9, '3JBU|1|A': 2.1, '5JU8|1|AA': 2.0, '4V9O|1|FA': 6.7, '5L3P|1|a': 2.5, '5J91|1|BA': 8.1, '4U20|1|AA': 11.0, '4V55|1|AA': 7.4, '4U26|1|CA': 7.7, '3JBV|1|A': 6.2, '5KPS|1|27': 2.3, '4V57|1|CA': 14.9, '5J7L|1|BA': 8.1, '4U1U|1|AA': 11.0, '4V9C|1|AA': 1.3, '6C4I|1|a': 2.3, '4V7T|1|CA': 8.3, '4V9P|1|DA': 9.8, '4V6C|1|AA': 11.2, '4V6E|1|CA': 2.7, '5J91|1|AA': 11.2, '4V9D|1|AA': 4.1, '4V64|1|AA': 7.5, '6ORL|1|2': 1.3, '5MGP|1|a': 2.2, '6OSQ|1|2': 1.6, '3J9Z|1|SA': 2.4, '6OT3|1|2': 2.0, '5KCS|1|1a': 2.5, '4V4H|1|CA': 15.7, '4V56|1|CA': 14.9, '6OUO|1|2': 2.0, '4V54|1|AA': 7.6, '4WOI|1|AA': 2.4, '3JCD|1|a': 2.0, '3JCE|1|a': 0.8, '5O2R|1|a': 1.4, '4V7S|1|AA': 11.1, '3J9Y|1|a': 2.5, '5J88|1|BA': 8.3, '4V4Q|1|CA': 15.7, '4V9O|1|DA': 7.8, '5MDZ|1|2': 2.0, '6O9J|1|a': 7.6, '4V55|1|CA': 15.3, '6BY1|1|AA': 1.2, '6OSK|1|2': 1.0, '6ENU|1|a': 1.8, '5MDV|1|2': 2.1, '5KCR|1|1a': 1.9, '5J88|1|AA': 11.3, '6OFX|1|3': 1.1, '4V7T|1|AA': 11.1, '4V57|1|AA': 7.5, '5NP6|1|D': 2.4, '4WWW|1|QA': 11.2, '6SZS|1|a': 1.9, '4V9P|1|FA': 11.8, '5UYM|1|A': 0.3, '5KPX|1|26': 1.1, '4V50|1|AA': 3.6, '4U27|1|AA': 11.0, '5WE6|1|a': 0.7, '6GXM|1|a': 2.4, '5J7L|1|AA': 11.2, '4V7V|1|AA': 11.0, '4YBB|1|AA': 11.2, '5WFK|1|a': 1.8, '5UYN|1|A': 2.2, '5UYQ|1|A': 1.0, '4V54|1|CA': 15.4, '5UYK|1|A': 2.2, '4V64|1|CA': 15.3, '4V9O|1|BA': 6.0, '4V4Q|1|AA': 7.6, '4U1V|1|AA': 10.7, '4V4H|1|AA': 7.5, '5WE4|1|a': 0.6, '4V7U|1|CA': 8.1, '4V56|1|AA': 7.2, '4V7S|1|CA': 8.2, '5WDT|1|a': 0.5, '6O9K|1|a': 2.6, '4U20|1|CA': 7.5, '4U26|1|AA': 11.3, '4V6D|1|AA': 1.5, '6DNC|1|A': 1.5, '5UYP|1|A': 2.4, '4V9D|1|BA': 1.5, '4V6D|1|CA': 3.6, '4U24|1|CA': 7.8, '5IT8|1|BA': 8.2, '5J5B|1|AA': 11.2, '4V53|1|CA': 15.4, '5JTE|1|AA': 1.8, '5WF0|1|a': 1.9, '4V9P|1|HA': 11.6, '6OGI|1|3': 7.4, '6Q97|1|2': 2.2, '4V7V|1|CA': 8.2, '5WFS|1|a': 0.9, '5U9G|1|A': 2.2, '4V9P|1|BA': 9.7, '5H5U|1|h': 2.4, '4U25|1|CA': 7.5, '4V6C|1|CA': 8.0, '4V9O|1|HA': 12.1, '6Q9A|1|2': 2.4, '6ENJ|1|a': 0.9, '5MDY|1|2': 2.4, '4V50|1|CA': 3.6, '4U27|1|CA': 7.5, '4V52|1|CA': 15.4, '4WF1|1|AA': 10.9, '4V7U|1|AA': 11.0, '5IT8|1|AA': 11.3, '5J5B|1|BA': 8.1, '4U1V|1|CA': 7.6, '5IQR|1|2': 2.3, '5LZA|1|a': 2.0, '5JC9|1|AA': 11.8, '4V5B|1|DA': 15.1, '5U4I|1|a': 2.2, '4V85|1|AA': 15.6, '4YBB|1|BA': 7.9, '4U24|1|AA': 11.1, '5UYL|1|A': 2.2, '6BU8|1|A': 0.9, '3JCJ|1|g': 3.8, '4U1U|1|CA': 7.4, '4V9C|1|CA': 2.5, '4V53|1|AA': 7.5, '5KPW|1|26': 2.3, '6GXO|1|a': 5.2, '6GXN|1|a': 2.6, '4V6E|1|AA': 1.0, '5J8A|1|AA': 11.2, '6NQB|1|A': 11.1, '5MDW|1|2': 2.2, '4WOI|1|DA': 1.1, '5U9F|1|A': 2.0, '6GWT|1|a': 1.9}

  var intersubunitRotation = {'4U25|1|AA': 4.6, '6BY1|1|BA': 1.1, '4WWW|1|XA': 1.2, '5JC9|1|BA': 1.6, '6OG7|1|3': 0.6, '5AFI|1|a': 0.4, '4V52|1|AA': 3.4, '4WF1|1|CA': 1.5, '4V89|1|AA': 7.4, '6OGF|1|3': 4.9, '5LZD|1|a': 0.4, '6ENF|1|a': 2.4, '6H4N|1|a': 2.5, '5NWY|1|0': 2.3, '5J8A|1|BA': 1.4, '6ORE|1|2': 2.2, '4V5B|1|BA': 3.1, '3JA1|1|SA': 7.7, '3JBU|1|A': 2.3, '5JU8|1|AA': 2.2, '4V9O|1|FA': 1.8, '5L3P|1|a': 2.7, '5J91|1|BA': 1.4, '4U20|1|AA': 4.7, '4V55|1|AA': 2.9, '4U26|1|CA': 1.5, '3JBV|1|A': 8.2, '5KPS|1|27': 2.2, '4V57|1|CA': 2.2, '5J7L|1|BA': 1.4, '4U1U|1|AA': 4.7, '4V9C|1|AA': 1.8, '6C4I|1|a': 2.5, '4V7T|1|CA': 1.2, '4V9P|1|DA': 2.2, '4V6C|1|AA': 4.8, '4V6E|1|CA': 1.6, '5J91|1|AA': 4.7, '4V9D|1|AA': 8.4, '4V64|1|AA': 3.3, '6ORL|1|2': 1.3, '5MGP|1|a': 2.5, '6OSQ|1|2': 1.6, '3J9Z|1|SA': 2.5, '6OT3|1|2': 2.0, '5KCS|1|1a': 2.7, '4V4H|1|CA': 2.2, '4V56|1|CA': 2.2, '6OUO|1|2': 2.0, '4V54|1|AA': 3.4, '4WOI|1|AA': 6.6, '3JCD|1|a': 2.4, '3JCE|1|a': 1.3, '5O2R|1|a': 1.7, '4V7S|1|AA': 4.7, '3J9Y|1|a': 2.7, '5J88|1|BA': 1.6, '4V4Q|1|CA': 2.2, '4V9O|1|DA': 2.6, '5MDZ|1|2': 2.4, '6O9J|1|a': 3.0, '4V55|1|CA': 2.1, '6BY1|1|AA': 0.5, '6OSK|1|2': 1.0, '6ENU|1|a': 2.2, '5MDV|1|2': 2.4, '5KCR|1|1a': 2.2, '5J88|1|AA': 4.7, '6OFX|1|3': 1.5, '4V7T|1|AA': 4.5, '4V57|1|AA': 3.1, '5NP6|1|D': 2.4, '4WWW|1|QA': 4.5, '6SZS|1|a': 2.6, '4V9P|1|FA': 2.6, '5UYM|1|A': 0.4, '5KPX|1|26': 0.6, '4V50|1|AA': 2.7, '4U27|1|AA': 4.7, '5WE6|1|a': 0.7, '6GXM|1|a': 0.1, '5J7L|1|AA': 4.7, '4V7V|1|AA': 4.7, '4YBB|1|AA': 4.7, '5WFK|1|a': 2.4, '5UYN|1|A': 2.5, '5UYQ|1|A': 0.9, '4V54|1|CA': 2.5, '5UYK|1|A': 2.5, '4V64|1|CA': 2.2, '4V9O|1|BA': 2.8, '4V4Q|1|AA': 3.2, '4U1V|1|AA': 4.8, '4V4H|1|AA': 3.3, '5WE4|1|a': 0.7, '4V7U|1|CA': 1.3, '4V56|1|AA': 3.2, '4V7S|1|CA': 1.2, '5WDT|1|a': 0.3, '6O9K|1|a': 1.9, '4U20|1|CA': 1.3, '4U26|1|AA': 4.6, '4V6D|1|AA': 4.8, '6DNC|1|A': 1.8, '5UYP|1|A': 2.5, '4V9D|1|BA': 1.3, '4V6D|1|CA': 2.5, '4U24|1|CA': 1.4, '5IT8|1|BA': 1.3, '5J5B|1|AA': 4.8, '4V53|1|CA': 2.2, '5JTE|1|AA': 0.6, '5WF0|1|a': 2.2, '4V9P|1|HA': 7.1, '6OGI|1|3': 7.1, '6Q97|1|2': 2.0, '4V7V|1|CA': 1.3, '5WFS|1|a': 0.8, '5U9G|1|A': 2.4, '4V9P|1|BA': 3.7, '5H5U|1|h': 1.6, '4U25|1|CA': 1.5, '4V6C|1|CA': 1.2, '4V9O|1|HA': 6.1, '6Q9A|1|2': 2.6, '6ENJ|1|a': 0.5, '5MDY|1|2': 2.5, '4V50|1|CA': 2.0, '4U27|1|CA': 1.4, '4V52|1|CA': 2.3, '4WF1|1|AA': 4.7, '4V7U|1|AA': 4.6, '5IT8|1|AA': 4.6, '5J5B|1|BA': 1.3, '4U1V|1|CA': 1.3, '5IQR|1|2': 2.2, '5LZA|1|a': 2.2, '5JC9|1|AA': 4.6, '4V5B|1|DA': 2.0, '5U4I|1|a': 2.3, '4V85|1|AA': 6.5, '4YBB|1|BA': 1.4, '4U24|1|AA': 4.6, '5UYL|1|A': 2.4, '6BU8|1|A': 0.4, '3JCJ|1|g': 1.5, '4U1U|1|CA': 1.4, '4V9C|1|CA': 6.5, '4V53|1|AA': 3.2, '5KPW|1|26': 2.1, '6GXO|1|a': 7.9, '6GXN|1|a': 4.2, '4V6E|1|AA': 5.0, '5J8A|1|AA': 4.7, '5MDW|1|2': 2.5, '4WOI|1|DA': 1.5, '5U9F|1|A': 2.3, '6GWT|1|a': 0.9}
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
          if (d.ife1 == d.ife2) { var row = d.ife1_index + 1;
            var label = stateLabel[d.ife1]
            var annotation = formatAnnotation(annotationEc, d.ife1, row)
            return annotation
            // return `Discrepancy between ${d.ife1} and ${d.ife2} is 0`
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

      // programmatically generate the gradient for the legend
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

      // attach event listener to control
      d3.select('#scale-select').on('change', function() {
        var colorMethod = d3.select(this).node().value;
        if (colorMethod === 'hr') {
            colorDiagonalsByHeadRotation();
        } else if (colorMethod === 'ir') {
            colorDiagonalsByIntersubunitRotation();
        } else if (colorMethod === 'fs') {
            colorDiagonalsByFunctionalState();
        } else if (colorMethod === 'pi') {
            colorDiagonalsByPrincipalInvestigator();
        }
      });

      function colorDiagonalsByHeadRotation () {
          var arr = Object.values(headRotation);
          var minScale = Math.min(...arr);
          var maxScale = Math.max(...arr);

          var colorScaleHR = d3.scaleLinear()
          .domain(linspace(minScale, maxScale, plasmaColor.length))
          .range(plasmaColor)

          d3.selectAll(".bordered")
            .style("fill", function(d) {
                if ((d.ife1 != d.ife2) && (d.discrepancy == null)) {
                    return "#C0C0C0";
                } else if (d.ife1 == d.ife2) {
                    var hr = headRotation[d.ife1];
                    $("div.legendIR").hide();
                    $("div.legendHR").show();
                    return colorScaleHR(hr)
                } else {
                return colorScale(d.discrepancy);
                }
            })
      }

      function colorDiagonalsByIntersubunitRotation () {
          var arr = Object.values(intersubunitRotation);
          var minScale = Math.min(...arr);
          var maxScale = Math.max(...arr);

          var colorScaleIR = d3.scaleLinear()
          .domain(linspace(minScale, maxScale, plasmaColor.length))
          .range(plasmaColor);

          console.log(maxScale)

          d3.selectAll(".bordered")
            .style("fill", function(d) {
                if ((d.ife1 != d.ife2) && (d.discrepancy == null)) {
                    return "#C0C0C0";
                } else if (d.ife1 == d.ife2) {
                    var hr = intersubunitRotation[d.ife1];
                    $("div.legendHR").hide();
                    $("div.legendIR").show();
                    return colorScaleIR(hr)
                } else {
                return colorScale(d.discrepancy);
                }
            })


      }

      function colorDiagonalsByFunctionalState () {
          d3.selectAll(".bordered")
            .style("fill", function(d) {
                if ((d.ife1 != d.ife2) && (d.discrepancy == null)) {
                    return "#C0C0C0";
                } else if (d.ife1 == d.ife2) {
                    $("div.legendIR").hide();
                    $("div.legendHR").hide();
                    var label = stateLabel[d.ife1];
                    return label;
                } else {
                return colorScale(d.discrepancy);
                }
            })
      }

      function colorDiagonalsByPrincipalInvestigator () {
          d3.selectAll(".bordered")
            .style("fill", function(d) {
                if ((d.ife1 != d.ife2) && (d.discrepancy == null)) {
                    return "#C0C0C0";
                } else if (d.ife1 == d.ife2) {
                    $("div.legendIR").hide();
                    $("div.legendHR").hide();
                    var label = authorLabel[d.ife1];
                    return label;
                } else {
                return colorScale(d.discrepancy);
                }
            })
      }
