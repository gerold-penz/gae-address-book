## coding: utf-8
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="DC.language" content="de" />

  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta http-equiv="imagetoolbar" content="no" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>${status}</title>

  <style type="text/css">
    #powered_by {
      margin-top: 20px;
      border-top: 2px solid black;
      font-style: italic;
    }
    #traceback {
      color: red;
    }
  </style>
</head>
<body>
  <h2>${status}</h2>
  <p>${message}</p>
  <pre id="traceback">${traceback}</pre>
  <div id="powered_by">
    <span>Powered by <a href="http://www.cherrypy.org">CherryPy ${version}</a></span>
  </div>
</body>
</html>
