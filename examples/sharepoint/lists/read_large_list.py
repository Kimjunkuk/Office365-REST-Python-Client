from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests import test_client_credentials, test_team_site_url


def print_progress(items_read):
    print("Items read: {0}".format(items_read))


def enum_items(target_list):
    items = target_list.items.top(1000)  # .top(1220)
    items.page_loaded += print_progress  # page load event
    ctx.load(items)
    ctx.execute_query()
    for index, item in enumerate(items):
        print("{0}: {1}".format(index, item.properties['Title']))


def get_total_count(target_list):
    """
    :type target_list: office365.sharepoint.lists.list.List
    """
    items = target_list.items
    items.page_loaded += print_progress  # page load event
    result = items.top(200).get_items_count().execute_query()
    print("Total items count: {0}".format(result.value))


def get_items(target_list):
    """
    :type target_list: office365.sharepoint.lists.list.List
    """
    items = target_list.items.paged(True).top(200)
    items.page_loaded += print_progress  # page load event
    ctx.load(items)
    ctx.execute_query()
    print("Loaded items count: {0}".format(len(items)))
    index = 0
    for item in items:
        # print("{0}: {1}".format(index, item.properties['Title']))
        index += 1


def query_large_list(target_list):
    """
    :type target_list: office365.sharepoint.lists.list.List
    """

    def create_paged_query(page_size):
        qry = CamlQuery()
        qry.ViewXml = f"""
        <View Scope='RecursiveAll'>
           <Query><Where><Neq><FieldRef Name=\"FullName\" /><Value Type=\"Text\">Travis Clayton</Value></Neq></Where></Query>
           <QueryOptions><QueryThrottleMode>Override</QueryThrottleMode></QueryOptions>
           <RowLimit Paged='TRUE'>{page_size}</RowLimit>
       </View>
       """
        return qry

    items = target_list.get_items(create_paged_query(100)).execute_query()
    print(items)


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

large_list = ctx.web.lists.get_by_title("Contacts_Large")
# query_large_list(large_list)
# get_total_count(large_list)
# get_items(large_list)
enum_items(large_list)
