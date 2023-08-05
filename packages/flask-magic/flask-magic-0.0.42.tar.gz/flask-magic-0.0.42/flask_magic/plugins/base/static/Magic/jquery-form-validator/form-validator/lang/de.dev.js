/**
 * jQuery Form Validator
 * ------------------------------------------
 *
 * German language package
 *
 * @website http://formvalidator.net/
 * @license MIT
 * @version 2.2.81
 */
(function($, window) {

  "use strict";

  $(window).bind('validatorsLoaded', function() {

    $.formUtils.LANG = {
      errorTitle: "Ihre Anfrage konnte nicht gesendet werden!",
      requiredFields: "Sie haben nicht alle Fragen beantwortet",
      badTime: "Sie haben nicht die korrekte Zeit eingegeben",
      badEmail: "Sie haben keine gültige E-Mail-Adresse eingegeben",
      badTelephone: "Sie haben keine richtige Telefonnummer eingetragen",
      badSecurityAnswer: "Sie haben die falsche Antwort auf die Sicherheitsfrage eingegeben",
      badDate: "Re-Eingabe eines falschen Datums",
      lengthBadStart: "Ihre Eingabe muss zwischen %s lang sein",
      lengthBadEnd: " Zeichen",
      lengthTooLongStart: "Sie haben eine Antwort die länger als %s angegeben",
      lengthTooShortStart: "Sie haben eine Antwort die kürzer ist als %s eingegebene",
      notConfirmed: "Die Antworten könnten nicht gegenseitig bestätigen,",
      badDomain: "Sie haben die falsche Domäne eingetragen",
      badUrl: "Sie haben nicht die richtige URL eingegeben",
      badCustomVal: "Re-Eingabe einer falschen Antwort",
      andSpaces: " und Leerzeichen",
      badInt: "Sie haben keine Nummer eingegeben",
      badSecurityNumber: "Sie haben eine falsche Sozialversicherungsnummer eingegeben",
      badUKVatAnswer: "Sie haben keine UK Umsatzsteuer-Identifikationsnummer eingegeben",
      badStrength: "Sie haben ein Kennwort, das nicht sicher genug ist eingegeben",
      badNumberOfSelectedOptionsStart: "Sie müssen mindestens %s wählen",
      badNumberOfSelectedOptionsEnd: " Antwort",
      badAlphaNumeric: "Sie können nur mit alphanumerische Zeichen (Buchstaben und Zahlen) eingaben",
      badAlphaNumericExtra: " und",
      wrongFileSize: "Die Datei, die Sie hochzuladen versuchen, zu groß ist (max %s)",
      wrongFileType: "Nur Dateien vom Typ %s sind zulässig",
      groupCheckedRangeStart: "Wählen Sie zwischen",
      groupCheckedTooFewStart: "Dann müssen Sie zumindest sicher,",
      groupCheckedTooManyStart: "Sie können nicht mehr als zu machen",
      groupCheckedEnd: " Auswahl",
      badCreditCard: "Sie haben eine ungültige Kreditkartennummer eingegeben",
      badCVV: "Sie haben eine falsche CVV eingegeben",
      wrongFileDim: "Illegal Bildgröße,",
      imageTooTall: "Das Bild kann nicht höher als %s sein",
      imageTooWide: "Das Bild kann nicht breiter als %s sein",
      imageTooSmall: "das Bild ist zu klein",
      min: "min",
      max: "max",
      imageRatioNotAccepted : 'Bildverhältnis wird nicht akzeptiert'
    };

  });

})(jQuery, window);


