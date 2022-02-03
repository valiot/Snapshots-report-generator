QUERY_SNAPSHOT = ''' query($categoryName:String, $beginDate:DateTime, $endDate:DateTime){
  snapshots(filter:{
    categoryName:$categoryName
    after:{date:$beginDate, attribute:INSERTED_AT}
    before:{date:$endDate, attribute:INSERTED_AT}
  }
  orderBy:{desc:INSERTED_AT}){
    insertedAt
    data{
      variable{code}
      value
    }
  }
} '''

QUERY_VARIABLE = '''query($codes:[String]){
  variables(filter: {codes: $codes})
  {
    data(orderBy: {desc: INSERTED_AT} limit:1){value, insertedAt, id},
    enabled,
    code,
    name,
    id,
  }
}'''
