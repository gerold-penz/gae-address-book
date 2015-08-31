## coding: utf-8
<!DOCTYPE html>
<html>
<head lang="de">
  <meta charset="UTF-8">
  <title>Justimmo-Hilfe</title>
  <link rel="stylesheet" href="/api/css/docutils.css" />
</head>
<body>

  <div class="outer-page">
    <div class="inner-page">

      <h1>${appname} - JSON-RPC-API Help</h1>

      <h2>Hint</h2>
      <p>
        Auf Grund einer serverseitigen Einschränkung, darf ein HTTP-Request
        <strong>maximal 30 Sekunden</strong> dauern.
        Wird für die Verarbeitung eines Requests mehr als 30 Sekunden benötigt,
        tritt ein Timeout-Fehler auf.
      </p>
      <p>
        Darauf ist zu achten, wenn gleichzeitig mehrere Anweisungen in einem
        JSON-RPC-BATCH übergeben werden.
      </p>


      ${add_doc}


      <div class="footer" style="text-align: right">
        <span style="font-size: x-small">Version: ${version}</span>
      </div>

    </div>
  </div>

</body>
</html>
