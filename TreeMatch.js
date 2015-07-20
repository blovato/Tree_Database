// nodejs and excel parser for running database tools
var excelParser = require('excel-parser');
excelParser.worksheets({
  inFile: 'my_file.in'
}, function(err, worksheets){
  if(err) console.error(err);
  consol.log(worksheets);
});
