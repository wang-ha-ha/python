(function() {
    var chromeType = navigator.userAgent.toLowerCase();
    var bType = '';
  
    function getBrowserType() {
      if ("ActiveXObject" in window) {
        bType = 'ie';
      } else if (chromeType.indexOf('firefox') > -1) {
        bType = "firefox";
      } else if (chromeType.indexOf('opera') > -1 || chromeType.indexOf('opr') > -1) {
        bType = "opera";
      } else if (chromeType.indexOf('safari') > -1 && chromeType.indexOf('chrome') == -1) {
        bType = "safari";
      } else if (chromeType.indexOf('chrome') > -1) {
        var check360 = checkChromeWeight();
        if (chromeType.indexOf('qqbrowser') > -1) {
          bType = "qq";
        } else if (chromeType.indexOf('maxthon') > -1) {
          bType = "maxthon";
        } else if (chromeType.indexOf('bidubrowser') > -1) {
          bType = 'baidu';
        } else if (chromeType.indexOf('ubrowser') > -1) {
          bType = 'uc';
        } else if (chromeType.indexOf('lbbrowser') > -1) {
          bType = 'liebao';
        } else if (chromeType.indexOf('taobrowser') > -1) {
          bType = 'taobao';
        } else if (chromeType.indexOf('2345explorer') > -1) {
          bType = '2345';
        } else if (chromeType.indexOf('coolnovo') > -1) {
          bType = 'fengshu';
        } else if (chromeType.indexOf('greenbrowser') > -1) {
          bType = 'gb';
        } else if (check360 === "Chrome") {
          bType = 'chrome';
        } else if (check360 === "360SE") {
          bType = '360se';
        } else if (check360 === "360EE") {
          bType = '360ee';
        } else if (chromeType.indexOf('se') > -1) {
          bType = 'sogou';
        }
      }
      return bType;
    }
  
    var chrome_weight = {
      "result": "Chrome",
      "details": {
        "Chrome": 5,
        "Chromium": 0,
        "_360SE": 0,
        "_360EE": 0
      },
      "sorted": ["Chrome", "360SE", "360EE", "Chromium"],
      "exec": function(results) {
        var details = {
          "Chrome": 5,
          "Chromium": 0,
          "_360SE": 0,
          "_360EE": 0
        }
        var _ua = window.navigator.userAgent;
        if ((/Chrome\/([\d.])+\sSafari\/([\d.])+$/).test(_ua)) {
          if (window.navigator.platform == "Win32") {
            if (!window.clientInformation.languages) {
              details._360SE += 8;
            }
            if ((/zh/i).test(navigator.language)) {
              details._360SE += 3;
              details._360EE += 3;
            }
            if (window.clientInformation.languages) {
              var lang_len = window.clientInformation.languages.length;
              if (lang_len >= 3) {
                details.Chrome += 10;
                details.Chromium += 6;
              } else if (lang_len == 2) {
                details.Chrome += 3;
                details.Chromium += 6;
                details._360EE += 6;
              } else if (lang_len == 1) {
                details.Chrome += 4;
                details.Chromium += 4;
              }
            }
            for (var i in window.navigator.plugins) {
              if (window.navigator.plugins[i].filename == "np-mswmp.dll") {
                details._360SE += 20;
                details._360EE += 20;
              }
            }
            if (window.chrome.webstore && Object.keys(window.chrome.webstore).length <= 1) {
              details._360SE += 7;
            } else if (window.chrome.webstore && Object.keys(window.chrome.webstore).length == 2) {
              details._360SE += 4;
              details.Chromium += 3;
            }
  
            if (window.navigator.plugins.length >= 30) {
              details._360EE += 7;
              details._360SE += 7;
              details.Chrome += 7;
            } else if (window.navigator.plugins.length < 30 && window.navigator.plugins.length > 10) {
              details._360EE += 3;
              details._360SE += 3;
              details.Chrome += 3;
            } else if (window.navigator.plugins.length <= 10) {
              details.Chromium += 6;
            }
  
          } else {
            details._360SE -= 50;
            details._360EE -= 50;
            if ((/Linux/i).test(window.navigator.userAgent)) {
              details.Chromium += 5;
            }
  
          }
          var found = 0;
          var respdf;
          for (var i in window.navigator.plugins) {
            if (!!(respdf = (/^(.+) PDF Viewer$/).exec(window.navigator.plugins[i].name))) {
              //console.log(respdf[1]);
              if (respdf[1] == "Chrome") {
                details.Chrome += 6;
                details._360SE += 6;
                found = 1;
                break;
              }
              if (respdf[1] == "Chromium") {
                details.Chromium += 10;
                details._360EE += 6;
                found = 1;
                break;
              }
            }
          }
          if (!found) {
            details.Chromium += 9;
          }
  
        }
        var chrome_result = new Object;
        chrome_result['Chrome'] = details.Chrome;
        chrome_result['Chromium'] = details.Chromium;
        chrome_result['360SE'] = details._360SE;
        chrome_result['360EE'] = details._360EE;
        var sortable = [];
        for (var value in chrome_result)
          sortable.push([value, chrome_result[value]])
        sortable.sort(function(a, b) {
          return b[1] - a[1]
        });
        this.sorted = sortable;
        this.details = details;
        this.result = sortable[0][0];
        if (results == "result") {
          return sortable[0][0];
        } else if (results == "details") {
          return chrome_result;
        } else if (results == "sorted") {
          return sortable;
        }
      }
    }
  
    function checkChromeWeight() {
      var _ua = window.navigator.userAgent;
      chrome_weight.exec();
      if ((/Chrome\/([\d.])+\sSafari\/([\d.])+$/).test(_ua)) {
        return chrome_weight.result;
      }
    }
  
    function connect(t) {
      document.addEventListener('gwd_extension', function(e) {
        if (e.detail.type === 'get_btype') {
          var evt = document.createEvent('CustomEvent')
          evt.initCustomEvent('gwd_content', true, true, {
            type: 'get_btype',
            value: t
          })
          document.dispatchEvent(evt)
        }
      })
    }
  
    function init() {
      var type = getBrowserType();
      connect(type)
    }
    init()
  })();