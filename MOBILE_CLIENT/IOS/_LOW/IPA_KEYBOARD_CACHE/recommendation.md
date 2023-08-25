Keyboard caching is caused by the `UITextInputTraits` protocol supported by `UITextField`, `UITextView` and `UISearchBar`.

- `var autocorrectionType: UITextAutocorrectionType` determines whether auto-correction is enabled during typing.
  When auto-correction is enabled, the text object tracks unknown words and suggests suitable replacements, replacing
  the typed text automatically unless the user overrides the replacement. The default value of this property is
  `UITextAutocorrectionTypeDefault`, which for most input methods enables auto-correction.

- `var secureTextEntry: BOOL` determines whether text copying and caching are disabled and hides the text being
  entered for `UITextField`. The default value of this property is `NO`.

=== "C"
	```c
	textInput.autocorrectionType = UITextAutocorrectionTypeNo;
	textInput.secureTextEntry = YES;
	```

