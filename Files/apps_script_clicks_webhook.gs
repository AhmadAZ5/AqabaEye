// Setup:
// 1. Open the content spreadsheet, Extensions > Apps Script
// 2. Delete whatever's in Code.gs, paste this in, save
// 3. Deploy > New deployment > gear icon > Web app
//      Execute as: Me
//      Who has access: Anyone
// 4. Copy the deployment url, that's CLICKS_WEBHOOK_URL in Render's env vars
// 5. Every click from the site appends a row to a "clicks" tab, it gets created
//    automatically the first time this runs if it doesn't already exist

function doPost(e) {
  var sheet = getOrCreateClicksSheet_();
  var data = JSON.parse(e.postData.contents);
  sheet.appendRow([
    data.slug || "",
    data.timestamp || "",
    data.lang || "",
    data.referrer || "",
    data.user_agent || "",
  ]);
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getOrCreateClicksSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("clicks");
  if (!sheet) {
    sheet = ss.insertSheet("clicks");
    sheet.appendRow(["slug", "timestamp", "lang", "referrer", "user_agent"]);
  }
  return sheet;
}

// Optional: for a monthly totals view without touching a formula bar, add
// a new tab called "clicks_summary" and put this in cell A1:
//
// =QUERY(clicks!A:B, "select A, count(A) where A is not null group by A label count(A) 'clicks'", 1)
//
// that gives all-time clicks per slug. For a month-by-month breakdown, use:
//
// =QUERY(clicks!A:B, "select A, month(B)+1, count(A) where A is not null group by A, month(B) label month(B)+1 'month', count(A) 'clicks'", 1)
