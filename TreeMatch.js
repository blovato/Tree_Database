// nodejs and excel parser for running database tools
var excelParser = require('excel-parser');
 
excelParser.parse({
  inFile: 'my_file.in',
  worksheet: 1,
  skipEmpty: true,
  searchFor: {
    term: ['my serach term'],
    type: 'loose'
  }
},function(err, records){
  if(err) console.error(err);
  consol.log(records);
});