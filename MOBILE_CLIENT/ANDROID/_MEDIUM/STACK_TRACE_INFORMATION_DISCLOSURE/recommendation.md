A custom exception page should be returned that does not include technical information. The exception should be logged
server side but not visible to a user. The stack trace should never be included within the page's HTML source even if
client side source code viewing has been disabled as it is still possible to recover this information though other
mechanisms.