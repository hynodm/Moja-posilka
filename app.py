function doGet(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Data");
    
    if (!sheet) {
      return ContentService.createTextOutput("Chyba: Nenájdený hárok Data").setMimeType(ContentService.MimeType.TEXT);
    }
    
    var p = e.parameter;
    
    if (sheet.getLastRow() == 0) {
      sheet.appendRow(["Časová pečiatka", "Kategória", "Cvik", "Váha", "Opakovania"]);
    }
    
    sheet.appendRow([
      new Date(), 
      p.kat || "Nezadané", 
      p.cvik || "Nezadané", 
      p.vaha || "0", 
      p.opak || "0"
    ]);
    
    return ContentService.createTextOutput("Success").setMimeType(ContentService.MimeType.TEXT);
    
  } catch (err) {
    return ContentService.createTextOutput("Chyba: " + err.toString());
  }
}

function doPost(e) {
  return doGet(e);
}
