- Authoritative server-side validation: implement server-side required-field validation that re-derives the full (unfiltered) survey definition and rejects any `proms` submission missing a non-null answer for every `isRequired` element, regardless of `visibleIf`. This is the only reliable control because the client gate is visibility-filtered.
- Reject constant `visibleIf` expressions: at survey-definition ingestion time, treat constant tautology/contradiction expressions (for example `1 = 1` and `1 = 2`) as invalid, and reject or flag survey definitions where an element combines `isRequired: true` with an always-false `visibleIf`.
- Client-side defence in depth: in the submission path, validate required fields over the full survey definition (not the visibility-filtered, flattened page) before calling the response submission routine.
- Parse-time rejection: reject constant-expression `visibleIf` values in the survey JSON parser/translator so a tampered `visibleIf`/`isRequired` combination is detectable on the client.
- Transport integrity: implement TLS certificate pinning (for example OkHttp `CertificatePinner`) on the survey-definition endpoint to raise the bar for man-in-the-middle-based definition tampering.
- Definition integrity: sign survey definitions or carry an integrity hash so that a tampered `visibleIf`/`isRequired` combination is detectable on the client.

=== "Kotlin"
  ```kotlin
  fun validateRequired(surveyDefinition: SurveyData, response: SurveyResponseData) {
      val missing = surveyDefinition.pages
          .flatMap { it.elements }
          .filter { it.isRequired == true }
          .filter { isResponseIncomplete(response, it) } // over the FULL unfiltered definition
      require(missing.isEmpty()) { "Missing required answers: ${missing.map { it.name }}" }
  }
  ```
