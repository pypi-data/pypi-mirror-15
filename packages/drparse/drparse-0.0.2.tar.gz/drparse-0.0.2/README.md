# Date Range Parse

Crudely extends [dateparser](https://github.com/scrapinghub/dateparser) to extract out one or two dates from a string.
Times are deliberately ignored, it *only* extracts the dates.

### Examples

    from drparse import parse

Single Date with time range

    dates = parse("Thursday, July 28 at 8 PM - 11 PM")

    dates.start => datetime.datetime(2016, 7, 28, 0, 0)

Date range without time

    dates = parse("Thu, 6 -  Sun, 16 Oct 2016")

    dates.start => datetime.datetime(2016, 10, 6, 0, 0)
    dates.end => datetime.datetime(2016, 10, 16, 0, 0)

Date range with time

    dates = parse("Sat May 28, 2016 to Sun May 29, 2016, 10PM till late")

    dates.start => datetime.datetime(2016, 5, 28, 0, 0)
    dates.end => datetime.datetime(2016, 5, 29, 0, 0)

### Further info

    How to work with time/date ranges, changing default values, etc
    https://github.com/bear/parsedatetime/issues/162

    Search text for dates
    https://github.com/scrapinghub/dateparser/issues/82

### Alternatives

You should probably just use this one instead!

    https://github.com/robintw/daterangeparser




