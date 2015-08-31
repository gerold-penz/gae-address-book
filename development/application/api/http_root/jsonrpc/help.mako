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

      <h1>Justimmo-Hilfe</h1>

      <h2>Kontakt</h2>
      <p>
        Immoads Marketing GmbH -
        Gerold Penz -
        <a href="mailto:gerold.penz@immoads.at">gerold.penz@immoads.at</a> -
        <a href="tel:+436643463652">+436643463652</a>
      </p>


      <h2>Hinweis</h2>
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
      <p>
        Bitte achten Sie darauf, dass Anweisungen <strong>seriell</strong>
        an den Server übergeben werden und <strong>nicht parallel</strong>.
        Es könnte zu unvorhersehbaren Problemen führen, wenn z.B. gleichzeitig
        mehrere Kunden im System erstellt werden. Ich habe das nicht getestet,
        möchte aber auf der sicheren Seite bleiben.
      </p>


      <h2>Definierte Fehlercodes</h2>
      <ul>
        <li>OpenimmoAnidExistsError: 4091</li>
        <li>EmailExistsError: 4092</li>
        <li>OpenimmoAnidNotFoundError: 4093</li>
        <li>EmailNotFoundError: 4094</li>
        <li>EmailInvalidError: 4095</li>
        <li>OpenimmoAnidInvalidError: 4096</li>
        <li>StringParameterError: 4098</li>
        <li>NumericParameterError: 4099</li>
        <li>StartDayInFutureError: 6000</li>
        <li>PeriodEndDateInFutureError: 6001</li>
      </ul>


      <h2>Funktionen</h2>

      ${subscribe_doc}

      ${unsubscribe_doc}

      ${charge_doc}

      ${status_doc}


      <div class="footer" style="text-align: right">
        <span style="font-size: x-small">Version: ${version}</span>
      </div>

    </div>
  </div>

</body>
</html>
