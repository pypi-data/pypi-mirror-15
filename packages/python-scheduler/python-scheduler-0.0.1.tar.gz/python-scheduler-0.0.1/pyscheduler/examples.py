from pyscheduler import schedule


@schedule('* * * * *')
def ping_task():
    print 'ping task'


@schedule('*/2 * * * *')
def crawl_task():
    print 'crawl task'


if __name__ == '__main__':
    print 'Test started.'
