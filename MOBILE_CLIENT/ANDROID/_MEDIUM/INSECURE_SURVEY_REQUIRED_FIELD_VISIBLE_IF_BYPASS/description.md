In mobile survey/PROMs engines, the visibility of a survey element is frequently controlled by a server-supplied expression (for example a `visibleIf` string evaluated by an embedded expression parser), while a separate `isRequired` flag marks questions that the user must answer before submission. When the required-field enforcement runs only over the set of elements that survived visibility filtering — instead of over the full, unfiltered survey definition — an attacker who can influence the survey definition can combine `isRequired: true` with a `visibleIf` expression that evaluates to a deterministic constant boolean (a tautology such as `1 = 1` or a contradiction such as `1 = 2`) to force an element to be always shown or always hidden.

The always-hidden case is the dangerous one for consent and PHI collection: a required consent or PHI question is dropped from the rendered and flattened page before the required-field gate is evaluated, so its `isRequired` flag is never consulted. The submission path then serialises the collected `proms` payload with the consent answer simply absent, and because no client- or server-side completeness check re-derives the full survey definition to assert that every `isRequired` element has a non-null answer, the mandatory consent gate is silently bypassed on the device.

This is a business-logic bypass rather than a memory-corruption or injection issue. Exploitation prerequisites are non-trivial: the attacker must control the survey definition, which in practice means a compromised survey-definition server or a man-in-the-middle position against a survey-definition transport that lacks TLS certificate pinning. When those prerequisites are met, the realistic impact is the silent bypass of mandatory PHI/consent gating on the device; downstream clinical-decision impact depends on backend re-validation of required-field presence.

=== "Kotlin"
  ```kotlin
  // The element is dropped before the required-field gate runs.
  fun buildPageElement(element: SurveyElement, mergedResponse: SurveyResponseData): SurveyElement? {
      // Visibility is driven verbatim by the server string `visibleIf`.
      if (!isElementVisible(element, mergedResponse)) return null
      // ... build the visible element
  }

  fun isElementVisible(element: SurveyElement, mergedResponse: SurveyResponseData): Boolean = when {
      element.visibleIf.isNullOrBlank() -> element.visible != false
      else -> evaluateSurveyExpression(input = element.visibleIf, response = mergedResponse)
  }

  // The required gate inspects only the current element of the visibility-filtered page.
  val elementResponseIncomplete =
      curElement.isRequired == true && isResponseIncomplete(surveyResponse, curElement)
  // A dropped element never becomes `curElement`, so its `isRequired` is never evaluated.
  ```

=== "JSON"
  ```json
  {
    "name": "consent",
    "type": "boolean",
    "isRequired": true,
    "visibleIf": "1 = 2"
  }
  ```

The `1 = 2` expression parses cleanly under the survey expression grammar as `NUMBER EQ NUMBER` and evaluates deterministically to `false`, dropping the element from the rendered page; the resulting `proms` submission omits the consent answer with no completeness guard. The converse `visibleIf: "1 = 1"` forces an element to display regardless of prior answers.
