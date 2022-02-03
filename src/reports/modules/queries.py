from pygqlc import GraphQLClient
from .variables import QUERY_SNAPSHOT

gql = GraphQLClient()

def getSnapshots(categoryName,beginDate,endDate):
  current_snapshots = []
  snapshots, errors = gql.query_one(QUERY_SNAPSHOT, variables={'categoryName':categoryName,'beginDate':beginDate,'endDate':endDate})
  if snapshots:
    current_snapshots = snapshots
  elif errors:
    print("Error while fetching snapshots")
    print(errors)
  elif snapshots == []:
    print("No snapshots found in selected date")
  return current_snapshots
