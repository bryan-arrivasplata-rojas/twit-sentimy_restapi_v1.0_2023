from Connection.ConnectionTweet import connect_twitter
def getSearch(identifier):
    connection = connect_twitter()
    try:
        comments = connection.get_status(identifier, tweet_mode='extended').text
        return comments
    except Exception as e:
        return {'message_error': str(e), 'section': 'getSearch'}