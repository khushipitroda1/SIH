import twint


def crawler():
    # Configure
    print('Hello')
    c = twint.Config()
    c.Username = "PTI_News"
    # c.Search = "great"
    # c.Since = "2018-01-01"
    # c.Until = "2020-12-01"
    c.Store_csv = True
    c.Output = "Crawl.csv"

    # Run
    twint.run.Search(c)