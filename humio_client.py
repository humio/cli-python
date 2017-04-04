import docopt
import json
import requests
import sys
from contextlib import closing

DEFAULTS = {
    "hostport": "cloud.humio.com:443",
    "dataspace": "developer",
    "from": "5minutes",
    "to": "now"

}
DOC = """Humio CLI tool

Tool for querying humio through its web API.

Usage:
    humio [options] QUERY

Options
    -f --from=<time>     Search from this point in time. Accepts Epochs, ISO8601 timestamps and
                         relative offsets such as 2hours, 3s. [default: {from}]
    -t --to=<time>       Search to this point in time. [default: {to}]
    -l --live            Determine whether query is a live streaming query
    -v --verbose         Print verbose output
    --curl               Print query as curl command and exit
    --dataspace=<space>  Dataspace to query [default: {dataspace}]
    --hostport=<host>    The host:port where Humio can be reached. [default: {hostport}]
""".format(**DEFAULTS)


def humio(args):
    """Opens request to humio and streams the query result"""
    body = {
        'queryString': args['QUERY'],
        'start': args['--from'],
        'end': args['--to'],
        'isLive': args['--live']
    }
    url = 'http://%s/api/v1/dataspaces/%s/query' % (
        args['--hostport'], args['--dataspace'])
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    if args['--curl']:
        print (
            'curl ' +
            ' '.join('-H "%s: %s"' % kv for kv in headers.iteritems()) +
            ' -XPOST ' +
            ' -d \'%s\' ' % json.dumps(body) +
            url
        )
        return 0

    if args['--verbose']:
        print 'Args:', args
        print 'URL:', url
        print 'Headers:', headers
        print 'Body:', body

    success = True
    with closing(requests.post(url, json=body, headers=headers, stream=True)) as resp:
        success = resp.status_code < 300
        for chunk in resp:
            sys.stdout.write(chunk)

    sys.stdout.flush()

    print  # Make sure we end with a newline
    return 0 if success else 1


def main():
    """Main entry point. Parses input and handles key interrupt"""
    try:
        return humio(docopt.docopt(DOC))
    except KeyboardInterrupt:
        print 'Aborted - bye!'
        return 1


if __name__ == '__main__':
    sys.exit(main())
